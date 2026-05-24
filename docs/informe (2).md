# Proyecto 3 – Hito 2: Aplicación de Vibe Coding mediante skills para el desarrollo de un repositorio de procesamiento de datos

---

# 1. Definición del Proyecto

## El Problema
El uso de asistentes de inteligencia artificial (modelos de lenguaje) para la generación de código permite una alta velocidad de desarrollo, pero al carecer de una guía metodológica, produce soluciones desestructuradas, sin validaciones técnicas y sin criterios de calidad de software predecibles.

## El Contexto
Ocurre en entornos de desarrollo de software modernos donde ingenieros y programadores integran herramientas tipo agencias como Copilot o Claude en su flujo de trabajo diario. Afecta directamente la fase de construcción y arquitectura del software.

## El Impacto
Genera una alta acumulación de deuda técnica, soluciones frágiles y pérdida de tiempo en la depuración (debugging) de código "espagueti". Para el desarrollador, el punto de dolor es la frustración de tener que reescribir o arreglar constantemente bloques de código generados por la IA que no se integran bien entre sí o que fallan en tareas lógicas secuenciales.

## El Objetivo
Estructurar el proceso de desarrollo asistido por IA mediante un pipeline de interacción estandarizado, utilizando skills predefinidas, para garantizar la generación de un código modular, consistente y validado. Esto se aplicará específicamente a la construcción iterativa de un repositorio de datos de salud (MVP).

---

# 2. Requerimientos del Sistema

Esta sección redefine las acciones que el sistema y el pipeline de IA deben poder realizar, separando el método (Vibe Coding) del producto (El Repositorio).

## 2.1 Requerimientos Funcionales (RF)

### Metodología y Pipeline de IA

### RF01 - Biblioteca de Skills Secuencial
El proyecto debe contar con un conjunto definido de habilidades (skills) documentadas que guíen al modelo de lenguaje a través de al menos 5 fases:

- PRD
- Modelamiento
- Backend
- Frontend
- Reportería

### RF02 - Catálogo de Prompts y Contexto
Se deben estructurar prompts específicos para cada etapa, utilizando el Documento de Requisitos del Producto (PRD) como contexto estricto para evitar desviaciones del alcance.

### RF03 - Validación mediante TDD
El pipeline debe exigir la definición de resultados esperados antes de evaluar si el código generado por un prompt es exitoso.

---

## Repositorio de Datos (El Producto)

### RF04 - Gobernanza y Modelamiento
El sistema debe definir su nivel de gobernanza (ej. baja, media, alta) antes de la creación del modelo relacional de datos.

### RF05 - Extracción y Backend
El sistema debe ser capaz de cargar datos desde fuentes externas mediante una API REST (endpoints).

### RF06 - Limpieza y Transformación
El sistema debe ejecutar procesos de normalización, manejo de valores nulos y filtrado de datos.

### RF07 - Validación e Interfaces
El sistema debe incluir un módulo que verifique la integridad y el esquema de los datos procesados antes de exponerlos en la interfaz de usuario.

---

# 2.2 Requerimientos No Funcionales (RNF)

Refieren a las propiedades, cualidades y restricciones del sistema.

### RNF01 - Determinismo y Reutilizabilidad
Los skills diseñados deben ser lo suficientemente reproducibles para que otro desarrollador pueda aplicarlos con resultados consistentes.

### RNF02 - Código Defensivo y Modularidad
El código generado debe estar organizado en módulos independientes para evitar el "código espagueti". Además, todo bloque debe incluir manejo de excepciones (`try-except`) previendo datos anómalos.

### RNF03 - Consistencia y Estilo
El pipeline debe asegurar que el estilo de programación y las convenciones de nombres sean uniformes en todo el repositorio.

### RNF04 - Entorno de Desarrollo Asistido
El flujo de trabajo debe integrarse con herramientas de asistencia de IA modernas (como VS Code con Copilot o Claude).

### RNF05 - Verificabilidad
Todo código generado automáticamente debe pasar por un set de pruebas unitarias que aseguren su correcto funcionamiento.

### RNF06 - Documentación y Trazabilidad
Cada módulo debe incluir un registro de cómo fue generado, detallando los prompts y la lógica de interacción utilizada.

---

# 2.3 Arquitectura y Diseño del Sistema

La arquitectura del sistema de prueba se diseñó para minimizar la fricción con el asistente de IA:

## Backend (FastAPI + Pydantic)
Se eligió por su tipado estricto, lo que obliga al LLM a generar esquemas de datos seguros. Actualmente utiliza diccionarios en memoria para acelerar la iteración.

## Frontend (Vanilla JS + Tailwind CDN)
Selección estratégica para evitar pasos de compilación complejos que puedan inducir alucinaciones en la IA.

## Capa de Datos
Modelada mediante DDL puro en PostgreSQL. Dado que el agente ya generó los scripts SQL exitosamente, la transición desde la memoria volátil se enfocará en automatizar su despliegue mediante contenedores (Docker).

---

# 3. Gestión de Riesgos en Vibe Coding

