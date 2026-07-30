# Dimensión D9: SDLC y Gestión del Cambio

## 1. Descripción
Evaluación del proceso de ciclo de vida de desarrollo de software (SDLC), el control sobre el modelo de ramificación (*branching*), las políticas de revisión de código por pares (*two-party review*), la trazabilidad desde requerimiento hasta producción y el manejo de cambios de emergencia.

## 2. Objetivo
Garantizar la integridad, auditabilidad y transparencia de cada modificación introducida en el código fuente, previniendo inyecciones de código no autorizadas o despliegues fuera de proceso.

## 3. Referencia de Estándares de la Industria
* **SLSA v1.2 Source Track (Levels 1 to 4):** Estándar de integridad en el control de fuentes. **Nota de rigor:** two-party review es *un* requisito de Source L4, no todo L4 — el nivel también exige controles continuos, evidencia contemporánea, Source Provenance y VSA emitida por el sistema de control de fuentes. Este framework evalúa controles **alineados con** SLSA; solo declara un nivel cuando se verifican todos sus requisitos y attestations.
* **ISO/IEC/IEEE 12207:2017:** Procesos del ciclo de vida del software.
* **Conventional Commits 1.0.0:** Especificación para estructuración legible y parseable de mensajes de commit.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala NPLF / ISO 33020)

### D9.1 Branching y Protección de Ramas (Sub-Dimensión Crítica)
* **1.0 (Inicial):** Commits directos permitidos a la rama principal (`main`/`master`) sin restricciones ni branch protection.
* **3.0 (En Desarrollo):** Branch protection activado en GitHub/GitLab requiring Pull Requests para fusionar a `main`.
* **5.0 (Optimizado):** Branch protection estricto reforzado vía API (control alineado con SLSA Source L3+), firmas GPG/SSH obligatorias en commits y deshabilitación de `force push` / `bypass`.

### D9.2 Calidad del Code Review (Two-Party Review)
* **1.0 (Inicial):** Autofusión de PRs por el mismo autor sin aprobación externa; reviews nominales ("LGTM") sin inspección sustantiva.
* **3.0 (En Desarrollo):** Al menos un desarrollador aprueba el PR antes de fusionar; verificación automatizada de status checks.
* **5.0 (Optimizado):** Enforcement de Two-Party Review estricto (control alineado con SLSA Source L4), CODEOWNERS configurados por módulo crítico y plantilla de PR obligatoria con lista de chequeo de pruebas.

### D9.3 Trazabilidad Commit → Ticket → Deploy
* **1.0 (Inicial):** Commits con mensajes ambiguos ("fixed bug", "changes"); imposibilidad de vincular un cambio en producción con su tarea original.
* **3.0 (En Desarrollo):** Uso de Conventional Commits (`feat:`, `fix:`) asociando ID de ticket (ej. `jira-123`) en la mayoría de los commits.
* **5.0 (Optimizado):** Trazabilidad bidireccional automatizada (Commit ↔ Ticket ↔ PR ↔ Release Tag ↔ Deploy) en segundos.

### D9.4 Hotfixes y Cambios de Emergencia
* **1.0 (Inicial):** Cambios de emergencia aplicados en caliente directamente en servidores de producción sin registro en Git.
* **3.0 (En Desarrollo):** Rama dedicada de `hotfix` que sigue el flujo abreviado de PR y despliegue automatizado.
* **5.0 (Optimizado):** Proceso formal de Hotfix con aprobación express auditada, despliegue automatizado y ejecución obligatoria de Postmortem en < 48 horas.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Auditoría de Branch Protection:** Ejecutar llamada API a GitHub/GitLab para verificar `enforce_admins`, `required_approving_review_count`, `allow_force_pushes`.
2. **Análisis de Commit Log:** Ejecutar `git log -n 50 --pretty=format:"%h %s"` para medir apego a Conventional Commits y presencia de IDs de ticket.
3. **Verificación de CODEOWNERS:** Comprobar la existencia y reglas dentro de `.github/CODEOWNERS` o `.gitlab/CODEOWNERS`.
