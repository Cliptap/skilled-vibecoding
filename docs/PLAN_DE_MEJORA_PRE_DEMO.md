# Plan de Mejora Pre-Demo — Biblioteca de Skills

> **Objetivo:** Refinar la biblioteca de skills para gobernanza media en un consultorio,
> demostrando que el uso guiado de skills produce software de mayor calidad, coherencia
> y trazabilidad que programar sin guías estructuradas.
>
> **Rama:** `predemo` | **Fecha última iteración:** Mayo 2026

---

## 0. Diagnóstico General

| Dimensión | Diagnóstico inicial | Tras iteración predemo |
|-----------|---------------------|------------------------|
| Cobertura del pipeline | 11 skills, sin frontend testing ni observabilidad | **14 skills** (agregadas: frontend testing, observabilidad, input validation) |
| Nodos de decisión | 3–7 secciones genéricas por skill | Refinados con preguntas quirúrgicas (ratio lecturas/escrituras, matriz RACI, dev vs prod, 3 estados UI) |
| Gobernanza | Solo explícita en skills 01, 04, 06 | **Propagada a 7 skills adicionales** (03, 05, 06, 07, 08, 09, 10) con nodo "Gobernanza Heredada" |
| Reglas obligatorias | Sin verificación | **14 skills con checklist de verificación post-generación** |
| Versionamiento | Solo skill 11 | **14 skills con frontmatter YAML** (name, version, depends_on, stage, governance) |
| Caveman mode | Mencionado sin documentar | **Documentado en 4 skills** con advertencias y bloque de "Decisiones Asumidas" |
| Templates | Ninguno | **PRD de ejemplo + comparativa antes/después** (14 violaciones → 0) |
| Aplicación práctica | Sin demo ejecutable | **App funcional con 3 roles, interfaz profesional en español** |

---

## 1. Nodos de Decisión: Lo que Funciona y lo que Falta

Cada skill define preguntas-sección. La calidad del software generado depende de qué tan bien
esas preguntas cubren las **decisiones arquitectónicas irreversibles** del proyecto.

### Evaluación de nodos de decisión (con mejoras implementadas)

| Skill | Decisiones cubiertas (incluyendo mejoras) | Pendiente |
|-------|-------------------------------------------|-----------|
| **01 PRD** | Problema, usuarios, tipo de datos, fuente, arquitectura, gobernanza, **contexto normativo** (HIPAA, GDPR, Ley 20.584) | — |
| **02 DB Schema** | Entidades, relaciones, atributos, **ratio lecturas/escrituras, picos predecibles**, volumen | Estrategia de auditoría (CDC, temporal tables) |
| **03 API Endpoints** | Lifespan, DTOs, inyección, excepciones, **RFC 7807 para APIs de terceros** | Versionamiento de API, rate limiting |
| **04 ETL Pipeline** | Fuentes, limpieza, gobernanza, destino, **7 preguntas de control de input (RUT)** | Estrategia de reintentos, idempotencia |
| **05 Frontend UI** | Stack, pantallas, navegación, consumo de API, **3 estados obligatorios por página** (empty, loading, error) | Accesibilidad WCAG 2.1 AA |
| **06 Reportería** | KPIs, granularidad, gobernanza en reportes, presentación | SLA de consultas, estrategia de caché |
| **07 Auth/Security** | Algoritmo, payload JWT, **matriz RACI para derivar scopes**, respuestas HTTP | MFA/TOTP, rate limiting en login |
| **08 ORM/Persistencia** | Motor, tipos, transacciones, concurrencia | Connection pooling, read replicas |
| **09 Docker** | Versiones, multi-contenedor, health checks, volúmenes, **dev vs producción** | Secrets management, resource limits |
| **10 Testing** | Herramientas, DB aislada, auth mocks, edge cases | Contract testing, performance testing |
| **11 Contexto** | Greenfield/brownfield, artefactos, flujo, **verificación post-generación** | Métricas de calidad de skills |
| **12 Frontend Testing** | Component tests (Vitest), E2E (Playwright), estados UI, accesibilidad axe-core | — |
| **13 Observability** | Logging JSON, métricas Prometheus, health checks, tracing distribuido | — |
| **16 Input Validation** | **7 preguntas generalizadas** para cualquier campo regulado (RUT, teléfono, email, fecha, moneda, IBAN) | — |

---

## 2. Comparativa: Skills vs Sin Guías

Para la demo se contrasta la construcción de un **módulo de citas médicas con gobernanza media**
usando dos enfoques:

### Caso: "Agendar cita médica con validación de RUT y control de acceso"

