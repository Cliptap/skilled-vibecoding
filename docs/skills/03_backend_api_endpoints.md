Skill: Generación de Endpoints y API REST

Objetivo
Construir una API REST estructurada, segura y eficiente (ej: HTTP/JSON) que permita el acceso e interacción con la base de datos definida en el modelo, asegurando el cumplimiento de la gobernanza.

________________________________________
Instrucciones
• No generar el código de la API al inicio.
• Hacer preguntas por sección siguiendo el flujo de interacción.
• Revisar las reglas y mejores prácticas antes de proponer código.
• No avanzar si falta información crítica.
• Al final, generar el código.

________________________________________
Flujo de interacción

1. Tecnología y Framework
Solicitar qué lenguaje y framework se utilizará para la API (ej: Python/FastAPI, Node.js/Express, Go).

2. Entidades y Operaciones (Endpoints)
Para cada entidad principal (definidas previamente en el PRD y DB), preguntar qué operaciones se necesitan:
• CRUD completo (Create, Read, Update, Delete).
• Solo lectura o solo escritura.
• Endpoints especiales o reglas de negocio complejas.

3. Gobernanza e Integración
Preguntar cómo se manejará la gobernanza acordada:
• Control de acceso: ¿La API requiere JWT, tokens o API keys (Gobernanza media/alta) o es pública/interna sin autenticación (Gobernanza baja)?
• Validaciones: ¿Existen dtos o esquemas fijos de entrada (ej: Pydantic, Zod)?

4. Pruebas
Preguntar si se desea incluir código para pruebas de los endpoints (Unit testing, integración).

________________________________________
Reglas y Mejores Prácticas OBLIGATORIAS

• RESTful Design: Usar nombres de recursos en plural y métodos HTTP correctos (GET, POST, PUT, DELETE). No usar verbos en las URLs (ej: usar POST /users, no POST /create_user).
• Códigos de Estado: Retornar los códigos HTTP correspondientes (200 OK, 201 Created, 400 Bad Request, 404 Not Found, 500 Internal Error).
• Arquitectura por Capas: Separar los "Controladores/Rutas" de los "Servicios/Lógica de Negocio" y del acceso a la "Base de Datos". No mezclar toda la lógica en la definición del endpoint.
• Seguridad y Payload: Validar siempre el 'payload' de entrada. Nunca confiar en los datos del cliente.
• Manejo de Errores: Atrapar excepciones y delvolver mensajes claros sin exponer la estructura interna ni los errores de la DB.

________________________________________
Condición de cierre
Antes de generar el código:
“Voy a generar el código de los Endpoints de la API. ¿Confirmas o quieres ajustar algo?”

________________________________________
Formato de salida

1. Resumen de Rutas
• Lista de endpoints a generar (Método, Ruta, Propósito).

2. Código Fuente
A. Modelos/Esquemas de validación de entrada.
B. Rutas/Controladores.
C. Código de pruebas (si aplica).