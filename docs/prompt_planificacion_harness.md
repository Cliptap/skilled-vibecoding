# Prompt de Planificación — Harness CLI + Biblioteca de Skills Generalizada

> **Objetivo:** Entregarle a Fable 5 el contexto completo para que genere un instalador de consola
> que despliegue un harness de desarrollo completo (skills + reglas + hooks + agentes) en un solo comando,
> generalizando el trabajo previo del Proyecto 3 hacia repositorios de propósito general.

---

## 1. CONTEXTO DEL PROYECTO ACTUAL

### 1.1 Qué hemos construido (Proyecto 3 — Vibe Coding)

Tenemos una **biblioteca de 14 skills** documentadas en `docs/skills/` que guían a un LLM
por un pipeline de 5 etapas para construir **repositorios de procesamiento de datos**:

| Etapa | Skills | Producto |
|-------|--------|----------|
| 1 — Definición | `01_prd` | PRD con contexto normativo, usuarios, datos, gobernanza |
| 2 — Modelado | `02_db` | Esquema de base de datos, entidades, relaciones |
| 3 — Backend | `03_api`, `04_etl`, `07_auth`, `08_orm` | API REST + ETL + Auth RBAC + ORM con soft-deletes |
| 4 — Frontend | `05_frontend` | Interfaz Vue 3 + Tailwind con 3 estados por página |
| 5 — Reportería | `06_reports` | KPIs, dashboards, consultas analíticas |
| Cross-cutting | `09_docker`, `10_testing`, `11_contexto`, `12_frontend_testing`, `13_observability`, `14_input_validation` | Docker, pruebas, observabilidad, contexto |

Cada skill sigue el **patrón pregunta-respuesta**: el modelo NO genera código al inicio.
Formula preguntas por sección, no avanza sin respuesta, y al final genera el entregable
con un checklist de verificación.

### 1.2 Lo que el investigador principal (PI) quiere

- Una **biblioteca de skills reutilizable** para desarrollar **cualquier tipo de repositorio**
  (no solo datos de salud), siguiendo buenas prácticas.
- Que el modelo **pregunte al desarrollador** en vez de decidir por su cuenta, para:
  - Evitar que el producto se desvíe de la idea MVP
  - Evitar goldplating innecesario (features no pedidas)
  - Evitar alucinaciones (inventar requisitos o tecnologías)
- Un **instalador por consola** que en un solo comando (o pocos pasos) despliegue
  el harness completo en el entorno del desarrollador.

### 1.3 El gap que debemos cerrar

| Lo que tenemos | Lo que necesitamos |
|----------------|-------------------|
| 14 skills acopladas a "repositorio de datos de salud" | Skills generalizadas para web apps, APIs, CLIs, data pipelines, mobile, etc. |
| Skills instalables manualmente copiando archivos `.md` | Instalador CLI (`npx` o `pip install`) que detecta el harness y copia todo |
| Sin reglas "always-on" (el modelo puede ignorar el patrón si no carga la skill) | Reglas permanentes que aseguren que **siempre** pregunta antes de decidir |
| Sin hooks ni persistencia entre sesiones | Hooks que guarden/restauren contexto entre sesiones |
| Sin subagentes especializados | Agentes delegados: planner, architect, code-reviewer, security-reviewer |
| Evaluación manual | Eval harness automatizado que mida calidad del output con/sin skills |

---

## 2. REFERENCIA: ARQUITECTURA DE ECC

ECC (`github.com/affaan-m/ecc`) es la referencia más cercana a lo que necesitamos construir.
Es un "sistema operativo para agentes de IA" que funciona como plugin/config pack para
múltiples harnesses (Claude Code, Cursor, OpenCode, Codex, Gemini, etc.).

### 2.1 Componentes relevantes de ECC a adaptar