| Aspecto | Sin skills (prompt libre) | Con skills (pipeline guiado) |
|---------|---------------------------|------------------------------|
| **Modelo de datos** | `VARCHAR(20)` para RUT, sin índice, sin FK explícita | `TEXT`, índice B-Tree en FK `patient_id`, `CHECK` constraint en estado, `TIMESTAMPTZ` |
| **Validación RUT** | Regex suelta solo en frontend | Validación módulo-11 en backend + auto-formato en frontend (skill 04 + 16) |
| **Autenticación** | Middleware ad-hoc sin scopes | JWT + RBAC con scopes por entidad y verbo (skill 07) |
| **API REST** | `POST /createAppointment` (no RESTful) | `POST /api/v1/appointments` → 201 Created (skill 03) |
| **Errores** | `500 Internal Server Error` genérico | 401, 403, 404, 422 diferenciados y estandarizados (skill 03 + 07) |
| **Transacciones** | Sin rollback en fallo parcial | `BEGIN/COMMIT/ROLLBACK` explícito (skill 08) |
| **Soft delete** | `DELETE FROM appointments WHERE id=X` | `UPDATE appointments SET deleted_at=NOW() WHERE id=X` (skill 08) |
| **Tests** | Solo happy path manual | AAA pattern, test de 401/403/404, DB aislada, dependency overrides (skill 10) |
| **Docker** | `FROM python:latest`, sin USER | Multi-stage, `USER 1000`, health checks, `.env` externo (skill 09) |
| **Trazabilidad** | Sin registro de quién creó/modificó | Columnas de auditoría en toda entidad (gobernanza media propagada) |
| **Frontend** | Inglés mezclado, mock data, un solo rol | **Español completo, 3 roles con vistas diferenciadas, sin mock data** |

**Resultado demostrable:** 14 violaciones sin skills → 0 con skills.
Ver [`docs/skills/templates/antes_vs_despues_citas_medicas.md`](skills/templates/antes_vs_despues_citas_medicas.md).

---

## 3. Mejoras Implementadas

### 3.1 Nuevas skills creadas

| # | Skill | Propósito | Estado |
|---|-------|-----------|--------|
| 12 | `12_frontend_testing.md` | Component tests (Vitest) + E2E (Playwright) + accesibilidad axe-core | **Creado** |
| 13 | `13_observability.md` | Logging JSON estructurado, métricas Prometheus, health checks, tracing | **Creado** |
| 14 | `14_input_validation_patterns.md` | 7 preguntas generalizadas para cualquier campo regulado | **Creado** |

### 3.2 Refinamiento de skills existentes

| Mejora | Skills afectadas | Descripción |
|--------|-----------------|-------------|
| **Propagación de gobernanza** | 03, 05, 06, 07, 08, 09, 10 | Nodo "0. Gobernanza Heredada" que explica implicancias de cada nivel para esa skill |
| **Verificación post-generación** | 01–11 | Checklist concreto de reglas a verificar antes de confirmar el output |
| **Frontmatter YAML** | 01–11 | `name`, `version: 1.0.0`, `depends_on`, `stage`, `governance` |
| **Grafo de dependencias** | CONTEXT.md | Visual ASCII del pipeline con todas las dependencias |
| **Caveman Mode documentado** | 03, 07, 09, 10 | Sección con advertencias, bloque de "Decisiones Asumidas" y cuándo usarlo |
| **Nodo "Contexto Normativo"** | 01 | HIPAA, GDPR, Ley 20.584, LGPD antes de cualquier otra pregunta |
| **Refinamiento de preguntas** | 01, 02, 03, 05, 07, 09 | SQL vs NoSQL → ACID vs escalabilidad, lecturas/escrituras → ratio + picos, excepciones → RFC 7807, páginas → 3 estados, roles → matriz RACI, Compose → dev vs prod |
| **skills-lock.json** | global | Ahora incluye las 14 skills propias versionadas |

### 3.3 Templates y ejemplos

| Archivo | Contenido |
|---------|-----------|
| `templates/01_prd_consultorio_ejemplo.md` | PRD completo de consultorio médico con gobernanza media (Ley 20.584) |
| `templates/antes_vs_despues_citas_medicas.md` | Comparativa concreta: DB, API, RUT, Docker, tests — 14 violaciones evitadas |

### 3.4 Aplicación práctica: demo funcional

Se construyó una aplicación completa que demuestra las skills en acción:

| Componente | Qué se hizo |
|-----------|-------------|
| **Frontend** | App.vue reescrito: 100% español, diseño profesional (grises + esmeralda), sin mock data ni inglés |
| **Roles** | 3 vistas diferenciadas: admin (full), médico (sus citas + lectura), recepcionista (pacientes + citas) |
| **Login** | Selector de usuario demo con 3 roles. JWT decodificado client-side para mostrar nombre y permisos |
| **Backend** | 3 usuarios demo (admin, medico, recepcionista). JWT enriquecido con `full_name` y `role` |
| **Scopes** | Endpoints corregidos: `patients:write`, `practitioners:write`, `appointments:write` en vez de solo `admin:all` |
| **UI** | Botón "Nuevo paciente" arriba de la tabla. Sidebar adaptado al rol. Estados vacíos con íconos y mensajes |
| **Limpieza** | Eliminados: HelloWorld.vue, hero.png, vite.svg, vue.svg, stitch_dashboard_mockup.html, download.py, lucide-vue-next |

