# Framework de Ejecución de Assessment de Plataformas de Software
## Guía de Orquestación y Ejecución Autónoma para Agentes IA / Auditores (Incluye Evaluación de Código Agéntico / IA)

---

### 1. Estructura del Framework

El framework de evaluación se organiza en los siguientes componentes dentro de la carpeta `assessment_framework/`:

```
assessment_framework/
├── README.md                           # Guía general de ejecución
├── RUNBOOK.md                          # Procedimiento operativo: orquestador + subagentes por dimensión
├── config/
│   ├── weights_and_thresholds.yaml     # Perfiles, gating rules, NPLF (pass/fail/unknown), tiers, severidad
│   └── checks_catalog.yaml             # Contrato de cada check + custodia de evidencia + modelo de ejecución seguro
├── schemas/                            # JSON Schemas: dimension, checks_catalog, config, pipeline
├── templates/
│   ├── assessment_master_pipeline.yaml # Pipeline maestro (paralelo + reconciliación, evidencia, gate humano, delta)
│   └── template_final_report.md        # Plantilla de informe final de salida
├── evidence/                           # (por assessment) outputs de herramientas con hash — NUNCA se commitea (.gitignore)
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

> **Para ejecutar un assessment real**, el procedimiento operativo completo (workspace, checks compartidos, plantilla de despacho de subagentes, contratos JSON de salida, scoring determinista, gate humano y presupuestos de tiempo) está en **[RUNBOOK.md](RUNBOOK.md)**. Lo que sigue es el resumen conceptual.

1. **Lectura de Configuración:** El Agente lee `config/weights_and_thresholds.yaml` para determinar las ponderaciones y el **nivel objetivo** del proyecto según su perfil (**Fintech, SaaS, MVP o AI-Native / Agentic** — los 4 perfiles existen en el YAML) y `config/checks_catalog.yaml` para el contrato de cada check.
2. **Inventario de Accesos:** Registra qué evidencia es accesible (repo, historial git, CI, consola cloud). Lo inaccesible se rige por la política N/D — nunca se estima.
3. **Ejecución Paralela de Dimensiones:** Ejecuta los checklists de `dimensions/` (D1 a D9 y DAI) — las 10 dimensiones son independientes. Dentro de DAI, la atribución (DAI.0) se resuelve primero porque define el universo del módulo.
4. **Archivo de Evidencia:** Todo output se registra en `evidence/manifest.json` con EV-id y hash; el **sello final** (secret-scan + freeze read-only) ocurre después del fan-out y la reconciliación. Un resultado T2 sin evidencia archivada se trata como T1 (su pass queda no-confirmado).
5. **Cálculo de Scores:** Método NPLF por sub-dimensión con tier derivado por criterio, política `unknown`, **`risk_gate`** (fail crítico demostrado acota el PHS a 2.9) vs. **`evidence_limit`** (provisional sin cap), y **HRIs + coverage_ratio** que acompañan siempre al PHS.
6. **Validación Humana:** Un auditor humano revisa y firma el borrador antes de la entrega — el mismo Human-in-the-Loop que el framework exige en DAI.5.
7. **Generación de Reporte:** Pobla `templates/template_final_report.md` con evidencias, severidades (Crítico/Alto/Medio/Bajo), confianza por dimensión, delta vs. assessment previo, **Platform Health Score (PHS)** y la sección obligatoria de Limitaciones y Alcance.

---

### 3. Principios No Negociables

* **Solo el riesgo demostrado capa:** un `risk_gate` (criterio-gate en fail con la evidencia exigida — secretos vivos, BOLA, backups irrecuperables, dependencia alucinada) acota el PHS a 2.9; la insuficiencia de evidencia (`evidence_limit`) vuelve el informe PROVISIONAL **sin** afirmar incumplimiento. El `coverage_ratio` acompaña siempre al PHS.
* **Presencia de strings ≠ verdad:** el tier se deriva **por criterio** desde sus evidence_refs — un `pass` solo-T1 queda no-confirmado (cuenta como unknown); un `fail` sí se demuestra con T1. Confirmar exige herramienta (T2) o juicio con citas (T3).
* **Evidencia o no pasó:** todo score debe ser re-verificable desde `evidence/` (manifest.json con EV-ids y hashes, sellado DESPUÉS del fan-out y congelado read-only) — y la evidencia se custodia: secretos redactados en origen, sin commit, cifrada y con retención definida.
* **El subagente no se auto-califica:** reporta estados + evidencia; gate, criticidad, tier y cobertura los deriva el orquestador desde la configuración canónica (schemas en `schemas/`).

### 4. Validación del Propio Framework

```bash
python3 scripts/validate_framework.py
```

Valida los YAML contra `schemas/` y cruza consistencia (pesos, check_refs, criticidad, IDs de criterios estables y únicos, criterios-gate, sub-dimensiones solo-T1) **y la coherencia operacional del RUNBOOK** (referencias `DX.Y`, tabla de checks compartidos ↔ declaraciones en dimensiones, JSON de ejemplo contra su schema, orden de fases, términos obsoletos). Corre en CI en cada push/PR (`.github/workflows/validate.yml`).

### 5. Roadmap de Ejecutabilidad

* **v3.1 (actual):** especificación validable — schemas + validador + CI; scoring determinista especificado (NPLF cerrado, gates, unknown).
* **v4 (siguiente):** runner sandboxed (contenedores efímeros, argv, red por allowlist, herramientas pinneadas por digest — requisitos ya normados en `checks_catalog.yaml §execution_model`), motor de scoring ejecutable, CLI (`paf validate | plan | run | score | report`), adaptadores por stack y fixtures con resultados esperados.
