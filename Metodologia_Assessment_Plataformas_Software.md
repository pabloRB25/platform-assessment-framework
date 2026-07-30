# Metodología de Assessment y Evaluación de Plataformas de Software
## Marco Híbrido Estandarizado para Software Studios (Incluye Auditoría de Código Generado por IA / Agentes)

---

### 1. Visión General de la Metodología

Esta metodología ha sido diseñada por y para **Studios de Desarrollo de Software de Alto Rendimiento**. Combina la velocidad y practicidad requeridas en consultoría técnica con el rigor de los estándares globales más reconocidos de la industria (**ISO/IEC 25010:2023, ISO/IEC 5055:2021, OWASP SAMM v2.1 / ASVS 5.0, DORA, AWS Well-Architected, SRE, SLSA v1.2 y Marcos de Gobernanza para IA / Agentes**).

El objetivo es evaluar holísticamente una plataforma tecnológica a través de **10 dimensiones clave**, generando una calificación cuantitativa por dimensión y una **Calificación General de la Plataforma (Platform Health Score)**, acompañada **siempre** del conteo de hallazgos de alto riesgo (HRIs), un diagnóstico cualitativo y la priorización de riesgos.

**Tres principios rectores del scoring:**

1. **Lo crítico no se promedia — y solo el riesgo *demostrado* capa.** Siguiendo ISO/IEC 33020, TMMi y AWS Well-Architected (que cuenta HRIs y jamás promedia), un **`risk_gate`** — criterio-gate en fail con la evidencia exigida (secretos vivos, inyección demostrable, BOLA, backups irrecuperables, datos expuestos, dependencia alucinada), o sub-dimensión crítica hundida por fails reales — **acota el PHS reportable a 2.9**. La *insuficiencia de evidencia* en zona crítica (**`evidence_limit`**) nunca capa: vuelve el informe PROVISIONAL sin afirmar incumplimiento.
2. **Presencia de strings ≠ verdad.** El tier de evidencia se deriva **por criterio** (nunca lo declara el evaluador): un `pass` sostenido solo por señales T1 (grep/file_exists) queda **no-confirmado** y se trata como desconocido; un `fail` sí puede demostrarse con T1 (la presencia del anti-patrón citado es la evidencia). Confirmar exige T2 (herramienta) o T3 (juicio con citas `archivo:línea`).
3. **Reproducibilidad ante todo.** Cada sub-dimensión se califica con el método **NPLF (ISO/IEC 33020)** sobre criterios con **IDs estables** (`DX.Y.Cn`, append-only) y tres estados (`pass`/`fail`/`unknown`). El **`coverage_ratio`** (peso realmente evaluado) acompaña siempre al PHS: un PHS con cobertura 60% no se compara con uno de 95%.

---

### 2. Estructura de Dimensiones y Estándares de Referencia

