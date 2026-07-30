# Metodología de Assessment y Evaluación de Plataformas de Software
## Marco Híbrido Estandarizado para Software Studios (Incluye Auditoría de Código Generado por IA / Agentes)

---

### 1. Visión General de la Metodología

Esta metodología ha sido diseñada por y para **Studios de Desarrollo de Software de Alto Rendimiento**. Combina la velocidad y practicidad requeridas en consultoría técnica con el rigor de los estándares globales más reconocidos de la industria (**ISO/IEC 25010, OWASP SAMM, DORA, AWS Well-Architected, SRE, TOGAF y Marcos de Gobernanza para IA / Agentes**).

El objetivo es evaluar holísticamente una plataforma tecnológica a través de **9 dimensiones clave**, generando una calificación cuantitativa por dimensión y una **Calificación General de la Plataforma (Platform Health Score)**, acompañada de un diagnóstico cualitativo y priorización de riesgos.

---

### 2. Estructura de Dimensiones y Estándares de Referencia

| Código | Dimensión | Capa Evaluada | Estándares e Instrumentos de Referencia |
| :--- | :--- | :--- | :--- |
| **D1** | **Arquitectura e Integración** | Estructura, Patrones y APIs | TOGAF, ATAM (SEI), IEEE 42010, OpenAPI Spec |
| **D2** | **Código Fuente y Mantenibilidad** | Aplicación y Clean Code | ISO/IEC 25010 (Mantenibilidad), SonarQube Rules |
| **D3** | **Seguridad Aplicativa y DevSecOps** | Ciberseguridad y Protección | OWASP SAMM, OWASP ASVS, OWASP Top 10, SLSA |
| **D4** | **Base de Datos y Gestión de Datos** | Persistencia y Modelado | ACID/BASE, DB Tuning Guidelines, ISO/IEC 11179 |
| **D5** | **Calidad y Estrategia de QA** | Pruebas y Cobertura | Pirámide de Cobertura, ISTQB, ISO/IEC/IEEE 29119 |
| **D6** | **DevOps, CI/CD e Infraestructura** | Despliegue y Cloud | Métricas DORA, AWS/GCP/Azure Well-Architected |
| **D7** | **Observabilidad, Operaciones y Resiliencia** | Monitoreo y SRE | Google SRE Principles, OpenTelemetry |
| **D8** | **Gobernanza, Riesgos y Deuda Técnica** | Negocio y Sostenibilidad | ISO 31000 (Riesgos), Cuadrante de Deuda Técnica |
| **DAI**| **Código Agéntico e Inteligencia Artificial**| Calidad y Seguridad de Código generado por IA | OWASP AI Safety, Mutation Testing, SLSA, Provenance |

---

### 3. Detalle de Dimensiones y Sub-Dimensiones

#### D1: Arquitectura e Integración
* **D1.1 Patrones de Arquitectura:** Coherencia de arquitectura (Monolito modular, Microservicios, Event-Driven, Serverless) con las necesidades del negocio.
* **D1.2 Integración y APIs:** Calidad en diseño de contratos (REST, GraphQL, gRPC), versionamiento, idempotencia y rate limiting.
* **D1.3 Acoplamiento y Cohesión:** Modularidad, independencia de despliegue y separación de capas (Domain-Driven Design).
* **D1.4 Escala y Resiliencia de Diseño:** Manejo de fallos en cascada, circuit breakers, retries con backoff y patrones de concurrencia.

#### D2: Código Fuente y Mantenibilidad
* **D2.1 Estándares de Código y Modismos:** Uso de linters, formateadores automáticos, convención de nombres y patrones propios del stack.
* **D2.2 Deuda Técnica Estructural:** Complejidad ciclomática, duplicación de código, métodos/clases Dios y code smells.
* **D2.3 Principios SOLID y Limpieza:** Aplicación de principios SOLID, DRY, KISS y YAGNI.
* **D2.4 Manejo de Errores y Excepciones:** Control estructurado de errores, manejo de casos de borde y log de excepciones sin datos sensibles.

#### D3: Seguridad Aplicativa y DevSecOps (OWASP SAMM / ASVS)
* **D3.1 Autenticación y Autorización:** Implementación de OAuth2/OIDC, JWT, RBAC/ABAC y principio de mínimo privilegio.
* **D3.2 Gestión de Secretos:** Ausencia de credenciales en código, uso de Key Vaults/Secret Managers y rotación de llaves.
* **D3.3 Análisis de Dependencias (SCA):** Gestión de componentes de terceros, vulnerabilidades conocidas (CVEs) y licencias.
* **D3.4 Sanitización e Inyección:** Protección contra SQLi, XSS, CSRF, SSRF y validación de entrada/salida (*Zero Trust*).