| ID  | Riesgo | Probabilidad | Impacto | Nivel | Estrategia de Mitigación |
|-----|---------|---------------|----------|--------|---------------------------|
| R01 | Medición de la calidad entre prompt y código errónea | Alta | Alto | Crítico | 1. Medir el éxito del prompt únicamente si el código generado pasa aserciones exactas sobre datasets predefinidos.<br>2. Asignar un agente para la revisión de la calidad del código en cada instancia. |
| R02 | LLM rompe la reproducibilidad en futuras instancias | Alta | Alto | Crítico | 1. Si un prompt funciona para un módulo, se guarda en el repositorio con una versión específica.<br>2. Instanciar el mismo prompt 5 veces para medir la reproducibilidad. |
| R03 | Código Frágil | Media | Alta | Alto | 1. Indicar específicamente qué tipo de datos se va a usar para tener una estrategia preventiva de manejo de errores. Integrar directrices estrictas de uso de `try-except`. |
| R04 | Alucinaciones del modelo | Media | Alta | Alto | 1. Cada skill debe tener una lista de verificación de lo que el código resultante debe contener (ej: manejo de excepciones, tipado). |
| R05 | Contaminación del Pipeline | Media | Bajo | Medio | 1. Aplicar técnicas de Prompt Engineering exigiendo un formato de salida estricto ("Output ONLY valid Python code, no markdown"). |

---

# 4. Propuesta Metodológica y Planificación

El desarrollo se rige por un ciclo de 5 fases iterativas:

1. Fase 1 (PRD): Transformación de requerimientos en un documento estructurado.
2. Fase 2 (Modelamiento): Generación de esquemas SQL restringidos por la gobernanza.
3. Fase 3 (Backend): Construcción de flujos ETL y Endpoints API.
4. Fase 4 (Frontend): Diseño de vistas e integración.
5. Fase 5 (Reportería): Consultas analíticas y métricas de salud.

---

# 4.1 Planificación del Sprint 1

## Backlog Priorizado

1. Creación de la biblioteca de skills
2. Ciclo de gobernanza baja (Pacientes)
3. Implementación Backend
4. Desarrollo de UI

## Reflexión
Se priorizó el asentamiento de las bases teóricas de las skills antes de la generación masiva de código. Esto permitió que el agente IA adoptara un comportamiento predecible desde el inicio.

---

# 5. Caso de Aplicación: Consultorio Médico (Resultados MVP)

El resultado empírico demuestra que la biblioteca de skills permite programar iteraciones sucesivas con alta calidad.

## Logros

- CRUD funcional de Pacientes
- Posibilidad de consultas en base a datos ingresados
- Seguridad básica en la API

## Limitaciones actuales

La persistencia operativa del sistema de prueba sigue siendo en memoria. Aunque los esquemas relacionales para PostgreSQL ya fueron generados y validados, el sistema carece temporalmente de la orquestación necesaria para levantar el motor de base de datos de forma automatizada.

---

# 6. Análisis Crítico

## Dependencia de la Calidad del Prompt
Se observó que el éxito del desarrollo en Vibe Coding no depende solo de la IA, sino de la capacidad del desarrollador para actuar como "arquitecto de instrucciones".

## Limitaciones del Determinismo
Aunque las Skills estandarizan el proceso, existe una variabilidad inherente en los modelos LLM que puede comprometer la reproducibilidad exacta del código en diferentes sesiones.

En este caso del consultorio, al ser hecho con una gobernanza baja, las posibles variabilidades del código y el repositorio son menores, por lo que esto puede presentarse en mayor medida una vez se presenten repositorios con mayor gobernanza.

## Gobernanza vs. Agilidad
La elección de una Gobernanza baja permitió una efectividad de desarrollo alta para un MVP, pero se reconoce que para un entorno de salud, la falta de auditoría y roles de acceso representaría una oportunidad de subir la gobernanza en una futura iteración.

## Problema con tokens
El uso de skills inyectados redujo las alucinaciones a niveles mínimos. Sin embargo, se identificó que el exceso de contexto consume más rápidamente la ventana de tokens.

Como mejora, se propone el "Caveman Skill": una instrucción global que obligue a la IA a ser extremadamente concisa, eliminando saludos y explicaciones redundantes para ahorrar hasta un 70% de recursos transaccionales.

## Evolución de Skills hacia Infraestructura (IaC)
Actualizar la skill de modelamiento de datos para que el agente, además de generar los esquemas PostgreSQL, construya automáticamente los archivos de configuración (`Dockerfile` y `docker-compose.yml`) necesarios para levantar y disponibilizar la base de datos sin intervención manual.

---

# 7. Conclusiones y Proyección

Se validó que el valor real de Vibe Coding no reside en corregir el código final, sino en perfeccionar las reglas de las skills.

## Aprendizajes Clave

### El Pipeline como Guía
La implementación de un flujo secuencial:

PRD -> Modelamiento -> Backend

evitó la acumulación de deuda técnica prematura y facilitó la integración de módulos.

### Modularidad Predictiva
El uso de Skills obligó a que cada componente (como el script SQL de pacientes) fuera independiente, cumpliendo con el RNF01 de evitar el "código espagueti".

---

# Próximos Pasos

1. Migración total de memoria a PostgreSQL mediante SQLAlchemy.
2. Implementación de Gobernanza Media incluyendo trazabilidad de Médicos y Citas.
3. Optimización de costos de tokens mediante capas de control de verbosidad.
4. Implementar el RF03 mediante el desarrollo de una Skill de generación de pruebas unitarias (TDD) para asegurar que cada carga de la recepcionista sea verificada automáticamente.