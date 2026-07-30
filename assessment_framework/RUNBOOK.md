# RUNBOOK — Ejecución del Assessment por Agente

> **Qué es:** el procedimiento operativo paso a paso para ejecutar el assessment contra un repositorio real, diseñado para un **agente orquestador** que despacha **subagentes por dimensión**. Es la implementación manual-agéntica del pipeline (`templates/assessment_master_pipeline.yaml`) mientras no exista el runner v4.
>
> **Qué no es:** no reemplaza los YAML (que son la fuente de verdad de criterios y checks) ni al auditor humano (paso 7, bloqueante).

---

## 0. Modelo de ejecución

| Rol | Responsabilidad |
| :--- | :--- |
| **Orquestador** | Encuadre, checks compartidos, despacho de subagentes, reconciliación, scoring, render del informe. NO lee evidencia cruda: consume `results/*.json`. |
| **Subagente de dimensión** (×10) | Evalúa UNA dimensión siguiendo su YAML: ejecuta/lee los checks, evalúa cada criterio NPLF con citas, emite hallazgos. Devuelve SOLO el JSON del contrato (§4.3) — nunca volcados de archivos. |
| **Auditor humano** | Revisa y firma el borrador (gate bloqueante, §7). |

**Regla de economía de contexto:** los subagentes escriben su resultado a `results/` y responden con un resumen de ≤ 10 líneas. El orquestador jamás carga outputs crudos de herramientas en su contexto — para eso está `evidence/` + el manifest.

---

## 1. Encuadre (Fase 0 — sin esto no se empieza)

Checklist que el orquestador completa y registra en `results/encuadre.json`:

1. **Perfil** elegido (`general_saas` | `fintech_critical` | `mvp_startup` | `ai_native_agentic`) → fija pesos y `target_phs`.
2. **Alcance congelado:** lista de repos, rama y **SHA exacto** por repo. Todo el assessment referencia esos SHAs.
3. **Inventario de accesos** (determina el techo de confianza del informe — lo inaccesible será `unknown`, nunca estimado):
   - [ ] Código fuente (clone completo, no shallow: `git clone --no-single-branch`, historial entero)
   - [ ] API del repositorio (gh/glab autenticado: branch protection, PRs, runs)
   - [ ] Consola cloud read-only o, en su defecto, el IaC
   - [ ] Historial del pipeline de CI
   - [ ] Acceso a ambientes (solo lectura, si aplica)
4. **Toolchain pinneada:** versiones exactas de gitleaks, semgrep (+ versión del ruleset), trivy/osv-scanner, jscpd, lizard, herramienta de grafo según stack, prowler/checkov, gh. Se registran en `evidence/manifest.json`.
5. **Workspace del assessment** (fuera del repo del cliente):

```
assessment-<cliente>-<YYYYMMDD>/
├── repo/          # clone congelado al SHA (read-only para subagentes)
├── framework/     # copia de assessment_framework/ (versión registrada)
├── evidence/      # outputs de herramientas — NUNCA se commitea, custodia según catálogo
├── results/       # encuadre.json, D1.json..DAI.json, reconciliacion.json, scoring.json
└── reports/       # informe final + baseline previa si existe
```

6. **Seguridad de ejecución** (`checks_catalog.yaml §execution_model`): repo no confiable ⇒ contenedor efímero, red off por defecto (allowlist solo para endoflife.date y registries), credenciales cloud read-only de alcance mínimo.
7. **Baseline delta:** si hay assessment previo, copiarlo a `reports/baseline/` y verificar `delta_comparability_rules` — si no se cumplen, marcar desde ya "delta indicativo".

---

## 2. Preflight técnico

El orquestador verifica que cada herramienta corre e imprime versión; lo que falte se anota de una vez como `unknown` en los checks que dependan de ella (no se sustituye por grep):

```
gitleaks version && semgrep --version && trivy --version && jscpd --version \
  && lizard --version && gh --version
```

Detección de stack (define los comandos del Anexo A): lockfiles presentes, lenguajes por extensión dominante, monorepo (workspaces/turbo.json), framework (next/express/spring/django...).

---

## 3. Checks compartidos (el orquestador los corre UNA sola vez)

Estos outputs alimentan a varias dimensiones — correrlos por subagente duplicaría costo y rompería consistencia. Nombres de archivo canónicos (los subagentes los referencian tal cual):