```
ECC/
├── .claude-plugin/plugin.json   ← manifiesto para instalación como plugin
├── .opencode/                   ← integración con OpenCode
├── .cursor/                     ← integración con Cursor
├── rules/                       ← ★ Reglas "always-on" (8 archivos en common/)
│   ├── common/
│   │   ├── coding-style.md      ← estilo de código inmutable
│   │   ├── git.md               ← formato de commits, flujo PR
│   │   ├── testing.md           ← TDD obligatorio, 80% cobertura
│   │   ├── security.md          ← chequeos de seguridad pre-commit
│   │   ├── agents.md            ← cuándo delegar a subagentes
│   │   ├── hooks.md             ← eventos del ciclo de vida
│   │   ├── patterns.md          ← patrones de diseño requeridos
│   │   └── performance.md       ← límites de contexto, selección de modelo
│   └── {lenguaje}/              ← reglas específicas por stack
├── skills/                      ← 262 skills de dominio
├── agents/                      ← 64 subagentes especializados
├── hooks/                       ← hooks.json + scripts de ciclo de vida
├── commands/                    ← slash-commands (siendo migrados a skills)
├── contexts/                    ← inyección dinámica según modo (dev/review/research)
├── install.sh / install.ps1     ← ★ Instalador cross-platform
└── package.json                 ← entrada npm
```

### 2.2 Lo que ECC hace bien (y debemos replicar)

1. **Instalación en un comando**: `./install.sh` o `./install.ps1` detecta el harness,
   copia directorios a las ubicaciones correctas, y configura todo.
2. **Reglas "always-on"**: Se inyectan en cada sesión sin que el usuario tenga que
   cargar una skill manualmente. Son el "sistema operativo" del agente.
3. **Hooks de ciclo de vida**: SessionStart (carga contexto previo), SessionEnd
   (guarda resumen), PreCompact (preserva lo importante antes de compactar).
4. **Multi-harness**: Un solo código base funciona en Claude Code, Cursor, OpenCode,
   Gemini, etc. copiando a diferentes directorios.
5. **Puro markdown**: No requiere binarios, compilación ni dependencias pesadas.
   Son plantillas de prompt que el harness del usuario interpreta nativamente.

### 2.3 Lo que NO necesitamos de ECC

- 262 skills (demasiado — empezar con ~20 bien diseñadas)
- 64 subagentes (empezar con 4-5)
- ECC 2.0 en Rust (sobre-ingeniería para MVP)
- Dashboard GUI en Python/Tkinter (fuera de scope)
- Soporte para 10+ harnesses (empezar con 2-3: Claude Code, Cursor, OpenCode)

---

## 3. VISIÓN DEL PRODUCTO: HARNESS CLI

### 3.1 Propuesta de valor

> Un instalador de consola que en un solo comando despliega un harness completo de
> desarrollo asistido por IA, con reglas que garantizan que el modelo **pregunta en vez
> de asumir**, skills generalizadas para múltiples tipos de repositorio, y hooks que
> mantienen continuidad entre sesiones.

### 3.2 Experiencia de usuario objetivo

```bash
# Instalación
npm install -g @vibecoding/harness
vc init

# El instalador detecta el harness activo y pregunta:
# ? Qué harness usas? Claude Code / Cursor / OpenCode / Otro
# ? Qué tipo de proyecto vas a construir? web-app / api / data-pipeline / cli-tool / mobile
# ? Nivel de gobernanza? bajo / medio / alto

# Output:
# ✓ Reglas always-on instaladas en ~/.claude/rules/vibecoding/
# ✓ Skills base instaladas (12 skills)
# ✓ Skills de stack instaladas (web-app: 8 skills adicionales)
# ✓ Hooks configurados
# ✓ Agentes delegados configurados
# ✓ Archivo vibecoding.json creado en el proyecto

# El desarrollador simplemente abre su harness y empieza a trabajar.
# Las reglas always-on garantizan que el modelo preguntará antes de decidir.
```

### 3.3 Alcance del MVP

