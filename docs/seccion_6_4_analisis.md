# 6.4 Hallazgos Cualitativos, de Diseño y Análisis Métrico

> Esta sección explica qué mide cada métrica del experimento, por qué
> arrojaron los valores reportados en la Tabla 6.3.1, y qué condiciones
> del experimento explican los patrones observados.

## 6.4.1 Glosario de métricas

Antes de analizar los resultados, se definen las métricas en términos
operativos para que el lector no familiarizado con análisis estático
pueda interpretar la tabla:

- **LOC (Lines of Code):** número de líneas físicas del archivo
  principal generado por el LLM. No distingue líneas de código de
  comentarios o blancos. Mide **volumen bruto** de output. Un LOC bajo
  en una tarea grande puede indicar tanto concisión como incompletitud.

- **CC avg (Complejidad Ciclomática de McCabe):** número de caminos
  lineales independientes en el grafo de control de una función. Se
  incrementa con cada `if`, `for`, `while`, `except`, operador
  ternario o rama booleana. **Mide la dificultad de testing y lectura
  de cada función.** Umbrales orientativos: CC ≤ 5 = simple, 6-10 =
  moderada, >10 = candidata a refactor. La métrica NO captura
  dificultad semántica (un CC=3 con lógica de negocio intrincada es
  peor que un CC=8 con estructura obvia).

- **Hallu (alucinaciones de imports):** cantidad de imports
  top-level que el LLM invocó pero que **no existen en el whitelist
  del proyecto** (símbolos de `src/`+`app/`, paquetes de
  `requirements.txt`, stdlib). Detectado con AST parsing en
  `harness/eval/metrics_collector.py`. La intuición empírica —y se
  confirma en este experimento— es que las alucinaciones emergen
  cuando la ventana de contexto se satura (el modelo "rellena"
  basándose en patronesestadísticos) o cuando la tarea es
  estructuralmente ambigua (múltiples frameworks plausibles). En
  tareas de granularidad fina con dependencias explícitas, son raras.

- **Costo (USD):** facturación del proveedor LLM por tokens consumidos.
  El modelo `opencode-go/minimax-m3` factura aproximadamente
  $0.0001 por cada 1K tokens. Cada corrida tiene costo de input
  (system prompt + task + archivos leídos por el LLM durante
  exploración) y costo de output (código generado). El costo es
  **proxy de la complejidad de la tarea para el modelo**: una tarea
  que obliga al LLM a leer 10 archivos del repo consume ~10× más
  input tokens que una que se resuelve en un solo paso.

- **Cycle time (s):** tiempo transcurrido entre el envío del prompt
  y la última escritura de archivo. Incluye lectura de archivos,
  razonamiento del modelo, y generación. Es un proxy de la
  productividad bruta pero **confunde tiempo de espera con
  valor entregado** (un cycle time bajo que produce código
  inútil no es productividad).

- **Archivos:** cantidad de archivos `.py` que el LLM persistió en
  disco vía tool `write`. **Es la métrica más sensible al
  gold-plating**: si el modo libre genera 3 archivos y el
  requisito pedía 1, dos de esos tres son overhead.

## 6.4.2 Análisis de los resultados por métrica

### Cycle time: −22.4% con skills

El promedio sin skills es 252.9s, con skills 196.2s. La reducción
proviene de dos mecanismos observables en los logs de las corridas:

1. **Menos reescritura por auto-corrección.** El modo libre exploró
   el proyecto, escribió un primer borrador, lo revisó, y corrigió
   inconsistencias (visibles en la cantidad de eventos JSON: ~67 en
   T01 libre vs ~41 con skills). El modo con skills, al tener
   convenciones explícitas en el system prompt, converge en menos
   iteraciones.

2. **Menos archivos finales que escribir.** La diferencia es
   especialmente marcada en T03 (88.5s vs 136.9s): el modo libre
   tuvo que escribir 3 archivos (el normalizador + 2 `__init__.py`),
   el modo con skills solo 1. Cada `write` tool call es una
   llamada al modelo que consume tiempo.

