# Dimensión DAI: Código Agéntico e Inteligencia Artificial

## 1. Descripción
Evaluación especializada de la calidad, seguridad, mantenibilidad y proveniencia del código generado por Agentes de IA o asistentes de código (LLMs como GitHub Copilot, Cursor, Antigravity, Claude Code). Esta dimensión audita riesgos específicos como alucinación de dependencias (Slopsquatting), sesgo de camino feliz (Happy-Path Bias), pruebas fantasma y duplicación por fragmentación de contexto.

## 2. Objetivo
Garantizar que el uso de IA en la generación de código no degrade la arquitectura del sistema, no introduzca vulnerabilidades en la cadena de suministro ni aumente la deuda técnica oculta por falta de supervisión humana (*Human-in-the-Loop*).

## 3. Referencia de Estándares de la Industria
* **OWASP Top 10 for LLM Applications & Generative AI Output Security.**
* **SLSA (Supply-chain Levels for Software Artifacts) — Provenance & Build Integrity.**
* **Mutation Testing Standards (Stryker / PITest):** Validación de la efectividad real de pruebas unitarias.
* **ISO/IEC 25010:** Sub-características de Mantenibilidad y Analizabilidad en código sintético.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

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
* **5.0 (Optimizado):** Política clara de gobernanza para desarrollo asistido por IA, commits etiquetados con provenancia y revisión estricta de *Human-in-the-Loop*.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Escaneo de Inseguridades Rápidas:** Buscar parches temporales generados por IA como `rejectUnauthorized: false`, `process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'`, `cors({origin: '*'})`.
2. **Auditoría Anti-Slopsquatting:** Contrastar todas las dependencias en `package.json` / `requirements.txt` contra el API de registros oficiales (npm, PyPI) comprobando fecha de publicación y descargas.
3. **Análisis de Pruebas Tautológicas:** Buscar en archivos de test expresiones como `expect(true)`, `assert True`, o bloques `it()` / `def test_*` sin llamadas a aserciones.
4. **Detección de Duplicación Semántica:** Analizar similitud entre archivos de utilidades creados en submódulos recientes.
