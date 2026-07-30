# Dimensión D2: Código Fuente y Mantenibilidad

## 1. Descripción
Evaluación de la calidad interna del código fuente, el apego a buenas prácticas de programación, legibilidad, diseño orientado a objetos/funcional, complejidad ciclomática y control de deuda técnica.

## 2. Objetivo
Garantizar que la aplicación sea fácil de mantener, extender y refactorizar por cualquier desarrollador del equipo, minimizando el costo de mantenimiento futuro.

## 3. Referencia de Estándares de la Industria
* **ISO/IEC 25010:2023 (SQuaRE):** Modelo de calidad de software vigente — 9 características (incluye Safety y Flexibility con escalabilidad); Mantenibilidad: Modificabilidad, Modularidad, Reusabilidad, Analizabilidad.
* **ISO/IEC 5055:2021:** 139 debilidades CWE medibles de calidad estructural — convierte la deuda técnica de estimación en medición (junto con ATDM2, deuda en horas/costo).
* **Clean Code (Robert C. Martin):** Principios de legibilidad y diseño de software.
* **SonarQube Quality Gates:** Estándares de la industria para complejidad ciclomática, duplicación y code smells.
* **Principios SOLID, DRY, KISS, YAGNI.**

> **Alcance:** D2 califica el **codebase completo**. Los defectos en código con atribución IA se registran en el módulo DAI — el mismo defecto nunca baja el PHS dos veces (regla anti doble conteo en `config/weights_and_thresholds.yaml`).

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D2.1 Estándares de Código y Modismos
* **1.0 (Inicial):** Sin linters ni formateadores; estilos dispares en el código, nombres crípticos o sin significado.
* **3.0 (En Desarrollo):** Linter configurado pero ignorado en algunos archivos; convenciones de nombres consistentes.
* **5.0 (Optimizado):** Linter y Formateador estricto ejecutados en CI/pre-commit; código limpio e idiomático.

### D2.2 Deuda Técnica Estructural y Complejidad
* **1.0 (Inicial):** Clases/Funciones gigantes (Funciones > 100 líneas), complejidad ciclomática > 15, alta duplicación (> 10%).
* **3.0 (En Desarrollo):** Complejidad moderada (5-10), funciones cortas pero con bloques de duplicación aislados.
* **5.0 (Optimizado):** Complejidad ciclomática < 5 por función, cero duplicación significativa, métodos pequeños y enfocados.

### D2.3 Principios SOLID y Diseño Clean Code
* **1.0 (Inicial):** Violaciones sistemáticas de SOLID; acoplamiento directo a implementaciones concretas, cero interfaces/abstracciones.
* **3.0 (En Desarrollo):** Principios SOLID aplicados en capas principales, pero violaciones en clases de servicio o controladores.
* **5.0 (Optimizado):** Inyección de dependencias estricta, desacoplamiento de interfaces, responsabilidad única respetada al 100%.

### D2.4 Manejo de Errores y Excepciones
* **1.0 (Inicial):** Captura silenciosa de errores (`catch (Exception e) {}`), falta de logs de error o exposición de *stack traces* sensibles a clientes.
* **3.0 (En Desarrollo):** Excepciones personalizadas usadas, pero con captura genérica en capas intermedias.
* **5.0 (Optimizado):** Excepciones de dominio bien jerarquizadas, jerarquía limpia, manejo global de errores (*Global Exception Handler*) sin fugar detalles de infraestructura.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Revisión de Linters:** Verificar existencia de `.eslintrc`, `.rubocop.yml`, `phpcs.xml`, `ruff.toml`, `biome.json` o similar, **y** que corran como gate en CI (existencia sola = señal T1, techo 3.0).
2. **Métricas T2:** Ejecutar `lizard`/`radon` (complejidad) y `jscpd` (duplicación) y archivar outputs en `evidence/` — la deuda estructural se mide, no se estima.
3. **SAST sintáctico:** Ejecutar `semgrep` para catch vacíos y promesas sin manejo — el grep por línea no detecta bloques multilínea.
4. **Juicio T3 (SOLID):** Leer constructores, límites de clase y configuración IoC en una muestra representativa con citas `archivo:línea`; contar keywords (`interface`, `Autowired`) no evalúa diseño.
