# Dimensión D6: DevOps, CI/CD e Infraestructura

## 1. Descripción
Evaluación de la madurez de la automatización en el ciclo de integración y despliegue continuo (CI/CD), métricas de velocidad y estabilidad de entrega (DORA), Infraestructura como Código (IaC) y postura de seguridad Cloud.

## 2. Objetivo
Garantizar entregas de software ágiles, frecuentes y seguras, con entornos reproducibles y una infraestructura Cloud resiliente y automatizada.

## 3. Referencia de Estándares de la Industria
* **DORA Metrics (Google Cloud DevOps Research & Assessment):** Métricas globales de velocidad y estabilidad.
* **AWS / GCP / Azure Well-Architected Framework:** Pilar de Excelencia Operativa y Seguridad.
* **CNCF Cloud Native Maturity Model:** Adopción de prácticas y estándares Cloud Native.
* **CIS Benchmarks (Center for Internet Security):** Seguridad de configuración de infraestructura Cloud.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D6.1 Automatización de Pipelines CI/CD
* **1.0 (Inicial):** Despliegues manuales por FTP/SSH copiando archivos directamente al servidor.
* **3.0 (En Desarrollo):** Pipeline CI/CD automático que realiza build y despliegue a QA/Staging; despliegue a Prod requiere pasos manuales.
* **5.0 (Optimizado):** Pipeline CI/CD 100% automatizado con artefactos inmutables (Docker containers / AMI), despliegues Canary o Blue-Green sin tiempo de caída.

### D6.2 Métricas DORA (Velocidad y Estabilidad)
* **1.0 (Inicial):** Despliegues mensuales o trimestrales; Lead Time > 1 mes; Change Failure Rate > 30%; MTTR > 1 día (*Low Performer*).
* **3.0 (En Desarrollo):** Despliegues semanales; Lead Time < 1 semana; Change Failure Rate 15-30%; MTTR < 1 día (*Medium Performer*).
* **5.0 (Optimizado):** Múltiples despliegues diarios a demanda; Lead Time < 1 hora; Change Failure Rate < 5%; MTTR < 1 hora (*Elite Performer*).

### D6.3 Infraestructura como Código (IaC) y Entornos
* **1.0 (Inicial):** Recursos Cloud aprovisionados manualmente desde la consola web ("ClickOps"); disparidad severa entre Dev, QA y Prod.
* **3.0 (En Desarrollo):** Módulos de Terraform / CloudFormation presentes para la mayoría de recursos; paridad razonable de entornos.
* **5.0 (Optimizado):** 100% de la infraestructura gestionada por IaC con estado remoto bloqueado, validaciones en CI (`terraform plan`) y paridad exacta de entornos.

### D6.4 Seguridad Cloud e IAM
* **1.0 (Inicial):** Roles de servicio con permisos `*` (AdministratorAccess); recursos expuestos públicamente a internet sin WAF ni Security Groups restringidos.
* **3.0 (En Desarrollo):** Políticas IAM con alcance definido; Security Groups restringidos a puertos necesarios.
* **5.0 (Optimizado):** Principio de mínimo privilegio estricto, redes privadas (VPC Subnets), WAF configurado, CloudTrail y GuardDuty activos.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Inspección de Pipelines:** Buscar `.github/workflows/`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`, `Jenkinsfile`.
2. **Inspección de IaC:** Buscar carpetas `terraform/`, `pulumi/`, `serverless.yml`, `cdk/`, `cloudformation/`.
3. **Verificación de Docker/Contenedores:** Buscar `Dockerfile`, `docker-compose.yml`, Helm Charts o Manifiestos K8s.
4. **Auditoría de Políticas Cloud/IAM:** Inspeccionar permisos en código Terraform o configuraciones de AWS/Cloud.
