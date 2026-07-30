# Dimensión D2: Código Fuente y Mantenibilidad

## 1. Descripción
Evaluación de la calidad interna del código fuente, el apego a buenas prácticas de programación, legibilidad, diseño orientado a objetos/funcional, complejidad ciclomática y control de deuda técnica.

## 2. Objetivo
Garantizar que la aplicación sea fácil de mantener, extender y refactorizar por cualquier desarrollador del equipo, minimizando el costo de mantenimiento futuro.

## 3. Referencia de Estándares de la Industria
* **ISO/IEC 25010 (SQuaRE):** Modelo de calidad de software (Característica de Mantenibilidad: Modificabilidad, Modularidad, Reusabilidad, Analizabilidad).
* **Clean Code (Robert C. Martin):** Principios de legibilidad y diseño de software.
* **SonarQube Quality Gates:** Estándares de la industria para complejidad ciclomática, duplicación y code smells.
* **Principios SOLID, DRY, KISS, YAGNI.**

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

1. **Revisión de Linters:** Verificar existencia de `.eslintrc`, `.rubocop.yml`, `phpcs.xml`, `tslint.json`, `flake8` o similar.
2. **Búsqueda de Code Smells:** Ejecutar comandos de análisis estático o buscar patrones como `try {} catch (e) {}` vacíos, `console.log` dispersos o `TODO` crónicos.
3. **Inspección de Tamaño de Archivos:** Identificar archivos con más de 500-1000 líneas de código (Clases Dios).
4. **Verificación de Inyección de Dependencias:** Inspeccionar constructores y configuraciones de contenedores IoC.
