# Dimensión D7: Observabilidad, Operaciones y Resiliencia

## 1. Descripción
Evaluación de la capacidad del sistema para ser monitoreado de manera transparente en producción, la estructuración de registros, el rastreo distribuido de peticiones, la gestión de alertas operativas basadas en SLOs/SLIs y la capacidad de recuperación ante desastres (SRE).

## 2. Objetivo
Garantizar la visibilidad completa del estado interno de la plataforma en tiempo real, permitiendo la detección proactiva de incidentes, la reducción del MTTR y el mantenimiento de niveles altos de disponibilidad.

## 3. Referencia de Estándares de la Industria
* **Google Site Reliability Engineering (SRE) Principles:** Los 4 Señales Doradas (Latencia, Tráfico, Errores, Saturación).
* **OpenTelemetry Specification:** Estándar abierto para la recolección de trazas, métricas y registros.
* **ISO/IEC 27031:** Guía para la preparación de las tecnologías de la información y la comunicación para la continuidad del negocio.
* **AWS Well-Architected Framework Performance & Operational Excellence Pillars.**

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D7.1 Logging Estructurado y Centralización
* **1.0 (Inicial):** Logs no estructurados (texto plano) guardados localmente en archivos en el servidor de aplicación, rotación no configurada.
* **3.0 (En Desarrollo):** Logs en formato JSON enviados a un agregador centralizado (Datadog, ElasticSearch/ELK, CloudWatch).
* **5.0 (Optimizado):** Logs estructurados con contexto uniforme, ocultamiento automático de PII/datos sensibles y propagación de `Trace-ID` en microservicios.

### D7.2 Métricas y Monitoreo (SRE Golden Signals)
* **1.0 (Inicial):** Sin recolectores de métricas; monitoreo limitado a verificar si el servidor "pingea" o si responde HTTP 200 manualmente.
* **3.0 (En Desarrollo):** APM o Prometheus recopilando CPU, Memoria y tasa de errores HTTP; dashboards visuales disponibles.
* **5.0 (Optimizado):** Monitoreo de las 4 Señales Doradas (Latencia, Tráfico, Errores, Saturación), métricas de negocio personalizadas y dashboards integrados.

### D7.3 Trazado Distribuido y Alertas (SLO/SLI)
* **1.0 (Inicial):** Sin alertas automáticas; los clientes son quienes reportan las caídas del sistema por soporte.
* **3.0 (En Desarrollo):** Alertas por e-mail/Slack ante caídas de servidor o errores 500 sostenidos.
* **5.0 (Optimizado):** Trazado distribuido activo (Jaeger/Zipkin/OpenTelemetry), alertas inteligentes por consumo de Error Budget (SLO/SLI) conectadas a PagerDuty/Opsgenie.

### D7.4 Continuidad del Negocio y Disaster Recovery (DRP)
* **1.0 (Inicial):** Sin plan DRP documentado ni probado; tiempo de recuperación en desastre desconocido (> 24 horas).
* **3.0 (En Desarrollo):** Backups diarios y procedimientos de recuperación documentados en Wiki/Runbook.
* **5.0 (Optimizado):** Plan DRP automatizado y probado semestralmente, arquitectura multirregión o rápida conmutación por error (Failover) con RPO < 15 min y RTO < 1 hora.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Búsqueda de Librerías de Logging:** Buscar `winston`, `bunyan`, `logback`, `serilog`, `zerolog`, `pino`, `structlog`.
2. **Búsqueda de APM y OpenTelemetry:** Buscar SDKs de `datadog`, `newrelic`, `opentelemetry`, `prometheus`, `sentry`.
3. **Verificación de Contexto y Trace ID:** Buscar interceptores de cabeceras HTTP como `X-Correlation-ID` o `traceparent`.
4. **Inspección de Dashboards/Alertas:** Buscar configuraciones de Grafana, Datadog Monitors, PagerDuty, Prometheus Alerts.
