# RUNBOOK — Ejecución del Assessment por Agente

> **Qué es:** el procedimiento operativo paso a paso para ejecutar el assessment contra un repositorio real, diseñado para un **agente orquestador** que despacha **subagentes por dimensión**. Es la implementación manual-agéntica del pipeline (`templates/assessment_master_pipeline.yaml`) mientras no exista el runner v4.
>
> **Qué no es:** no reemplaza los YAML (fuente de verdad de criterios y checks) ni al auditor humano (§8, bloqueante). Los comandos que aparecen aquí y en el catálogo son **ilustrativos para humanos**; un runner automatizado construye argv sin shell (`checks_catalog.yaml §execution_model`) y el argv real queda en el manifest.

**Orden de fases (invariante):** encuadre → preflight → checks compartidos → fan-out → reconciliación → **sello de evidencia** → scoring → gate humano → informe → cierre. El sello ocurre **después** del fan-out y la reconciliación: la evidencia específica de dimensiones nunca queda fuera del manifest ni del secret-scan final.

---

## 0. Modelo de ejecución

| Rol | Responsabilidad |
| :--- | :--- |
| **Orquestador** | Encuadre, checks compartidos (incluye TODOS los autenticados), despacho de subagentes, reconciliación, sello de evidencia, scoring, render. NO lee evidencia cruda: consume `results/*.json`. |
| **Subagente de dimensión** (×10) | Evalúa UNA dimensión siguiendo su YAML: lee la evidencia compartida por EV-id, hace los muestreos T3, emite estados y hallazgos. Devuelve SOLO el JSON del contrato (§4.3). **No recibe credenciales de ninguna clase** — los checks autenticados ya corrieron en el orquestador. |
| **Auditor humano** | Revisa y firma el borrador; sus correcciones quedan en un log append-only (§8). |

**Regla de economía de contexto:** los subagentes escriben su resultado a `results/` y responden con un resumen de ≤ 10 líneas. El orquestador jamás carga outputs crudos de herramientas en su contexto — para eso están los EV-ids del manifest.

**Regla de confianza mínima:** el subagente solo reporta `criterion_ref + estado + evidencia`. Todo lo que afecta el scoring — gate, criticidad, tier de evidencia, texto del criterio, cobertura — lo **deriva el orquestador** desde el YAML de dimensión, el catálogo y el manifest. Un subagente no puede declarar su propio tier ni su propio gate.

---

## 1. Encuadre (Fase 0 — sin esto no se empieza)

El orquestador completa `results/encuadre.json` (schema: `schemas/encuadre.schema.json`):

1. **Perfil** (`general_saas` | `fintech_critical` | `mvp_startup` | `ai_native_agentic`) → pesos y `target_phs`.
2. **`targets[]` congelados:** lista de `{repo, branch, sha}` — el encuadre admite múltiples repositorios; todo resultado referencia el SHA de su target.
3. **Inventario de accesos** (código, historial git completo, API del repo, historial de CI, cloud/IaC, ambientes) — lo inaccesible será `unknown`, nunca estimado. Define el techo de confianza y el `coverage_ratio` esperable.
4. **Toolchain pinneada:** herramienta + versión + ruleset/digest (gitleaks, semgrep, trivy/osv, jscpd, lizard, grafo según stack, prowler/checkov, gh). Preferir imagen de contenedor con todo preinstalado; `npx` solo con `--no-install`.
5. **Workspace** (fuera del repo del cliente):

```
assessment-<cliente>-<YYYYMMDD>/
├── repo/          # clone(s) congelado(s) al SHA (read-only para subagentes; clone completo, no shallow)
├── framework/     # copia de assessment_framework/ (versión registrada en encuadre.json)
├── evidence/      # outputs + manifest.json — NUNCA se commitea; custodia según catálogo
├── results/       # encuadre.json, D1.json..DAI.json, reconciliacion.json, scoring.json, correcciones.jsonl
└── reports/       # informe final + reports/baseline/ si existe assessment previo
```

6. **Seguridad de ejecución** (`§execution_model`): repo no confiable ⇒ contenedor efímero, red off por defecto (allowlist: endoflife.date, registries), credenciales read-only de alcance mínimo **solo en el orquestador**.
7. **Baseline delta:** si hay assessment previo, copiarlo a `reports/baseline/` y registrar en `encuadre.json` si cumple `delta_comparability_rules` (si no: `comparable: false` + motivos ⇒ "delta indicativo").

