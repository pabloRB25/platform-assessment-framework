# Dimensión D1: Arquitectura e Integración

## 1. Descripción
Evaluación de la estructura global del sistema, los patrones de arquitectura aplicados, el diseño de APIs y contratos de integración, así como la capacidad del diseño para soportar alta concurrencia, modularidad y resiliencia.

## 2. Objetivo
Determinar la solidez del diseño arquitectónico, el grado de acoplamiento entre componentes y la madurez en la integración de servicios de la plataforma.

## 3. Referencia de Estándares de la Industria
* **TOGAF (The Open Group Architecture Framework):** Gobernanza y desarrollo de arquitectura de empresa.
* **SEI ATAM (Architecture Tradeoff Analysis Method):** Evaluación de atributos de calidad y análisis de trade-offs.
* **ISO/IEC/IEEE 42010:2022:** Estándar internacional vigente para la descripción de arquitecturas (la edición 2011 está retirada).
* **ISO/IEC/IEEE 42030:2019:** Estándar de *evaluación* de arquitecturas — el marco formal de esta dimensión.
* **OpenAPI Specification 3.1:** Estándar de diseño de contratos API RESTful.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D1.1 Patrones de Arquitectura y Coherencia
* **1.0 (Inicial):** Monolito desestructurado (*Big Ball of Mud*), sin patrones claros ni separación de responsabilidades.
* **3.0 (En Desarrollo):** Arquitectura definida (monolito modular o microservicios), pero con fugas de abstracción.
* **5.0 (Optimizado):** Patrón claro (Event-Driven, Hexagonal, CQRS, Serverless) perfectamente alineado con la carga y dominio.

### D1.2 Integración y Diseño de APIs
* **1.0 (Inicial):** APIs informales, sin contratos, sin versionamiento, cambiando impredeciblemente.
* **3.0 (En Desarrollo):** RESTful con documentación OpenAPI parcial, respuestas inconsistentes y sin rate limiting.
* **5.0 (Optimizado):** Contratos OpenAPI/gRPC versionados, respuestas estándar, idempotencia implementada y API Gateway con throttling.

### D1.3 Acoplamiento, Cohesión y DDD
* **1.0 (Inicial):** Alto acoplamiento; cambios en una clase/servicio rompen componentes no relacionados.
* **3.0 (En Desarrollo):** Módulos definidos pero compartiendo base de datos o lógica de negocio duplicada.
* **5.0 (Optimizado):** Bounded Contexts bien delimitados, acoplamiento débil, alta cohesión y base de datos por servicio.

### D1.4 Escala y Resiliencia de Diseño
* **1.0 (Inicial):** Sin mecanismos de tolerancia a fallos; un error en un servicio externo tumba toda la aplicación.
* **3.0 (En Desarrollo):** Reintentos simples ante fallos, timeouts definidos pero sin circuit breakers.
* **5.0 (Optimizado):** Circuit breakers (Resilience4j/Hystrix), retries con exponential backoff, bulkheads y degradación elegante.

---

> **Nota de scoring:** la rúbrica canónica con 5 anclas (1.0–5.0) y los criterios binarios NPLF viven en el `.yaml` de esta dimensión. La documentación (`docs/`, ADRs) es solo evidencia T1: **la nota la da lo que el código demuestra**, contrastado vía `architecture_conformance_review` (T3) y `dependency_graph_analysis` (T2). Un README que declara "hexagonal" no puntúa como hexagonal.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Inspección de Diagramas/Código:** Buscar archivos `architecture.md`, `README.md`, diagramas C4 o explorar la estructura de paquetes/carpetas — como *insumo*, nunca como evidencia final.
2. **Análisis de Contratos API:** Buscar especificaciones Swagger/OpenAPI (`.yaml` / `.json`), controladores REST o schemas gRPC/GraphQL.
3. **Identificación de Patrones de Resiliencia:** Buscar librerías de circuit breakers, retries, clientes HTTP configurados con timeouts.
4. **Verificación de Comunicación Inter-servicio:** Inspeccionar si la comunicación es síncrona acoplada o asíncrona mediante colas (RabbitMQ, Kafka, SQS).
5. **Grafo de Dependencias (T2):** Ejecutar `madge --circular` (JS/TS), `deptrac` (PHP), ArchUnit (JVM) o `import-linter` (Python) y archivar el output en `evidence/` — es la evidencia dura de D1.3.
