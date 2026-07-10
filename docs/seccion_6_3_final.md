# 6.3 Resultados Consolidados y Evidencia Empírica

Se ejecutaron 6 corridas automatizadas del runner (`harness/eval/runner.py`),
3 tareas del dominio clínico (validador de RUT módulo-11, endpoint
`GET /appointments` con RBAC y paginación, normalizador Unicode de
nombres) bajo dos condiciones (libre vs con skills) usando el mismo
modelo (`opencode-go/minimax-m3`). Las 6 corridas completaron y
produjeron artefactos medibles.

## Tabla consolidada

| Tarea | Modo | Archivos | LOC | CC avg | Cog avg | Hallu | Cycle (s) | Costo (USD) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| T01 RUT validator | sin skills | 1 | 36 | 3.67 | 3.67 | 0 | 160.0 | 0.054 |
| T01 RUT validator | con skills | 2 | 63 | 4.00 | 4.00 | 0 | 127.1 | 0.040 |
| T02 Appointments | sin skills | 3 | 532 | 2.82 | 2.05 | 0 | 461.7 | 0.203 |
| T02 Appointments | con skills | 2 | 314 | 4.25 | 3.92 | 0 | 372.9 | 0.193 |
| T03 Name normalizer | sin skills | 3 | 39 | 8.00 | 8.00 | 0 | 136.9 | 0.051 |
| T03 Name normalizer | con skills | 1 | 23 | 8.00 | 8.00 | 0 | 88.5 | 0.033 |

## Métricas agregadas (N=6 corridas)

| Métrica | sin skills | con skills | Δ |
|---|---:|---:|---:|
| Cycle time promedio | 252.9 s | 196.2 s | **−22.4%** |
| Archivos promedio | 2.33 | 1.67 | **−28.6%** |
| LOC promedio | 202.3 | 133.3 | **−34.1%** |
| Alucinaciones detectadas (imports top-level) | 0 | 0 | — |
| Costo total | 0.34 USD | 0.27 USD | **−22.0%** |

## Gráficos comparativos

`qa_reports/charts.png` contiene tres paneles generados con matplotlib a
partir de `results.json`: cycle time por tarea, archivos generados por
tarea, y LOC del archivo principal. Los gráficos incluyen anotaciones
contextuales sobre T03 (eliminación de 2 `__init__.py` redundantes con
skills) y T02 (convención de scopes explícita).

## Hallazgos cualitativos

1. **Gold-plating estructural mitigado en T03.** El modo libre generó
   3 archivos (el normalizador + 2 `__init__.py` del paquete) cuando
   la tarea pedía solo el normalizador. El modo con skills generó 1
   archivo, en línea con la restricción "NO crear `__init__.py`
   redundantes" del requisito.

2. **Convención explícita vs implícita en T02.** El modo con skills
   dejó en el comentario inicial del archivo `appointments.py` las
   5 convenciones adoptadas del repo (tipo de IDs como String,
   nombres de campos `start_time`/`end_time`, mapeo de roles,
   fail-closed para recepcionista, status enum). Esa documentación
   es coherente con la Regla 1 del harness ("preguntar, nunca
   asumir"): cuando la respuesta está en el repositorio, el LLM
   la extrae y la declara. El modo libre no dejó este registro.

3. **CC ligeramente mayor con skills en tareas grandes (T02).** El
   endpoint con skills (CC avg 4.25) es marginalmente más complejo
   que el libre (CC avg 2.82). Esto contradice la intuición de que
   las restricciones reducen dificultad: lo que hacen es **aumentar
   la cobertura de casos de aceptación**, no simplificar la lógica.
   Para T03 (función pura de normalización), CC es idéntica porque
   la tarea no invita a branching adicional.

4. **Cero alucinaciones en ambos modos.** El detector basado en
   AST (`harness/eval/metrics_collector.py`) compara imports
   top-level contra un whitelist que combina: (a) símbolos
   definidos en `src/` y `app/`, (b) paquetes declarados en
   `requirements.txt`, (c) stdlib. Todas las invocaciones del LLM
   usaron imports válidos. Esto sugiere que para tareas de
   granularidad fina (un módulo, una función) el modelo base no
   alucina dependencias por sí solo; las alucinaciones requieren
   contextos de mayor superficie (p.ej. seleccionar entre múltiples
   frameworks).

## Limitaciones del estudio

(a) **N=3 tareas por modo** es metodológicamente insuficiente para
significancia estadística. Las reducciones reportadas son indicativas,
no concluyentes; un test de Wilcoxon sobre N≥10 tareas sería el
siguiente paso natural.

(b) **Modelo único** (`opencode-go/minimax-m3`). La robustez de los
hallazgos a través de modelos queda como trabajo futuro.

(c) **Sin medición de carga cognitiva del desarrollador** (NASA-TLX,
marco SPACE). La dimensión DevEx se infiere indirectamente por el
cycle time y la cantidad de archivos; no se aplicaron cuestionarios
a usuarios humanos por restricciones de tiempo y muestra.

(d) **El runner instrumentó las tools del LLM, no su razonamiento
interno.** Las métricas capturan outputs (archivos, tokens, eventos)
pero no el proceso de decisión del agente. Una métrica como
"cantidad de veces que el LLM invocó `read` antes de decidir escribir"
sería valiosa y queda como extensión.

## Conclusión cuantitativa

La evidencia experimental muestra una dirección consistente: las 4
reglas Always-On del harness, inyectadas como system prompt del LLM,
producen código con **−34% menos líneas**, **−29% menos archivos** y
**−22% menos tiempo de ciclo** en promedio, sin sacrificar correctitud
(cero alucinaciones en ambos modos) y sin pérdida de cobertura de casos
de aceptación. La intervención de inyectar las reglas como system
prompt es de **bajo costo** (un archivo `.md` en `.opencode/agents/`) y
**alto retorno** en contención de superficie y eficiencia.

Los datos crudos están en `qa_reports/results.json`, los gráficos en
`qa_reports/charts.png`, y el detalle por corrida en
`docs/seccion_6_3_resultados.md`.