## 2. Preflight técnico

Verificar que cada herramienta corre e imprime versión; lo que falte ⇒ `unknown` en los criterios dependientes desde ya (no se sustituye por grep). Detectar stack (lockfiles, lenguajes, monorepo, framework) para elegir las variantes del Anexo A.

---

## 3. Checks compartidos (el orquestador los corre UNA sola vez)

El comando de cada check vive en `config/checks_catalog.yaml` — acá solo se lista el `check_ref`, su output canónico y qué sub-dimensiones lo consumen (deben declararlo en su YAML; el validador de CI cruza esta tabla contra las dimensiones). Cada output se registra **incrementalmente** en `evidence/manifest.json` con su EV-id (`sealed: false` — el sello final es en §6).

| # | check_ref (catálogo) | Output canónico | Consumido por |
| :-- | :--- | :--- | :--- |
| 1 | `secret_scan` | `evidence/gitleaks.json` | D3.2 |
| 2 | `sast_scan` | `evidence/semgrep.json` | D2.4, D3.1, D3.4, D4.2, DAI.2 |
| 3 | `sca_scan` | `evidence/trivy.json` | D3.3 |
| 4 | `duplication_scan` | `evidence/jscpd/` | D2.2, DAI.3 |
| 5 | `complexity_scan` | `evidence/lizard.csv` | D2.2, D8.4 |
| 6 | `dependency_graph_analysis` | `evidence/depgraph.json` | D1.1, D1.3 |
| 7 | `ci_config_analysis` | `evidence/ci_config/` | D2.1, D4.3, D5.2, D5.3, D6.1, D6.3 |
| 8 | `git_branch_protection_api` | `evidence/branch_protection.json` | D9.1 |
| 9 | `git_pr_review_analysis` | `evidence/prs.json` | D9.2, DAI.5 |
| 10 | `pipeline_history_analysis` | `evidence/ci_runs.json` | D5.3, D6.2 |
| 11 | `git_commit_log_analysis` | `evidence/commit_log.txt` | D9.3 |
| 12 | `git_history_analysis` | `evidence/shortlog_<comp>.txt` | D8.3, D9.1, D9.4 |
| 13 | `version_check` | `evidence/eol_<producto>.json` | D8.1 |
| 14 | `package_registry_audit` | `evidence/registry_audit.json` | DAI.1 |
| 15 | `ai_attribution_analysis` | `evidence/ai_attribution.txt` | DAI.0 — **corre ANTES del fan-out de DAI** |
| 16 | `cloud_posture_scan` | `evidence/cloud_posture.json` | D4.4, D6.4, D6.5 |
| 17 | `mutation_testing` | `evidence/mutation/` | D5.1, DAI.4 |

Los checks que no están en esta tabla (`grep_search`, `file_exists`, `directory_structure_analysis`, `performance_test_analysis` y los T3 de juicio) los ejecuta cada subagente dentro de su dimensión, sin credenciales; si producen archivos, se registran también en el manifest con `produced_by: subagente`.

---

## 4. Fan-out — un subagente por dimensión

### 4.1 Orden de despacho

- **Primero:** resolver DAI.0 con `evidence/ai_attribution.txt` → sin atribución: DAI.2–4 nacen `unknown` (el subagente DAI lo sabe desde el despacho) y DAI.1/DAI.5 se evalúan igual.
- **Después:** las 10 dimensiones en paralelo (máx. 3–4 simultáneas; lanzar primero las T3-pesadas: D1, D3, D9, DAI).

### 4.2 Plantilla de despacho (prompt del subagente)

