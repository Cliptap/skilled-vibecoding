Proyecto 3: Aplicación de Vibe Coding mediante skills para el desarrollo de un repositorio de procesamiento de datos

1. Definición del Proyecto
El Problema: El uso de asistentes de inteligencia artificial (modelos de lenguaje) para la generación de código permite una alta velocidad de desarrollo, pero al carecer de una guía metodológica, produce soluciones desestructuradas, sin validaciones técnicas y sin criterios de calidad de software predecibles.
El Contexto: Ocurre en entornos de desarrollo de software modernos donde ingenieros y programadores integran herramientas tipo agencias como Copilot o Claude en su flujo de trabajo diario. Afecta directamente la fase de construcción y arquitectura del software.
El Impacto: Genera una alta acumulación de deuda técnica, soluciones frágiles y pérdida de tiempo en la depuración (debugging) de código "espagueti". Para el desarrollador, el punto de dolor es la frustración de tener que reescribir o arreglar constantemente bloques de código generados por la IA que no se integran bien entre sí o que fallan en tareas lógicas secuenciales.
El Objetivo: Estructurar el proceso de desarrollo asistido por IA mediante un pipeline de interacción estandarizado, utilizando skills predefinidas, para garantizar la generación de un código modular, consistente y validado. Esto se aplicará específicamente a la construcción iterativa de un repositorio de datos de salud (MVP).

2. Requerimientos del Sistema
Esta sección redefine las acciones que el sistema y el pipeline de IA deben poder realizar, separando el método (Vibe Coding) del producto (El Repositorio).

2.1 Requerimientos Funcionales (RF)
Metodología y Pipeline de IA
- RF01 - Biblioteca de Skills Secuencial: El proyecto debe contar con un conjunto definido de habilidades (skills) documentadas que guíen al modelo de lenguaje a través de al menos 5 fases: PRD, Modelamiento, Backend, Frontend y Reportería.
- RF02 - Catálogo de Prompts y Contexto: Se deben estructurar prompts específicos para cada etapa, utilizando el Documento de Requisitos del Producto (PRD) como contexto estricto para evitar desviaciones del alcance.
- RF03 - Validación mediante TDD: El pipeline debe exigir la definición de resultados esperados antes de evaluar si el código generado por un prompt es exitoso.

Repositorio de Datos (El Producto)
- RF04 - Gobernanza y Modelamiento: El sistema debe definir su nivel de gobernanza (ej. baja, media, alta) antes de la creación del modelo relacional de datos.
- RF05 - Extracción y Backend: El sistema debe ser capaz de cargar datos desde fuentes externas mediante una API REST (endpoints).
- RF06 - Limpieza y Transformación: El sistema debe ejecutar procesos de normalización, manejo de valores nulos y filtrado de datos.
- RF07 - Validación e Interfaces: El sistema debe incluir un módulo que verifique la integridad y el esquema de los datos procesados antes de exponerlos en la interfaz de usuario.

2.2 Requerimientos No Funcionales (RNF)
- RNF01 - Determinismo y Reutilizabilidad: Los skills diseñados deben ser lo suficientemente reproducibles para que otro desarrollador pueda aplicarlos con resultados consistentes.
- RNF02 - Código Defensivo y Modularidad: El código generado debe estar organizado en módulos independientes para evitar el "código espagueti". Además, todo bloque debe incluir manejo de excepciones (try-except) previendo datos anómalos.
- RNF03 - Consistencia y Estilo: El pipeline debe asegurar que el estilo de programación y las convenciones de nombres sean uniformes en todo el repositorio.
- RNF04 - Entorno de Desarrollo Asistido: El flujo de trabajo debe integrarse con herramientas de asistencia de IA modernas (como VS Code con Copilot o Claude).
- RNF05 - Verificabilidad: Todo código generado automáticamente debe pasar por un set de pruebas unitarias que aseguren su correcto funcionamiento.
- RNF06 - Documentación y Trazabilidad: Cada módulo debe incluir un registro de cómo fue generado, detallando los prompts y la lógica de interacción utilizada.

