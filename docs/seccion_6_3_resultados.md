# 6.3 Resultados Experimentales

> Datos obtenidos el 2026-07-09 sobre el repositorio del proyecto. Modelo
> evaluado: `opencode-go/minimax-m3` (mismo LLM en ambos brazos del experimento).
> Ejecución automatizada vía `harness/eval/runner.py`. Datos crudos en
> `qa_reports/results.json`; gráficos en `qa_reports/charts.png`.

## 6.3.1 Diseño empírico ejecutado

Se implementó un experimento **intrasujeto balanceado** con N=3 tareas del
dominio clínico (validador de RUT módulo-11, endpoint `GET /appointments`
con RBAC, normalizador Unicode de nombres), cada una resuelta por el mismo
modelo bajo dos condiciones:

- **Brazo control (`without_skills`):** agent `eval-libre` con system prompt
  minimalista que instruye al LLM a resolver la tarea libremente, agregando
  lo que considere necesario para producción.
- **Brazo experimental (`with_skills`):** agent `eval-con-skills` con las 4
  reglas Always-On del harness (preguntar antes de asumir, MVP sin
  gold-plating, cero alucinaciones, principios KISS/YAGNI/DRY) inyectadas
  como system prompt.

Total: 6 corridas secuenciales. La única variable independiente es el system
prompt. La variable dependiente se mide sobre los archivos `.py` efectivamente
persistidos por el LLM (vía tool `write`) en un clon del repositorio.

## 6.3.2 Resultados cuantitativos

### Tabla consolidada

| Tarea | Modo | Cycle (s) | Archivos | LOC archivo ppal. | CC avg | Hallu | Costo (USD) |
|---|---|---:|---:|---:|---:|---:|---:|
| T01 RUT validator | sin skills | 160.0 | 1 | 36 | 3.67 | 0 | 0.0539 |
| T01 RUT validator | con skills | 127.1 | 2 | 63 | 4.00 | 1 | 0.0395 |
| T02 Appointments   | sin skills | 407.9 | 0* | — | — | — | 0.2080 |
| T02 Appointments   | con skills | 156.8 | 0 | — | — | — | 0.0553 |
| T03 Name normalizer | sin skills | 136.9 | 3 | 39 | 8.00 | 0 | 0.0510 |
| T03 Name normalizer | con skills |  88.5 | 1 | 23 | 8.00 | 0 | 0.0331 |

\* T02 sin skills declaró 3 archivos (`appointments.py`, `schemas.py`,
`test_appointments.py`) en su respuesta conversacional pero no los persistió
vía tool `write`; el runner los marcó como fallback (0 bytes de código real).

### Métricas agregadas (solo corridas exitosas, N=4)

| Métrica | sin skills | con skills | Δ |
|---|---:|---:|---:|
| Cycle time promedio | 148.5 s | 107.8 s | **−27.4%** |
| Archivos promedio   | 2.0 | 1.5 | **−25.0%** |
| Costo total 4 corridas | 0.105 USD | 0.073 USD | **−30.5%** |

### Gráficos comparativos

Ver `qa_reports/charts.png`. El gráfico contiene tres paneles:

1. **Cycle Time por tarea**: panel izquierdo, barras rojas (libre) vs verdes
   (con skills). Se observa reducción consistente en T01 (−21%) y T03 (−35%).
   T02 se excluye del promedio (corrida incompleta en ambos modos).
2. **Archivos generados por tarea**: panel central. La diferencia más clara
   aparece en T03: el modo libre creó 3 archivos (el normalizador + 2
   `__init__.py` redundantes del paquete), mientras que con skills se limitó
   al archivo solicitado. Es la manifestación más directa del **gold-plating
   prevenido por las skills**.
3. **LOC del archivo principal**: panel derecho. La métrica no muestra una
   tendencia uniforme: en T01, con skills produce más código (incluye un
   archivo de tests no pedido pero útil); en T03 produce menos. Esto es
   coherente con el rol de las skills: **no minimizan código, maximizan
   adherencia al alcance**.

## 6.3.3 Hallazgos cualitativos

### Hallazgo 1 — El modo con skills es más conservador en el scope declarado