```
Rol: auditor técnico de la dimensión {DX — nombre}.
Fuente de verdad: framework/dimensions/{DX}.yaml (criterios NPLF con IDs estables,
checks, rúbrica) + framework/config/checks_catalog.yaml (contrato de cada check).
Targets bajo auditoría: repo/ (SOLO LECTURA, congelados en {targets[]}).
Evidencia compartida: referenciala por EV-id del evidence/manifest.json; NO
re-ejecutes checks compartidos. No tenés ni necesitás credenciales.

Reglas no negociables:
1. Evaluá cada criterio por su ID estable (DX.Y.Cn) con estado pass | fail |
   unknown. unknown = no pudiste comprobarlo; NUNCA lo marques fail salvo que
   producir la evidencia sea el control evaluado (unknown_policy).
2. Todo pass o fail lleva evidence_refs: EV-ids del manifest y/o citas
   archivo:línea@sha. Sin evidencia, el veredicto es inválido. unknown exige
   unknown_reason.
3. Recordá: un pass sostenido SOLO por señales T1 será reclasificado como
   no-confirmado por el orquestador — si un criterio importa, buscá evidencia
   T2 (EV de herramienta) o T3 (tu lectura de código citada).
4. Criterios critical/gate: rigor máximo y evidencia del tier exigido.
5. NO calcules scores, NO declares tiers, NO declares gates: eso lo deriva el
   orquestador desde la configuración canónica.
6. Escribí results/{DX}.json cumpliendo schemas/dimension_result.schema.json y
   respondé SOLO con: nº de pass/fail/unknown, hallazgos por severidad y
   bloqueos. Máximo 10 líneas. No pegues contenido de archivos.
```

### 4.3 Contrato de salida — `results/{DX}.json`

Schema canónico: **`schemas/dimension_result.schema.json`** (el orquestador valida cada resultado contra él; inválido = re-despacho con el error, nunca parcheo manual). Ejemplo mínimo:

```json
{
  "dimension_id": "D3",
  "targets": [{ "repo": "repo", "branch": "main", "sha": "a1b2c3d" }],
  "executed_at": "2026-08-01T14:30:00Z",
  "criteria_results": [
    {
      "criterion_ref": "D3.2.C1",
      "state": "fail",
      "evidence_refs": ["EV-0001", "src/config/db.ts:14@a1b2c3d"],
      "finding_refs": ["D3-F01"]
    },
    {
      "criterion_ref": "D3.2.C4",
      "state": "unknown",
      "evidence_refs": [],
      "unknown_reason": "Sin acceso a la configuración del gestor de secretos del ambiente productivo"
    }
  ],
  "findings": [
    {
      "id": "D3-F01",
      "severity": "critico",
      "title": "Credencial de base de datos viva en el historial de git",
      "description": "gitleaks la detecta en el historial y trufflehog confirma que sigue activa contra el endpoint productivo.",
      "evidence_refs": ["EV-0001", "src/config/db.ts:14@a1b2c3d"],
      "control_ref": "ISO 27001:2022 A.8.24 / ASVS 5.0 V14",
      "sub_dimension": "D3.2"
    }
  ],
  "na_subdimensions": []
}
```

El orquestador deriva de la configuración canónica: el **texto y criticidad** del criterio (YAML de dimensión), el **gate** (`failure_effect` + `evidence_required`), el **tier por criterio** (EV-id → check → tier del catálogo; citas `archivo:línea` = T3 solo si la sub-dimensión declara un check T3) y la **cobertura** (criterios del YAML sin resultado = unknown implícito, señalado como incompletitud del subagente).

---

## 5. Reconciliación (orquestador, antes del sello)

1. Cargar y validar los 10 `results/*.json`.
2. **Dedup de hallazgos:** clave = (archivo, línea±3, tipo). Duplicado ⇒ vive en su **dimensión primaria** (`double_counting_rules`): calidad genérica → D2; sobre código IA-atribuido → DAI; tests → D5 salvo phantom-IA → DAI.4; review → D9.2 salvo específico-IA → DAI.5; PII en logs → D4.5 (D7.1 lo cita).
3. Renumerar hallazgos globales (H-01…) preservando `source_ids`; los criterios no se deduplican.
4. Escribir `results/reconciliacion.json` (schema: `schemas/reconciliacion.schema.json`).

## 6. Sello de evidencia (después de fan-out y reconciliación — nunca antes)

1. Verificar que TODA la evidencia (compartida + generada por subagentes) está registrada en el manifest.
2. **Secret-scan final sobre `evidence/`** — valores vivos detectados ⇒ regenerar con redacción antes de continuar.
3. Completar `evidence/manifest.json`: `sealed: true`, `sealed_at`, SHA-256 de cada entrada (schema: `schemas/manifest.schema.json`). Publicar el SHA-256 del manifest en el informe.
4. **Congelar `evidence/` como read-only** (`chmod -R a-w evidence/`). Desde acá, cualquier corrección pasa por el log de §8 — la evidencia no se toca.

