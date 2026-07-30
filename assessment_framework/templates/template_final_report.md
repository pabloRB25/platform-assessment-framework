# Informe Final de Assessment de Plataforma Tecnológica
## Diagnóstico de Calidad, Arquitectura, Seguridad, SDLC, Código Agéntico (IA) y Madurez Operativa

**Fecha de Evaluación:** {{EVALUATION_DATE}}  
**Plataforma / Proyecto:** {{PROJECT_NAME}}  
**Commit / Revisión Evaluada:** {{COMMIT_SHA}}  
**Versión del Framework / Catálogo:** {{FRAMEWORK_VERSION}} / {{CATALOG_VERSION}}  
**Perfil Aplicado:** {{PROFILE_NAME}} (Target PHS: {{TARGET_PHS}})  
**Evaluador:** {{EVALUATOR_AGENT}}  
**Auditor Humano Responsable:** {{HUMAN_AUDITOR_SIGNATURE}}  

---

### 1. Resumen Ejecutivo y Platform Health Score (PHS)

#### Platform Health Score Reportable: **{{PHS_REPORTABLE}} / 5.0** (PHS Ponderado: {{PHS_PONDERADO}}){{PHS_PROVISIONAL_FLAG}}
**Estado de Salud:** **{{HEALTH_STATUS}}**  
**Conteo de Hallazgos de Alto Riesgo (HRIs Abiertos):** **{{HRI_COUNT}}** ({{HRI_CRITICAL_COUNT}} Críticos / {{HRI_HIGH_COUNT}} Altos)  
**Cobertura de la Evaluación (coverage_ratio):** {{COVERAGE_RATIO}} *(porcentaje del peso del perfil realmente evaluado — un PHS con cobertura baja no es comparable con uno de cobertura alta)*  
**Risk Gates Activados:** {{RISK_GATES}} *(fail crítico DEMOSTRADO ⇒ PHS acotado a máximo 2.9)*  
**Limitaciones de Evidencia (evidence_limit):** {{EVIDENCE_LIMITS}} *(insuficiencia de evidencia en zona crítica ⇒ PHS PROVISIONAL, sin cap — no afirma incumplimiento)*  
**Gap vs. Nivel Objetivo del Perfil:** {{TARGET_GAP}}  
**Diagnóstico Sintético:** {{EXECUTIVE_SUMMARY}}

> **Riesgo demostrado ≠ evidencia insuficiente.** Un `risk_gate` acota el PHS porque hay un fail crítico con evidencia. Un `evidence_limit` marca el PHS como **PROVISIONAL** (no declarable ≥ "Bueno / Estable") porque un control crítico no pudo comprobarse — se pide la evidencia, no se declara el riesgo.

#### Evolución vs. Assessment Anterior
{{DELTA_SECTION}} <!-- "Baseline inicial — sin assessment previo" | tabla PHS anterior→actual + delta por dimensión + HRIs cerrados/nuevos. Si no se cumplen delta_comparability_rules: "delta indicativo, no comparable" con el motivo. -->

#### Mapa de Madurez por Dimensión (10 Dimensiones - NPLF / ISO 33020)

| Código | Dimensión | Puntaje Obtenido (1-5) | Peso Relativo | Confianza | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **D1** | Arquitectura e Integración | {{D1_SCORE}} | {{D1_WEIGHT}} | {{D1_CONF}} | {{D1_STATUS}} |
| **D2** | Código Fuente y Mantenibilidad | {{D2_SCORE}} | {{D2_WEIGHT}} | {{D2_CONF}} | {{D2_STATUS}} |
| **D3** | Seguridad Aplicativa y DevSecOps | {{D3_SCORE}} | {{D3_WEIGHT}} | {{D3_CONF}} | {{D3_STATUS}} |
| **D4** | Base de Datos y Gestión de Datos | {{D4_SCORE}} | {{D4_WEIGHT}} | {{D4_CONF}} | {{D4_STATUS}} |
| **D5** | Calidad y Estrategia de QA | {{D5_SCORE}} | {{D5_WEIGHT}} | {{D5_CONF}} | {{D5_STATUS}} |
| **D6** | DevOps, CI/CD e Infraestructura | {{D6_SCORE}} | {{D6_WEIGHT}} | {{D6_CONF}} | {{D6_STATUS}} |
| **D7** | Observabilidad y SRE | {{D7_SCORE}} | {{D7_WEIGHT}} | {{D7_CONF}} | {{D7_STATUS}} |
| **D8** | Gobernanza, Riesgos y Deuda | {{D8_SCORE}} | {{D8_WEIGHT}} | {{D8_CONF}} | {{D8_STATUS}} |
| **D9** | SDLC y Gestión del Cambio | {{D9_SCORE}} | {{D9_WEIGHT}} | {{D9_CONF}} | {{D9_STATUS}} |
| **DAI**| Código Agéntico e IA | {{DAI_SCORE}} | {{DAI_WEIGHT}} | {{DAI_CONF}} | {{DAI_STATUS}} |