| Componente | MVP | Futuro |
|-----------|-----|--------|
| **Instalador** | Script PowerShell + Bash que copia directorios | Paquete npm/pip publicado |
| **Harnesses soportados** | Claude Code, OpenCode | Cursor, Gemini, Zed |
| **Reglas always-on** | 4 reglas core | Por lenguaje/stack |
| **Skills** | 12 generalizadas + 3 por tipo de proyecto | Biblioteca completa por dominio |
| **Subagentes** | 3 (planner, reviewer, security) | 6+ especializados |
| **Hooks** | SessionStart, SessionEnd | PreCompact, EvaluateSession |
| **Eval harness** | Script manual | Suite automatizada |

---

## 4. ARQUITECTURA DEL HARNESS

### 4.1 Estructura de directorios del harness

```
vibecoding-harness/
├── install.ps1                    # Instalador Windows
├── install.sh                     # Instalador Unix/Mac
├── package.json                   # Entrada npm (opcional para MVP)
├── README.md                      # Documentación
│
├── rules/                         # ★ REGLAS ALWAYS-ON (inyectadas en cada sesión)
│   ├── common/
│   │   ├── 01_ask_dont_assume.md   # El modelo SIEMPRE pregunta, nunca asume
│   │   ├── 02_mvp_scope.md         # No goldplating, no features no pedidas
│   │   ├── 03_no_hallucinations.md # No inventar librerías, versiones, ni APIs
│   │   └── 04_best_practices.md    # Principios universales (KISS, SOLID, YAGNI)
│   └── stacks/                     # Reglas específicas por lenguaje/framework
│       ├── python.md
│       ├── typescript.md
│       └── go.md
│
├── skills/                         # Skills generalizadas por etapa del pipeline
│   ├── 01_prd.md                   # PRD para cualquier tipo de repo (no solo datos)
│   ├── 02_architecture.md          # Elección de arquitectura (monolito, microservicios, serverless)
│   ├── 03_data_modeling.md         # Modelado de datos (SQL, NoSQL, esquemas)
│   ├── 04_api_design.md            # Diseño de API (REST, GraphQL, gRPC)
│   ├── 05_backend_implementation.md
│   ├── 06_frontend_implementation.md
│   ├── 07_auth_security.md         # Autenticación y autorización generalizada
│   ├── 08_testing_strategy.md      # Estrategia de testing (unit, integration, e2e)
│   ├── 09_ci_cd.md                 # CI/CD pipeline
│   ├── 10_deployment.md            # Deploy (Docker, cloud, on-prem)
│   ├── 11_observability.md         # Logging, métricas, tracing
│   ├── 12_documentation.md         # Generación de documentación
│   └── project_types/              # Skills especializadas por tipo de proyecto
│       ├── web_app.md              # Web app full-stack (React/Vue + API)
│       ├── api.md                  # API pura (sin frontend)
│       ├── data_pipeline.md        # Pipeline ETL / datos
│       ├── cli_tool.md             # Herramienta de línea de comandos
│       └── mobile.md               # App móvil (React Native / Flutter)
│
├── agents/                         # Subagentes delegados
│   ├── planner.md                  # Planificador: descompone features en tareas
│   ├── code_reviewer.md            # Revisor: revisa código contra reglas
│   └── security_reviewer.md        # Seguridad: audita vulnerabilidades
│
├── hooks/                          # Hooks de ciclo de vida
│   ├── hooks.json                  # Configuración de hooks
│   └── scripts/
│       ├── session_start.js        # Carga contexto de sesión anterior
│       └── session_end.js          # Guarda resumen de sesión
│
├── contexts/                       # Contextos dinámicos por modo de trabajo
│   ├── dev.md                      # Modo desarrollo (default)
│   ├── review.md                   # Modo code review
│   └── debug.md                    # Modo debugging
│
└── eval/                           # Eval harness para medir calidad
    ├── test_cases/
    │   ├── case_01_no_context.md    # Caso: prompt sin skills (baseline)
    │   └── case_02_with_skills.md   # Caso: mismo prompt con skills cargadas
    └── metrics.md                   # Métricas: alucinaciones, goldplating, desviación MVP
```

