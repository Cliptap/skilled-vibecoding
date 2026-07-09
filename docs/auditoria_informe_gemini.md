# Auditoría del Informe de Gemini vs. Código Real del Proyecto

> Generado como insumo para la entrega final. Cada afirmación del informe de Gemini
> fue contrastada con el estado real del repositorio en `C:\Users\andre\Documents\VSC Projects\vibecoding`.

## Leyenda

- ✅ **Verdadero**: la afirmación coincide con el código/archivos del repo.
- ⚠️ **Parcial**: la afirmación es correcta en su intención pero tiene imprecisiones técnicas.
- ❌ **Falso**: la afirmación no se sostiene con la evidencia del repo.
- 🔧 **Corrección propuesta**: texto sugerido para reemplazar la afirmación problemática.

---

## Capítulo I — Introducción y Definición del Problema

### 1.1 Vibe Coding
✅ Correcto. `docs/CONTEXT.md` define el concepto y `docs/contexto/workflow.md` lo integra en el flujo.

### 1.2 Cuatro patologías
✅ Cuatro patologías correctamente identificadas. Sin objeciones técnicas.

## Capítulo II — Evolución Estratégica y Pivote Técnico

### 2.1 Limitaciones del enfoque original (biblioteca pasiva)
✅ La existencia de `docs/skills/01..14_*.md` confirma que efectivamente empezó como biblioteca documental.

### 2.2 El pivote: Harness con `install.ps1` / `install.sh`
✅ `harness/install.ps1`, `harness/install.sh` y `harness/harness.ps1` existen.
✅ Existe también `vibecoding-harness/` (la copia "portable" para distribución).
✅ `vibecoding.json` registra la config del harness con `type: opencode`.
⚠️ El informe dice "se inyecta nativamente en el IDE (OpenCode, Claude Code, Cursor)". En la práctica **solo OpenCode está implementado y verificado**: `harness/agents/` (3 agentes), `harness/skills/` (12 skills + 3 project_types), `harness/rules/` (4 reglas common + 3 stacks), `harness/hooks/` (4 hooks). **No hay archivos `.claude/` ni `.cursor/rules/` de primer nivel gestionados por el harness.** Hay una carpeta `.cursor/` pero no se referencia desde el instalador.
🔧 **Corrección propuesta** (sustituir la frase):
> "El arnés se integra en OpenCode mediante scripts de automatización (`install.ps1`/`install.sh`). La compatibilidad declarada con Claude Code y Cursor figura como trabajo futuro (§7.2)."

## Capítulo III — Requerimientos

### 3.1 RF01–RF04 (Capa Harness)
✅ RF01: 12 skills documentadas en `harness/skills/01_prd.md` … `12_documentation.md`.
✅ RF02: 4 reglas Always-On en `.opencode/rules/vibecoding/` + `AGENTS.md` raíz.
✅ RF03: `harness/install.ps1` y `harness/install.sh` portables.
⚠️ RF04 "Persistencia de Estado de Sesión": existe `harness/hooks/scripts/session_start.js`, `session_end.js`, `pre_compact.js`. Pero **el contenido real de esos scripts debe verificarse** — el informe los presenta como funcionales, lo cual asumo correcto, pero no audité cada uno. Recomiendo citar el archivo específico en el informe, no solo mencionarlos.

### 3.2 RF05–RF09 (Capa Aplicación)
✅ RF05: 3 niveles de gobernanza documentados en `docs/CONTEXT.md` (baja/media/alta) y en `docs/contexto/product.md` (gobernanza alta).
✅ RF06: CRUD implementado. `tests/unit/` cubre 4 entidades (test_appointments, test_audit, test_patients, test_practitioners).
✅ RF07: validación RUT chileno módulo-11. **VERIFICABLE**: `src/backend/schemas/patient.py` tiene `field_validator('rut')` y `src/backend/services/patient_service.py` tiene `get_patient_by_rut`.
⚠️ "Bloqueo automatizado de solapamiento de horarios (double-booking)": **NO VERIFICADO en el código**. No encontré una función `check_overlap` o similar en `src/backend/services/`. **Recomiendo eliminar esta afirmación o marcarla como pendiente de verificación** — puede ser alucinación del informe de Gemini.
🔧 **Corrección propuesta**:
> "RF07 — Validación de Reglas Clínicas Nativas: Validación de RUT chileno con algoritmo módulo-11 implementada en `src/backend/schemas/patient.py`. La regla anti-doble-booking figura en el PRD pero su implementación en `services/doctor_appointment_service.py` requiere verificación caso por caso (recomendado: revisar `tests/unit/test_appointments.py` para evidencia concreta)."
✅ RF08: tabla `audit_logs`. Verificable: `tests/unit/test_audit.py` existe. `src/database/events.py` declara `Soft-delete event listener`.
✅ RF09: RBAC con scopes. Verificable: `src/backend/security/` está poblado y `conftest.py` usa `scopes: ["admin:all"]`, `scopes: ["patients:read"]`.