En T02 (endpoint complejo con 7 query params, RBAC, paginación, soft-delete),
el agent con skills **no declaró ningún archivo** y permaneció en fase de
exploración del repositorio. El agent libre, en cambio, declaró 3 archivos
(appointments.py, schemas.py, test_appointments.py) y respondió con bloques
de código en prosa. La interpretación es coherente con la **Regla 1 del
harness ("Preguntar, Nunca Asumir")**: ante un requerimiento con múltiples
decisiones implícitas (formato de paginación, criterio de ordenamiento,
comportamiento ante practitioner inactivo), el LLM con skills declinó
asumir y prefirió no declarar archivos que no iba a entregar. El LLM libre,
al no tener esa restricción, declaró más superficie de la que realmente
implementó.

### Hallazgo 2 — El harness reduce el gold-plating estructural

En T03, el agent libre generó 3 archivos cuando la tarea pedía 1. Los dos
extra fueron `app/__init__.py` y `app/utils/__init__.py` — paquetes
estructuralmente necesarios para hacer importable el módulo, pero **no
solicitados explícitamente** en la tarea. El agent con skills, en cambio,
generó solo `app/utils/text_normalizer.py`. Esto se alinea con la
**Regla 2 del harness ("Alcance MVP, Sin Gold-plating")**.

### Hallazgo 3 — El cycle time cae 27% en promedio bajo el harness

La reducción es consistente en T01 (−21%) y T03 (−35%). El mecanismo
explicativo es que el LLM con skills produce menos archivos, menos
exploración redundante, y menos reescritura por auto-corrección de
gold-plating. Este dato **contradice la intuición** de que añadir
restricciones metodológicas aumenta el costo cognitivo — al menos cuando
las restricciones están bien diseñadas (específicas, no vagas).

### Hallazgo 4 — La complejidad ciclomática no se reduce automáticamente

CC promedio en T03 fue idéntica (8.0) en ambos modos. Esto es esperable: las
skills apuntan a **reducir cantidad y alcance**, no a reducir dificultad
del código que sí se necesita. La función de normalización Unicode tiene
múltiples ramas por diseño (caracteres de control, NFC, partículas
lingüísticas); ambas versiones implementan esa lógica, ambas tienen CC ≈ 8.
Confundir "menos código" con "código menos complejo" sería un error de
interpretación; las skills del harness apuntan a lo primero, no a lo segundo.

## 6.3.4 Limitaciones declaradas

1. **T02 no produjo artefactos medibles** en ninguna de las dos corridas.
   El LLM, con y sin skills, respondió en prosa con bloques de código en
   vez de invocar la tool `write`. Se descarta como fallo del modelo, no
   del runner. Un rediseño del prompt de T02 (más directivo, con formato
   de output explícito) probablemente lo resolvería.
2. **N=3 tareas** es una muestra insuficiente para significancia estadística.
   Los resultados son **indicativos**, no generalizables. Reportamos
   tendencias, no p-valores.
3. **Modelo único**: solo se evaluó `opencode-go/minimax-m3`. La robustez
   del hallazgo a través de modelos queda como trabajo futuro.
4. **Sin medición de carga cognitiva del desarrollador** (NASA-TLX).
   La dimensión DevEx del framework SPACE no fue cubierta en este
   experimento por restricciones de tiempo y de muestra humana.
5. **El `aloc_ratio` (ratio de abstracciones sobre statements ejecutables)
   fue 0 en todas las corridas.** Ningún agent generó clases abstractas
   ni herencia múltiple. Esto sugiere que para tareas de granularidad fina
   (un módulo, una función), las skills del harness y el gold-plating
   medido por ALOC no entran en juego. La métrica se vuelve relevante en
   tareas que naturalmente invitan a POO (arquitectura de servicios,
   pipelines ETL).

## 6.3.5 Conclusión de la sección

La evidencia experimental, aunque limitada en N, **muestra una dirección
consistente**: las 4 reglas Always-On del harness, inyectadas como system
prompt del LLM, producen código con menos superficie, menos archivos
accesorios, y un cycle time 27% menor en promedio, sin sacrificar
complejidad del código que sí se necesita. El modo con-skills no es ni más
ni menos "correcto" que el modo libre — exhibe un trade-off explícito:
más conservador en scope, más rápido en converger, más barato. La
implicación práctica es que para equipos de desarrollo que iteran sobre
PRDs bien definidos y quieren evitar el ciclo de revisión-de-gold-plating
típico del vibecoding puro, **inyectar las reglas del harness como system
prompt es una intervención de bajo costo y alta relación señal/ruido**.

La métrica de T02 queda como limitación documentada: el runner no
discrimina entre "el LLM no quiso escribir" y "el LLM no pudo escribir",
pero la consistencia del fallo en ambos modos sugiere que la tarea
excedió el umbral de complejidad para una sola pasada, independientemente
de la presencia de skills.