#### D4: Base de Datos y Gestión de Datos
* **D4.1 Modelado y Normalización:** Diseño conceptual/lógico/físico, normalización adecuada y uso correcto de tipos de datos.
* **D4.2 Rendimiento de Consultas e Indexación:** Estrategias de indexación, consultas N+1, uso de ORMs y optimización de execution plans.
* **D4.3 Migraciones y Versionamiento:** Control de cambios en esquemas (Flyway, Liquibase, ORM Migrations) y despliegues sin tiempo de caída (*Zero Downtime*).
* **D4.4 Escalabilidad y Alta Disponibilidad:** Réplicas de lectura, sharding, conexión pooling, backups y tiempo de recuperación (RPO/RTO).

#### D5: Calidad y Estrategia de QA
* **D5.1 Cobertura de Pruebas Unitarias:** Cobertura efectiva de código y calidad de los tests (evitando falsos positivos).
* **D5.2 Pruebas de Integración y E2E:** Automatización de flujos críticos de negocio y aislamiento de entornos de prueba.
* **D5.3 Automatización en CI:** Ejecución automática de suites de prueba como gate obligatorio para merges (*Branch Protection*).
* **D5.4 Gestión de Datos de Prueba:** Estrategia de Mocks, Stubs y sanitización de datos de prueba.

#### D6: DevOps, CI/CD e Infraestructura (DORA & Cloud Frameworks)
* **D6.1 Automatización de CI/CD:** Pipelines como código (GitHub Actions, GitLab CI, Bitbucket Pipelines), artefactos inmutables.
* **D6.2 Métricas DORA:** Evaluación de Frecuencia de Despliegue, Lead Time for Changes, Change Failure Rate y MTTR.
* **D6.3 Infraestructura como Código (IaC):** Uso de Terraform, CloudFormation, Pulumi, y consistencia de entornos.
* **D6.4 Seguridad Cloud e IAM:** Seguridad de red (VPCs, WAF, Security Groups), roles de servicio y principio de mínimo privilegio en Cloud.

#### D7: Observabilidad, Operaciones y Resiliencia (Google SRE)
* **D7.1 Logging Estructurado:** Logs en formato JSON con correlación de peticiones (*Trace ID*) centralizados.
* **D7.2 Métricas y Monitoreo:** Indicadores dorados de SRE (Latencia, Tráfico, Errores, Saturación).
* **D7.3 Trazado Distribuido y Alertas:** Observabilidad APM/Tracing y configuración de alertas basadas en SLIs/SLOs.
* **D7.4 Plan de Recuperación ante Desastres (DRP):** Respaldos, redundancia multizona/multirregión y procedimientos de rollback.

#### D8: Gobernanza, Riesgos y Deuda Técnica
* **D8.1 Riesgos Técnicos y Obsolescencia:** Identificación de versiones End-of-Life (EOL), lenguajes descontinuados o librerías sin soporte.
* **D8.2 Documentación y Onboarding:** Existencia de arquitectura documentada, diagramas C4, READMEs claros y Runbooks operativos.
* **D8.3 Gobernanza de Dependencia de Personas:** Bus Factor (riesgo por concentración de conocimiento en individuos clave).
* **D8.4 Cuadrante de Deuda Técnica:** Priorización de deuda (Prudente/Reconsiderada vs. Temeraria/Inadvertida).

#### DAI: Módulo Especializado de Código Agéntico e Inteligencia Artificial
* **DAI.1 Verificación Anti-Alucinación y Supply Chain (Slopsquatting):** Garantía de que todas las librerías generadas por LLMs/Agentes existan en registros oficiales y no sean vectores de confusión de dependencias.
* **DAI.2 Robustez ante Casos Borde (Mitigación de Happy-Path Bias):** Verificación de que el código generado por IA contenga manejo explícito de fallos de red, timeouts, casos nulos e imprevistos en I/O.
* **DAI.3 Cohesión y Duplicación Agéntica (Snippet Isolation):** Detección de código repetido u over-engineering producido por agentes al trabajar en archivos aislados sin contexto global.
* **DAI.4 Aserción Real en Pruebas Generadas por IA:** Verificación de que las suites de prueba generadas por IA contengan aserciones verdaderas de lógica y no sean "pruebas fantasma" creadas solo para inflar métricas de cobertura.
* **DAI.5 Gobernanza y Supervisión Humana (Human-in-the-Loop):** Presencia de marcas de procedencia, etiquetado de commits e inspección de pares sobre código producido por IA.

