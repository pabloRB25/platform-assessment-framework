# Dimensión D6: DevOps, CI/CD e Infraestructura

## 1. Descripción
Evaluación de la madurez de la automatización en el ciclo de integración y despliegue continuo (CI/CD), métricas de velocidad y estabilidad de entrega (DORA), Infraestructura como Código (IaC) y postura de seguridad Cloud.

## 2. Objetivo
Garantizar entregas de software ágiles, frecuentes y seguras, con entornos reproducibles y una infraestructura Cloud resiliente y automatizada.

## 3. Referencia de Estándares de la Industria
* **DORA (Accelerate State of DevOps):** **5 métricas** — deployment frequency, lead time for changes, change failure rate, *failed deployment recovery time* (antes MTTR) y *rework rate*. Benchmark por clusters: informe **2024** (el informe 2025 reemplazó Elite/High/Medium/Low por 7 perfiles de equipo; se cita 2024 como última tabla por clusters).
* **AWS / GCP / Azure Well-Architected Framework:** Pilares de Excelencia Operativa, Seguridad y **Cost Optimization**.
* **CNCF Cloud Native Maturity Model:** Adopción de prácticas y estándares Cloud Native.
* **CIS Benchmarks v7.0 (Center for Internet Security):** Seguridad de configuración de infraestructura Cloud.
* **FinOps Framework (FinOps Foundation):** Gestión de costos cloud — evaluada en D6.5.

---

## 4. Sub-Dimensiones y Rúbrica de Calificación (Escala 1.0 a 5.0)

### D6.1 Automatización de Pipelines CI/CD
* **1.0 (Inicial):** Despliegues manuales por FTP/SSH copiando archivos directamente al servidor.
* **3.0 (En Desarrollo):** Pipeline CI/CD automático que realiza build y despliegue a QA/Staging; despliegue a Prod requiere pasos manuales.
* **5.0 (Optimizado):** Pipeline CI/CD 100% automatizado con artefactos inmutables (Docker containers / AMI), despliegues Canary o Blue-Green sin tiempo de caída.

### D6.2 Métricas DORA (Velocidad y Estabilidad — benchmark 2024)
* **1.0 (Inicial):** *Low:* despliegues mensuales o menos; Lead Time > 1 mes; recuperación de deploy fallido > 1 semana.
* **3.0 (En Desarrollo):** *Medium:* despliegues semanales; Lead Time < 1 semana; CFR ~10%.
* **5.0 (Optimizado):** *Elite (2024):* despliegues on-demand; Lead Time **< 1 día**; CFR **5%**; recuperación de deploy fallido < 1 hora.

> Nota: la 5ª métrica (*rework rate*) se releva desde el historial del pipeline. Sin acceso al historial, D6.2 es **N/D** — no se estima a ojo.

### D6.3 Infraestructura como Código (IaC) y Entornos
* **1.0 (Inicial):** Recursos Cloud aprovisionados manualmente desde la consola web ("ClickOps"); disparidad severa entre Dev, QA y Prod.
* **3.0 (En Desarrollo):** Módulos de Terraform / CloudFormation presentes para la mayoría de recursos; paridad razonable de entornos.
* **5.0 (Optimizado):** 100% de la infraestructura gestionada por IaC con estado remoto bloqueado, validaciones en CI (`terraform plan`) y paridad exacta de entornos.

### D6.4 Seguridad Cloud e IAM
* **1.0 (Inicial):** Roles de servicio con permisos `*` (AdministratorAccess); recursos expuestos públicamente a internet sin WAF ni Security Groups restringidos.
* **3.0 (En Desarrollo):** Políticas IAM con alcance definido; Security Groups restringidos a puertos necesarios.
* **5.0 (Optimizado):** Principio de mínimo privilegio estricto, redes privadas (VPC Subnets), WAF configurado, CloudTrail y GuardDuty activos.

### D6.5 Costos y FinOps
* **1.0 (Inicial):** Sin visibilidad de costos; recursos huérfanos y sobredimensionados sin dueño.
* **3.0 (En Desarrollo):** Tagging parcial y presupuesto mensual conocido; sin alertas de costo.
* **5.0 (Optimizado):** FinOps operante: tagging consistente, budgets con alertas, limpieza de recursos huérfanos, right-sizing continuo y unit economics por servicio.

---

## 5. Metodología de Ejecución para el Agente IA

1. **Inspección de Pipelines:** Buscar `.github/workflows/`, `.gitlab-ci.yml`, `bitbucket-pipelines.yml`, `Jenkinsfile`.
2. **Inspección de IaC:** Buscar carpetas `terraform/`, `pulumi/`, `serverless.yml`, `cdk/`, `cloudformation/`.
3. **Verificación de Docker/Contenedores:** Buscar `Dockerfile`, `docker-compose.yml`, Helm Charts o Manifiestos K8s.
4. **Auditoría de Políticas Cloud/IAM (T2):** Ejecutar **Prowler** contra la cuenta (o `checkov`/`tfsec` sobre el IaC si no hay acceso a consola) y mapear findings a IDs del CIS Benchmark. Sin acceso a ninguno de los dos, D6.4 (crítica) se marca N/D ⇒ score 1.0 según `not_available_policy`.
5. **Historial del Pipeline (D6.2):** `gh run list` + `gh api .../deployments` para derivar frecuencia de deploy, lead time y tasa de fallos — archivar en `evidence/`.
6. **FinOps (D6.5):** Verificar tagging en IaC, budgets/alertas configuradas y recursos huérfanos facturando.