| # | Comando (contrato completo en `config/checks_catalog.yaml`) | Output canónico | Consumido por |
| :-- | :--- | :--- | :--- |
| 1 | `gitleaks git --redact --report-format json --report-path evidence/gitleaks.json repo/` | `evidence/gitleaks.json` | D3.2 |
| 2 | `semgrep scan --config <ruleset pinneado> --json -o evidence/semgrep.json repo/src` | `evidence/semgrep.json` | D2.4, D3.1, D3.4, D4.2, DAI.2 |
| 3 | `trivy fs --scanners vuln,license --format json -o evidence/trivy.json repo/` | `evidence/trivy.json` | D3.3, D8.1 |
| 4 | `jscpd --reporters json --output evidence/ repo/src` | `evidence/jscpd/` | D2.2, DAI.3 |
| 5 | `lizard -l <lang> --csv repo/src > evidence/lizard.csv` | `evidence/lizard.csv` | D2.2, D8.4 |
| 6 | grafo según stack (`madge --circular --json`, `deptrac`, ArchUnit, `import-linter`) | `evidence/depgraph.json` | D1.1, D1.3 |
| 7 | `gh api repos/{o}/{r}/branches/<main>/protection` | `evidence/branch_protection.json` | D5.3, D9.1 |
| 8 | `gh pr list --state merged --limit 100 --json number,reviews,author,additions,mergedAt` | `evidence/prs.json` | D9.2, DAI.5 |
| 9 | `gh run list --limit 200 --json status,conclusion,createdAt,updatedAt` + deployments | `evidence/ci_runs.json` | D6.2 |
| 10 | `git -C repo log -n 200 --no-merges --pretty=format:'%h\|%s'` | `evidence/commit_log.txt` | D9.3 |
| 11 | `git -C repo shortlog -sn --no-merges --since='12 months ago' -- <path>` (por componente core) | `evidence/shortlog_<comp>.txt` | D8.3, D9.1, D9.4 |
| 12 | endoflife.date API por producto detectado | `evidence/eol_<producto>.json` | D8.1 |
| 13 | registry audit npm/PyPI de dependencias directas (osv-scanner + API) | `evidence/registry_audit.json` | DAI.1 |
| 14 | `git -C repo log --grep='Co-Authored-By' --oneline` + política AGENTS/CLAUDE.md + labels de PR | `evidence/ai_attribution.txt` | **DAI.0 — corre ANTES del fan-out de DAI** |
| 15 | `prowler <cloud> -M json-ocsf -o evidence/` o `checkov -d repo/infra -o json` | `evidence/cloud_posture.json` | D4.4, D6.4, D6.5 |

Al terminar: generar `evidence/manifest.json` (por archivo: ruta, SHA-256, herramienta+versión, argv, SHA objetivo, timestamps, exit code) y correr **secret-scan sobre `evidence/`** — si detecta valores vivos, regenerar con redacción antes de seguir.

---

## 4. Fan-out — un subagente por dimensión

### 4.1 Orden de despacho

- **Primero:** resolver DAI.0 con `evidence/ai_attribution.txt` → si no hay atribución: DAI.2–4 nacen `unknown` (pesos redistribuidos) y el subagente DAI lo sabe desde el despacho.
- **Después:** las 10 dimensiones en paralelo (máx. 3–4 simultáneas para no saturar; las de más T3 — D1, D3, D9 — conviene lanzarlas primero porque son las lentas).

### 4.2 Plantilla de despacho (prompt del subagente)

```
Rol: auditor técnico de la dimensión {DX — nombre}.
Fuente de verdad: framework/dimensions/{DX}.yaml (criterios NPLF, checks, rúbrica)
                  + framework/config/checks_catalog.yaml (contrato de cada check).
Repo bajo auditoría: repo/ (SOLO LECTURA, congelado en {SHA}).
Evidencia compartida ya generada: evidence/ (usar los archivos canónicos listados
en tu YAML; NO re-ejecutar checks compartidos).

Reglas no negociables:
1. Cada criterio NPLF se evalúa pass | fail | unknown. unknown = no pudiste
   comprobarlo; NUNCA lo marques fail salvo que producir la evidencia sea el
   control evaluado (unknown_policy).
2. Todo pass o fail lleva evidencia citada: archivo:línea del repo, y/o el
   archivo de evidence/ que lo respalda. Sin cita, el veredicto es inválido.
3. Los checks T1 (grep/file_exists) solos NO alcanzan: si tu única evidencia es
   T1, decláralo (el scoring lo capará a P). Para criterios T3 debés LEER el
   código (muestra mínima: la definida en el catálogo).
4. Criterios marcados critical/gate: verificalos con rigor máximo; un fail ahí
   acota el assessment completo.
5. NO calcules scores. Tu output son estados + evidencia + hallazgos.
6. Escribí tu resultado en results/{DX}.json con el contrato exacto (abajo) y
   respondé SOLO con: nº de criterios pass/fail/unknown, hallazgos por severidad
   y cualquier bloqueo. Máximo 10 líneas. No pegues contenido de archivos.
```

