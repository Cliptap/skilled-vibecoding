# 6.1 Configuración del Entorno de Evaluación

> Esta sección describe la infraestructura de medición, justifica las
> decisiones de diseño experimental y explicita los controles aplicados
> para minimizar contaminación de los resultados por variables
> confusoras.

## 6.1.1 Objetivo del runner

El runner (`harness/eval/runner.py`) es un **orquestador automatizado
de sesiones de LLM** cuyo propósito es ejecutar el mismo LLM sobre un
conjunto fijo de tareas en dos condiciones (con y sin las reglas
Always-On del harness) y medir el código producido bajo criterios
objetivos, sin intervención humana durante la ejecución. La
automatización es **condición necesaria** para la validez del
experimento: si el desarrollador (humano) formulara el prompt
manualmente en cada corrida, su estilo, sus decisiones de
redacción y su criterio variarían entre condiciones, contaminando
la variable independiente (presencia/ausencia de las skills).

## 6.1.2 Por qué se eligió este diseño

El experimento sigue un **diseño intrasujeto balanceado** porque
ofrece tres ventajas sobre un diseño entre-sujetos:

1. **Elimina variabilidad entre modelos.** El mismo LLM
   (`opencode-go/minimax-m3`) responde ambos brazos del experimento.
   No se compara un modelo "bueno" contra uno "malo", se compara el
   mismo modelo bajo dos system prompts distintos. La única variable
   que cambia es la presencia de las reglas del harness.

2. **Permite atribución causal.** Si las métricas difieren entre
   condiciones, la diferencia es atribuible a las skills, no a
   diferencias de capacidad base del modelo, de temperatura, de
   ventana de contexto, ni de cualquier otro factor.

3. **Reduce el tamaño muestral necesario.** Al controlar las
   variables confundidoras a nivel de configuración (mismo modelo,
   mismo proyecto, mismo prompt de tarea, misma temperatura), la
   varianza intra-condición se reduce, haciendo más detectable la
   diferencia entre condiciones con N=3 tareas.

## 6.1.3 Infraestructura técnica

La instrumentación se construyó sobre los componentes ya existentes
del proyecto:

- **OpenCode CLI** (`opencode-ai` v1.17.18) como motor de invocación
  del LLM. Se eligió opencode por dos razones: (a) ya estaba
  instalado y autenticado en el entorno del proyecto, evitando
  configuración adicional de claves de API; (b) opencode expone
  los eventos JSON de cada sesión (tool calls, texto, tokens,
  costos) en formato estructurado, lo que permite medir las
  métricas de proceso sin implementar un wrapper propio sobre la
  API del proveedor.

- **Dos agents diferenciados** (`.opencode/agents/eval-libre.md` y
  `.opencode/agents/eval-con-skills.md`) definidos como archivos
  de configuración. La única diferencia entre los dos es el
  system prompt: el primero instruye al LLM a resolver
  libremente; el segundo inyecta las 4 reglas Always-On del
  harness. Esta separación permite que la variable independiente
  del experimento sea **un archivo de configuración**, no un
  parámetro en línea de comandos, lo que facilita la
  reproducibilidad y auditoría.

- **Workspace clonado por corrida** (`qa_reports/_workspace/`).
  Antes de cada invocación al LLM, el runner copia el proyecto
  completo a un directorio temporal, eliminando en la condición
  "without_skills" los archivos `.opencode/` y `AGENTS.md`
  (renombrado a `.md.disabled`). Esto garantiza que el LLM en
  modo libre no tiene acceso a las reglas del harness ni por
  configuración del IDE ni por convención documental.

- **Captura de artefactos** vía eventos `tool_use` del JSON
  stream. El runner parsea cada evento, identifica las
  invocaciones a la tool `write`, y persiste el contenido en
  disco. Métricas estáticas (CC, complejidad cognitiva, ALOC
  ratio, alucinaciones de imports) se calculan post-hoc sobre
  los archivos efectivamente persistidos usando `radon`,
  `lizard` y el módulo `ast` de stdlib (`harness/eval/
  metrics_collector.py`).

## 6.1.4 Controles para minimizar contaminación

Tres controles explícitos se incorporaron al diseño para reducir
la influencia del experimentador sobre los resultados:

1. **Prompt de tarea idéntico entre condiciones.** Las tres
   tareas se almacenan como archivos `harness/eval/tasks/
   task_*.md` y se inyectan al LLM tal cual, sin reformulación
   ni paráfrasis. La variabilidad en la formulación del prompt
   (que en vibecoding humano es enorme) queda eliminada.

2. **Sin reformulación post-llamada.** Cuando el LLM produce
   código, el runner lo mide y persiste **tal cual** el LLM lo
   entregó. No hay reescritura, edición o "limpieza" del código
   por parte del experimentador. Esto preserva el comportamiento
   real del LLM bajo cada condición, aunque incluya decisiones
   estilísticas discutibles.

3. **Métricas automatizadas, no inspección humana.** Las
   métricas reportadas (CC, LOC, alucinaciones, archivos,
   cycle time, costo) son calculadas por scripts sobre
   artefactos en disco. No hay paso de revisión humana donde
   el experimentador podría puntuar subjetivamente la "calidad"
   del código. El gráfico `qa_reports/charts.png` se genera con
   matplotlib a partir de `results.json`; nadie "elige" qué
   incluir o cómo presentarlo.

## 6.1.5 Trade-offs reconocidos

El diseño tiene tres limitaciones inherentes que el lector debe
tener presentes al interpretar los resultados:

- **Las soluciones pre-existentes del modelo son desconocidas.**
  No se puede controlar si el LLM ya vio tareas similares durante
  su entrenamiento (HumanEval, MBPP, etc.). Esto afecta la
  validez externa: los resultados aplican a tareas que el
  modelo no ha memorizado, pero no podemos garantizar que estas
  tres tareas específicas caigan en esa categoría.

- **El "modo libre" no es equivalente a vibecoding humano.** El
  vibecoding humano involucra prompts iterativos, preguntas de
  clarificación del humano, y validación manual del output. El
  modo libre del runner es un **prompt único sin
  retroalimentación**, que es la condición más favorable al
  LLM. Si el LLM falla en modo libre, fallaría más aún en
  vibecoding humano. La comparación con skills debe leerse como
  "modo libre aséptico vs modo skills aséptico", no como
  "vibecoding humano vs harness".

- **N=3 tareas.** La significancia estadística es limitada. Los
  resultados son indicativos de tendencia, no concluyentes. Un
  test de Wilcoxon sobre N≥10 tareas sería el siguiente paso
  natural.

## 6.1.6 Reproducibilidad

Para reproducir el experimento:

```bash
# 1. Clonar el branch experimental/runner-v2
git clone -b experimental/runner-v2 https://github.com/Cliptap/skilled-vibecoding

# 2. Instalar dependencias
pip install radon lizard matplotlib

# 3. Ejecutar las 6 corridas (~15-20 min, ~USD 0.60 con opencode-go)
python harness/eval/runner.py --timeout 300

# 4. Generar graficos desde los resultados
python harness/eval/plot_results.py
```

Los datos crudos quedan en `qa_reports/results.json`; los
gráficos en `qa_reports/charts.png`. El costo total de las 6
corridas a modelo `opencode-go/minimax-m3` fue de **USD 0.58**
(0.34 sin skills + 0.24 con skills).