## 7. Scoring determinista (orquestador — cero juicio, solo aritmética)

Por cada sub-dimensión, sobre `criteria_results` + derivaciones del orquestador:

1. **Reclasificación por evidencia** (`evidence_resolution`): `pass` cuyo tier derivado es solo-T1 ⇒ **`unconfirmed`** (se trata como unknown). `fail` con T1 es válido (la presencia del anti-patrón citado ES la evidencia).
2. `evaluables = pass_confirmados + fail`. Si `evaluables = 0` ⇒ sub-dimensión `unknown`.
3. `pct = pass_confirmados / evaluables × 100` → F (86–100) | L (51–85) | P (16–50) | N (0–15) → {5.0, 3.5, 2.0, 1.0}.
4. **`risk_gate`** (demostrado): criterio-gate en `fail` con su `evidence_required` cumplido, o sub-dimensión crítica con rating ≤ P derivado de fails reales ⇒ `score = min(score, 2.0)` y cap global.
5. **`evidence_limit`** (insuficiencia): sub-dimensión crítica `unknown` (incluye todos-unconfirmed) o criterio-gate `unknown` ⇒ **NO** capa el PHS; marca PROVISIONAL + confidence low.
6. N/A y unknown ⇒ excluidos con renormalización de pesos; el peso excluido baja el **`coverage_ratio`**.

Por dimensión: `SD = Σ(score_i × w_i)` renormalizado; `confidence` según `confidence_levels`; `coverage_ratio` = peso evaluado / peso total.

Global: `PHS_ponderado = Σ(SD_k × W_k)`; **`PHS_reportable = min(PHS_ponderado, 2.9)` solo si hay `risk_gate`**; `provisional = true` si hay `evidence_limit`; `hri_count` desde `reconciliacion.json`; `coverage_ratio` global ponderado; `gap = target_phs − PHS_reportable`. Escribir `results/scoring.json` (schema: `schemas/scoring.schema.json`).

**Ejemplo 1 — riesgo demostrado (capa):** D3.2 con 6 criterios: 5 pass confirmados T2, 1 fail = D3.2.C1 (gate, evidencia T2 presente). pct 83% → L → 3.5, pero risk_gate ⇒ 2.0 ⇒ PHS reportable capado a 2.9 aunque el ponderado dé 4.1. Informe: "PHS 2.9 (ponderado 4.1) — risk_gate por D3.2.C1: secreto vivo. HRIs: 1 Crítico".

**Ejemplo 2 — evidencia insuficiente (NO capa):** D6.4 con todos sus criterios "pass" pero sostenidos solo por greps en IaC (T1, sin acceso a cloud). Todos ⇒ unconfirmed ⇒ evaluables 0 ⇒ sub-dimensión `unknown` ⇒ `evidence_limit`: PHS PROVISIONAL, confidence low, coverage_ratio baja — **sin cap**, porque no hay riesgo demostrado, hay falta de acceso. El informe lo lista como limitación bloqueante y pide el acceso.

## 8. Gate humano (bloqueante — sin firma no hay informe)

Checklist del auditor sobre `results/`:
- [ ] Cada hallazgo Crítico/Alto: ¿la evidencia citada realmente lo sostiene?
- [ ] Cada `risk_gate`: ¿true positive con el tier de evidencia exigido?
- [ ] Cada `evidence_limit`: ¿de verdad no había forma de obtener la evidencia? ¿Se pidió el acceso?
- [ ] Muestreo: 2–3 criterios `pass` al azar de dimensiones distintas — ¿la cita respalda el pass?
- [ ] Limitaciones completas; diagnóstico defendible frente al CTO del cliente.

**Correcciones — append-only, nunca edición directa:** cada corrección se registra como línea en `results/correcciones.jsonl`:

```json
{"ts": "2026-08-01T18:00:00Z", "auditor": "nombre", "target": "results/D3.json", "criterion_ref": "D3.2.C3", "from": "pass", "to": "fail", "motivo": "la evidencia citada no muestra rotación", "sha256_before": "…", "sha256_after": "…"}
```