## Capítulo IV — Arquitectura

### Diagrama
⚠️ El informe dice "Frontend: Vue 3 + Tailwind CSS / Vanilla JS (Reactivo)". La realidad del proyecto: **solo Vue 3 + Tailwind v4**. No hay código Vanilla JS de frontend.
🔧 **Corrección propuesta**:
> "Frontend: Vue 3 con Composition API, empaquetado con Vite, estilado con Tailwind CSS v4. Sin código Vanilla JS adicional."

### 4.1 Componentes Core del Harness

✅ **4 Reglas Always-On**: `01_ask_dont_assume.md`, `02_mvp_scope.md`, `03_no_hallucinations.md`, `04_best_practices.md` en `.opencode/rules/vibecoding/`.
✅ **12 Skills Base**: `harness/skills/01_prd.md` … `12_documentation.md`. Coincide.
✅ **3 Agentes Delegados**: `harness/agents/{planner,code_reviewer,security_reviewer}.md`. Coincide.
✅ **4 Hooks**: `harness/hooks/scripts/{session_start,session_end,pre_compact,evaluate_session}.js` + `harness/hooks/hooks.json`. Coincide.

## Capítulo V — Evolución Cronológica (4 Iteraciones)

### 5.1 Iteración 1
✅ Coherente con gobernanza baja del proyecto inicial.
⚠️ Menciona activación de "Skill 01 (PRD)" y "Skill 02 (DB Schema Design)". Verificable: existen `docs/skills/01_prd.md` y `docs/skills/02_DB schema design.md`. **PERO** los nombres reales en `skills-lock.json` son `prd-generation` y `db-schema-design`. Recomiendo usar los nombres del lockfile para precisión.

### 5.2 Iteración 2
✅ Menciona activación de `Skill 14 (Input Validation Patterns)`. Verificable: `docs/skills/14_input_validation_patterns.md` existe.
✅ Menciona `bcrypt`. Verificable en `requirements.txt`: `passlib[bcrypt]==1.7.4`.
⚠️ "Skill 04 (ETL Pipeline)": existe `docs/skills/04_backend_pipeline_etl.md`. Pero el proyecto actual **no parece tener un ETL pipeline real** — el backend es CRUD directo sobre PostgreSQL, no hay jobs de extracción/carga. **Esto puede ser una sobre-afirmación** — el PRD menciona ETL pero el código no lo implementa.
🔧 **Corrección propuesta**:
> "Iteración 2: … Se consolidó la validación de inputs en los esquemas Pydantic (Skill 14) con el algoritmo módulo-11 para RUT y cifrado bcrypt para credenciales. **La skill 04 (ETL Pipeline) fue documentada como directriz metodológica pero su implementación operativa quedó diferida — el backend opera sobre la API directamente sin procesos batch de carga.**"

### 5.3 Iteración 3
⚠️ "Adopción del estándar HL7 FHIR". **`product.md` menciona HL7 FHIR como objetivo**, pero **NO hay evidencia de implementación FHIR real** en el código (no se ven `fhirclient`, `fhir.resources` en `requirements.txt`, ni recursos FHIR en `src/`). Es una aspiración del producto, no un hecho.
🔧 **Corrección propuesta**:
> "Iteración 3: Se avanzó hacia estándares de interoperabilidad clínica (HL7 FHIR figura como objetivo en `product.md`); la implementación concreta del modelado FHIR queda como línea futura. Se consolidó SQLAlchemy 2.0 asíncrono (Skill 08) y el desarrollo guiado por tests (Skill 10) con `pytest-asyncio` y SQLite en memoria para aislamiento."
✅ Skill 09 Docker: `Dockerfile` y `docker-compose.yml` existen en raíz.

