#!/usr/bin/env python3
"""Validador estructural y operacional del Platform Assessment Framework (PAF).

Valida los YAML del framework contra los JSON Schemas de assessment_framework/schemas/
y ejecuta cross-checks que un schema no puede expresar:

  Estructura:
   1. Pesos de sub-dimensiones suman 1.0 por dimensión.
   2. Pesos de cada perfil suman 1.0 (claves exactas D1-D9 + DAI).
   3. Todo check_ref usado en dimensiones existe en el catálogo.
   4. critical_sub_dimensions (config) <-> flags critical: true (dimensiones), ambos sentidos.
   5. Todo dimension_file del pipeline existe en disco.
   6. IDs de criterios: únicos, con prefijo de su sub-dimensión; criterios-gate con evidence_required.
   7. Todos los *.schema.json son schemas Draft 2020-12 válidos.
   8. WARNING: sub-dimensiones cuyos checks son todos T1 (sus pass quedarían unconfirmed).
   9. WARNING: rúbricas sin las 5 anclas.

  Coherencia operacional del RUNBOOK (el verde de CI la cubre):
  10. Toda referencia DX.Y / DX.Y.Cn del RUNBOOK existe en las dimensiones.
  11. Tabla de checks compartidos: cada check_ref existe en el catálogo y cada
      sub-dimensión consumidora lo declara en sus agent_checks.
  12. Los bloques ```json del RUNBOOK parsean; el ejemplo del contrato valida
      contra dimension_result.schema.json.
  13. Orden de fases: fan-out < reconciliación < sello de evidencia < scoring < gate humano.
  14. Términos obsoletos prohibidos en docs y config (semánticas ya reemplazadas).

Exit code 0 = OK (warnings permitidos), 1 = errores.
Uso: python3 scripts/validate_framework.py [raíz del repo]
"""

import json
import re
import sys
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:
    print("ERROR: falta jsonschema (pip install jsonschema pyyaml)")
    sys.exit(1)

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
FW = ROOT / "assessment_framework"
DIMENSION_IDS = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "DAI"]
T3_CHECKS = {"code_judgment_review", "architecture_conformance_review", "llm_feature_security_review"}

OBSOLETE_TERMS = ["not_available_policy", "t1_only_cap", "techo 3.0", "rating máximo P"]
OBSOLETE_SCOPE = [
    FW / "RUNBOOK.md",
    FW / "README.md",
    FW / "config" / "weights_and_thresholds.yaml",
    FW / "config" / "checks_catalog.yaml",
    FW / "templates" / "assessment_master_pipeline.yaml",
    FW / "templates" / "template_final_report.md",
    ROOT / "Metodologia_Assessment_Plataformas_Software.md",
]

PHASE_ORDER_MARKERS = [
    "## 3. Checks compartidos",
    "## 4. Fan-out",
    "## 5. Reconciliación",
    "## 6. Sello de evidencia",
    "## 7. Scoring",
    "## 8. Gate humano",
]

errors: list[str] = []
warnings: list[str] = []


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_schema(name: str):
    with open(FW / "schemas" / name, encoding="utf-8") as fh:
        return json.load(fh)


def stringify_rubric_keys(doc):
    for sd in doc.get("sub_dimensions", []):
        if isinstance(sd.get("rubric"), dict):
            sd["rubric"] = {f"{float(k):.1f}": v for k, v in sd["rubric"].items()}
    return doc


def validate_schema(doc, schema, label):
    validator = jsonschema.Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        path = ".".join(str(p) for p in err.path) or "<raíz>"
        errors.append(f"[schema] {label} :: {path}: {err.message}")


