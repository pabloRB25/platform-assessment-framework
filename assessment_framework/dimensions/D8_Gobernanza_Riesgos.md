# Dimensión D8: Gobernanza, Riesgos y Deuda Técnica

## 1. Descripción
Evaluación del marco de gobernanza del desarrollo, la gestión proactiva de riesgos técnicos y obsolescencia tecnológica, la documentación del sistema y el control de la deuda técnica acumulada.

## 2. Objetivo
Garantizar la sostenibilidad del software a largo plazo, mitigando la dependencia de personas clave (*Bus Factor*), reduciendo la deuda técnica temeraria y asegurando el cumplimiento normativo.

## 3. Referencia de Estándares de la Industria
* **ISO 31000:** Gestión del riesgo — Principios y directrices.
* **Cuadrante de Deuda Técnica (Martin Fowler):** Clasificación de deuda (Prudente/Reconsiderada vs. Temeraria/Inadvertida).
* **ISO/IEC 27001 (Dominio A.8 y A.12):** Seguridad en la gestión de activos y operaciones.
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
* **1.0 (Inicial):** Deuda técnica temeraria acumulada din control, sin backlog de refactorización ni visibilidad por parte del negocio.
* **3.0 (En Desarrollo):** Deuda técnica identificada y etiquetada como `TODO` / `FIXME` en código, con tiempo dedicado a refactorizar en sprints.
* **5.0 (Optimizado):** Presupuesto constante de ingeniería (ej. 15-20% por sprint) asignado a pagar deuda técnica priorizada por impacto de negocio.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Verificación de Versiones EOL:** Inspeccionar `package.json`, `Dockerfile`, `.nvmrc`, `runtime.txt`, `pom.xml`, `go.mod` para comprobar versiones contra calendarios EOL oficiales.
2. **Inspección de Documentación:** Buscar archivos `README.md`, `CONTRIBUTING.md`, carpetas `docs/`, `adrs/`, `architecture/`.
3. **Análisis de Deuda Técnica:** Contar incidencias de `TODO:`, `FIXME:`, `HACK:`, `XXX:` en todo el código fuente.
4. **Verificación de ADRs (Architecture Decision Records):** Inspeccionar si se documentan las decisiones de arquitectura.