---

## 4. Plan de Implementación (Demo)

### Fase 0: Preparación — COMPLETADO
- [x] Versionar todas las skills con frontmatter YAML
- [x] Agregar `depends_on` y grafo de dependencias en CONTEXT.md
- [x] Documentar Caveman Mode en skills 03, 07, 09, 10

### Fase 1: Refinamiento de nodos de decisión — COMPLETADO
- [x] Agregar nodo "Contexto Normativo" en skill 01
- [x] Agregar nodo "Gobernanza Heredada" en skills 03, 05, 06, 07, 08, 09, 10
- [x] Refinar preguntas débiles (6 skills)
- [x] Agregar "Verificación post-generación" en las 11 skills originales

### Fase 2: Nuevas skills — COMPLETADO
- [x] Crear `12_frontend_testing.md`
- [x] Crear `13_observability.md`
- [x] Crear `14_input_validation_patterns.md`

### Fase 3: Templates + demo funcional — COMPLETADO
- [x] Crear PRD de ejemplo: consultorio médico 3 tablas con gobernanza media
- [x] Crear diff "antes/después" para el caso de citas médicas
- [x] README.md con instrucciones de inicialización
- [x] App funcional con 3 roles, español completo, sin mock data

### Fase 4: Pendiente (post-demo)
- [ ] `14_cicd_pipeline.md`
- [ ] `15_accessibility_ux.md`

---

## 4.1 Retroalimentación de la Supervisora — Hito 3

La supervisora estableció 6 exigencias para la entrega final. A continuación se evalúa
el grado de cumplimiento actual y las acciones necesarias.

### 1. Fortalecer presentación de resultados con evidencia clara del sistema en funcionamiento

| Estado | Parcial (60%) |
|--------|---------------|
| **Lo que tenemos** | Comparativa antes/después (`antes_vs_despues_citas_medicas.md`), PRD de ejemplo, app funcional con 3 roles |
| **Lo que falta** | Capturas de pantalla del sistema en cada rol, tutorial paso a paso de un caso de uso completo, salidas reales del sistema (logs, respuestas HTTP) |
| **Acción** | Crear `docs/demo/guia_de_demo.md` con flujo narrado para cada rol + capturas. Ejecutar `test_api.py` y documentar su salida. |

### 2. Incorporar mecanismos de validación formales (tests, criterios de verificación)

| Estado | Parcial (70%) |
|--------|---------------|
| **Lo que tenemos** | Checklists de verificación post-generación en 14 skills, tests unitarios en `tests/unit/`, `test_api.py` |
| **Lo que falta** | Evidencia de ejecución de tests (reporte pytest), cobertura documentada, tests de frontend no implementados |
| **Acción** | Ejecutar `pytest tests/unit/ -v --tb=short` y guardar salida en `qa_reports/`. Documentar cobertura actual y gaps. |

### 3. Ampliar y estructurar el backlog a nivel de proyecto completo

| Estado | No cumplido (10%) |
|--------|-------------------|
| **Lo que tenemos** | `tracks.md` con 3 tracks básicos (auth, UI, contexto) |
| **Lo que falta** | Backlog completo con sprints futuros, milestones, relación skills → funcionalidades, priorización |
| **Acción** | Reestructurar `tracks.md` como backlog con: Sprint 0 (setup), Sprint 1 (core: pacientes + citas), Sprint 2 (gobernanza media), Sprint 3 (reportes), Sprint 4 (CI/CD + QA). Mapear cada track a la skill que lo genera. |

### 4. Centralizar desarrollo en repositorio GitHub e incluir enlace

| Estado | No cumplido (0%) |
|--------|------------------|
| **Lo que tenemos** | Git local, rama `predemo` con todos los cambios |
| **Lo que falta** | Repositorio en GitHub, README con enlace, commits organizados |
| **Acción** | Crear repo en GitHub, pushear rama `predemo`, agregar enlace en README y en este documento. |

### 5. Mejorar la demostración visual del funcionamiento real

| Estado | Parcial (50%) |
|--------|---------------|
| **Lo que tenemos** | App funcional con 3 roles, interfaz profesional en español |
| **Lo que falta** | Guía de demo con flujo narrado por rol, capturas de cada vista, video o GIF de la interacción |
| **Acción** | Crear `docs/demo/guia_de_demo.md` con: login de cada rol → vista principal → operación (crear paciente, agendar cita) → resultado. Incluir capturas de cada paso. |