2.3 Arquitectura y Diseño del Sistema
Dado que el producto real de este proyecto es la **Biblioteca de Skills**, la arquitectura del software de prueba (el Repositorio del Consultorio) se diseñó intencionalmente para acoplarse a las fases del Vibe Coding con mínima fricción:
* **Backend (FastAPI + Pydantic):** Elegido por su tipado estricto, lo cual fuerza al LLM a generar esquemas de datos seguros y robustos. Actualmente utiliza un servicio de diccionarios en memoria para acelerar el feedback del agente sin lidiar con contenedores en etapas tempranas.
* **Frontend (Vanilla JS + Tailwind vía CDN):** Elegido para evitar *build steps* (Node/NPM) que suelen desorientar o alucinar respuestas en asistentes de IA en contextos reducidos.
* **Base de Datos (SQL PostgreSQL):** Modelada mediante DDL puro, lista para integrarse cuando el proyecto alcance un nivel de gobernanza superior.

*Diagrama Lógico de Iteraciones:*
* **Iteración 1 (Modelo Base):** Interfaz -> `FastAPI` -> `Patient_Service (Memoria)` -> `patients.sql`.
* **Iteración 2 (Relacional):** Extensión de la interfaz -> `FastAPI` -> Validación de Double-Booking -> `medicos_citas.sql` con Constraints estrictos.

El pipeline orquesta este diseño inyectando restricciones arquitectónicas precisas a través de los archivos `.md` de cada skill.

3. Gestión de Riesgos en Vibe Coding
- R01 (Crítico): Medición de la calidad entre prompt y código errónea. Mitigación: Medir éxito con aserciones exactas y asignar agente revisor.
- R02 (Crítico): LLM rompe la reproducibilidad. Mitigación: Guardar prompts versionados e instanciar 5 veces para medir reproducibilidad.
- R03 (Alto): Código Frágil. Mitigación: Indicar tipos de datos y forzar try-except.
- R04 (Alto): Alucinaciones del modelo. Mitigación: Checklist por cada skill.
- R05 (Medio): Contaminación del Pipeline. Mitigación: Prompt Engineering estricto (ej: "Output ONLY valid Python code").

4. Propuesta Metodológica: Pipeline de Vibe Coding
1. Fase 1: Definición del PRD (Skill 01): Transformación de requerimientos en un PRD con Gobernanza de Datos.
2. Fase 2: Modelamiento de Datos (Skill 02): Generación de esquemas relacionales SQL.
3. Fase 3: Implementación Backend (Skill 03 y 04): Flujos ETL, validación y Endpoints API.
4. Fase 4: Implementación Frontend (Skill 05): Diseño de vistas e integración con endpoints.
5. Fase 5: Reportería (Skill 06): Consultas analíticas y métricas.

5. Caso de Aplicación: Repositorio para Consultorio Médico

**4.1 Planificación y Gestión (Sprint 1)**
Previo a ejecutar el pipeline, establecimos metas bajo el marco de una Iteración Cero (construcción metodológica) y un Sprint 1 (Prueba empírica de 2 ciclos).