### 4.2 Las 4 reglas "always-on" (el verdadero diferenciador)

Estas reglas se inyectan en **cada sesión** del agente, sin que el usuario tenga que
cargar nada. Son la capa base que garantiza el comportamiento correcto.

#### Regla 1: `01_ask_dont_assume.md`
```
Eres un asistente de desarrollo que SIGUE instrucciones, no las inventa.

REGLAS INQUEBRANTABLES:
1. NUNCA decidas tecnologías, arquitectura, librerías o patrones por tu cuenta.
2. Ante cualquier ambigüedad, PREGUNTA al desarrollador. No asumas.
3. Si el desarrollador dice "no sé", recomienda la opción más común y pide confirmación.
4. NUNCA agregues features, endpoints, tablas o componentes que no hayan sido solicitados.
5. Cada decisión que tomes debe ser trazable a una respuesta explícita del desarrollador.

VIOLACIONES COMUNES A EVITAR:
- "Asumí que querías PostgreSQL" → PREGUNTA: ¿SQL o NoSQL?
- "Agregué un endpoint de health check" → PREGUNTA: ¿Necesitas health checks?
- "Usé bcrypt para passwords" → PREGUNTA: ¿Qué algoritmo de hashing prefieres?
- "Agregué paginación" → PREGUNTA: ¿Necesitas paginación en este endpoint?
- "Puse Docker porque es buena práctica" → PREGUNTA: ¿Necesitas containerización?
```

#### Regla 2: `02_mvp_scope.md`
```
REGLAS DE ALCANCE MVP:
1. Solo implementa lo que el PRD especifica explícitamente.
2. No agregues "buenas prácticas" que no hayan sido solicitadas.
3. No implementes features "por si acaso" o "porque es común".
4. Si una feature toma más de 10% del esfuerzo total y no está en el PRD, es goldplating.
5. Antes de implementar algo no solicitado, PREGUNTA: "¿Quieres que agregue [X]? Toma [Y] esfuerzo extra."
```

#### Regla 3: `03_no_hallucinations.md`
```
REGLAS ANTI-ALUCINACIONES:
1. NUNCA inventes librerías, APIs, versiones o paquetes que no existan.
2. Si no conoces una librería, DILO. No inventes su API.
3. Siempre verifica que las versiones de dependencias sean compatibles entre sí.
4. Si citas documentación, asegúrate de que la fuente existe realmente.
5. No asumas capacidades de librerías — verifica antes de usar.
```

#### Regla 4: `04_best_practices.md`
```
PRINCIPIOS UNIVERSALES (aplica solo lo solicitado):
- KISS: La solución más simple que funcione
- YAGNI: No implementes lo que no se necesita ahora
- SOLID: Aplica solo si el proyecto lo requiere por escala
- DRY: No dupliques, pero no sobre-abstraigas prematuramente
- Testing: Solo el nivel de testing solicitado en el PRD
```

---

## 5. LAS SKILLS GENERALIZADAS

### 5.1 Principios de diseño de cada skill

Cada skill debe seguir este esqueleto obligatorio:

```markdown
---
name: {nombre}
version: 1.0.0
depends_on: [{skills previas}]
stage: {etapa}
project_types: [web_app, api, data_pipeline, cli_tool, mobile]
---

# Skill: {título descriptivo}

## Objetivo
{Qué produce esta skill — una frase}

## Instrucciones
- NO generar código/producto al inicio
- Hacer preguntas por sección
- NO avanzar si falta información
- Al final, generar el entregable y pedir confirmación

## Flujo de interacción
{Secciones numeradas, cada una con preguntas obligatorias}

## Verificación post-generación
- [ ] Checklist de calidad
- [ ] Nada inventado ni asumido

## Condición de cierre
"Voy a generar [el entregable]. ¿Confirmas que la información es correcta?"
```