Tras registrar, se aplica el cambio al `results/*.json` y se **recalcula** el scoring completo. El score jamás se edita a mano; el log viaja con el informe.

## 9. Render del informe

Poblar `templates/template_final_report.md` desde `scoring.json` + `reconciliacion.json` + `encuadre.json`: targets y perfil; PHS reportable/ponderado + PROVISIONAL si aplica; HRIs; risk_gates y evidence_limits nombrados; coverage_ratio; tabla de dimensiones con confianza; hallazgos H-xx con control_ref; delta si `baseline.comparable`; limitaciones con unknowns y SHA-256 del manifest; firma.

## 10. Cierre

1. Entregar informe; archivar `reports/` + `results/` + `correcciones.jsonl` como baseline del próximo delta.
2. **Custodia:** `evidence/` cifrada si sale de la máquina; destrucción al cierre del engagement, registrada.
3. Post-mortem del assessment (15 min): checks que no aplicaron, criterios ambiguos, tiempos reales → issues al repo del framework.

---

## Anexo A — Variantes por stack (el comando canónico vive en el catálogo)

| check_ref | JS/TS (Node) | Python | JVM | PHP | Go |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `dependency_graph_analysis` | madge | import-linter | ArchUnit | deptrac | go mod graph + análisis |
| `complexity_scan` | lizard -l javascript | radon / lizard | lizard -l java | lizard -l php | lizard -l go |
| `mutation_testing` | Stryker (`npx --no-install`) | mutmut | PITest | Infection | go-mutesting |
| `package_registry_audit` | npm registry API | PyPI JSON API | Maven Central API | Packagist API | proxy.golang.org |
| `version_check` (runtime) | node | python | openjdk | php | go |

## Anexo B — Presupuestos de tiempo (repo mediano, orientativos)

| Ítem | Presupuesto | Si se excede |
| :--- | :--- | :--- |
| Checks compartidos (§3) | 1–2 h máquina | Acotar semgrep/jscpd a `src/`; trivy sin licencias en primera pasada |
| Subagente mayormente-T2 (D2, D5, D6, D8) | 30–60 min c/u | Verificar que no re-ejecute checks compartidos |
| Subagente T3-pesado (D1, D3, D9, DAI) | 1–3 h c/u | Reducir muestra al mínimo del catálogo y declararlo |
| `mutation_testing` | ≤ 30 min, solo módulos core | Baseline en un solo módulo + limitación |
| Reconciliación + sello + scoring + render | 1–2 h | — |
| Gate humano | 1–2 h | No se recorta: es el control |

## Anexo C — Errores comunes y respuesta

| Situación | Respuesta correcta |
| :--- | :--- |
| Herramienta no instalada / sin licencia | `unknown` en los criterios dependientes + limitaciones. NO sustituir por grep. |
| Sin acceso a cloud ni IaC | D4.4/D6.4/D6.5 ⇒ `unknown`; D6.4 es crítica ⇒ `evidence_limit` (provisional, sin cap). Pedir acceso antes de cerrar. |
| Sub-dimensión con todos los pass en T1 | Se reclasifican `unconfirmed` ⇒ sub-dimensión `unknown`. Buscar evidencia T2/T3 antes de re-despachar. |
| Repo gigante (> 500k LOC) | Priorizar módulos core declarados por el cliente; declarar cobertura parcial. |
| Subagente devuelve JSON que no valida contra el schema | Re-despachar con el error de validación; nunca parchear a mano. |
| Subagente "estima" un criterio sin evidencia | Rechazar el resultado: evidence_refs o `unknown` con motivo. |
| Subagente declara tier/gate/score | Ignorar esos campos (el schema los rechaza) y recordarle el contrato. |
| Monorepo multi-app | Un assessment por app desplegable, o `targets[]` explícito de qué se evalúa. |
| Historial git truncado (shallow clone) | Re-clonar completo; si imposible, D3.2 pierde historial ⇒ `unknown` (crítica ⇒ `evidence_limit`). |
| Evidencia nueva después del sello | No se agrega a mano: se reabre §6 (nuevo manifest, nuevo sello, nuevo hash publicado) y se recalcula. |
