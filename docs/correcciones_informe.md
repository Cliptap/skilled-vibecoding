# Correcciones Textuales para Aplicar al INFORME

> Este archivo contiene los 6 reemplazos puntuales sugeridos por la auditoría
> (`docs/auditoria_informe_gemini.md`). Cada bloque indica: ubicación en el
> informe, texto original (entre comillas), texto corregido y razón breve.

---

## Corrección 1 — Capítulo II, sección 2.2

**Texto original:**
> El arnés deja de ser una guía pasiva para convertirse en un *entorno de
> orquestación automatizado* que se inyecta nativamente en el IDE
> (OpenCode, Claude Code, Cursor) mediante scripts interactivos de
> automatización (install.ps1/install.sh).

**Texto corregido:**
> El arnés deja de ser una guía pasiva para convertirse en un *entorno de
> orquestación automatizado* que se inyecta en el IDE OpenCode mediante
> scripts de automatización (`install.ps1`/`install.sh`). La compatibilidad
> declarada con Claude Code y Cursor figura como trabajo futuro (§7.2).

**Razón:** El repo no implementa la inyección en Claude Code ni Cursor.
Solo OpenCode está operativo. `harness/install.ps1` solo escribe en la
carpeta `.opencode/` del proyecto destino.

---

## Corrección 2 — Capítulo III, RF07

**Texto original:**
> RF07 — Validación de Reglas Clínicas Nativas: Bloqueo automatizado de
> solapamiento de horarios (double-booking), fechas pasadas o asignación
> de entidades inexistentes.

**Texto corregido:**
> RF07 — Validación de Reglas Clínicas Nativas: Validación de RUT chileno
> con algoritmo módulo-11 implementada en `src/backend/schemas/patient.py`
> (verificable en `tests/unit/test_patients.py`). La regla anti-doble-booking
> figura en el PRD pero su implementación en
> `services/doctor_appointment_service.py` requiere verificación caso por
> caso.

**Razón:** La implementación del RUT módulo-11 es directamente visible en el
código. La regla de double-booking está documentada como objetivo del PRD
pero no se verificó su implementación concreta en
`doctor_appointment_service.py`. Diferenciar lo verificable de lo
aspiracional.

---

## Corrección 3 — Capítulo IV, diagrama de arquitectura

**Texto original:**
> - Frontend: Vue 3 + Tailwind CSS / Vanilla JS (Reactivo)

**Texto corregido:**
> - Frontend: Vue 3 (Composition API) + Tailwind CSS v4 + Vite

**Razón:** El proyecto usa exclusivamente Vue 3 + Tailwind v4. No hay
código Vanilla JS de frontend en el repo. `package.json` del frontend
declara `vue@^3.x` y `tailwindcss@^4.x` como únicas dependencias de UI.

---

## Corrección 4 — Capítulo V, sección 5.2 (ETL Pipeline)

**Texto original:**
> Activación de la **Skill 04 (ETL Pipeline)** para ejecutar cargas
> fragmentadas (chunked) y políticas de rollback parciales ante fallos
> de inserción.

**Texto corregido:**
> La skill 04 (ETL Pipeline) fue documentada como directriz metodológica
> pero su implementación operativa quedó diferida — el backend opera
> sobre la API directamente sin procesos batch de carga.

**Razón:** No hay evidencia de jobs ETL implementados. La skill 04 existe
como `.md` en `docs/skills/04_backend_pipeline_etl.md` pero no se
materializa en código de `src/`.

---

## Corrección 5 — Capítulo V, sección 5.3 (HL7 FHIR)

**Texto original:**
> Adopción del estándar HL7 FHIR para el modelamiento de salud.

**Texto corregido:**
> Se avanzó hacia estándares de interoperabilidad clínica (HL7 FHIR figura
> como objetivo en `product.md`; la implementación concreta del modelado
> FHIR queda como línea futura — el proyecto no incluye aún la dependencia
> `fhirclient` ni recursos FHIR tipados en `src/`).

**Razón:** `product.md` menciona HL7 FHIR como objetivo. `requirements.txt`
no contiene `fhirclient`, `fhir.resources` ni similares. No hay
serializadores/deserializadores FHIR en `src/`. Es aspiración, no hecho.