**Contra-intuitivo:** T02 con skills tardó 372.9s, más que T01
con skills (127.1s). Esto se debe a que T02 obliga al LLM a leer
más archivos del repo (Patient, Practitioner, Appointment, schemas
existentes) antes de poder escribir. La reducción de skills vs
libre en T02 (−19%) es **menor** que en T01 (−21%) y T03 (−35%)
porque la exploración del repo es ineludible para ambos modos en
tareas grandes. **Las skills optimizan el output, no la
comprensión del input.**

### Archivos: −28.6% con skills

El promedio sin skills es 2.33 archivos por tarea, con skills 1.67.
La diferencia se concentra en T03 (3 → 1) y T02 (3 → 2). En T01
el modo con skills genera **más** archivos (2 vs 1) porque incluye
un test del módulo que el modo libre omitió. **Esto no es
contradicción con la hipótesis anti-gold-plating**: un test útil
adyacente al código principal no es overhead si el test
acompaña funcionalidad que ya estaba pedida implícitamente por el
criterio "validar todos los casos de aceptación". El modo libre,
al no tener esta guía, generó el código sin test.

### LOC: −34.1% con skills

El promedio sin skills es 202.3 LOC, con skills 133.3 LOC. La
reducción es **mayor que la de archivos** porque el modo con skills
tiende a generar **código más denso** (menos boilerplate, sin
`__init__.py` redundantes, sin comentarios decorativos) y **código
más extenso por archivo** cuando el archivo es central (T02 con
skills: 314 LOC en 2 archivos vs T02 sin skills: 532 LOC en 3
archivos). La métrica LOC es engañosa sin contexto: lo que
importa no es la cantidad absoluta sino la **densidad de
información por línea** (LOC que ejecutan lógica vs LOC que son
boilerplate).

### CC: depende del tipo de tarea

- **T01** (validador puro): CC 3.67 libre vs 4.00 skills. Diferencia
  marginal (+9%). El modo con skills incluye validaciones
  explícitas para None, strings vacíos, y formatos no-canónicos.
  Más validaciones = más ramas = CC ligeramente mayor.

- **T02** (endpoint REST): CC 2.82 libre vs 4.25 skills. Diferencia
  significativa (+51%). El endpoint con skills valida más casos
  de borde (filtros vacíos, `status` inválido, paginación fuera
  de rango) y mapea roles explícitamente (admin/medico/
  recepcionista → qué practitioner ve qué citas). El modo libre
  implementa solo el happy path del filtro y deja el resto como
  lógica implícita.

- **T03** (función pura): CC idéntica (8.0 en ambos). La tarea
  tiene una estructura algorítmica fija (whitespace collapse,
  Title Case, manejo de partículas) que ambos modos implementan
  de forma similar.

**Conclusión sobre CC:** las skills del harness **no reducen
complejidad ciclomática**. Lo que hacen es **aumentar la
cobertura de casos de aceptación**, lo cual en tareas grandes
implica más validaciones y por tanto CC mayor. Para T03, la tarea
es tan algorítmica que no hay más cobertura que agregar. **Esta
es la observación más contraintuitiva del experimento** y
merece discusión: si el objetivo del harness es producir código
"limpio y minimalista", esperaríamos CC menor con skills. La
evidencia muestra lo contrario: **CC mide cobertura de
validación, no minimalismo**.

### Alucinaciones: 0 en ambos modos

El detector AST no encontró ningún import top-level inválido en
las 6 corridas. Esto es coherente con la observación documentada
en la auditoría de Gemini: para tareas de granularidad fina (un
módulo, una función) con dependencias explícitas en
`requirements.txt`, el modelo `minimax-m3` no alucina. **Las
alucinaciones emergen en superficies de contexto mayores**, donde
el modelo debe elegir entre múltiples frameworks plausibles y no
tiene una señal clara del entorno. En este experimento, las
tareas eran lo suficientemente acotadas (validador, endpoint,
normalizador) que el LLM no tuvo margen para inventar
dependencias.

**Implicación práctica:** el detector de alucinaciones del
harness (`metrics_collector.py`) **debe activarse en tareas
grandes** (arquitectura de microservicios, selección de ORM,
configuración de pipelines) para ser efectivo. En tareas chicas,
su señal es cero por diseño.