### 4.3 Contrato de salida — `results/{DX}.json`

```json
{
  "dimension_id": "D3",
  "commit_sha": "<SHA evaluado>",
  "executed_at": "<ISO 8601>",
  "sub_dimensions": [
    {
      "id": "D3.2",
      "criteria": [
        {
          "ref": "D3.2.C1",
          "text": "No existen secretos VIVOS...",
          "state": "pass | fail | unknown",
          "gate": true,
          "evidence": ["evidence/gitleaks.json", "src/config/db.ts:14 @ <sha>"],
          "note": "opcional, 1 línea"
        }
      ],
      "tiers_used": ["T1", "T2"],
      "unknown_reason": null,
      "na_reason": null
    }
  ],
  "findings": [
    {
      "severity": "critico | alto | medio | bajo",
      "title": "Secreto AWS vivo en historial",
      "description": "1-3 líneas",
      "evidence": "cita archivo:línea + commit + archivo de evidence/",
      "control_ref": "ASVS 5.0 V14 / ISO 27001:2022 A.8.24",
      "gate": true,
      "sub_dimension": "D3.2"
    }
  ]
}
```

Notas: los criterios string del YAML se referencian por índice (`D3.2#2`); `na_reason` solo para condicionales (DAI.6 sin LLMs). El orquestador valida cada JSON contra este contrato antes de aceptar el resultado del subagente — JSON inválido = re-despacho, no parcheo manual.

---

## 5. Reconciliación (orquestador, antes del scoring)

1. Cargar los 10 `results/*.json`.
2. **Dedup de hallazgos:** clave = (archivo, línea±3, tipo de defecto). Duplicado entre dimensiones ⇒ vive en su **dimensión primaria** (`double_counting_rules`): calidad de código genérica → D2; sobre código IA-atribuido → DAI; tests → D5 salvo phantom-IA → DAI.4; review → D9.2 salvo específico-IA → DAI.5; PII en logs → D4.5 (D7.1 lo cita).
3. Los criterios NO se deduplican (cada dimensión evalúa lo suyo); solo los hallazgos.
4. Escribir `results/reconciliacion.json`: hallazgos fusionados + mapa de duplicados resueltos.

---

## 6. Scoring determinista (orquestador — cero juicio, solo aritmética)

Por cada sub-dimensión:

1. `evaluables = pass + fail` (los `unknown` salen del denominador). Si `evaluables = 0` ⇒ sub-dimensión `unknown`.
2. `pct = pass / evaluables × 100` → rating: F (86–100) | L (51–85) | P (16–50) | N (0–15) → score {5.0, 3.5, 2.0, 1.0}.
3. **Techo T1:** si `tiers_used ⊆ {T1}` ⇒ `score = min(score, 2.0)`.
4. **Criterio-gate en fail** ⇒ `score = min(score, 2.0)` y se marca `gate_activated`.
5. N/A (condicionales) ⇒ se excluye y se renormalizan los pesos de la dimensión; `unknown` no crítico ⇒ ídem + confianza degradada.

Por dimensión: `SD = Σ(score_i × w_i)` con pesos renormalizados si hubo exclusiones. Confianza: `high` (todo T2/T3, sin unknown en críticas) | `medium` | `low` (unknown en crítica o mayoría T1).

Global:
- `PHS_ponderado = Σ(SD_k × W_k)` con los pesos del perfil.
- **Gating:** alguna sub-dimensión crítica ≤ 2.0 o gate activado ⇒ `PHS_reportable = min(PHS_ponderado, 2.9)`.
- **Provisional:** `unknown` en sub-dimensión crítica ⇒ PHS marcado PROVISIONAL, estado de salud no declarable ≥ "Bueno/Estable".
- `HRI_count` = hallazgos Crítico + Alto (de `reconciliacion.json`). `gap = target_phs − PHS_reportable`.

**Ejemplo numérico** (D3.2 con 5 criterios: 4 pass, 1 fail y ese fail es el gate C1): pct = 80% → L → 3.5; pero gate en fail ⇒ score 2.0 ⇒ D3.2 ≤ 2.0 y es crítica ⇒ PHS reportable capado a 2.9 aunque el ponderado dé 4.1. El informe dice: "PHS 2.9 (ponderado 4.1) — gating por D3.2.C1: secreto vivo. HRIs: 1 Crítico".

Escribir `results/scoring.json` con todo lo anterior (por sub-dimensión, dimensión y global).

---

## 7. Gate humano (bloqueante — sin firma no hay informe)

