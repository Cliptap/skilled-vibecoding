Skill: Definición de Pipeline ETL (Carga, Transformación y Validación)

Objetivo
Construir un script/pipeline en el Backend que extraiga, valide (con niveles de gobernanza y aseguramiento de calidad), transforme los datos de los usuarios o fuentes de origen y los ingrese de manera limpia y estandarizada a la base de datos.

________________________________________
Instrucciones
• No generar el código del ETL al inicio.
• Hacer preguntas por sección siguiendo el flujo de interacción.
• Evaluar cada requerimiento aplicando las reglas de calidad (ver "Reglas OBLIGATORIAS").
• No avanzar si falta información crítica.
• Al final, generar el código del Pipeline.

________________________________________
Flujo de interacción

1. Fuentes y Volumenes
Solicitar de dónde entrarán los datos (ej: lectura de CSV masivo, stream de datos, o datos directos desde un endpoint). Preguntar por el volumen de la carga.

2. Criterios de Limpieza y Estandarización
Preguntar por todas las operaciones necesarias (Transformación):
• Campos de texto: Mayúsculas/minúsculas, recorte de espacios.
• Campos numéricos/fechas: Transformación de strings a datetime, moneda, unidades.
• Datos faltantes: ¿Se imputan, se eliminan filas nulas o se insertan como nulos (NULL)?

3. Gobernanza, Validación y Calidad
Solicitar cómo se gestionará la gobernanza de esta carga:
• Nivel Bajo: Validar formato mínimo. Si falla, descartar, pero no registrar más.
• Nivel Medio/Alto: Registro de logs de la ejecución de carga, rechazo/aceptación y control de quién inició el proceso. Reglas estrictas de validación.

4. Destino
Solicitar el motor o servicio objetivo y la estrategia de inserción (Insert-Heavy masivo, Upserts con ON CONFLICT o Inserción fila por fila).

________________________________________
Reglas OBLIGATORIAS

• Modularidad y Clases de Servicio/Scripts Separados: El proceso ETL no debe existir dentro del de las rutas de la API, debe separarse en funciones unitarias.
• Extracción Inteligente: Si los de datos son masivos, usar chunks o batches, y no saturar memoria RAM cargando todo en variables al mismo tiempo.
• Registro Fiel (Logging): No utilizar "prints" o depuradores genéricos, integrar librerías de logging que permitan rastrear errores críticos (ERROR), alertas (WARNING), o seguimiento (INFO). Para un PRD de gobernanza Media a Alta, se requiere registro en DB del proceso batch.
• Transaccionalidad: O todo entra bien, o se aborta el bloque. Proteger usando BEGIN y COMMIT / ROLLBACK, no tener datos corruptos ni a medias en caso de que ocurra una de error a la mitad de una carga masiva.

________________________________________
Condición de cierre
Antes de producir el código:
“Voy a generar el Pipeline / Script de ETL para el backend. ¿Confirmas los criterios de limpieza y validación?”

________________________________________
Formato de salida

1. Resumen de Flujo de Carga
Flujo lógico con los pasos exactos de E -> T -> L y validaciones.

2. Código Completo de Carga y Validaciones
Script de ejemplo / funciones principales e implementación.