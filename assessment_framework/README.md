# Framework de Ejecución de Assessment de Plataformas de Software
## Guía de Orquestación y Ejecución Autónoma para Agentes IA / Auditores (Incluye Evaluación de Código Agéntico / IA)

---

### 1. Estructura del Framework

El framework de evaluación se organiza en los siguientes componentes dentro de la carpeta `assessment_framework/`:

```
assessment_framework/
├── README.md                           # Guía general de ejecución
├── config/
│   ├── weights_and_thresholds.yaml     # Perfiles, gating rules, NPLF, tiers de evidencia, N/D, severidad
│   └── checks_catalog.yaml             # Contrato de ejecución de cada check (herramienta, comando, parsing, score)
├── templates/
│   ├── assessment_master_pipeline.yaml # Pipeline maestro (paralelo, evidencia, validación humana, delta)
│   └── template_final_report.md        # Plantilla de informe final de salida
├── evidence/                           # (por assessment) outputs crudos de herramientas, con hash — re-verificables
├── reports/                            # (por assessment) informes finales; el previo sirve de baseline para el delta
└── dimensions/
    ├── D1_Arquitectura_Integracion.md  | .yaml # Guía técnica y YAML D1
    ├── D2_Codigo_Mantenibilidad.md     | .yaml # Guía técnica y YAML D2
    ├── D3_Seguridad_DevSecOps.md       | .yaml # Guía técnica y YAML D3 (incluye D3.5 BOLA/BFLA)
    ├── D4_BaseDatos_GestionDatos.md    | .yaml # Guía técnica y YAML D4 (incluye D4.5 Privacidad)
    ├── D5_Calidad_EstrategiaQA.md      | .yaml # Guía técnica y YAML D5 (incluye D5.5 Performance)
    ├── D6_DevOps_Infraestructura.md    | .yaml # Guía técnica y YAML D6 (incluye D6.5 FinOps)
    ├── D7_Observabilidad_Resiliencia.md| .yaml # Guía técnica y YAML D7
    ├── D8_Gobernanza_Riesgos.md        | .yaml # Guía técnica y YAML D8
    ├── D9_SDLC_GestionCambio.md        | .yaml # SDLC: branching, code review, trazabilidad, hotfixes
    └── DAI_Codigo_Agentico_IA.md       | .yaml # Módulo especializado para Código Generado por IA
```

---

### 2. Flujo de Ejecución del Agente IA

1. **Lectura de Configuración:** El Agente lee `config/weights_and_thresholds.yaml` para determinar las ponderaciones y el **nivel objetivo** del proyecto según su perfil (**Fintech, SaaS, MVP o AI-Native / Agentic** — los 4 perfiles existen en el YAML) y `config/checks_catalog.yaml` para el contrato de cada check.
2. **Inventario de Accesos:** Registra qué evidencia es accesible (repo, historial git, CI, consola cloud). Lo inaccesible se rige por la política N/D — nunca se estima.
3. **Ejecución Paralela de Dimensiones:** Ejecuta los checklists de `dimensions/` (D1 a D9 y DAI) — las 10 dimensiones son independientes. Dentro de DAI, la atribución (DAI.0) se resuelve primero porque define el universo del módulo.
4. **Archivo de Evidencia:** Todo output de herramienta se guarda en `evidence/` con hash. Un score T2 sin evidencia archivada se degrada a T1 (techo 3.0).
5. **Cálculo de Scores:** Método NPLF por sub-dimensión, techos por tier de evidencia, política N/D, **gating rules** (un crítico ≤ 2.0 acota el PHS a 2.9) y conteo de **HRIs** que acompaña siempre al PHS.
6. **Validación Humana:** Un auditor humano revisa y firma el borrador antes de la entrega — el mismo Human-in-the-Loop que el framework exige en DAI.5.
7. **Generación de Reporte:** Pobla `templates/template_final_report.md` con evidencias, severidades (Crítico/Alto/Medio/Bajo), confianza por dimensión, delta vs. assessment previo, **Platform Health Score (PHS)** y la sección obligatoria de Limitaciones y Alcance.

---

### 3. Principios No Negociables

* **Lo crítico no se promedia:** el PHS es narrativa ejecutiva; los HRIs se cuentan y acotan (ISO 33020 / TMMi / AWS WA).
* **Presencia de strings ≠ verdad:** los greps son señal T1 con techo 3.0; los scores altos exigen herramienta (T2) o juicio con citas (T3).
* **Evidencia o no pasó:** todo score debe ser re-verificable desde `evidence/`.
* **La ausencia de evidencia en un control crítico ES el hallazgo**, no un vacío neutro.