*Confianza: **Alta** (T2/T3 completa, sin unknown en críticas) · **Media** (checks parciales) · **Baja** (unknown en crítica — bloquea dictamen de alta confianza).*

---

### 2. Auditoría de Código Generado por IA (Módulo DAI)

* **Atribución y Trazabilidad de Código IA (DAI.0):** {{DAI_ATTRIBUTION_STATUS}}
* **Riesgo de Dependencias (Slopsquatting - DAI.1):** {{DAI_SLOPSQUATTING_STATUS}}
* **Robustez de Casos Borde (Happy-Path Bias - DAI.2):** {{DAI_HAPPYPATH_STATUS}}
* **Pruebas Fantasma (Phantom Tests - DAI.4):** {{DAI_PHANTOMTESTS_STATUS}}
* **Supervisión Humana (Human-in-the-Loop - DAI.5):** {{DAI_HITL_STATUS}}
* **Seguridad de Features LLM (DAI.6, si aplica):** {{DAI_LLM_STATUS}}

*Nota de universo: sin atribución verificable, DAI.2–DAI.4 se reportan como `unknown` (no se asume que el código reciente sea de IA); DAI.1 y DAI.5 se evalúan sobre el repo y el proceso completos.*

---

### 3. Hallazgos Críticos y Matriz de Riesgos (HRIs)

Severidad: **Crítico** (HRI, ≤ 7 días) · **Alto** (HRI, ≤ 30 días) · **Medio** (trimestre) · **Bajo** (backlog) — definiciones en `config/weights_and_thresholds.yaml`.

| ID Hallazgo | Dimensión | Severidad | Descripción del Hallazgo / Brecha | Evidencia Técnica (Cita `archivo:línea`) | Control Ref. |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **H-01** | {{H_DIM}} | {{H_SEV}} | {{H_DESC}} | {{H_EVID}} | {{H_CONTROL_REF}} |

<!-- Repetir una fila por hallazgo (H-02, H-03, …) — la tabla lista TODOS los Crítico/Alto/Medio; los Bajos pueden agruparse en anexo. Evidencia = cita archivo:línea + commit + archivo en evidence/ referenciado por manifest.json. -->

---

### 4. Limitaciones y Alcance del Assessment

* **Alcance evaluado:** {{SCOPE_DESCRIPTION}} <!-- repos, ramas, commit, ambientes -->
* **Accesos disponibles durante la evaluación:** {{ACCESS_INVENTORY}}
* **Controles en estado unknown (evidencia no disponible):** {{UNKNOWN_LIST}} <!-- cada uno con su sub-dimensión y efecto sobre confianza/estado -->
* **Supuestos de Evaluación:** {{EVALUATION_ASSUMPTIONS}}
* **Fuera de alcance:** {{OUT_OF_SCOPE}}
* **Integridad de la evidencia:** SHA-256 del `evidence/manifest.json`: `{{MANIFEST_HASH}}`
* **Vigencia:** Este diagnóstico refleja el estado en el commit {{COMMIT_SHA}} a fecha {{EVALUATION_DATE}}; no cubre cambios posteriores.

---

### 5. Roadmap de Remediación Priorizado (Matriz 2x2)

* **Ganancias Rápidas (Quick Wins - Alto Impacto / Bajo Esfuerzo):**
  * {{QUICK_WINS}}
* **Proyectos Estratégicos (Alto Impacto / Alto Esfuerzo):**
  * {{STRATEGIC_PROJECTS}}
* **Mejoras Menores (Bajo Impacto / Bajo Esfuerzo):**
  * {{MINOR_IMPROVEMENTS}}

---
**Firma del Auditor Humano Responsable:**  
`____________________________________`  
**Fecha de Aprobación:** {{APPROVAL_DATE}}