| Código | Dimensión | Capa Evaluada | Estándares e Instrumentos de Referencia |
| :--- | :--- | :--- | :--- |
| **D1** | **Arquitectura e Integración** | Estructura, Patrones y APIs | TOGAF, ATAM (SEI), ISO/IEC/IEEE 42010:2022, ISO/IEC/IEEE 42030:2019, OpenAPI 3.1 |
| **D2** | **Código Fuente y Mantenibilidad** | Aplicación y Clean Code | ISO/IEC 25010:2023 (Mantenibilidad), ISO/IEC 5055:2021, SonarQube Rules |
| **D3** | **Seguridad Aplicativa y DevSecOps** | Ciberseguridad y Protección | OWASP SAMM v2.1, ASVS 5.0.0, Top 10:2025, API Security Top 10 (2023), SLSA v1.2 |
| **D4** | **Base de Datos y Gestión de Datos** | Persistencia, Modelado y Privacidad | ACID/BASE, DB Tuning, ISO/IEC 5055, AWS WA (Datos), GDPR / Ley 8968 CR |
| **D5** | **Calidad y Estrategia de QA** | Pruebas, Cobertura y Performance | Pirámide de Cobertura, ISTQB, ISO/IEC/IEEE 29119, Mutation Testing |
| **D6** | **DevOps, CI/CD e Infraestructura** | Despliegue, Cloud y Costos | DORA (5 métricas, benchmark 2024), AWS/GCP/Azure WA, CIS v7.0, FinOps Framework |
| **D7** | **Observabilidad, Operaciones y Resiliencia** | Monitoreo y SRE | Google SRE Principles, OpenTelemetry, ISO/IEC 27031 |
| **D8** | **Gobernanza, Riesgos y Deuda Técnica** | Negocio y Sostenibilidad | ISO 31000, ISO 27001:2022 (Anexo A 8.25-8.34), ISO 5055 + ATDM2, C4 Model |
| **D9** | **SDLC y Gestión del Cambio** | Proceso de Desarrollo | SLSA v1.2 Source Track (L1-L4), Conventional Commits, ISO/IEC 12207 |
| **DAI**| **Código Agéntico e Inteligencia Artificial**| Calidad y Seguridad de Código generado por IA | OWASP LLM Top 10 (2025), Top 10:2025 A03, SLSA v1.2, NIST SP 800-218A, DORA AI Capabilities |

---

### 3. Detalle de Dimensiones y Sub-Dimensiones

#### D1: Arquitectura e Integración
* **D1.1 Patrones de Arquitectura:** Coherencia de arquitectura verificada contra el **código real** (no contra la documentación aspiracional) vía review de conformidad + grafo de dependencias.
* **D1.2 Integración y APIs:** Calidad en diseño de contratos (REST, GraphQL, gRPC), versionamiento, idempotencia y rate limiting.
* **D1.3 Acoplamiento y Cohesión:** Modularidad y bounded contexts medidos con herramienta (madge/deptrac/ArchUnit) — cero ciclos como criterio duro.
* **D1.4 Escala y Resiliencia de Diseño:** Manejo de fallos en cascada, circuit breakers, retries con backoff y patrones de concurrencia.

#### D2: Código Fuente y Mantenibilidad
*(Califica el codebase completo; los defectos de código IA-atribuido van a DAI — sin doble conteo.)*
* **D2.1 Estándares de Código y Modismos:** Linters/formateadores **aplicados como gate en CI**, no solo presentes.
* **D2.2 Deuda Técnica Estructural:** Complejidad (lizard/radon) y duplicación (jscpd) **medidas**, no estimadas.
* **D2.3 Principios SOLID y Limpieza:** Evaluado por lectura real de diseño (T3), no por conteo de keywords.
* **D2.4 Manejo de Errores y Excepciones:** Capturas silenciosas y async sin manejo detectados con análisis sintáctico (Semgrep).

#### D3: Seguridad Aplicativa y DevSecOps (SAMM v2.1 / ASVS 5.0)
* **D3.1 Autenticación y Autorización:** OAuth2/OIDC, tokens, RBAC/ABAC — ASVS 5.0 V6/V8/V9/V10. *(crítica)*
* **D3.2 Gestión de Secretos:** gitleaks sobre el **historial completo** de git + verificación de credencial viva (TruffleHog). *(crítica)*
* **D3.3 Dependencias, Licencias y Supply Chain (SCA):** CVEs + inventario de licencias + SBOM en una sola pasada de trivy/osv-scanner. El copyleft fuerte no es hallazgo automático: se contrasta contra la política de licencias del cliente (AGPL en servicio de red = prioridad de revisión legal) y se emite como "requiere revisión legal contextual".
* **D3.4 Sanitización e Inyección:** SQLi/XSS/SSRF con SAST sintáctico + validación de esquemas. *(crítica)*
* **D3.5 Seguridad de APIs en Runtime:** **BOLA/BFLA** (OWASP API Top 10 2023, API1/API5) — autorización a nivel de objeto y de función, auditada endpoint por endpoint. *(crítica)*

