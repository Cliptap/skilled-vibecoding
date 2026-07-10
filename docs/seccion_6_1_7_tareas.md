# 6.1.7 Anexo: Descripción de las Tareas del Experimento

> Las métricas de la Tabla 6.3.1 se reportan como T01, T02 y T03. Este
> anexo documenta a qué tarea concreta corresponde cada identificador
> y por qué se eligieron esas tres.

## Justificación de la selección

Las tres tareas se eligieron para cubrir **tres niveles de granularidad
y complejidad** dentro del dominio del proyecto (gestión clínica con
FastAPI + SQLAlchemy):

| Tarea | Granularidad | Tipo de código | Dominio |
|---|---|---|---|
| T01 | Módulo aislado | Función pura con regex y aritmética | Validación de identidad |
| T02 | Módulo + integración | Endpoint REST con 7 query params, RBAC, paginación, soft-delete | API transaccional |
| T03 | Función pura | Normalización Unicode (NFC, partículas lingüísticas) | Saneamiento de input |

Las tres comparten: (a) dominio clínico real (no son "Fibonacci" o
tareas benchmark genéricas), (b) restricciones explícitas escritas en
la spec (listas de criterios de aceptación y de "NO hacer"), (c)
dependencias solo de stdlib o de librerías ya presentes en
`requirements.txt` (evita forzar al LLM a instalar paquetes durante
la corrida). Las tres difieren en la cantidad de archivos del repo
que el LLM debe leer para producir una solución correcta: T01 no
requiere leer nada del repo, T02 requiere leer modelos ORM y
dependencias de auth, T03 no requiere leer nada.

## T01 — Validador de RUT chileno

**Path:** `harness/eval/tasks/task_01_rut_validator.md`

**Requisito:** implementar un módulo `app/utils/rut_validator.py` que
exporte dos funciones: `normalize_rut(raw: str) -> str` (canoniza
formato `"12.345.678-K"`, `"12345678k"`, `" 12345678-k "` a
`"12345678K"`) e `is_valid_rut(rut: str) -> bool` (valida
sintaxis + dígito verificador módulo-11 sin lanzar excepciones).

**Criterios de aceptación documentados:** 9 asserts en el archivo de
tarea, cubriendo RUTs válidos, inválidos, vacíos, None, strings no
numéricos, y formatos no canónicos.

**Complejidad algorítmica:** O(n) sobre el largo del string.

**Por qué se eligió:** es una tarea clásica del dominio chileno,
tiene especificación algorítmica precisa y verificable, no requiere
conocer el resto del proyecto, y permite medir el efecto del harness
sobre código algorítmico puro (sin branching complejo).

## T02 — Endpoint GET /appointments con filtros

**Path:** `harness/eval/tasks/task_02_appointments_endpoint.md`

**Requisito:** agregar un endpoint `GET /api/v1/appointments` en
`src/backend/api/appointments.py` que liste citas con 7 query params
(`patient_id`, `practitioner_id`, `date_from`, `date_to`, `status`,
`limit`, `offset`), respete soft-delete, ordene por `scheduled_at`,
requiera JWT, e implemente RBAC (admin ve todo, médico solo citas
propias, recepcionista solo citas de su practitioner).

**Criterios de aceptación documentados:** 6 criterios verificables
(OpenAPI en /docs, validación de limit y status con 422, sin token
401, con receptionist pidiendo citas ajenas 403 o lista vacía
según decisión documentada, test unitario de filtrado por rango
de fechas).

**Complejidad algorítmica:** O(n log n) por el ORDER BY; O(1) en
memoria para queries simples.

**Por qué se eligió:** es la tarea de mayor superficie del
experimento, obliga al LLM a leer 3-4 archivos del repo (modelos
ORM, dependencias de auth, schemas existentes), y permite medir
el efecto del harness cuando la tarea es estructuralmente
compleja. Es el caso donde se espera mayor divergencia entre
modos.

## T03 — Sanitizador de nombres propios

**Path:** `harness/eval/tasks/task_03_name_normalizer.md`

**Requisito:** implementar una función `normalize_person_name(raw:
str) -> str` en `app/utils/text_normalizer.py` que aplique 7
reglas en orden específico: (1) None/no-str → "", (2) eliminar
caracteres de control Unicode Cc/Cf, (3) normalizar a NFC, (4)
colapsar whitespace, (5) trim, (6) si vacío → "", (7) Title Case
preservando partículas (`de`, `del`, `la`, `las`, `los`, `y`, `e`).

**Criterios de aceptación documentados:** 9 asserts cubriendo None,
no-str, vacío, caracteres de control, NFD vs NFC, partículas
lingüísticas en diferentes posiciones.

**Complejidad algorítmica:** O(n) sobre el largo del string.

**Por qué se eligió:** es una función pura algorítmica (como T01)
pero con detalle Unicode (no trivial como T01). Permite medir
el efecto del harness sobre tareas donde el código está bien
especificado y la divergencia entre modos debería ser
principalmente de estilo, no de cobertura.

## Por qué no se incluyeron más tareas

Tres consideraciones limitaron la expansión del dataset:

1. **Costo.** Cada corrida cuesta entre $0.03 y $0.21 USD. Con 5
   tareas x 2 modos = 10 corridas, el costo total ascendería a
   ~$1.00 USD, lo cual excede el presupuesto asignado para la
   experimentación.

2. **Tiempo.** Cada corrida tarda entre 1.5 y 8 minutos. Con 10
   corridas secuenciales, el experimento tomaría 1-1.5 horas,
   más el tiempo de debugging entre corridas.

3. **Estabilidad del modelo.** El modelo `opencode-go/minimax-m3`
   presenta variabilidad de output entre invocaciones
   (mismo prompt, misma temperatura, puede dar respuestas
   distintas). Con 3 tareas, el ruido se promedia; con 5
   tareas, podría dominar. **Antes de expandir la muestra, se
   recomienda correr las 3 tareas 3 veces cada una** (3 x 3 x 2
   = 18 corridas) para estimar la variabilidad intra-condición
   y luego decidir si extender el dataset.

## Identificadores vs nombres de archivo

Para referencia rápida durante la revisión de artefactos:

| ID | Path de la tarea | Archivo generado típico (modo libre) | Archivo generado típico (modo con skills) |
|---|---|---|---|
| T01 | `harness/eval/tasks/task_01_rut_validator.md` | `app/utils/rut_validator.py` | `app/utils/rut_validator.py` + `_test_rut.py` |
| T02 | `harness/eval/tasks/task_02_appointments_endpoint.md` | `src/backend/api/appointments.py` + `schemas.py` + `tests/unit/test_appointments.py` | `src/backend/api/appointments.py` + `tests/unit/test_appointments.py` |
| T03 | `harness/eval/tasks/task_03_name_normalizer.md` | `app/utils/text_normalizer.py` + 2 `__init__.py` | `app/utils/text_normalizer.py` |
