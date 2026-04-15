Skill: Construcción de Interfaz (Frontend UI)

Objetivo
Proponer y estructurar una capa de presentación interactiva (Interfaz de Usuario) que permita recolectar datos, enviar eventos a las APIs y mostrar consultas/resultados al usuario, validando lo definido en el PRD.

________________________________________
Instrucciones
• No generar el código UI al inicio.
• Hacer preguntas por sección siguiendo el flujo de interacción.
• Evaluar cada requerimiento aplicando las "Reglas OBLIGATORIAS" en conjunto de las decisiones de diseño.
• No avanzar si falta información crítica.
• Al final, generar la propuesta de páginas y componentes.

________________________________________
Flujo de interacción

1. Stack Tecnológico de Vistas
Preguntar por el stack deseado para la interfaz: 
• Múltiples páginas o SPA (React, Next.js, Vue).
• Server Side rendering (Jinja, EJS, HTML puro).
• Tableros simplificados (Streamlit, Gradio, Shiny).
• Librerías de diseño visual (Tailwind, Bootstrap, Materia UI).

2. Funcionalidad de las Pantallas e Interacciones
Para cada caso de uso definido, solicitar:
• Qué páginas/vistas se requieren implementar (Login, Dashboard, Formulario de Carga, Lista de Registros, etc.).
• Componentes principales por página (Formularios multi-paso, Filtros, Tablas).

3. Flujo o Navegabilidad de la Información
Preguntar los pasos de la UI:
¿Desde dónde entra el usuario? Si envía un formulario y hay éxito o error, ¿A dónde redirige o qué alerta aparece?

4. Consumo de Backend
Confirmar la ruta exacta base o estructura general del servidor:
Solicitar el esquema de JSON de los requests base.

________________________________________
Reglas OBLIGATORIAS

• Interfaz Responsivo: Todos los elementos visuales propuestos deben funcionar adecuadamente tanto en dispositivos de escritorio como móviles.
• UI Orientada a Validaciones Client-side: Usar Typescript (si existe), o etiquetas HTML `required / pattern` para evitar hacer llamadas basura. 
• Retroalimentación de Estado (Feedback): Toda acción tardía (ej. Carga a la BD, Login) DEBE mostrar algún indicador visual de "Loading...". Todos los errores devueltos por el backend (400, 500) DEBEN ser notificados al usuario en forma de TOAST o mensaje de alerta rojo, y de verde si tiene éxito (200 OK).
• Modularidad de Componentes: Fragmentar visualmente las piezas de código que se repetirán (Botones genéricos, Layout, Input de formularios) en lugar de crear un único archivo enorme por página.

________________________________________
Condición de cierre
Antes de generar las vistas:
“Voy a generar el código base del Frontend. ¿Revisas este diagrama de pantallas antes de seguir?”

________________________________________
Formato de salida

1. Flow Visual Propuesto
Páginas, estructura general de navegación.

2. Componentes UI (Código)
Archivos necesarios del HTML o Componentes del framework por módulos.
CSS o Estilos funcionales, peticiones fetch o la forma respectiva a cada framework para consumo HTTP de la API creada.