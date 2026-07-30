# Framework de Ejecución de Assessment de Plataformas de Software
## Guía de Orquestación y Ejecución Autónoma para Agentes IA / Auditores

---

### 1. Estructura del Framework

El framework de evaluación se organiza en los siguientes componentes dentro de la carpeta `assessment_framework/`:

```
assessment_framework/
├── README.md                           # Guía general de ejecución
├── config/
│   └── weights_and_thresholds.yaml      # Configuración de ponderaciones y niveles
├── templates/
│   ├── assessment_master_pipeline.yaml # Pipeline maestro de orquestación para el Agente
│   └── template_final_report.md        # Plantilla de informe final de salida
└── dimensions/
    ├── D1_Arquitectura_Integracion.md  # Guía técnica y rúbrica D1
    ├── D1_Arquitectura_Integracion.yaml # Especificación ejecutable YAML D1
    ├── D2_Codigo_Mantenibilidad.md     # Guía técnica y rúbrica D2
    ├── D2_Codigo_Mantenibilidad.yaml   # Especificación ejecutable YAML D2
    ├── D3_Seguridad_DevSecOps.md       # Guía técnica y rúbrica D3
    ├── D3_Seguridad_DevSecOps.yaml     # Especificación ejecutable YAML D3
    ├── D4_BaseDatos_GestionDatos.md    # Guía técnica y rúbrica D4
    ├── D4_BaseDatos_GestionDatos.yaml  # Especificación ejecutable YAML D4
    ├── D5_Calidad_EstrategiaQA.md      # Guía técnica y rúbrica D5
    ├── D5_Calidad_EstrategiaQA.yaml    # Especificación ejecutable YAML D5
    ├── D6_DevOps_Infraestructura.md    # Guía técnica y rúbrica D6
    ├── D6_DevOps_Infraestructura.yaml  # Especificación ejecutable YAML D6
    ├── D7_Observabilidad_Resiliencia.md# Guía técnica y rúbrica D7
    ├── D7_Observabilidad_Resiliencia.yaml# Especificación ejecutable YAML D7
    ├── D8_Gobernanza_Riesgos.md        # Guía técnica y rúbrica D8
    └── D8_Gobernanza_Riesgos.yaml      # Especificación ejecutable YAML D8
```

---

### 2. Flujo de Ejecución del Agente IA

1. **Lectura de Configuración:** El Agente lee `config/weights_and_thresholds.yaml` para determinar las ponderaciones del proyecto según su perfil (Fintech, SaaS, MVP).
2. **Ejecución Secuencial/Paralela:** El Agente ejecuta los checklists definidos en los archivos YAML de la carpeta `dimensions/` (D1 a D8).
3. **Cálculo de Scores:** Aplica las fórmulas de ponderación por sub-dimensión y dimensión.
4. **Generación de Reporte:** Pobla la plantilla `templates/template_final_report.md` agregando evidencias, severidad de hallazgos y el **Platform Health Score (PHS)**.