#### D4: Base de Datos y Gestión de Datos
* **D4.1 Modelado y Normalización:** Integridad por esquema, tipado adecuado.
* **D4.2 Rendimiento de Consultas e Indexación:** N+1, índices por patrón de acceso, pooling.
* **D4.3 Migraciones y Versionamiento:** Migraciones versionadas, expand-contract, zero downtime.
* **D4.4 Escalabilidad y Alta Disponibilidad:** Réplicas, backups **probados**, RPO/RTO.
* **D4.5 Protección de Datos Personales:** Inventario de PII, cifrado, derecho de supresión (GDPR / Ley 8968 CR), anonimización en test.

#### D5: Calidad y Estrategia de QA
* **D5.1 Cobertura de Pruebas Unitarias:** Cobertura medida + **mutation testing** como verificación de efectividad.
* **D5.2 Pruebas de Integración y E2E:** Flujos críticos automatizados corriendo en CI.
* **D5.3 Automatización en CI:** Gates obligatorios con branch protection verificable.
* **D5.4 Gestión de Datos de Prueba:** Mocks, datos sintéticos, sin PII real en test.
* **D5.5 Pruebas de Rendimiento y Carga:** k6/Gatling/JMeter con umbrales explícitos y ejecución recurrente.

#### D6: DevOps, CI/CD e Infraestructura (DORA & Cloud Frameworks)
* **D6.1 Automatización de CI/CD:** Pipelines como código, artefactos inmutables, blue/green o canary.
* **D6.2 Métricas DORA:** Las **5 métricas** (deployment frequency, lead time, CFR, failed deployment recovery time, rework rate) contra el benchmark 2024: Elite = lead time **< 1 día**, CFR **5%**. Derivadas del historial real del pipeline — sin acceso, N/D.
* **D6.3 Infraestructura como Código (IaC):** Terraform/Pulumi con estado remoto y paridad de entornos.
* **D6.4 Seguridad Cloud e IAM:** Prowler/checkov contra CIS Benchmark v7.0; mínimo privilegio. *(crítica)*
* **D6.5 Costos y FinOps:** Tagging, budgets, recursos huérfanos, right-sizing (AWS WA Cost Optimization).

#### D7: Observabilidad, Operaciones y Resiliencia (Google SRE)
* **D7.1 Logging Estructurado:** JSON + Trace-ID + **sin PII en claro** (cruce D4.5).
* **D7.2 Métricas y Monitoreo:** 4 Señales Doradas instrumentadas de verdad (SDK instalado ≠ monitoreo operante).
* **D7.3 Trazado Distribuido y Alertas:** SLO/SLI con presupuesto de error y alertas accionables.
* **D7.4 Plan de Recuperación ante Desastres (DRP):** Documentado, actualizado y **probado**.

#### D8: Gobernanza, Riesgos y Deuda Técnica
* **D8.1 Riesgos Técnicos y Obsolescencia:** Versiones contra la API de endoflife.date.
* **D8.2 Documentación y Onboarding:** Docs que reflejan el código actual, ADRs, C4, runbooks.
* **D8.3 Dependencia de Personas (Bus Factor):** `git shortlog -sn` por componente crítico.
* **D8.4 Cuadrante de Deuda Técnica:** Deuda inventariada y **medida** (ISO 5055/ATDM2), con capacidad asignada.

#### D9: SDLC y Gestión del Cambio *(controles alineados con SLSA v1.2 Source Track — declarar un nivel SLSA exige verificar todos sus requisitos y attestations, no un control aislado)*
* **D9.1 Branching y Protección de Ramas:** Branch protection verificable por API; todo cambio vía PR. *(crítica; push directo sin protección = criterio-gate)*
* **D9.2 Calidad del Code Review:** Two-party review con enforcement (alineado con SLSA Source L4), CODEOWNERS, PRs revisables, reviews sustantivos.
* **D9.3 Trazabilidad Commit → Ticket → Deploy:** Auditar qué se desplegó y por qué, en segundos.
* **D9.4 Hotfixes y Cambios de Emergencia:** Proceso auditable + postmortems en < 48h.