---

### 4. Sistema de Calificación y Algoritmo de Scoring

#### 4.1 Escala de Madurez por Sub-Dimensión (1.0 a 5.0)

* **1.0 – 1.9 (Crítico / Ad-Hoc):** Ausente o gravemente deficiente. Riesgo alto para la operación.
* **2.0 – 2.9 (Básico / Informal):** Práctica incipiente, inconsistente o dependiente de personas clave.
* **3.0 – 3.7 (Aceptable / En Desarrollo):** Proceso definido y funcional pero con brechas evidentes.
* **3.8 – 4.4 (Robusto / Gestionado):** Estándar consolidado, automatizado y medido con consistencia.
* **4.5 – 5.0 (Optimizado / Referencia):** Estado del arte, mejora continua automatizada basada en métricas.

#### 4.2 Cálculo del Puntaje por Dimensión ($SD$)

Cada sub-dimensión ($sd_i$) tiene un peso relativo ($w_i$). El puntaje de la dimensión es:

$$SD_k = \sum_{i=1}^{n} (sd_i \times w_i) \quad \text{donde} \quad \sum w_i = 1$$

#### 4.3 Cálculo de la Calificación General de la Plataforma (Platform Health Score)

La Calificación General ($PHS$) es el promedio ponderado de las 9 dimensiones:

$$PHS = \sum_{k=1}^{9} (SD_k \times W_k) \quad \text{donde} \quad \sum W_k = 1$$

#### Pesos por Defecto según Tipo de Plataforma ($W_k$):

| Dimensión | Ponderación General (SaaS/Core) | Ponderación Fintech/Misión Crítica | Ponderación AI-Native / Agentic |
| :--- | :---: | :---: | :---: |
| **D1: Arquitectura e Integración** | 12% | 15% | 10% |
| **D2: Código Fuente y Mantenibilidad** | 12% | 10% | 10% |
| **D3: Seguridad Aplicativa y DevSecOps** | 15% | 20% | 15% |
| **D4: Base de Datos y Datos** | 12% | 15% | 10% |
| **D5: Calidad y Estrategia QA** | 10% | 10% | 10% |
| **D6: DevOps e Infraestructura** | 10% | 10% | 10% |
| **D7: Observabilidad y SRE** | 10% | 10% | 10% |
| **D8: Gobernanza y Riesgos** | 9% | 5% | 5% |
| **DAI: Código Agéntico e IA** | 10% | 5% | 20% |
| **TOTAL** | **100%** | **100%** | **100%** |

---

### 5. Clasificación Final de la Plataforma

| Rango de Score General (PHS) | Estado de Salud | Diagnóstico del Studio | Acción Recomendada |
| :---: | :---: | :---: | :---: |
| **4.5 – 5.0** | **Excelente / Enterprise Ready** | Plataforma madura, escalable y mantenible. | Optimización continua y evolución. |
| **3.8 – 4.4** | **Bueno / Estable** | Base sólida con oportunidades puntuales. | Plan de refactorización menor. |
| **3.0 – 3.7** | **Regular / Con Deuda Técnica** | Funcional pero acumula deuda y riesgos. | Roadmap de remediación a mediano plazo. |
| **2.0 – 2.9** | **En Riesgo / Inestable** | Fragilidad operacional, seguridad débil. | Intervención prioritaria en arquitectura/seguridad. |
| **1.0 – 1.9** | **Crítico / No Mantenible** | Alto riesgo de fallo masivo o brecha. | Reestructuración profunda o Re-platforming. |

---

### 6. Matriz de Entregables del Studio

1. **Executive Dashboard (Score & Radar Chart):** Gráfico de araña con el nivel por dimensión y PHS general.
2. **Technical Deep-Dive Report:** Detalle línea por línea de hallazgos por sub-dimensión con evidencia de código e infraestructura.
3. **AI Code Integrity & Risk Audit:** Reporte específico sobre la calidad de código agéntico y prevención de alucinaciones/slopsquatting.
4. **Remediation Roadmap (Prioridad vs. Esfuerzo):** Matriz 2x2 para orientar la inversión del cliente en mejoras inmediatas (Quick Wins), a mediano plazo y proyectos estratégicos.
