# Framework de Ejecución de Assessment de Plataformas de Software
## Guía de Orquestación y Ejecución Autónoma para Agentes IA / Auditores (Incluye Evaluación de Código Agéntico / IA)

---

### 1. Estructura del Framework

El framework de evaluación se organiza en los siguientes componentes dentro de la carpeta `assessment_framework/`:

```
assessment_framework/
├── README.md                           # Guía general de ejecución
├── config/
│   └── weights_and_thresholds.yaml      # Configuración de ponderaciones y niveles (incluye perfil AI-Native)
├── templates/
│   ├── assessment_master_pipeline.yaml # Pipeline maestro de orquestación para el Agente
│   └── template_final_report.md        # Plantilla de informe final de salida
└── dimensions/
    ├── D1_Arquitectura_Integracion.md  | .yaml # Guía técnica y YAML D1
    ├── D2_Codigo_Mantenibilidad.md     | .yaml # Guía técnica y YAML D2
    ├── D3_Seguridad_DevSecOps.md       | .yaml # Guía técnica y YAML D3
    ├── D4_BaseDatos_GestionDatos.md    | .yaml # Guía técnica y YAML D4
    ├── D5_Calidad_EstrategiaQA.md      | .yaml # Guía técnica y YAML D5
    ├── D6_DevOps_Infraestructura.md    | .yaml # Guía técnica y YAML D6
    ├── D7_Observabilidad_Resiliencia.md| .yaml # Guía técnica y YAML D7
    ├── D8_Gobernanza_Riesgos.md        | .yaml # Guía técnica y YAML D8
    └── DAI_Codigo_Agentico_IA.md       | .yaml # Módulo especializado para Código Generado por IA
```

---

### 2. Flujo de Ejecución del Agente IA

1. **Lectura de Configuración:** El Agente lee `config/weights_and_thresholds.yaml` para determinar las ponderaciones del proyecto según su perfil (Fintech, SaaS, MVP o AI-Native / Agentic).
2. **Ejecución Secuencial/Paralela:** El Agente ejecuta los checklists definidos en los archivos YAML de la carpeta `dimensions/` (D1 a D8 y DAI).
3. **Cálculo de Scores:** Aplica las fórmulas de ponderación por sub-dimensión y dimensión.
4. **Generación de Reporte:** Pobla la plantilla `templates/template_final_report.md` agregando evidencias, auditoría de código generado por IA, severidad de hallazgos y el **Platform Health Score (PHS)**.