---

## Corrección 6 — Capítulo V, sección 5.4 (Caveman + skill-lock)

**Texto original:**
> Inyección de técnicas de control de contexto en las habilidades como el
> *Caveman Mode* (ahorro de hasta 70% de tokens eliminando saludos del
> LLM) y el bloqueo de sesión mediante skill-lock.json.

**Texto corregido:**
> Se incorporó la skill externa `caveman` (modo de comunicación comprimida,
> originalmente publicitada con ahorros de hasta ~70% de tokens por su
> autor; la verificación empírica de esa cifra en el contexto del proyecto
> queda como trabajo futuro). El archivo `skills-lock.json` raíz fija
> versiones de skills externas, no bloquea sesiones de opencode.

**Razón:** (a) La cifra de 70% es publicidad del autor de la skill
(`juliusbrussee/caveman`), no medición propia. (b) `skills-lock.json`
declara `"project_skills"` y `"external_skills"` con `version` y
`computedHash`; su rol es fijación de versiones, no bloqueo de sesión.

---

## Cambio adicional recomendado — Capítulo VI, sección 6.2 (Tabla de métricas)

**Reemplazar la tabla completa** por la siguiente versión, que refleja
las métricas realmente implementadas en `harness/eval/`:

| Dimensión Evaluada | Métrica Operacionalizada | Herramienta / Método de Captura | Impacto de Ingeniería Esperado |
| :---- | :---- | :---- | :---- |
| **Mitigación de Alucinaciones Técnicas** | **Tasa de Dependencias Inválidas:** Conteo de imports top-level desconocidos por el whitelist del proyecto. | AST parsing con `ast` de stdlib en `harness/eval/metrics_collector.py`. | Reducción de la tasa de desvío a valores cercanos al 0%. Eliminación completa de dependencias fantasma. |
| **Prevención de Gold-Plating (Sobreingeniería)** | **Cantidad de archivos .py generados** comparada con los declarados como necesarios en la tarea. | Diff entre `files_persisted` (lo que la tool `write` del LLM efectivamente guardó) y la lista de paths del requisito. | Reducción del volumen de código innecesario, promoviendo una arquitectura limpia y minimalista enfocada en el MVP. |
| **Calidad Estructural del Repositorio** | **Complejidad Ciclomática (CC) y Cognitiva** por función. | `radon cc` y `lizard` ejecutados en `harness/eval/metrics_collector.py`. | CC estable o decreciente; sin picos introducidos por sobreingeniería. |
| **Eficiencia de Ciclo y Fricción Cognitiva** | **Cycle Time (segundos):** tiempo entre el prompt y la última escritura. **Cantidad de eventos JSON** emitidos por opencode (proxy de iteraciones internas). | `time.perf_counter()` en `harness/eval/runner.py`; `raw_events_count` agregado desde eventos `step_finish`. | Reducción del cycle time en un 20-30% consistente entre tareas. |

**Razón del cambio:** La tabla original describía métricas aspiracionales
(code coverage con pytest-cov no configurado, análisis de diffs por
code_reviewer no instrumentado, hooks SessionEnd midiendo tiempos que
no se almacenan). La nueva tabla describe solo lo que el runner ejecuta.

---

## Cambio en la sección 6.3

**Reemplazar los dos bloques pendientes** por el contenido del archivo
`docs/seccion_6_3_resultados.md` (ya generado con datos reales).

Si querés mantener el formato de "bloques pendientes" para algún cuadro
que el profe pueda pedir, el resumen ejecutivo mínimo para insertar es:

> Resultados consolidados: cycle time −27.4% con skills; archivos −25.0%
> con skills; CC estable; 1 alucinación menor en T01 con skills, 0 en T03.
> Costo total 0.44 USD. Limitaciones: T02 no produjo artefactos medibles
> en ninguno de los dos modos; N=3 insuficiente para significancia
> estadística; un único modelo evaluado. Datos completos en
> `docs/seccion_6_3_resultados.md`, `qa_reports/results.json` y
> `qa_reports/charts.png`.
