# Informe Final de Assessment de Plataforma Tecnológica
## Diagnóstico de Calidad, Arquitectura, Seguridad, Código Agéntico (IA) y Madurez Operativa

**Fecha de Evaluación:** {{EVALUATION_DATE}}  
**Plataforma / Proyecto:** {{PROJECT_NAME}}  
**Commit / Revisión Evaluada:** {{COMMIT_SHA}}  
**Perfil Aplicado:** {{PROFILE_NAME}} (nivel objetivo: {{TARGET_PHS}} / 5.0)  
**Evaluador:** {{EVALUATOR_AGENT}}  
**Revisión Humana:** {{HUMAN_REVIEWER}} — {{REVIEW_DATE}}  

---

### 1. Resumen Ejecutivo y Platform Health Score (PHS)

#### Platform Health Score (PHS Reportable): **{{PHS_SCORE}} / 5.0**
#### Hallazgos de Alto Riesgo (HRIs) abiertos: **{{HRI_COUNT}}** ({{HRI_CRITICAL_COUNT}} Críticos, {{HRI_HIGH_COUNT}} Altos)

**Estado de Salud:** **{{HEALTH_STATUS}}**  
**Gap vs. Nivel Objetivo del Perfil:** {{TARGET_GAP}} ({{TARGET_GAP_INTERPRETATION}})  
**Techo por Gating:** {{GATING_NOTE}} <!-- "No aplica" o "PHS acotado a 2.9 por D3.2 = 1.0 (secretos en historial de git)" -->
**Diagnóstico Sintético:** {{EXECUTIVE_SUMMARY}}

> El PHS es una narrativa ejecutiva del promedio ponderado. **Nunca sustituye al conteo de HRIs**: un solo hallazgo Crítico abierto impide clasificar la plataforma por encima de "En Riesgo", sin importar el promedio (gating rules, `config/weights_and_thresholds.yaml`).

#### Evolución vs. Assessment Anterior
{{DELTA_SECTION}} <!-- "Baseline inicial — sin assessment previo" o tabla: PHS anterior -> actual, delta por dimensión, HRIs cerrados/nuevos -->

#### Mapa de Madurez por Dimensión (Radar Summary)

| Código | Dimensión | Puntaje (1-5) | Peso | Confianza | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **D1** | Arquitectura e Integración | {{D1_SCORE}} | {{D1_WEIGHT}} | {{D1_CONFIDENCE}} | {{D1_STATUS}} |
| **D2** | Código Fuente y Mantenibilidad | {{D2_SCORE}} | {{D2_WEIGHT}} | {{D2_CONFIDENCE}} | {{D2_STATUS}} |
| **D3** | Seguridad Aplicativa y DevSecOps | {{D3_SCORE}} | {{D3_WEIGHT}} | {{D3_CONFIDENCE}} | {{D3_STATUS}} |
| **D4** | Base de Datos y Gestión de Datos | {{D4_SCORE}} | {{D4_WEIGHT}} | {{D4_CONFIDENCE}} | {{D4_STATUS}} |
| **D5** | Calidad y Estrategia de QA | {{D5_SCORE}} | {{D5_WEIGHT}} | {{D5_CONFIDENCE}} | {{D5_STATUS}} |
| **D6** | DevOps, CI/CD e Infraestructura | {{D6_SCORE}} | {{D6_WEIGHT}} | {{D6_CONFIDENCE}} | {{D6_STATUS}} |
| **D7** | Observabilidad y SRE | {{D7_SCORE}} | {{D7_WEIGHT}} | {{D7_CONFIDENCE}} | {{D7_STATUS}} |
| **D8** | Gobernanza, Riesgos y Deuda | {{D8_SCORE}} | {{D8_WEIGHT}} | {{D8_CONFIDENCE}} | {{D8_STATUS}} |
| **D9** | SDLC y Gestión del Cambio | {{D9_SCORE}} | {{D9_WEIGHT}} | {{D9_CONFIDENCE}} | {{D9_STATUS}} |
| **DAI**| Código Agéntico e IA | {{DAI_SCORE}} | {{DAI_WEIGHT}} | {{DAI_CONFIDENCE}} | {{DAI_STATUS}} |

