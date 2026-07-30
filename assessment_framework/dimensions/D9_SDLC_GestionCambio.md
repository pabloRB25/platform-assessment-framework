# Dimensión D9: SDLC y Gestión del Cambio

## 1. Descripción
Evaluación del proceso de desarrollo como sistema: estrategia de branching y protección de ramas, calidad real del code review, trazabilidad de cada cambio (commit → ticket → deploy) y gestión de hotfixes y cambios de emergencia. Recupera la dimensión de proceso del documento MNK original, que el framework había perdido (quedaba solo bus factor en D8.3 y gates de CI en D5.3).

## 2. Objetivo
Garantizar que todo cambio que llega a producción sea auditable, revisado por un segundo par de ojos y reversible — y que las emergencias sigan un proceso, no un SSH heroico.

## 3. Referencia de Estándares de la Industria
* **SLSA v1.2 — Source Track (L1–L4):** la escala de esta dimensión. L2 = rama protegida con historial íntegro; L4 = two-party review obligatoria.
* **Trunk-Based Development / GitFlow:** estrategias de branching según contexto del equipo.
* **Conventional Commits v1.0.0:** convención de mensajes que habilita changelogs automatizados.
* **ISO/IEC 12207:** Procesos del ciclo de vida del software.
* **ISO/IEC 27001:2022 A.8.32:** Gestión del cambio.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D9.1 Estrategia de Branching y Protección de Ramas *(crítica — gating rules)*
* **1.0 (Inicial):** Commits directos a la rama principal sin protección; sin estrategia de ramas discernible.
* **3.0 (En Desarrollo):** PRs como vía dominante; protección de rama parcial (sin required checks o con bypass libre de admins).
* **5.0 (Optimizado):** SLSA Source L3+: protección estricta sin bypass, todo cambio vía PR, historial íntegro y auditable.

### D9.2 Calidad del Code Review
* **1.0 (Inicial):** Merges sin ninguna revisión de terceros; PRs gigantes (miles de líneas) o inexistentes.
* **3.0 (En Desarrollo):** Review habitual con comentarios sustantivos, pero sin enforcement en la plataforma (es costumbre, no regla).
* **5.0 (Optimizado):** SLSA Source L4: two-party review obligatoria por branch protection, PRs de tamaño revisable (< ~400 líneas netas) y revisión reforzada en rutas críticas (auth, pagos, migraciones).

### D9.3 Trazabilidad Commit → Ticket → Deploy
* **1.0 (Inicial):** Commits tipo "fix", "wip", "cambios" sin vínculo a nada; imposible auditar qué se desplegó y por qué.
* **3.0 (En Desarrollo):** Convención de commits seguida en su mayoría; releases etiquetados manualmente.
* **5.0 (Optimizado):** Trazabilidad completa commit → ticket → deploy con changelog automatizado por release; responder "¿qué entró en el deploy X?" toma segundos.

### D9.4 Gestión de Hotfixes y Cambios de Emergencia
* **1.0 (Inicial):** Hotfixes por SSH directo a producción sin registro ni reconciliación con la rama principal.
* **3.0 (En Desarrollo):** Proceso de hotfix conocido por el equipo; pipeline usado en la mayoría de emergencias.
* **5.0 (Optimizado):** Cambios de emergencia auditables por pipeline (acelerado, no salteado) + cultura de postmortem sin culpa con seguimiento de acciones.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Branch Protection (T2):** `gh api repos/{owner}/{repo}/branches/<main>/protection` — evidencia dura de required checks, required reviews y enforce_admins. Archivar JSON en `evidence/`.
2. **Historial de PRs (T2):** `gh pr list --state merged --limit 100 --json number,reviews,author,additions` — % con aprobación de tercero, tamaño mediano, auto-merges.
3. **Profundidad de Review (T3):** Muestrear 5+ PRs y evaluar si los reviews son sustantivos o rubber-stamps de 30 segundos, con citas.
4. **Trazabilidad (T2):** % de commits/PRs con referencia a ticket; existencia de tags/releases que enlacen deploys con commits.
5. **Hotfixes (T2/T3):** Identificar en el historial merges directos, ramas `hotfix/*` y reverts; verificar si siguieron proceso y si generaron postmortem.
