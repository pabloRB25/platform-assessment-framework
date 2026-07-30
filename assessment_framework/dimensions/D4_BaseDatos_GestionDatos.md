# Dimensión D4: Base de Datos y Gestión de Datos

## 1. Descripción
Evaluación de la arquitectura de la capa de persistencia, modelado de datos, estrategias de indexación, consultas y rendimiento, migraciones de esquema versionadas y resiliencia/recuperabilidad de los datos.

## 2. Objetivo
Asegurar que la capa de base de datos sea altamente disponible, escalable, con integridad de datos garantizada y tiempos de respuesta optimizados para el volumen operacional esperado.

## 3. Referencia de Estándares de la Industria
* **Principios ACID / BASE:** Garantías de transaccionalidad vs. consistencia eventual.
* **Database Performance Tuning Guidelines (PostgreSQL / MySQL / MongoDB / Oracle).**
* **ISO/IEC 11179:** Estándar de especificación y estandarización de elementos de datos.
* **AWS Database Best Practices & Well-Architected Reliability Pillar.**

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D4.1 Modelado, Normalización y Tipado
* **1.0 (Inicial):** Tabla única "sábana" desnormalizada sin criterio, llaves foráneas ausentes, uso masivo de tipos `text` / `varchar(255)` indiscriminadamente.
* **3.0 (En Desarrollo):** Modelo relacional en 3NF razonable, llaves foráneas definidas, falta de documentación de esquema.
* **5.0 (Optimizado):** Modelado óptimo (Relacional 3NF o NoSQL según caso), restricciones de integridad estrictas, tipos de datos eficientes e índices compuestos diseñados.

### D4.2 Rendimiento de Consultas e Indexación
* **1.0 (Inicial):** Consultas tipo `SELECT *`, problema recurrente de N+1 queries con ORM, ausencia total de índices en columnas de búsqueda frecuente.
* **3.0 (En Desarrollo):** Índices en llaves primarias y foráneas; problema de N+1 mitigado con `eager loading` en flujos principales.
* **5.0 (Optimizado):** Consultas optimizadas con `EXPLAIN ANALYZE`, cero N+1, índices parciales/GIN/BTREE bien ajustados y pooling de conexiones (PgBouncer/HikariCP).

### D4.3 Migraciones y Versionamiento de Esquema
* **1.0 (Inicial):** Cambios de esquema aplicados manualmente ejecutando SQLs directos en producción sin control de versiones.
* **3.0 (En Desarrollo):** Herramienta de migración utilizada (Flyway, Liquibase, ORM Migrations) en repositorios, pero con migraciones destructivas ocasionales.
* **5.0 (Optimizado):** Migraciones automatizadas en CI/CD con cambios retrocompatibles (*Expand-Contract Pattern*) permitiendo despliegues sin downtime.

### D4.4 Escalabilidad, Alta Disponibilidad y Resiliencia (HA/DRP)
* **1.0 (Inicial):** Instancia única sin réplicas, backups manuales infrecuentes o sin pruebas de restauración verificadas.
* **3.0 (En Desarrollo):** Base de datos administrada (AWS RDS / GCP Cloud SQL) con Multi-AZ y backups automáticos diarios.
* **5.0 (Optimizado):** Multi-AZ con réplicas de lectura segregadas, backups continuos con RPO < 5 min y RTO < 15 min probados periódicamente.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Revisión de Migraciones:** Buscar carpetas `migrations/`, `db/migrate/`, `flyway/` o archivos de esquema ORM (`schema.prisma`, `models.py`, `entities/`).
2. **Inspección de Consultas N+1:** Buscar bucles `for` que ejecutan consultas dentro de la iteración.
3. **Verificación de Connection Pooling:** Inspeccionar configuraciones de BD buscando `max_connections`, `pool_size`, PgBouncer.
4. **Verificación de Configuración Cloud DB:** Revisar archivos Terraform/IaC sobre configuraciones RDS/CloudSQL.
