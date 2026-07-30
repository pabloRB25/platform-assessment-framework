# Dimensión DAI: Código Agéntico e Inteligencia Artificial

## 1. Descripción
Evaluación especializada de la calidad, seguridad, mantenibilidad y proveniencia del código generado por Agentes de IA o asistentes de código (LLMs como GitHub Copilot, Cursor, Antigravity, Claude Code). Esta dimensión audita riesgos específicos como alucinación de dependencias (Slopsquatting), sesgo de camino feliz (Happy-Path Bias), pruebas fantasma y duplicación por fragmentación de contexto.

## 2. Objetivo
Garantizar que el uso de IA en la generación de código no degrade la arquitectura del sistema, no introduzca vulnerabilidades en la cadena de suministro ni aumente la deuda técnica oculta por falta de supervisión humana (*Human-in-the-Loop*).

## 3. Referencia de Estándares de la Industria
* **OWASP Top 10 for LLM Applications (2025):** LLM01 Prompt Injection, LLM02 Insecure Output Handling, LLM06 Sensitive Information Disclosure — con checks concretos en DAI.6.
* **OWASP Top 10:2025 — A03 Software Supply Chain Failures:** conexión directa con DAI.1 (slopsquatting es un fallo de supply chain).
* **SLSA v1.2:** Build Track (provenance) y **Source Track L1–L4** — el L4 (two-party review) es exactamente el control de DAI.5.
* **NIST SP 800-218A:** Secure Software Development Practices for Generative AI.
* **DORA AI Capabilities Model (2025):** capacidades organizacionales para desarrollo asistido por IA.
* **Mutation Testing Standards (Stryker / PITest):** Validación de la efectividad real de pruebas unitarias.
* **ISO/IEC 25010:2023:** Sub-características de Mantenibilidad y Analizabilidad en código sintético.

> **Alcance y anti doble conteo:** DAI evalúa **solo código con atribución IA**, definida por DAI.0. D2 evalúa el codebase completo; el mismo defecto nunca baja el PHS dos veces. Si no existe mecanismo de atribución, DAI opera sobre el código de los últimos 12 meses con `confidence: low`.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### DAI.0 Atribución y Trazabilidad de Código IA
* **1.0 (Inicial):** Sin ningún mecanismo para identificar qué código es de IA — todo el módulo DAI queda sin universo definido.
* **3.0 (En Desarrollo):** Trailers de commit (`Co-Authored-By:`) o etiquetas de PR usados en la mayoría del trabajo asistido; política informal.
* **5.0 (Optimizado):** Política escrita en `AGENTS.md`/`CLAUDE.md`/`CONTRIBUTING.md` con atribución automática y auditable en cada commit/PR.

### DAI.1 Verificación Anti-Alucinación y Supply Chain (Slopsquatting)
* **1.0 (Inicial):** Presencia de dependencias alucinadas por la IA o librerías sugeridas sin verificar en el registro oficial (riesgo de *Typosquatting* / *Dependency Confusion*). Atajos de seguridad deshabilitados (`rejectUnauthorized: false`, CORS desmedido).
* **3.0 (En Desarrollo):** Dependencias auditadas contra registros públicos oficiales; lockfiles estrictos (`package-lock.json`, `poetry.lock`) mantenidos en el repositorio.
* **5.0 (Optimizado):** Registro privado de paquetes con lista blanca estricta, escaneo en CI contra alucinaciones de código y firma de proveniencia de dependencias.

### DAI.2 Robustez ante Casos Borde (Mitigación de Happy-Path Bias)
* **1.0 (Inicial):** Código asumiendo que la red e infraestructura son 100% confiables; ausencia de `catch`, timeouts o manejo de valores `null`/`undefined` en llamadas I/O generadas por IA.
* **3.0 (En Desarrollo):** Manejo de errores básico generado en la mayoría de llamadas asíncronas; comprobaciones de nulos presentes.
* **5.0 (Optimizado):** Manejo robusto de casos de borde en llamadas asíncronas, reintentos con exponential backoff, timeouts explícitos y validaciones defensivas de esquema.