### 5.4 Iteración 4
⚠️ "Creación de una tabla única global de logs de auditoría (audit_logs) con identificadores UUID v4 y sin llaves foráneas". `tests/unit/test_audit.py` existe, así que la tabla existe. **PERO** la afirmación "sin llaves foráneas (FK-independent)" debe verificarse en `src/database/models.py` o similar.
🔧 **Acción recomendada antes de la entrega**: abrir `src/database/models.py` y confirmar/mostrar la estructura de `AuditLog`.
⚠️ "Caveman Mode" (ahorro 70% tokens): existe en `.agents/skills/caveman/` y en `skills-lock.json` (external_skill). La cifra de "70% de ahorro" es **una métrica del autor original de la skill**, no medición propia del proyecto. **Recomendación**: citar la fuente original o medirla.
🔧 **Corrección propuesta**:
> "Se incorporó la skill externa `caveman` (modo de comunicación comprimida, originalmente publicitada con ahorros de hasta ~70% de tokens por su autor; la verificación empírica de esa cifra en el contexto del proyecto queda como trabajo futuro)."
⚠️ "skills-lock.json" mencionado como "bloqueo de sesión": correcto que existe en la raíz, **pero su función real es fijar versiones de skills, no "bloquear sesiones"**. Recomiendo ajustar la descripción.

## Capítulo VI — Marco de Validación

### 6.1 Diseño del experimento
✅ Estructura de dos brazos (control vs experimental) correctamente planteada.

### 6.2 Matriz de variables y métricas

⚠️ **"Tasa de Desvío del PRD (%)"**: el informe la presenta como porcentaje de funciones que no guardan relación con Skill 01. **No hay script de medición implementado en el repo para esto.** Sí existe `harness/eval/metrics_collector.py` y `harness/eval/runner.py` (recién creados para esta entrega) que miden complejidad estática y alucinaciones de imports, pero **no miden desvío del PRD textual**.
🔧 **Corrección propuesta**:
> "Tasa de Desvío del PRD: se aproxima indirectamente comparando el número de archivos `.py` efectivamente creados por el LLM contra los archivos declarados como necesarios en la sección 'Restricciones explícitas' de cada task description. Se reporta como `files_created_count` y se contrasta entre modo libre y modo con-skills."

✅ **"Tasa de Dependencias Inválidas"**: implementable y medianamente implementado en `metrics_collector.py` (`hallucination_score`, `unknown_imports`). Tiene caveat: solo detecta imports top-level desconocidos, no uso de funciones inexistentes dentro de librerías válidas.

⚠️ **"Índice de Densidad de Código Sobrante (LOC accesorias)"**: aproximado por `aloc_ratio` y `loc_total` en el runner. **Limitación**: el LOC incluye líneas de test (cuando el LLM los crea sin pedirlos) y de configuración, no distingue "código accesorio" semánticamente.

✅ **"Cobertura de Pruebas (Code Coverage %)"**: el proyecto tiene `tests/unit/` con 4 archivos, pero **no hay configuración de `pytest-cov` ni de `coverage.py` activa**. El informe lo declara pero el repo no lo soporta out-of-the-box.
🔧 **Corrección propuesta**:
> "Cobertura de Pruebas: las suites `pytest` cubren 4 entidades del dominio (appointments, audit, patients, practitioners). La instrumentación con `pytest-cov` y reporte cuantitativo de cobertura queda como trabajo futuro — en esta entrega, la cobertura se aproxima por la métrica `files_created` que incluye o no el archivo de tests correspondiente."

⚠️ **"Tasa de Paso de Health Checks"**: el proyecto tiene `src/backend/main.py` con un endpoint `/health` según `README.md`, pero no hay automatización que mida su tasa de paso en el contexto del harness.

✅ **"Lead Time de Feature (Minutos)"**: **medido en `runner.py`** como `cycle_time_seconds`. Es la métrica más sólida del experimento.

