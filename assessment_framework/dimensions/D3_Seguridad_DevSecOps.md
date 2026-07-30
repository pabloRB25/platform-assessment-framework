# Dimensión D3: Seguridad Aplicativa y DevSecOps

## 1. Descripción
Evaluación de la postura de ciberseguridad en el código fuente, la protección de datos sensibles, la gestión de la autenticación/autorización, el análisis de dependencias vulnerables y los controles DevSecOps integrados en el SDLC.

## 2. Objetivo
Garantizar la confidencialidad, integridad y disponibilidad de la aplicación y sus datos, previniendo brechas de seguridad, fugas de credenciales o explotación de vulnerabilidades conocidas.

## 3. Referencia de Estándares de la Industria
* **OWASP SAMM v2.1.0 (sep 2024):** Modelo de madurez para seguridad en el ciclo de desarrollo.
* **OWASP ASVS 5.0.0 (mayo 2025):** Estándar de verificación — 14 capítulos, incluye V3 Frontend Security, V9 Tokens y V10 OAuth/OIDC.
* **OWASP Top 10:2025:** A03 es ahora *Software Supply Chain Failures* — literalmente el tema de DAI.1.
* **OWASP API Security Top 10 (2023):** API1 (BOLA) y API5 (BFLA) — la clase #1 de vulnerabilidad en APIs, evaluada en D3.5.
* **SLSA v1.2:** Build Track L0–L3 y Source Track L1–L4 (el Source L4 = two-party review ancla DAI.5 y D9.2).
* **ISO/IEC 27001:2022 Anexo A:** controles de desarrollo seguro 8.25–8.34.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D3.1 Autenticación y Autorización (ASVS 5.0 V6/V8/V9/V10)
* **1.0 (Inicial):** Autenticación customizada insegura (contraseñas en texto plano/MD5), JWT sin firma/expiración, falta de comprobación de permisos (BOLA/IDOR).
* **3.0 (En Desarrollo):** OAuth2/JWT estándar utilizado, contraseñas hasheadas con BCrypt/Argon2, controles RBAC parciales.
* **5.0 (Optimizado):** OAuth2/OIDC con mTLS/PKCE, JWT de vida corta con rotación de refresh tokens, RBAC/ABAC estricto en cada endpoint.

### D3.2 Gestión de Secretos y Credenciales
* **1.0 (Inicial):** Credenciales, API Keys o certificados hardcodeados en el código fuente o presentes en el **historial** de Git sin rotar (el hallazgo real más frecuente vive en el historial, no en el HEAD).
* **3.0 (En Desarrollo):** Variables de entorno (`.env`) utilizadas pero guardadas localmente sin rotación; falta de uso de Key Vault.
* **5.0 (Optimizado):** Uso de Vault / AWS Secrets Manager / GCP Secret Manager, rotación automática y escaneo continuo anti-secretos en git (GitGuardian/Trufflehog).

### D3.3 Análisis de Dependencias, Licencias y Supply Chain (SCA)
* **1.0 (Inicial):** Uso de componentes de terceros obsoletos sin auditar; presencia de CVEs críticos/altos sin parchear.
* **3.0 (En Desarrollo):** Ejecución ocasional de `npm audit` o `pip audit`; dependencias actualizadas manualmente.
* **5.0 (Optimizado):** Escaneo automatizado de SCA en CI/CD (Dependabot, Snyk, Trivy), política de bloqueo por CVEs, inventario de licencias controlado (sin GPL/AGPL incompatibles con el modelo SaaS) y SBOM (Software Bill of Materials) generado.

### D3.4 Sanitización, Input Validation e Inyección
* **1.0 (Inicial):** Consultas SQL concatenadas directamente (SQL Injection), falta de sanitización HTML/JS (XSS) y SSRF.
* **3.0 (En Desarrollo):** ORM / Sentencias preparadas utilizadas para SQL; validación de entradas básica en controladores.
* **5.0 (Optimizado):** Validación estricta de esquema en todas las entradas (Zod, Joi, Class-Validator), ORM con consultas parametrizadas, cabeceras de seguridad HTTP (CSP, HSTS, CORS restringido).

### D3.5 Seguridad de APIs en Runtime (BOLA/BFLA — OWASP API Top 10 2023)
* **1.0 (Inicial):** Endpoints que devuelven cualquier objeto por ID sin comprobar pertenencia al usuario/tenant (BOLA manifiesto); funciones administrativas accesibles con solo estar autenticado (BFLA).
* **3.0 (En Desarrollo):** Comprobación de pertenencia (anti-BOLA) en los flujos principales; funciones admin con verificación parcial de rol.
* **5.0 (Optimizado):** Autorización a nivel de objeto y de función centralizada, aislamiento multi-tenant aplicado en la capa de datos (RLS o filtro obligatorio) y pruebas automatizadas de control de acceso.

> Todas las sub-dimensiones D3.1, D3.2, D3.4 y D3.5 son **críticas** (gating rules): un score ≤ 2.0 en cualquiera acota el PHS reportable a 2.9, sin importar el promedio.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Escaneo de Secretos (T2, historial completo):** Ejecutar `gitleaks git` sobre **todo el historial** (no solo el HEAD) + verificación de credencial viva con `trufflehog`. El set de 4 regex manuales queda obsoleto — contrato en `config/checks_catalog.yaml`.
2. **SCA + Licencias (T2):** `trivy fs --scanners vuln,license` u `osv-scanner`: CVEs y riesgo legal (GPL/AGPL) en la misma pasada; archivar JSON en `evidence/`.
3. **SAST de Inyección (T2):** `semgrep --config auto` con reglas del lenguaje (SQL concatenado, XSS, SSRF) — análisis sintáctico, no regex por línea.
4. **Auditoría BOLA/BFLA (T3):** Tomar 5+ endpoints que reciben IDs y verificar en código la comprobación de pertenencia/tenancy, con citas `archivo:línea`.
5. **Verificación de Hashing:** Buscar funciones de hashing (`md5`, `sha1`, `bcrypt`, `argon2`) y confirmar el algoritmo usado para contraseñas.