#### DAI: Módulo Especializado de Código Agéntico e Inteligencia Artificial
*(DAI.2–DAI.4 evalúan SOLO código con atribución IA verificable; DAI.1 y DAI.5 operan sobre el repo y el proceso completos. Sin atribución: DAI.0 puntúa bajo — ese es el hallazgo — y DAI.2–DAI.4 quedan en `unknown` con pesos redistribuidos; nunca se asume que el código reciente es de IA.)*
* **DAI.0 Atribución y Trazabilidad de Código IA:** El mecanismo que define el universo del módulo — trailers de commit (`Co-Authored-By`), política en `AGENTS.md`/`CLAUDE.md`, etiquetas de PR.
* **DAI.1 Anti-Alucinación y Supply Chain (Slopsquatting):** Registry audit ejecutable (osv-scanner + APIs npm/PyPI: existencia, fecha, descargas). *(crítica)*
* **DAI.2 Robustez ante Casos Borde (Happy-Path Bias):** Async sin manejo detectado con Semgrep (sintáctico) sobre el universo IA.
* **DAI.3 Cohesión y Duplicación Agéntica:** jscpd sobre el universo IA vs. línea base del proyecto.
* **DAI.4 Anti-Phantom Tests:** Tautologías + mutation testing como evidencia de efectividad.
* **DAI.5 Gobernanza y Supervisión Humana:** Alineada con el control de **two-party review de SLSA v1.2 Source Track L4** (con enforcement de plataforma).
* **DAI.6 Seguridad de Features LLM (condicional):** OWASP LLM Top 10 **2025** — LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM05 Improper Output Handling, LLM06 Excessive Agency — solo si la plataforma usa LLMs en runtime; si no, N/A sin penalizar.

---

### 4. Sistema de Calificación y Algoritmo de Scoring

#### 4.1 Método NPLF por Sub-Dimensión (ISO/IEC 33020)

Cada sub-dimensión define en su YAML una lista de **criterios** (`nplf_criteria`) con tres estados posibles: `pass`, `fail`, `unknown`. El % de cumplimiento se calcula **solo sobre pass+fail** (los `unknown` salen del denominador y degradan la confianza) y mapea a:

| Rating | % criterios cumplidos | Score |
| :---: | :---: | :---: |
| **F** (Fully) | 86–100% | 5.0 |
| **L** (Largely) | 51–85% | 3.5 |
| **P** (Partially) | 16–50% | 2.0 |
| **N** (Not) | 0–15% | 1.0 |

Reglas adicionales:
* **Criterios-gate:** un criterio `critical: true, failure_effect: gate` cuyo `fail` está **demostrado** (con el tier de `evidence_required` cumplido) activa el `risk_gate` directamente, sin esperar al promedio. Una sub-dimensión que aprueba 4 de 5 criterios pero falla el crítico (p.ej. secretos vivos) no puede esconderse detrás de un "L = 3.5".
* **Resolución T1/NPLF (anti tier-laundering):** el tier se deriva **por criterio** desde sus referencias de evidencia (EV-id del manifest → check → tier del catálogo). Un `pass` solo-T1 se reclasifica **no-confirmado** (sale del denominador como unknown); un `fail` con T1 es válido. El dominio de scores se mantiene cerrado en {1.0, 2.0, 3.5, 5.0} — y una evidencia T2 aislada ya no "lava" una sub-dimensión mayormente T1, porque no hay techo por sub-dimensión que levantar.
* Las rúbricas narrativas (ancladas 1.0–5.0 en los YAML) son sanity-check cualitativo. **Prohibido reportar decimales no derivados del método** (un "3.74" sin ancla es falsa precisión).

#### 4.2 Tiers de Evidencia

