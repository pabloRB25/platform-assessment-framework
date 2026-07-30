#!/usr/bin/env python3
"""Validador estructural del Platform Assessment Framework (PAF).

Valida los YAML del framework contra los JSON Schemas de assessment_framework/schemas/
y ejecuta cross-checks de consistencia que un schema no puede expresar:

  1. Pesos de sub-dimensiones suman 1.0 por dimensión.
  2. Pesos de cada perfil suman 1.0 (claves exactas D1-D9 + DAI).
  3. Todo check_ref usado en dimensiones existe en el catálogo.
  4. critical_sub_dimensions (config) <-> flags critical: true (dimensiones), en ambos sentidos.
  5. Todo dimension_file del pipeline existe en disco.
  6. Criterios-gate: exigen evidence_required declarado.
  7. WARNING: sub-dimensiones cuyos checks son todos T1 (rating máximo P=2.0).
  8. WARNING: rúbricas sin las 5 anclas (1.0, 2.0, 3.0, 4.0, 5.0).

Exit code 0 = OK (warnings permitidos), 1 = errores.
Uso: python3 scripts/validate_framework.py [raíz del repo]
"""

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

errors: list[str] = []
warnings: list[str] = []


def load_yaml(path: Path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_schema(name: str):
    import json
    with open(FW / "schemas" / name, encoding="utf-8") as fh:
        return json.load(fh)


def stringify_rubric_keys(doc):
    """yaml.safe_load parsea las anclas de rúbrica como float; el schema espera claves string."""
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

    # --- Validación contra schemas ---
    validate_schema(config, load_schema("weights_and_thresholds.schema.json"), "config/weights_and_thresholds.yaml")
    validate_schema(catalog, load_schema("checks_catalog.schema.json"), "config/checks_catalog.yaml")
    validate_schema(pipeline, load_schema("pipeline.schema.json"), "templates/assessment_master_pipeline.yaml")
    dim_schema = load_schema("dimension.schema.json")
    for fname, doc in dims.items():
        validate_schema(doc, dim_schema, f"dimensions/{fname}")

    # --- Cross-checks ---
    catalog_checks = set(catalog.get("checks", {}).keys())
    tier_by_check = {k: v.get("tier") for k, v in catalog.get("checks", {}).items()}
    all_subdim_ids: set[str] = set()
    flagged_critical: set[str] = set()

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

            tiers = set()
            for chk in sd.get("agent_checks", []):
                ref = chk.get("check_ref")
                if ref not in catalog_checks:
                    errors.append(f"[catálogo] {fname} {sid}: check_ref '{ref}' no definido en checks_catalog.yaml")
                else:
                    tiers.add(tier_by_check[ref])
            if tiers and tiers <= {"T1"}:
                warnings.append(f"[T1-only] {fname} {sid}: todos los checks son T1 => rating máximo P (2.0). ¿Falta un check T2/T3?")

            for crit in sd.get("nplf_criteria", []):
                if isinstance(crit, dict) and crit.get("failure_effect") == "gate":
                    if not crit.get("evidence_required"):
                        errors.append(f"[gate] {fname} {sid} {crit.get('id')}: criterio-gate sin evidence_required")

            rubric_keys = set(sd.get("rubric", {}).keys())
            expected = {"1.0", "2.0", "3.0", "4.0", "5.0"}
            if not expected <= rubric_keys:
                warnings.append(f"[rúbrica] {fname} {sid}: faltan anclas {sorted(expected - rubric_keys)}")

    # criticidad: config <-> flags, ambos sentidos
    config_critical = set(config.get("critical_sub_dimensions", []))
    for sid in config_critical - all_subdim_ids:
        errors.append(f"[criticidad] config declara '{sid}' crítica pero esa sub-dimensión no existe")
    for sid in config_critical - flagged_critical:
        if sid in all_subdim_ids:
            errors.append(f"[criticidad] '{sid}' es crítica en config pero no tiene critical: true en su dimensión")
    for sid in flagged_critical - config_critical:
        errors.append(f"[criticidad] '{sid}' tiene critical: true pero no está en critical_sub_dimensions de config")

    # perfiles: claves y suma
    for pname, profile in config.get("profiles", {}).items():
        w = profile.get("weights", {})
        if set(w.keys()) != set(DIMENSION_IDS):
            errors.append(f"[perfiles] {pname}: claves de pesos != D1-D9+DAI ({sorted(w.keys())})")
        total = sum(w.values())
        if abs(total - 1.0) > 1e-9:
            errors.append(f"[perfiles] {pname}: los pesos suman {total:.4f}, no 1.0")

    # pipeline: archivos de dimensiones existen
    for step in pipeline.get("steps", []):
        for rel in step.get("dimension_files", []) or []:
            if not (FW / rel).exists():
                errors.append(f"[pipeline] dimension_file inexistente: {rel}")

    # --- Reporte ---
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    n_criteria = sum(
        len(sd.get("nplf_criteria", []))
        for doc in dims.values()
        for sd in doc.get("sub_dimensions", [])
    )
    print(f"\n{len(dims)} dimensiones, {len(all_subdim_ids)} sub-dimensiones, "
          f"{n_criteria} criterios NPLF, {len(catalog_checks)} checks en catálogo.")
    print(f"Resultado: {len(errors)} errores, {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