### 6. Incluir arquitectura asociada al caso práctico con los skills utilizados

| Estado | Parcial (40%) |
|--------|---------------|
| **Lo que tenemos** | Grafo de dependencias en CONTEXT.md, frontmatter YAML con `depends_on` en cada skill |
| **Lo que falta** | Diagrama que mapee skills → componentes del sistema, tabla de trazabilidad (qué skill generó qué archivo), justificación de cada skill en el caso consultorio |
| **Acción** | Crear `docs/ARQUITECTURA_SKILLS.md` con: diagrama de capas (skills → código), tabla de trazabilidad (skill → archivos generados), justificación de cada skill para gobernanza media en consultorio. |

---

## 4.2 Plan de Acción — Hito 3

| # | Tarea | Prioridad | Estimación |
|---|-------|-----------|------------|
| 1 | Crear repo GitHub + pushear rama `predemo` | **Crítico** | 15 min |
| 2 | Reestructurar `tracks.md` como backlog multi-sprint | **Crítico** | 30 min |
| 3 | Crear `docs/ARQUITECTURA_SKILLS.md` con trazabilidad skills → código | **Alta** | 45 min |
| 4 | Crear `docs/demo/guia_de_demo.md` con flujo por rol + capturas | **Alta** | 60 min |
| 5 | Ejecutar tests + guardar reporte en `qa_reports/` | **Alta** | 20 min |
| 6 | Actualizar README con enlace al repo y sección de demo | **Media** | 15 min |

---

## 5. Métricas de Éxito para la Demo

| Métrica | Sin skills | Con skills (resultado real) |
|---------|------------|--------------------------|
| Anti-patrones de DB (VARCHAR, sin FK index, TIMESTAMP sin TZ, sin CHECK) | 5+ | 0 |
| Endpoints sin RBAC | 60%+ | 0% |
| Soft deletes omitidos | Sí | No (obligatorio por gobernanza media) |
| Códigos HTTP incorrectos | 4+ endpoints | 0 |
| Errores sin log estructurado | `print()` | `logging` con niveles |
| Tests inexistentes o solo happy path | 0 tests negativos | 401, 403, 404 testeados |
| Docker como root | Sí | No (`USER` directive) |
| Validación RUT solo frontend | Regex suelto | Módulo-11 backend + auto-formato frontend |
| Trazabilidad de cambios | Sin `created_by`/`updated_at` | Todas las tablas con auditoría |
| Inglés en la interfaz | "Health Systems v2.4", "Booked", "FHIR Sync" | **0 términos en inglés** |
| Vistas por rol | Una sola vista genérica | **3 vistas diferenciadas** (admin, médico, recepcionista) |
| Mock data hardcodeada | "14 sesiones activas", "99.9% FHIR Sync" | **0 datos mock — todo del backend** |

---

## 6. Conclusión

La biblioteca pasó de 11 skills base a **14 skills versionadas y verificables**, con:

1. **Nodos de decisión quirúrgicos** — cada skill fuerza decisiones arquitectónicas reales (ACID vs escalabilidad, matriz RACI, dev vs prod, 3 estados UI) en vez de preguntas genéricas.

2. **Gobernanza propagada** — el nivel elegido en skill 01 condiciona explícitamente cada skill subsiguiente con un nodo "Gobernanza Heredada" que explica las implicancias concretas.

3. **Verificación y trazabilidad** — frontmatter YAML, `depends_on`, checklist post-generación, `skills-lock.json` y grafo visual cierran el ciclo de calidad.

4. **Demo funcional** — aplicación real con 3 roles, interfaz profesional en español, sin mock data ni inglés, que demuestra el valor de las skills en un consultorio con gobernanza media bajo Ley 20.584.

### Pendientes críticos para Hito 3 (retroalimentación supervisora)

De las 6 exigencias, **2 están en estado crítico** (sin avance) y **4 en estado parcial**:

| Exigencia | Estado | Bloqueante |
|-----------|--------|------------|
| Repositorio GitHub con enlace | 0% — sin crear | Sí |
| Backlog multi-sprint estructurado | 10% — solo 3 tracks | Sí |
| Arquitectura con trazabilidad skills → código | 40% — solo grafo | No |
| Demostración visual con capturas y flujo narrado | 50% — app existe pero sin guía | No |
| Evidencia de tests ejecutados | 70% — tests existen pero sin reporte | No |
| Casos de uso con salidas del sistema | 60% — comparativa existe pero sin logs reales | No |

Las 6 tareas del plan de acción (sección 4.2) resuelven estos gaps y deben completarse
antes de la presentación del Hito 3.