### 5.2 Las 12 skills base (independientes del tipo de proyecto)

Cada skill formula preguntas quirúrgicas. El modelo no puede avanzar a la siguiente
sección sin respuesta. Esto fuerza el patrón "ask-don't-assume" por diseño.

| # | Skill | Preguntas clave que hace |
|---|-------|------------------------|
| 01 | **PRD** | ¿Problema? ¿Usuarios? ¿Tipo de proyecto? ¿Stack preferido? ¿Restricciones? ¿Gobernanza? |
| 02 | **Arquitectura** | ¿Monolito o microservicios? ¿Serverless? ¿On-prem o cloud? ¿Escala esperada? ¿Presupuesto? |
| 03 | **Modelado de datos** | ¿SQL o NoSQL? ¿Motor específico? ¿Entidades principales? ¿Volumen? ¿Ratio lectura/escritura? |
| 04 | **API Design** | ¿REST, GraphQL o gRPC? ¿Autenticación? ¿Versionamiento? ¿Rate limiting? ¿Documentación (OpenAPI)? |
| 05 | **Backend** | ¿Lenguaje? ¿Framework? ¿ORM? ¿Manejo de errores? ¿Estructura de proyecto? |
| 06 | **Frontend** | ¿Framework? ¿CSS framework? ¿Estados UI (loading/empty/error)? ¿Responsive? ¿Accesibilidad? |
| 07 | **Auth/Security** | ¿JWT, OAuth2, sesiones? ¿Roles? ¿Matriz RACI? ¿Cifrado? ¿Secrets management? |
| 08 | **Testing** | ¿Unit tests? ¿Integration? ¿E2E? ¿Coverage target? ¿Framework de testing? |
| 09 | **CI/CD** | ¿GitHub Actions, GitLab CI, otro? ¿Stages? ¿Linting? ¿Build? ¿Deploy automático? |
| 10 | **Deployment** | ¿Docker? ¿Kubernetes? ¿Cloud provider? ¿Dominio? ¿SSL? ¿Monitoreo? |
| 11 | **Observabilidad** | ¿Logging estructurado? ¿Métricas (Prometheus)? ¿Tracing? ¿Alertas? |
| 12 | **Documentación** | ¿README? ¿API docs? ¿ADR? ¿Diagramas? ¿Wiki? |

### 5.3 Skills por tipo de proyecto (3 adicionales según elección)

Cuando el desarrollador elige `web_app`, `api`, `data_pipeline`, `cli_tool` o `mobile`,
se cargan skills adicionales específicas:

| Tipo | Skills extra |
|------|-------------|
| `web_app` | Frontend avanzado (routing, state management, SEO), Backend for Frontend, Assets/static |
| `api` | Rate limiting, API versioning, Webhooks, SDK generation |
| `data_pipeline` | ETL (fuentes, transformaciones, destino), Validación de datos, Scheduled jobs |
| `cli_tool` | Argument parsing, Config file, Output formatting, Distribution/packaging |
| `mobile` | Offline-first, Push notifications, App store deployment, Native modules |

---

## 6. EL INSTALADOR CLI

### 6.1 Comportamiento deseado

```bash
# Opción A: vía npm (si se publica)
npx @vibecoding/harness init

# Opción B: vía script directo (MVP más rápido)
iwr -Uri "https://raw.githubusercontent.com/.../install.ps1" | iex  # Windows
curl -sSL https://raw.githubusercontent.com/.../install.sh | bash    # Unix
```

El instalador debe:

1. **Detectar el harness activo** buscando directorios conocidos:
   - Claude Code: `~/.claude/` o `%USERPROFILE%\.claude\`
   - Cursor: `.cursor/` en el proyecto
   - OpenCode: `.opencode/` en el proyecto
   - Preguntar si no detecta ninguno

2. **Preguntar tipo de proyecto** para cargar skills específicas:
   ```
   ? Qué tipo de proyecto vas a construir?
   > web-app (full-stack con frontend y backend)
     api (backend puro, sin frontend)
     data-pipeline (ETL, procesamiento de datos)
     cli-tool (herramienta de línea de comandos)
     mobile (app móvil)
   ```

3. **Preguntar nivel de gobernanza:**
   ```
   ? Nivel de gobernanza?
   > bajo — sin auth, sin auditoría, validaciones mínimas
     medio — auth básica, logs, validaciones
     alto — RBAC, auditoría completa, trazabilidad, cumplimiento normativo
   ```

4. **Copiar archivos a las ubicaciones correctas** según el harness detectado.

5. **Crear `vibecoding.json`** en la raíz del proyecto con la configuración.

6. **Mostrar resumen** de lo instalado y próximos pasos.

### 6.2 Archivo de configuración (`vibecoding.json`)

```json
{
  "version": "1.0.0",
  "project": {
    "type": "web_app",
    "governance": "medio",
    "created_at": "2026-06-11"
  },
  "harness": {
    "type": "claude_code",
    "rules_dir": "~/.claude/rules/vibecoding/",
    "skills_dir": "~/.claude/skills/vibecoding/"
  },
  "skills": {
    "base": ["01_prd", "02_architecture", "..."],
    "project_type": ["web_app"],
    "governance_overrides": {
      "07_auth_security": "medio",
      "11_observability": "medio"
    }
  }
}
```

### 6.3 Estructura del script instalador

```
install.ps1 (Windows) / install.sh (Unix):

