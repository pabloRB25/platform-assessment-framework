# Dimensión D3: Seguridad Aplicativa y DevSecOps

## 1. Descripción
Evaluación de la postura de ciberseguridad en el código fuente, la protección de datos sensibles, la gestión de la autenticación/autorización, el análisis de dependencias vulnerables y los controles DevSecOps integrados en el SDLC.

## 2. Objetivo
Garantizar la confidencialidad, integridad y disponibilidad de la aplicación y sus datos, previniendo brechas de seguridad, fugas de credenciales o explotación de vulnerabilidades conocidas.

## 3. Referencia de Estándares de la Industria
* **OWASP SAMM (Software Assurance Maturity Model):** Modelo de madurez para seguridad en el ciclo de desarrollo.
* **OWASP ASVS (Application Security Verification Standard):** Estándar de verificación de requisitos de seguridad aplicativa.
* **OWASP Top 10 / API Security Top 10:** Principales riesgos de seguridad en aplicaciones web y APIs.
* **NIST SP 800-53 / 800-115:** Guía de seguridad de la información y pruebas de seguridad.
* **SLSA (Supply-chain Levels for Software Artifacts):** Seguridad en la cadena de suministro de software.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D3.1 Autenticación y Autorización (OWASP ASVS V2 / V3)
* **1.0 (Inicial):** Autenticación customizada insegura (contraseñas en texto plano/MD5), JWT sin firma/expiración, falta de comprobación de permisos (BOLA/IDOR).
* **3.0 (En Desarrollo):** OAuth2/JWT estándar utilizado, contraseñas hasheadas con BCrypt/Argon2, controles RBAC parciales.
* **5.0 (Optimizado):** OAuth2/OIDC con mTLS/PKCE, JWT de vida corta con rotación de refresh tokens, RBAC/ABAC estricto en cada endpoint.

### D3.2 Gestión de Secretos y Credenciales
* **1.0 (Inicial):** Credenciales, API Keys o certificados harcodeados directamente en el código fuente o subidos al repositorio Git.
* **3.0 (En Desarrollo):** Variables de entorno (`.env`) utilizadas pero guardadas localmente sin rotación; falta de uso de Key Vault.
* **5.0 (Optimizado):** Uso de Vault / AWS Secrets Manager / GCP Secret Manager, rotación automática y escaneo continuo anti-secretos en git (GitGuardian/Trufflehog).

### D3.3 Análisis de Dependencias (SCA & Supply Chain)
* **1.0 (Inicial):** Uso de componentes de terceros obsoletos sin auditar; presencia de CVEs críticos/altos sin parchear.
* **3.0 (En Desarrollo):** Ejecución ocasional de `npm audit` o `pip audit`; dependencias actualizadas manualmente.
* **5.0 (Optimizado):** Escaneo automatizado de SCA en CI/CD (Dependabot, Snyk, Trivy), política de bloqueo por CVEs y SBOM (Software Bill of Materials) generado.

### D3.4 Sanitización, Input Validation e Inyección
* **1.0 (Inicial):** Consultas SQL concatenadas directamente (SQL Injection), falta de sanitización HTML/JS (XSS) y SSRF.
* **3.0 (En Desarrollo):** ORM / Sentencias preparadas utilizadas para SQL; validación de entradas básica en controladores.
* **5.0 (Optimizado):** Validación estricta de esquema en todas las entradas (Zod, Joi, Class-Validator), ORM con consultas parametrizadas, cabeceras de seguridad HTTP (CSP, HSTS, CORS restringido).

---

## 5. Metodología de Ejecución para el Agente IA

1. **Búsqueda de Secretos Hardcodeados:** Buscar patrones de claves API, tokens, contraseñas en código mediante expresiones regulares.
2. **Escaneo de Vulnerabilidades de Dependencias:** Inspeccionar `package.json`, `pom.xml`, `requirements.txt`, `go.mod` o ejecutar herramientas SCA.
3. **Auditoría de Consultas a BD:** Buscar concatenación directa de cadenas en SQL (`SELECT * FROM table WHERE id = ' + id`).
4. **Verificación de Encriptación de Contraseñas:** Buscar funciones de hashing en código (`md5`, `sha1`, `bcrypt`, `argon2`).