### DAI.3 Cohesión y Duplicación Agéntica (Snippet Isolation & DRY)
* **1.0 (Inicial):** Alta duplicación de utilidades (funciones de formateo, llamadas HTTP, validaciones) creadas por agentes al trabajar aisladamente sin reutilizar módulos existentes del proyecto. Over-engineering innecesario.
* **3.0 (En Desarrollo):** Módulos compartidos utilizados en la mayoría de características; nivel de duplicación de código agéntico < 5%.
* **5.0 (Optimizado):** Código conciso, idiomático, reutilizando al 100% los módulos y abstracciones del núcleo del sistema sin redundancias ni patrones innecesarios.

### DAI.4 Aserción Real en Pruebas Generadas por IA (Anti-Phantom Tests)
* **1.0 (Inicial):** Pruebas unitarias "fantasma" generadas para inflar la cobertura que no contienen aserciones o usan aserciones tautológicas (`expect(true).toBe(true)`).
* **3.0 (En Desarrollo):** Pruebas generadas por IA con aserciones válidas de retornos y excepciones en escenarios comunes.
* **5.0 (Optimizado):** Mutation Testing ejecutado en CI para validar que las pruebas generadas por IA realmente detecten fallas ante mutaciones de código.

### DAI.5 Gobernanza y Supervisión Humana (Human-in-the-Loop)
* **1.0 (Inicial):** Código generado por IA integrado directamente en ramas principales sin revisión de pares (Code Review) ni trazabilidad.
* **3.0 (En Desarrollo):** PRs generados por IA revisados por al menos un desarrollador senior antes de fusionar.
* **5.0 (Optimizado):** SLSA Source Track L4 (two-party review con enforcement de plataforma) + política de gobernanza agéntica, commits etiquetados con proveniencia y revisión estricta de *Human-in-the-Loop*.

### DAI.6 Seguridad de Features LLM en Runtime (condicional)
*Solo aplica si la plataforma integra LLMs en runtime (chatbots, generación, agentes). Si no aplica, se marca N/A y su peso se redistribuye — no penaliza.*
* **1.0 (Inicial):** Input del usuario concatenado directamente al prompt de sistema (prompt injection trivial); output del LLM ejecutado/renderizado sin sanitizar.
* **3.0 (En Desarrollo):** Separación básica de prompts y sanitización de output en los flujos principales.
* **5.0 (Optimizado):** Amenazas del OWASP LLM Top 10 modeladas, controles LLM01/LLM02/LLM06 testeados, tools/funciones del LLM con autorización propia y monitoreo de abuso en producción.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Definir el universo (DAI.0):** `git log --grep='Co-Authored-By'` + política en `AGENTS.md`/`CLAUDE.md` + etiquetas de PR. Sin atribución posible ⇒ universo = últimos 12 meses, `confidence: low`.
2. **Escaneo de Inseguridades Rápidas:** Buscar parches temporales generados por IA como `rejectUnauthorized: false`, `process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'`, `cors({origin: '*'})`.
3. **Auditoría Anti-Slopsquatting (T2):** Ejecutar `package_registry_audit` según su contrato en `config/checks_catalog.yaml` — existencia en registro oficial, fecha de publicación, descargas, repo enlazado (osv-scanner + APIs de npm/PyPI).
4. **Robustez asíncrona (T2):** Semgrep con reglas de async-sin-catch — el regex por línea no puede detectar bloques multilínea.
5. **Análisis de Pruebas Tautológicas:** Buscar `expect(true)`, `assert True`, bloques `it()` / `def test_*` sin aserciones, y correr mutation testing como evidencia T2 (cruce D5.1).
6. **Detección de Duplicación (T2):** `jscpd` acotado al universo IA-atribuido, comparado contra la línea base de D2.2.
7. **Seguridad LLM (DAI.6, si aplica):** Revisar flujos LLM contra LLM01/LLM02/LLM06 con citas `archivo:línea`.