| Tier | Tipo | Ejemplos | Efecto en el score (por criterio) |
| :---: | :--- | :--- | :--- |
| **T1** | Señal | grep, file_exists | Demuestra `fail` (presencia del anti-patrón); un `pass` solo-T1 = **no-confirmado** (cuenta como unknown) |
| **T2** | Métrica de herramienta | gitleaks, Semgrep, Trivy/OSV, jscpd, lizard, Prowler, Stryker, endoflife.date | Confirma `pass` y `fail` |
| **T3** | Juicio con evidencia | Lectura real de código/arquitectura, citas `archivo:línea` obligatorias | Confirma `pass` y `fail` |

El contrato de ejecución de cada check (herramienta, comando, parsing, mapeo a score), la **custodia de evidencia** (redacción en origen, cifrado, retención, `evidence/` jamás commiteado) y los **requisitos del runner seguro** (argv, contenedores efímeros, red deshabilitada por defecto, versiones pinneadas por digest) viven en `config/checks_catalog.yaml`.

#### 4.3 Estado `unknown`, `evidence_limit` y Cobertura — desconocido ≠ incumplimiento

* Check no ejecutable ⇒ los criterios afectados quedan en **`unknown`**: salen del denominador NPLF y se listan en "Limitaciones y Alcance". **No** se convierte en fail: "no pude comprobarlo" no es "no existe".
* `unknown` (o todos-los-pass no-confirmados) en **sub-dimensión crítica** ⇒ **`evidence_limit`**: `confidence: low`, PHS **PROVISIONAL**, estado no declarable ≥ "Bueno / Estable" — y **sin cap**: la insuficiencia de evidencia nunca se reporta como riesgo demostrado.
* Una sub-dimensión `unknown` **no aporta número** al SD: se excluye renormalizando pesos, y su peso excluido baja el **`coverage_ratio`** (porcentaje del peso realmente evaluado), que acompaña siempre al PHS.
* **Excepción:** cuando producir la evidencia ES el control evaluado (auditoría/logging habilitado, historial de pipeline existente), la ausencia sí es `fail`.
* Cada dimensión reporta `confidence: Alta | Media | Baja` y su `coverage_ratio` en el informe.

#### 4.4 Cálculo del Puntaje por Dimensión ($SD$)

$$SD_k = \sum_{i=1}^{n} (sd_i \times w_i) \quad \text{donde} \quad \sum w_i = 1$$

#### 4.5 Platform Health Score (PHS) y Gating Rules

El promedio ponderado de las 10 dimensiones es la base narrativa:

$$PHS_{ponderado} = \sum_{k=1}^{10} (SD_k \times W_k) \quad \text{donde} \quad \sum W_k = 1$$

Pero el PHS **reportable** aplica las gating rules (`config/weights_and_thresholds.yaml`):

* Sub-dimensiones críticas: **D3.1, D3.2, D3.4, D3.5, D6.4, D9.1, DAI.1**.
* **`risk_gate`** (riesgo demostrado): criterio-gate en `fail` con su `evidence_required` cumplido, o crítica con rating ≤ P por fails reales ⇒ $PHS_{reportable} = \min(PHS_{ponderado},\ 2.9)$.
* **`evidence_limit`** (insuficiencia): crítica `unknown` o criterio-gate `unknown` ⇒ PHS PROVISIONAL sin cap — se pide la evidencia, no se declara el riesgo.
* El informe muestra **siempre**: PHS + **HRIs abiertos: N** (Crítico + Alto, nunca promediados) + **coverage_ratio** + el criterio/sub-dimensión que activa el `risk_gate` o el `evidence_limit`.

#### 4.6 Pesos por Defecto según Tipo de Plataforma ($W_k$)