1. Banner ASCII "VibeCoding Harness"
2. Detectar SO y shell
3. Buscar harnesses instalados (Claude Code, Cursor, OpenCode)
4. Si no detecta → preguntar al usuario
5. Preguntar tipo de proyecto y gobernanza (menú interactivo)
6. Crear directorios destino (~/.claude/rules/vibecoding/, etc.)
7. Copiar rules/common/* → directorio destino
8. Copiar skills base (12) → directorio destino
9. Copiar skills por tipo de proyecto → directorio destino
10. Configurar hooks si el harness lo soporta
11. Crear vibecoding.json en el proyecto actual
12. Mostrar resumen + "Listo. Abre tu harness y empieza a desarrollar."
```

---

## 7. MIGRACIÓN DE LAS 14 SKILLS ACTUALES

Las skills actuales en `docs/skills/` están acopladas al dominio de datos de salud.
Deben generalizarse así:

| Skill actual (dominio salud) | Skill generalizada |
|------------------------------|-------------------|
| `01_prd.md` (contexto normativo HIPAA/Ley 20.584) | `01_prd.md` (pregunta "¿Manejan datos regulados? ¿Qué regulación aplica?") |
| `02_DB schema design.md` (FHIR, pacientes, médicos) | `03_data_modeling.md` (entidades genéricas, pregunta dominio) |
| `03_backend_api_endpoints.md` (endpoints de citas) | `04_api_design.md` (REST/GraphQL/gRPC genérico) |
| `04_backend_pipeline_etl.md` (ETL de datos clínicos) | Parte de `project_types/data_pipeline.md` |
| `05_frontend_ui.md` (formularios médicos) | `06_frontend_implementation.md` (3 estados UI genéricos) |
| `06_data_reporting.md` (KPI clínicos) | Se integra en `project_types/data_pipeline.md` |
| `07_auth_security.md` (RBAC con RACI) | `07_auth_security.md` (se mantiene, ya tiene RACI genérico) |
| `08_persistence_and_orm.md` (SQLAlchemy + soft-delete) | `05_backend_implementation.md` (ORM agnóstico al stack) |
| `09_docker_deployment.md` | `10_deployment.md` |
| `10_backend_testing.md` | `08_testing_strategy.md` |
| `11_contexto.md` | Se integra como `contexts/dev.md` |
| `12_frontend_testing.md` | Parte de `08_testing_strategy.md` |
| `13_observability.md` | `11_observability.md` (ya es genérica) |
| `14_input_validation_patterns.md` | Parte de `project_types/data_pipeline.md` o `web_app.md` |

---

## 8. PLAN DE IMPLEMENTACIÓN (LO QUE FABLE 5 DEBE GENERAR)

### Fase 1: Estructura base del harness (día 1-2)

- [x] Crear estructura de directorios del harness
- [x] Escribir las 4 reglas always-on (`rules/common/`)
- [x] Escribir `hooks/hooks.json` con SessionStart/SessionEnd
- [x] Crear `package.json` con metadata

### Fase 2: Skills base generalizadas (día 3-5)

- [x] Reescribir las 12 skills base usando el esqueleto estándar
- [x] Cada skill debe incluir frontmatter YAML, preguntas por sección, checklist
- [x] Garantizar que ninguna skill asume stack o dominio

### Fase 3: Skills por tipo de proyecto (día 6-7)

- [x] Crear 5 skills de project_types (web_app, api, data_pipeline, cli_tool, mobile)
- [x] Cada una hereda el patrón ask-don't-assume

### Fase 4: Subagentes delegados (día 8)

- [x] `agents/planner.md` — descompone tareas del PRD
- [x] `agents/code_reviewer.md` — revisa código contra las 4 reglas
- [x] `agents/security_reviewer.md` — audita OWASP Top 10

### Fase 5: Instalador CLI (día 9-10)

- [x] `install.ps1` para Windows con detección de harness
- [x] `install.sh` para Unix/Mac
- [x] Menú interactivo (tipo proyecto, gobernanza)
- [x] Generación de `vibecoding.json`

### Fase 6: Eval harness (día 11-12)

- [x] Script que compara output del modelo con skills vs sin skills
- [x] Métricas: alucinaciones, goldplating, desviación del PRD
- [x] Reporte automatizado

---

## 9. RESTRICCIONES PARA LA GENERACIÓN

1. **Cero alucinaciones**: No inventar librerías, APIs, comandos o herramientas que no existan.
2. **Puro markdown + scripts**: El harness son archivos `.md` + scripts `.sh`/`.ps1`. No requiere compilación.
3. **Idioma**: Todo el contenido de las skills en **español** (el público objetivo es hispanohablante).
4. **Generalización real**: Si una skill menciona "paciente", "médico", "RUT" o "ficha clínica",
   está MAL. Debe hablar de "entidad", "usuario", "identificador" y "registro".
5. **El patrón ask-don't-assume es INQUEBRANTABLE**: Cada skill debe forzar preguntas antes
   de generar. Si el modelo puede generar sin preguntar, la skill está mal diseñada.
6. **No goldplating**: El MVP del harness no necesita 262 skills ni 64 agentes. 12 skills base
   + 3-5 por tipo de proyecto + 3 agentes es suficiente para demostrar valor.

---

## 10. PREGUNTAS PARA FABLE 5 (LO QUE NECESITAMOS QUE GENERE)

Con este contexto, necesitamos que generes:

1. **Los 4 archivos de reglas always-on** (`rules/common/*.md`) — el core del harness
2. **Las 12 skills base generalizadas** (`skills/01_prd.md` a `skills/12_documentation.md`)
3. **3 skills de tipo de proyecto** (web_app, api, data_pipeline) como ejemplo
4. **3 agentes delegados** (`planner.md`, `code_reviewer.md`, `security_reviewer.md`)
5. **El instalador** (`install.ps1` + `install.sh`)
6. **El esqueleto del eval harness** (`eval/metrics.md` + caso de prueba)

¿Por dónde quieres que empecemos? Te sugiero:

- **Opción A**: Generar todo de una vez (más código, menos interacción)
- **Opción B**: Iterar skill por skill, revisando cada una antes de avanzar (más control)
- **Opción C**: Empezar con las 4 reglas always-on + el instalador, y luego las skills