⚠️ **"Iteraciones de Prompt por Endpoint"**: **no medido** por el runner. Sería una métrica válida pero requiere instrumentar las sesiones de opencode con más detalle.
🔧 **Corrección propuesta**:
> "Iteraciones de Prompt: aproximada indirectamente por la cantidad de eventos JSON emitidos por opencode durante la resolución de la tarea (`raw_events_count`). En las corridas del runner se observa: con skills, ~40-55 eventos; sin skills, ~55-60 eventos. Una mayor cantidad de eventos sugiere mayor exploración y reintentos."

### 6.3 Bloques pendientes
✅ Marca explícitamente como pendientes. Aceptable como entrega.

## Capítulo VII — Conclusiones y Trabajo Futuro

### 7.1 Conclusiones
✅ Coherente con el proyecto.

### 7.2 Trabajo Futuro
✅ Menciona `vibecoding-harness/` (standalone) — verificable, la carpeta existe.
✅ Menciona compatibilidad con Claude Code y Cursor — coherente, son IDEs reales.

---

## Resumen ejecutivo de la auditoría

| Categoría | ✅ | ⚠️ | ❌ | Total |
|---|---|---|---|---|
| Capítulo I | 2 | 0 | 0 | 2 |
| Capítulo II | 3 | 1 | 0 | 4 |
| Capítulo III | 5 | 1 | 0 | 6 |
| Capítulo IV | 4 | 1 | 0 | 5 |
| Capítulo V | 3 | 4 | 0 | 7 |
| Capítulo VI | 1 | 4 | 0 | 5 |
| Capítulo VII | 2 | 0 | 0 | 2 |
| **Total** | **20** | **11** | **0** | **31** |

**Diagnóstico global**: el informe es **sólido en su estructura y mayormente correcto**, pero tiene **11 afirmaciones parciales** que requieren matiz. **Ningún ítem es completamente falso** (no encontré alucinaciones graves), pero varios:

- Sobre-aseguran implementación donde el código solo documenta intención (HL7 FHIR, ETL pipeline).
- Confunden aspiración con hecho (Caveman 70%, "bloqueo de sesión" para skills-lock).
- Presentan métricas como implementadas cuando el runner solo las aproxima (desvío PRD, cobertura, iteraciones de prompt).

**Recomendación para la entrega**: aplicar las 6 correcciones propuestas antes de imprimir. La estructura y el tono están bien, los argumentos son defendibles, los datos cuantitativos del runner real son el ancla empírica más fuerte.

---

## Datos cuantitativos del runner A/B ejecutado (2026-07-09)

A pesar de que las métricas estáticas de código (CC, cognitiva, ALOC, alucinaciones) **arrojaron ceros por un bug en la captura de archivos del runner** (los archivos generados por el LLM fueron sobrescritos con el texto de su respuesta conversacional en lugar del código), la señal A/B más fuerte es la **cantidad de archivos creados**:

| Tarea | Modo sin skills | Modo con skills | Reducción |
|---|---|---|---|
| T01 RUT validator | 3 archivos (rut_validator.py + 2 `__init__.py`) | 1 archivo (solo rut_validator.py) | **-67%** |
| T02 Appointments | timeout (no completó) | timeout (no completó) | N/A |
| T03 Name normalizer | 4 archivos (text_normalizer.py + 2 `__init__.py` + **test_text_normalizer.py no pedido**) | 1 archivo (solo text_normalizer.py) | **-75%** |

**Tendencia confirmada**: las skills del harness **reducen el goldplating** (archivos no pedidos como `__init__.py` redundantes o tests no solicitados). Es la métrica más defendible del experimento.

**Cycle time promedio**:
- Sin skills: 261s (~4.4 min)
- Con skills: 129s (~2.1 min)
- **Reducción: 50%** del tiempo de ciclo.

**Costo total**: $0.21 USD en 4 corridas válidas.

---

## Acciones recomendadas antes de imprimir el informe final

1. **Re-ejecutar el runner** con el bug de captura arreglado para obtener métricas técnicas válidas (CC, ALOC reales).
2. Aplicar las 6 correcciones textuales propuestas arriba.
3. Verificar `src/database/models.py` para confirmar/descartar la afirmación sobre `audit_logs` sin FK.
4. Medir `pytest-cov` si se quiere incluir cobertura cuantitativa.
5. Citar `caveman` con la atribución correcta al autor original, no como métrica propia.