El auditor revisa contra `results/`:
- [ ] Cada hallazgo Crítico/Alto: ¿la evidencia citada realmente lo sostiene?
- [ ] Cada gate activado: ¿es un true positive?
- [ ] Cada `unknown` en crítica: ¿de verdad no había forma de obtener la evidencia?
- [ ] Muestreo: 2–3 criterios `pass` al azar de dimensiones distintas — ¿la cita respalda el pass?
- [ ] Sección de limitaciones completa y honesta.
- [ ] ¿El diagnóstico sintético es defendible frente al CTO del cliente?

Correcciones ⇒ se corrige el `results/*.json` correspondiente y se **recalcula** el scoring (nunca se edita el score a mano).

---

## 8. Render del informe

Poblar `templates/template_final_report.md` desde `results/scoring.json` + `reconciliacion.json` + `encuadre.json`: metadatos y perfil del encuadre; PHS reportable/ponderado, HRIs, gating y provisional del scoring; tabla de dimensiones con confianza; hallazgos ordenados por severidad (una fila cada uno, control_ref incluido); delta si hay baseline comparable; limitaciones con la lista de unknown y el SHA-256 del manifest; firma.

---

## 9. Cierre

1. Entregar informe; archivar `reports/` + `results/` como baseline del próximo delta.
2. **Custodia:** `evidence/` cifrada si sale de la máquina; destrucción al cierre del engagement, registrada (`evidence_custody`).
3. Post-mortem del assessment (15 min): checks que no aplicaron, criterios ambiguos, tiempos reales → issues al repo del framework. El primer assessment real es también el piloto del framework.

---

## Anexo A — Comandos por stack (variantes del §3)

| Check | JS/TS (Node) | Python | JVM | PHP | Go |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Grafo dependencias | `madge --circular --json src/` | `lint-imports` (import-linter) | ArchUnit (test) | `deptrac analyse` | `go mod graph` + análisis |
| Complejidad | `lizard -l javascript` | `radon cc -j` o lizard | `lizard -l java` | `lizard -l php` | `lizard -l go` |
| Mutation (acotado a core) | `npx stryker@<ver> run` | `mutmut run --paths-to-mutate <core>` | PITest (plugin build) | Infection | go-mutesting |
| Registry audit | npm registry API | PyPI JSON API | Maven Central API | Packagist API | proxy.golang.org |
| Lockfile | package-lock/pnpm-lock/yarn.lock | poetry.lock/Pipfile.lock/uv.lock | (versionado en pom/gradle) | composer.lock | go.sum |
| EOL runtime | `node` en endoflife.date | `python` | `openjdk` | `php` | `go` |

## Anexo B — Presupuestos de tiempo (por repo mediano, orientativos)

| Ítem | Presupuesto | Si se excede |
| :--- | :--- | :--- |
| Checks compartidos (§3) | 1–2 h máquina | Acotar semgrep/jscpd a `src/`; trivy sin `--scanners license` en primera pasada |
| Subagente dimensión mayormente-T2 (D2, D5, D6, D8) | 30–60 min c/u | Revisar que no re-ejecute checks compartidos |
| Subagente T3-pesado (D1, D3, D9, DAI) | 1–3 h c/u | Reducir muestra al mínimo del catálogo, declarar el resto |
| Mutation testing | ≤ 30 min, solo módulos core | Baseline en un solo módulo y anotar limitación |
| Reconciliación + scoring + render | 1–2 h | — |
| Gate humano | 1–2 h | No se recorta: es el control |

## Anexo C — Errores comunes y respuesta

| Situación | Respuesta correcta |
| :--- | :--- |
| Herramienta no instalada / sin licencia | `unknown` en los criterios dependientes + nota en limitaciones. NO sustituir por grep. |
| Sin acceso a cloud ni IaC | D4.4/D6.4/D6.5 ⇒ `unknown`; D6.4 es crítica ⇒ PHS provisional. Pedir acceso antes de cerrar el informe. |
| Repo gigante (> 500k LOC) | Priorizar módulos core declarados por el cliente; muestrear el resto; declarar cobertura parcial en limitaciones. |
| Subagente devuelve JSON inválido | Re-despachar con el error de validación; nunca parchear a mano el resultado. |
| Subagente "estima" un criterio sin cita | Rechazar el resultado: cita o `unknown`. |
| Monorepo multi-app | Un assessment por app desplegable, o alcance explícito de cuál app se evalúa. |
| Historial git truncado (shallow clone) | Re-clonar completo; si imposible, D3.2 pierde el escaneo de historial ⇒ `unknown` (crítica ⇒ provisional). |