| Dimensión | SaaS/Core | Fintech/Crítica | MVP/Startup | AI-Native |
| :--- | :---: | :---: | :---: | :---: |
| **D1: Arquitectura e Integración** | 11% | 13% | 8% | 9% |
| **D2: Código y Mantenibilidad** | 11% | 9% | 10% | 9% |
| **D3: Seguridad y DevSecOps** | 15% | 20% | 15% | 14% |
| **D4: Base de Datos y Datos** | 11% | 14% | 10% | 9% |
| **D5: Calidad y QA** | 9% | 9% | 12% | 9% |
| **D6: DevOps e Infraestructura** | 9% | 9% | 12% | 9% |
| **D7: Observabilidad y SRE** | 9% | 9% | 8% | 9% |
| **D8: Gobernanza y Riesgos** | 8% | 5% | 5% | 5% |
| **D9: SDLC y Gestión del Cambio** | 8% | 8% | 8% | 7% |
| **DAI: Código Agéntico e IA** | 9% | 4% | 12% | 20% |
| **TOTAL** | **100%** | **100%** | **100%** | **100%** |
| **Nivel objetivo (target PHS)** | **3.8** | **4.5** | **3.0** | **3.8** |

---

### 5. Clasificación Final de la Plataforma

El estado de salud se reporta en dos ejes: **absoluto** (tabla siguiente) y **relativo al nivel objetivo del perfil** (Current vs. Target Profile, NIST CSF 2.0). Un 3.0 es un buen resultado para un MVP (target 3.0) y una brecha seria para fintech (target 4.5).

| Rango de PHS Reportable | Estado de Salud | Diagnóstico del Studio | Acción Recomendada |
| :---: | :---: | :---: | :---: |
| **4.5 – 5.0** | **Excelente / Enterprise Ready** | Plataforma madura, escalable y mantenible. | Optimización continua y evolución. |
| **3.8 – 4.4** | **Bueno / Estable** | Base sólida con oportunidades puntuales. | Plan de refactorización menor. |
| **3.0 – 3.7** | **Regular / Con Deuda Técnica** | Funcional pero acumula deuda y riesgos. | Roadmap de remediación a mediano plazo. |
| **2.0 – 2.9** | **En Riesgo / Inestable** | Fragilidad operacional, seguridad débil **o HRI crítico abierto (gating)**. | Intervención prioritaria en arquitectura/seguridad. |
| **1.0 – 1.9** | **Crítico / No Mantenible** | Alto riesgo de fallo masivo o brecha. | Reestructuración profunda o Re-platforming. |

Taxonomía de severidad de hallazgos: **Crítico** (HRI, ≤ 7 días) · **Alto** (HRI, ≤ 30 días) · **Medio** (trimestre) · **Bajo** (backlog) — definiciones operativas en `config/weights_and_thresholds.yaml`.

---

### 6. Matriz de Entregables del Studio

1. **Executive Dashboard (Score & Radar Chart):** Nivel por dimensión, PHS + **conteo de HRIs** + **coverage_ratio**, confianza por dimensión y gap vs. nivel objetivo.
2. **Technical Deep-Dive Report:** Hallazgos por sub-dimensión con evidencia `archivo:línea` + commit + output de herramienta archivado en `evidence/` (re-verificable por hash).
3. **AI Code Integrity & Risk Audit:** Reporte específico sobre atribución, calidad y riesgos del código agéntico.
4. **Remediation Roadmap (Prioridad vs. Esfuerzo):** Matriz 2x2 para orientar la inversión del cliente.
5. **Delta Report (re-evaluaciones):** Evolución PHS y HRIs vs. el assessment anterior (milestones à la AWS WA Tool) — el valor comercial recurrente: "PHS 2.8 → 3.6 en 6 meses". Solo es comparable con mismo perfil, alcance, versión del framework/catálogo y herramientas pinneadas (`delta_comparability_rules`); si no, se reporta como delta indicativo.
6. **Limitaciones y Alcance:** Sección obligatoria del informe — accesos disponibles, controles en `unknown`, supuestos, vigencia y hash del `evidence/manifest.json` (heredada del assessment MNK original).

Todo informe lleva **firma de auditor humano** antes de la entrega (paso bloqueante del pipeline): el mismo Human-in-the-Loop que el framework exige al código de los clientes en DAI.5.
