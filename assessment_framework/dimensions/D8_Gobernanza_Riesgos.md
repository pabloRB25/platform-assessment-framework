# Dimensión D8: Gobernanza, Riesgos y Deuda Técnica

## 1. Descripción
Evaluación del marco de gobernanza del desarrollo, la gestión proactiva de riesgos técnicos y obsolescencia tecnológica, la documentación del sistema y el control de la deuda técnica acumulada.

## 2. Objetivo
Garantizar la sostenibilidad del software a largo plazo, mitigando la dependencia de personas clave (*Bus Factor*), reduciendo la deuda técnica temeraria y asegurando el cumplimiento normativo.

## 3. Referencia de Estándares de la Industria
* **ISO 31000:** Gestión del riesgo — Principios y directrices.
* **Cuadrante de Deuda Técnica (Martin Fowler):** Clasificación de deuda (Prudente/Reconsiderada vs. Temeraria/Inadvertida).
* **ISO/IEC 27001:2022 Anexo A:** controles 5.19–5.21 (proveedores), 8.4 (acceso a código fuente), 8.8 (vulnerabilidades técnicas), 8.9 (gestión de configuración) y 8.25–8.34 (desarrollo seguro). *(La numeración A.8/A.12 correspondía a la edición 2013, retirada.)*
* **ISO/IEC 5055:2021 + ATDM2:** Medición de deuda técnica en esfuerzo (horas/costo) — convierte D8.4 de estimación en medición.
* **C4 Model (Simon Brown):** Estándar de visualización de arquitectura de software.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D8.1 Riesgos Técnicos y Obsolescencia Tecnológica
* **1.0 (Inicial):** Uso de versiones de lenguajes o frameworks descontinuados (*End-of-Life* - EOL) sin plan de migración (ej. Python 2.7, PHP 5.6, Angular 1.x).
* **3.0 (En Desarrollo):** Versiones respaldadas por el proveedor, pero con retrasos menores en actualizaciones mayores.
* **5.0 (Optimizado):** Pila tecnológica en versiones Long-Term Support (LTS) vigentes, con proceso automatizado de actualización de dependencias.

### D8.2 Documentación y Transferencia de Conocimiento
* **1.0 (Inicial):** Cero documentación; README vacío o desactualizado, sin diagramas de arquitectura ni guías de despliegue.
* **3.0 (En Desarrollo):** README funcional con guía de desarrollo local; diagramas de arquitectura básicos presentes en wiki o repositorio.
* **5.0 (Optimizado):** Documentación viva como código (Architecture Decision Records - ADRs), diagramas C4 mantenidos y Runbooks operativos completos.

### D8.3 Dependencia de Personas (Bus Factor & RBAC)
* **1.0 (Inicial):** Bus Factor de 1 (solo una persona entiende el módulo/sistema); falta de revisión de pares o rotación de tareas.
* **3.0 (En Desarrollo):** Conocimiento compartido en el equipo; al menos dos personas capaces de mantener cualquier componente.
* **5.0 (Optimizado):** Bus Factor alto (> 3 personas), documentación onboarding que permite a un nuevo dev desplegar en < 2 días.

### D8.4 Gestión de Deuda Técnica
* **1.0 (Inicial):** Deuda técnica temeraria acumulada sin control, sin backlog de refactorización ni visibilidad por parte del negocio.
* **3.0 (En Desarrollo):** Deuda técnica identificada y etiquetada como `TODO` / `FIXME` en código, con tiempo dedicado a refactorizar en sprints.
* **5.0 (Optimizado):** Presupuesto constante de ingeniería (ej. 15-20% por sprint) asignado a pagar deuda técnica priorizada por impacto de negocio.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Verificación de Versiones EOL (T2):** Contrastar `package.json`, `Dockerfile`, `.nvmrc`, `runtime.txt`, `pom.xml`, `go.mod` contra la **API de endoflife.date** (`https://endoflife.date/api/<producto>.json`) — nunca de memoria.
2. **Inspección de Documentación:** Buscar `README.md`, `CONTRIBUTING.md`, carpetas `docs/`, `adrs/`, `architecture/` y **validar que reflejen el código actual** (existencia = T1).
3. **Bus Factor (T2):** `git shortlog -sn --no-merges --since='12 months ago' -- <path>` por componente crítico; >80% de commits de un autor = bus factor 1.
4. **Análisis de Deuda Técnica:** El conteo de `TODO:`/`FIXME:` es señal T1; la medición real sale de `lizard`/`jscpd` (proxy ISO 5055) y del backlog visible.
5. **Verificación de ADRs (Architecture Decision Records):** Inspeccionar si se documentan las decisiones de arquitectura.