*Backlog Priorizado:*
1. Generar la "Biblioteca de Skills" base (docs/skills/*) [ALTA PRIORIDAD].
2. Ciclo 1 (Gobernanza Baja): Ejecutar el PRD inicial y Base de Datos (Pacientes). [MEDIA].
3. Ciclo 1: Implementar Backend (FastAPI) [MEDIA].
4. Ciclo 1: Implementar UI e interacciones con Tailwind [MEDIA].
5. Ciclo 2 (Gobernanza Media): Elevar complejidad relacional introduciendo Médicos y Citas [BAJA (Dependiente de 1 a 4)].

*Reflexión entre Planificado vs Ejecutado:*
Inicialmente planeamos iterar todo el software en paralelo o con código masivo, pero construir las bases teóricas de Vibe Coding tomó mayor dedicación. Obligamos al Agente IA a segmentar sus conocimientos en los archivos `prd.md`, `api_endpoints.md` y `frontend_ui.md`. El Sprint 1 sirvió para asentar estos 5 archivos fundacionales y llevarlos a la práctica exitosamente, creando todo el MVP para Pacientes y sentando la base de código de Citas (Iteración 2).

**5. Caso de Aplicación (Desarrollo y Resultados MVP)**
El producto final y evidencia de nuestra propuesta no es estrictamente el repositorio del consultorio con toda su funcionalidad, sino que **la Biblioteca Preliminar de Skills funciona repetitivamente y con calidad para programar iteraciones sucesivas (1 y 2)**. 

*Evidencias Reales del Funcionamiento:*
* [Insertar aquí captura del Prompt usando un archivo skill: "Actúa usando el skill de api_endpoints.md"]
* **Resultados de Reproducibilidad:** Esta metodología probó ser robusta. Dos estudiantes distintos corrieron prompts genéricos bajo el ala restrictiva de estas habilidades (skills), y consiguieron el mismo resultado funcional: una REST API bien empaquetada que sirvió para levantar una base de datos de pacientes similar.
* **Qué funciona en el MVP (Software):**
    * Toda la creación, lectura, actualización y borrado (CRUD) del padrón de Pacientes usando UI nativa en `index.html`.
    * El recálculo de KPI estadísticos en Dashboard usando agrupaciones algorítmicas expuestas visualmente (Reportería).
    * El backend levanta los roles prevenidos en los Skill y restringe acceso a la API (Ej: filtrado IP 127.0.0.1 solo local).
    * El cruce estricto de citas "Double-booking" en la Iteración 2, testeado localmente en Pytest y probado consistentemente.
* **Qué NO funciona aún en el MVP (Pendientes del Software):**
    * La capa de base de datos no es permanente real todavía: se desarrolló el SQL correspondiente, pero actualmente ambos módulos del backend descansan sobre almacenamiento iterativo en memoria (Diccionarios) por velocidad de corrección con el LLM.

**6. Análisis Crítico**
La experiencia de empujar asistentes LLM mediante Vibe Coding con "Skills preinyectados" dejó dos lecciones críticas. En primer lugar, la tasa de alucinaciones se redujo prácticamente a cero desde que aplicamos contexto. Solo enfrentamos 1 error (dependencias entre `pydantic` y validator de emails) en la compilación de `pytest`. Paradójicamente, la IA rastreó autónomamente su fallo con las tools e inyectó `email-validator` corrigiéndolo sin intervención humana.
Sin embargo, vimos una curva de adaptación en la IA. Al principio de los Sprints, el requerimiento es altamente exploratorio y la IA tiende a realizar demasiadas contra-preguntas o explicar detalladamente conceptos obvios. Sin embargo, a medida que avanza a estadios de gobernanza media (Iteración 2), adopta naturalmente las certidumbres arquitectónicas previas y se enfoca directo en el diseño (Ej: cruce de IDs en turnos de Doctores) descartando interrupciones obvias.
**Problema Limitante (Riesgo No Planificado):** El exceso de contexto y repetición con los Skills en `*.md` consumió abruptamente los "tokens" de la ventana de contexto. Como propuesta de mejora arquitectónica, contemplamos modelar el concepto de `caveman_skill.md`: una habilidad que le indique al sistema "Responde únicamente en comandos puros, ignora los saludos y minimiza la verbosidad". Esta mitigación ahorraría recursos transaccionales y aumentaría la viabilidad comercial y el foco del agente.

**7. Conclusiones y Proyección**
A través del desarrollo de este proyecto logramos transformar el uso ad-hoc de modelos conversacionales en una herramienta predecible y estandarizada gracias a la creación y parametrización de **Skills Base de Vibe Coding**. El equipo aprendió que el mayor valor agregado no es corregir el código del sistema local, sino "corregir las reglas del Skill" para que el error no se repita en nuevas entidades. 

*Aprendizajes Técnicos y Riesgos:* 
Comprobamos que las arquitecturas ligeras o sin frameworks invasivos (como Tailwind vía CDN o FastAPI sin ORM complejo de inicio) resuenan mejor en la IA y permiten iteraciones extremadamente veloces. El riesgo más considerable a futuro es el límite de tokens, amenazando la retención global del archivo de proyecto actual al superar las miles de líneas.

*Próximos Pasos Realistas:* 
1. Reemplazar los servicios en memoria que rigen los Pacientes y la agenda de Citas (Double-booking implementado en código local) insertando físicamente la capa PostgreSQL y el Motor SQLAlchemy (migración transparente del `API_Routes` y paso de testings completos).
2. Incorporar formalmente las optimizaciones de `caveman_skill.md` como capa global de control de verbosidad (costos de token).
3. Levantar la UI final de citas médicas con Gobernanza Media (control total relacional en front-y-back) documentando su eficiencia final en la base de nuestros skills.