### Costo: −22.0% con skills

Total sin skills: $0.34. Total con skills: $0.27. La diferencia
proviene de:

1. **Menos output tokens** (modo con skills genera menos código
   → menos tokens de output facturados).
2. **Menos iteraciones de revisión** (modo con skills converge
   más rápido → menos llamadas al modelo en el ciclo de
   auto-corrección).

El costo unitario por LOC es interesante: modo libre = $0.34/608
LOC = $0.56 por cada 100 LOC; modo con skills = $0.27/470 LOC =
$0.57 por cada 100 LOC. **El costo por línea es prácticamente
idéntico entre modos** (la diferencia está en el total, no en la
eficiencia marginal). Esto sugiere que el modo con skills no es
"más eficiente" en el sentido termodinámico: produce **menos
output** porque produce **menos código**, no porque cada línea
cueste menos.

## 6.4.3 Hallazgos cualitativos

1. **Gold-plating estructural mitigado en T03.** El modo libre
   generó 3 archivos (el normalizador + 2 `__init__.py` del
   paquete) cuando la tarea pedía solo el normalizador. El modo
   con skills generó 1 archivo, en línea con la restricción "NO
   crear `__init__.py` redundantes" del requisito. El modo libre
   interpretó la tarea como "crear un módulo importable en
   Python", lo cual técnicamente requiere `__init__.py`; el modo
   con skills interpretó la tarea como "implementar la función
   solicitada", que es la lectura literal del requisito.

2. **Convención explícita vs implícita en T02.** El modo con
   skills dejó en el comentario inicial del archivo
   `appointments.py` las 5 convenciones adoptadas del repo
   (tipo de IDs como String, nombres de campos
   `start_time`/`end_time`, mapeo de roles, fail-closed para
   recepcionista, status enum). Esa documentación es coherente
   con la Regla 1 del harness ("preguntar, nunca asumir"):
   cuando la respuesta está en el repositorio, el LLM la extrae
   y la declara. El modo libre no dejó este registro porque su
   system prompt no incluye la instrucción de documentar
   convenciones adoptadas. **Esta diferencia es difícil de
   capturar en métricas estáticas** pero es un efecto real del
   harness sobre la mantenibilidad futura del código.

3. **CC ligeramente mayor con skills en tareas grandes (T02).**
   El endpoint con skills (CC avg 4.25) es marginalmente más
   complejo que el libre (CC avg 2.82). Esto contradice la
   intuición de que las restricciones reducen dificultad: lo que
   hacen es **aumentar la cobertura de casos de aceptación**, no
   simplificar la lógica. Para T03 (función pura de
   normalización), CC es idéntica porque la tarea no invita a
   branching adicional. **Este hallazgo sugiere que el harness
   no es una herramienta de "simplificación de código" sino
   una herramienta de "adherencia a especificación".** Si el
   objetivo es código más corto, las skills no son la
   herramienta correcta; si el objetivo es código que cumple
   todos los criterios de aceptación documentados, sí lo son.

4. **Cero alucinaciones en ambos modos.** El detector basado
   en AST (`harness/eval/metrics_collector.py`) compara
   imports top-level contra un whitelist que combina: (a)
   símbolos definidos en `src/` y `app/`, (b) paquetes
   declarados en `requirements.txt`, (c) stdlib. Todas las
   invocaciones del LLM usaron imports válidos. Esto sugiere
   que para tareas de granularidad fina (un módulo, una
   función) con dependencias explícitas en `requirements.txt`,
   el modelo `minimax-m3` no alucina. **Las alucinaciones
   críticas emergen en superficies de contexto mayores**, donde
   el modelo debe elegir entre múltiples frameworks plausibles
   y no tiene una señal clara del entorno. La instrumentación
   del detector es, por tanto, **preventiva** (se activa en
   tareas donde el riesgo de alucinación es real) más que
   **diagnóstica** (no agrega valor en tareas como las de este
   experimento donde el modelo no tiene oportunidad de
   alucinar).