*Confianza: **Alta** (evidencia T2/T3 completa) · **Media** (checks parciales) · **Baja** (evidencia crítica no disponible). Definiciones en `config/weights_and_thresholds.yaml`.*

---

### 2. Auditoría de Código Generado por IA (Módulo DAI)

* **Atribución de Código IA (universo evaluado):** {{DAI_ATTRIBUTION_STATUS}}
* **Riesgo de Dependencias (Slopsquatting):** {{DAI_SLOPSQUATTING_STATUS}}
* **Robustez de Casos Borde (Happy-Path Bias):** {{DAI_HAPPYPATH_STATUS}}
* **Pruebas Fantasma (Phantom Tests):** {{DAI_PHANTOMTESTS_STATUS}}
* **Supervisión Humana (Human-in-the-Loop / SLSA Source L4):** {{DAI_HITL_STATUS}}
* **Seguridad de Features LLM (si aplica):** {{DAI_LLM_STATUS}}

---

### 3. Hallazgos y Matriz de Riesgos

Taxonomía de severidad (definiciones completas en `config/weights_and_thresholds.yaml`):
**Crítico** (HRI, remediar ≤ 7 días) · **Alto** (HRI, ≤ 30 días) · **Medio** (roadmap del trimestre) · **Bajo** (backlog).

Estándar de evidencia por hallazgo: cita `archivo:línea` + commit SHA + archivo de evidencia en `evidence/` + control de referencia (ASVS/CIS/ISO/SLSA).

| ID | Dimensión | Severidad | Descripción del Hallazgo / Brecha | Evidencia Técnica | Control Ref. |
| :--- | :--- | :---: | :--- | :--- | :--- |
| **H-01** | {{H_DIM}} | {{H_SEV}} | {{H_DESC}} | {{H_EVID}} | {{H_CONTROL_REF}} |

<!-- Repetir una fila por hallazgo (H-02, H-03, …). La tabla no tiene límite de filas: se listan TODOS los hallazgos Crítico/Alto/Medio; los Bajos pueden agruparse en un anexo. -->

---

### 4. Detalle de Evaluación por Dimensión

*(Poblado automáticamente con los resultados de cada ejecución D1-D9 y DAI: score NPLF por sub-dimensión, criterios cumplidos/incumplidos con citas, y checks N/D con su motivo)*

---

### 5. Roadmap de Remediación Priorizado (Matriz 2x2)

* **Ganancias Rápidas (Quick Wins - Alto Impacto / Bajo Esfuerzo):**
  * {{QUICK_WINS}}
* **Proyectos Estratégicos (Alto Impacto / Alto Esfuerzo):**
  * {{STRATEGIC_PROJECTS}}
* **Mejoras Menores (Bajo Impacto / Bajo Esfuerzo):**
  * {{MINOR_IMPROVEMENTS}}

---

### 6. Limitaciones y Alcance

*Sección obligatoria — sin ella, el informe no es defendible.*

* **Alcance evaluado:** {{SCOPE_DESCRIPTION}} <!-- repos, ramas, commit, ambientes -->
* **Accesos disponibles durante la evaluación:** {{ACCESS_INVENTORY}} <!-- código sí, historial CI no, consola cloud no, etc. -->
* **Evidencia no disponible (N/D):** {{ND_LIST}} <!-- cada check N/D, su sub-dimensión y cómo afectó el score/confianza -->
* **Supuestos:** {{ASSUMPTIONS}}
* **Fuera de alcance:** {{OUT_OF_SCOPE}}
* **Vigencia:** Este diagnóstico refleja el estado en el commit {{COMMIT_SHA}} a fecha {{EVALUATION_DATE}}; no cubre cambios posteriores.

---

### 7. Firma

| Rol | Nombre | Fecha |
| :--- | :--- | :--- |
| Agente evaluador | {{EVALUATOR_AGENT}} | {{EVALUATION_DATE}} |
| Auditor humano (revisión y aprobación) | {{HUMAN_REVIEWER}} | {{REVIEW_DATE}} |