def main() -> int:
    # --- Carga ---
    config = load_yaml(FW / "config" / "weights_and_thresholds.yaml")
    catalog = load_yaml(FW / "config" / "checks_catalog.yaml")
    pipeline = load_yaml(FW / "templates" / "assessment_master_pipeline.yaml")
    dim_files = sorted((FW / "dimensions").glob("*.yaml"))
    dims = {f.name: stringify_rubric_keys(load_yaml(f)) for f in dim_files}

    # --- 7. Los schemas mismos son válidos ---
    for sf in sorted((FW / "schemas").glob("*.schema.json")):
        try:
            jsonschema.Draft202012Validator.check_schema(json.loads(sf.read_text(encoding="utf-8")))
        except Exception as exc:
            errors.append(f"[meta-schema] {sf.name}: {exc}")

    # --- Validación contra schemas ---
    validate_schema(config, load_schema("weights_and_thresholds.schema.json"), "config/weights_and_thresholds.yaml")
    validate_schema(catalog, load_schema("checks_catalog.schema.json"), "config/checks_catalog.yaml")
    validate_schema(pipeline, load_schema("pipeline.schema.json"), "templates/assessment_master_pipeline.yaml")
    dim_schema = load_schema("dimension.schema.json")
    for fname, doc in dims.items():
        validate_schema(doc, dim_schema, f"dimensions/{fname}")

    # --- Cross-checks estructurales ---
    catalog_checks = set(catalog.get("checks", {}).keys())
    tier_by_check = {k: v.get("tier") for k, v in catalog.get("checks", {}).items()}
    all_subdim_ids: set[str] = set()
    all_criterion_ids: set[str] = set()
    flagged_critical: set[str] = set()
    checks_by_subdim: dict[str, set[str]] = {}

    for fname, doc in dims.items():
        subdims = doc.get("sub_dimensions", [])
        total = sum(sd.get("weight", 0) for sd in subdims)
        if abs(total - 1.0) > 1e-9:
            errors.append(f"[pesos] {fname}: los pesos de sub-dimensiones suman {total:.4f}, no 1.0")

        for sd in subdims:
            sid = sd.get("id", "?")
            all_subdim_ids.add(sid)
            if sd.get("critical"):
                flagged_critical.add(sid)

            refs = set()
            for chk in sd.get("agent_checks", []):
                ref = chk.get("check_ref")
                if ref not in catalog_checks:
                    errors.append(f"[catálogo] {fname} {sid}: check_ref '{ref}' no definido en checks_catalog.yaml")
                else:
                    refs.add(ref)
            checks_by_subdim[sid] = refs
            tiers = {tier_by_check[r] for r in refs if r in tier_by_check}
            if tiers and tiers <= {"T1"}:
                warnings.append(f"[T1-only] {fname} {sid}: todos los checks son T1 => sus pass quedarían unconfirmed. ¿Falta un check T2/T3?")

            for crit in sd.get("nplf_criteria", []):
                cid = crit.get("id") if isinstance(crit, dict) else None
                if not cid:
                    errors.append(f"[criterios] {fname} {sid}: criterio sin id estable (los strings ya no son válidos)")
                    continue
                if cid in all_criterion_ids:
                    errors.append(f"[criterios] {fname} {sid}: id duplicado '{cid}'")
                all_criterion_ids.add(cid)
                if not cid.startswith(sid + ".C"):
                    errors.append(f"[criterios] {fname} {sid}: id '{cid}' no tiene el prefijo de su sub-dimensión")
                if crit.get("failure_effect") == "gate" and not crit.get("evidence_required"):
                    errors.append(f"[gate] {fname} {sid} {cid}: criterio-gate sin evidence_required")

            rubric_keys = set(sd.get("rubric", {}).keys())
            expected = {"1.0", "2.0", "3.0", "4.0", "5.0"}
            if not expected <= rubric_keys:
                warnings.append(f"[rúbrica] {fname} {sid}: faltan anclas {sorted(expected - rubric_keys)}")

    config_critical = set(config.get("critical_sub_dimensions", []))
    for sid in config_critical - all_subdim_ids:
        errors.append(f"[criticidad] config declara '{sid}' crítica pero esa sub-dimensión no existe")
    for sid in config_critical - flagged_critical:
        if sid in all_subdim_ids:
            errors.append(f"[criticidad] '{sid}' es crítica en config pero no tiene critical: true en su dimensión")
    for sid in flagged_critical - config_critical:
        errors.append(f"[criticidad] '{sid}' tiene critical: true pero no está en critical_sub_dimensions de config")

    for pname, profile in config.get("profiles", {}).items():
        w = profile.get("weights", {})
        if set(w.keys()) != set(DIMENSION_IDS):
            errors.append(f"[perfiles] {pname}: claves de pesos != D1-D9+DAI ({sorted(w.keys())})")
        total = sum(w.values())
        if abs(total - 1.0) > 1e-9:
            errors.append(f"[perfiles] {pname}: los pesos suman {total:.4f}, no 1.0")

    for step in pipeline.get("steps", []):
        for rel in step.get("dimension_files", []) or []:
            if not (FW / rel).exists():
                errors.append(f"[pipeline] dimension_file inexistente: {rel}")

    # --- Coherencia operacional del RUNBOOK ---
    runbook_path = FW / "RUNBOOK.md"
    runbook = runbook_path.read_text(encoding="utf-8")

    # 10. referencias DX.Y / DX.Y.Cn
    for m in re.finditer(r"\b((?:D[1-9]|DAI)\.\d)(\.C\d+)?\b", runbook):
        sub, crit = m.group(1), m.group(0)
        if sub not in all_subdim_ids:
            errors.append(f"[runbook] referencia a sub-dimensión inexistente: {sub}")
        elif m.group(2) and crit not in all_criterion_ids:
            errors.append(f"[runbook] referencia a criterio inexistente: {crit}")

    # 11. tabla de checks compartidos <-> declaraciones en dimensiones
    table_rows = re.findall(r"^\|\s*\d+\s*\|\s*`(\w+)`\s*\|[^|]*\|([^|]*)\|\s*$", runbook, re.MULTILINE)
    if not table_rows:
        errors.append("[runbook] no se encontró la tabla de checks compartidos (§3)")
    for check_ref, consumers_cell in table_rows:
        if check_ref not in catalog_checks:
            errors.append(f"[runbook] tabla §3: check_ref '{check_ref}' no existe en el catálogo")
            continue
        consumers = re.findall(r"\b(?:D[1-9]|DAI)\.\d\b", consumers_cell)
        if not consumers:
            errors.append(f"[runbook] tabla §3: fila '{check_ref}' sin consumidores parseables")
        for sub in consumers:
            if check_ref not in checks_by_subdim.get(sub, set()):
                errors.append(f"[runbook] tabla §3: '{sub}' listado como consumidor de '{check_ref}' pero su YAML no lo declara")

    # 12. bloques JSON parsean; el contrato valida contra su schema
    result_schema = load_schema("dimension_result.schema.json")
    for i, block in enumerate(re.findall(r"```json\n(.*?)```", runbook, re.DOTALL), 1):
        try:
            doc = json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(f"[runbook] bloque json #{i} no parsea: {exc}")
            continue
        if isinstance(doc, dict) and "criteria_results" in doc:
            validate_schema(doc, result_schema, f"RUNBOOK.md ejemplo de contrato (bloque #{i})")

    # 13. orden de fases
    positions = []
    for marker in PHASE_ORDER_MARKERS:
        idx = runbook.find(marker)
        if idx < 0:
            errors.append(f"[runbook] falta el marcador de fase: '{marker}'")
        positions.append(idx)
    if all(p >= 0 for p in positions) and positions != sorted(positions):
        errors.append("[runbook] el orden de fases está roto: se exige checks < fan-out < reconciliación < sello < scoring < gate humano")

    # 14. términos obsoletos
    for path in OBSOLETE_SCOPE:
        text = path.read_text(encoding="utf-8")
        for term in OBSOLETE_TERMS:
            if term in text:
                errors.append(f"[obsoleto] {path.relative_to(ROOT)}: contiene '{term}' (semántica reemplazada)")

    # --- Reporte ---
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    n_criteria = len(all_criterion_ids)
    print(f"\n{len(dims)} dimensiones, {len(all_subdim_ids)} sub-dimensiones, "
          f"{n_criteria} criterios NPLF con id estable, {len(catalog_checks)} checks en catálogo, "
          f"{len(list((FW / 'schemas').glob('*.schema.json')))} schemas, "
          f"{len(table_rows)} filas en la tabla de checks compartidos.")
    print(f"Resultado: {len(errors)} errores, {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
