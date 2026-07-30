# Dimensión D5: Calidad y Estrategia de QA

## 1. Descripción
Evaluación de la madurez del proceso de pruebas de software, la cobertura efectiva de pruebas unitarias/integración/E2E, la automatización en los pipelines de entrega y la gestión de datos e infraestructura de pruebas.

## 2. Objetivo
Garantizar la estabilidad funcional del software, prevenir regresiones en producción y permitir despliegues rápidos y confiables impulsados por redes de seguridad automatizadas.

## 3. Referencia de Estándares de la Industria
* **Pirámide de Automatización de Pruebas (Mike Cohn / Martin Fowler).**
* **ISTQB (International Software Testing Qualifications Board):** Estándares de diseño y ejecución de pruebas.
* **ISO/IEC/IEEE 29119:** Estándar internacional para pruebas de software.
* **Métricas SonarQube / Jacoco / Istanbul:** Cobertura de código y calidad de pruebas.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D5.1 Cobertura de Pruebas Unitarias
* **1.0 (Inicial):** Ausencia total de pruebas unitarias (Cobertura < 10%) o pruebas vacías/dummy sin aserciones reales.
* **3.0 (En Desarrollo):** Cobertura moderada (30% - 60%) en módulos principales; presencia de aserciones válidas.
* **5.0 (Optimizado):** Cobertura de código > 80% en lógica de negocio, pruebas significativas con aserciones estrictas y TDD ocasional.

### D5.2 Pruebas de Integración y E2E
* **1.0 (Inicial):** Pruebas de integración inexistentes; dependencias de base de datos o servicios externos no son probadas o requieren entornos manuales.
* **3.0 (En Desarrollo):** Pruebas de integración presentes para APIs principales usando bases de datos de prueba o contenedores (Testcontainers).
* **5.0 (Optimizado):** Pruebas de integración complejas y suites E2E (Cypress/Playwright) automatizadas corriendo flujos críticos de usuario.

### D5.3 Automatización en CI/CD y Gates de Calidad
* **1.0 (Inicial):** Las pruebas se ejecutan únicamente en las máquinas locales de los desarrolladores ("en mi máquina funciona").
* **3.0 (En Desarrollo):** Las pruebas se ejecutan automáticamente en el pipeline de CI antes de hacer merge a ramas principales.
* **5.0 (Optimizado):** Gate de calidad en CI obligatorio que bloquea la fusión si la cobertura baja o falla algún test (*Quality Gate enforcement*).

### D5.4 Gestión de Datos y Entornos de Prueba
* **1.0 (Inicial):** Pruebas dependen de datos reales de producción o bases de datos compartidas inestables.
* **3.0 (En Desarrollo):** Mocks/Stubs utilizados para servicios externos; base de datos de prueba reiniciada en cada suite.
* **5.0 (Optimizado):** Entornos efímeros de prueba instanciados bajo demanda (Preview Environments) con datos sintéticos totalmente aislados.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Búsqueda de Frameworks de Test:** Identificar `jest`, `mocha`, `pytest`, `phpunit`, `junit`, `cypress`, `playwright`.
2. **Medición de Cobertura:** Inspeccionar reportes de coverage (`coverage/`, `clover.xml`, `jacoco.xml`, `lcov.info`).
3. **Verificación de Aserciones:** Buscar presencia de `expect()`, `assert`, `should` en archivos `*.spec.*` o `*.test.*`.
4. **Verificación en CI:** Revisar si el comando `npm test`, `pytest` o similar se ejecuta en los workflows de CI.
