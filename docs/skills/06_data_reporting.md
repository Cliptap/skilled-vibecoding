Skill: Definición de Reportería (Métricas y Consultas SQL Avanzadas)

Objetivo
Crear las consultas estructuradas, vistas en la base de datos (VIEWS, MATERIALIZED VIEWS) y paneles de información que procesen los datos recolectados para generar reportes analíticos para los tomadores de decisiones. Cumpliendo requerimientos previos del PRD, sobre trazabilidad y fechas de los registros (según el nivel de gobernanza).

________________________________________
Instrucciones
• No generar el SQL analítico ni código de reportes al inicio.
• Hacer preguntas por sección siguiendo el flujo.
• Evaluar cada requerimiento por medio de "Reglas OBLIGATORIAS".
• No avanzar si falta información crítica.
• Al final, generar el código completo.

________________________________________
Flujo de interacción

1. Indicadores (KPIs) y Propósito del Análisis
Solicitar cuáles son los reportes que se buscan resolver (ej: Cantidad de Pacientes Totales por Semana, Proporción de Previsiones de Salud, Ingresos vs Costos).
Pregunte al usuario cuáles son los KPI (Key Performance Indicators) a destacar más fundamentales para el Dashboard/Reporte principal.

2. Origen del Modelo y Granularidad (Dimensión / Hechos)
Preguntar si se cruzan tablas, qué filtros temporales (Mes a Mes, Año pasado vs Actual) y qué dimensiones importan en los resultados (Agrupamientos por sucursal, sexo, sistema de salud, etc.).

3. Gobernanza e Inclusión en Reportes
Según el PRD original:
Pregunte cómo deben exponerse las reglas de acceso/auditoría.
• ¿Bajo? Reporte plano sin restricciones.
• ¿Medio/Alto? Los reportes requieren exponer datos como `updated_at`, o quién fue el creador del registro original, si hay controles adicionales, e información de auditoría o limpieza (sino, preguntar cómo modelarlo en SQL).

4. Presentación
¿Este resorte se expondrá en una herramienta de BI externa (Power BI, Metabase, Looker), a través de un endpoint API en JSON, o como una vista en el Frontend recién desarrollado (HTML)?

________________________________________
Reglas y Mejores Prácticas (OBLIGATORIAS)

• Vistas Analíticas en DB, No en Backend: Usar Views o CTEs (Common Table Expressions) y Window Functions de forma preferencial, en vez de hacer 30 iteraciones FOR de python/Nodejs en memoria. Los cálculos agregados rápidos se hacen en SQL (`COUNT, AVG, SUM, ROW_NUMBER`).
• Optimizaciones: Utilizar `MATERIALIZED VIEWS` si las vistas tardan muchos segundos/minutos. Pre-calcular todo reporte grande.
• Sin "SELECT *": Reportar exclusivamente los campos que componen la estadística.
• Legibilidad SQL Analítico: Usar sentencias `WITH` en mayúsculas y en bloques legibles de 1 nivel a la vez. Añadir comentarios `/* ... */` sobre las transformaciones matemáticas aplicadas.

________________________________________
Condición de cierre
Antes de que diseñe/escriba código:
“Voy a generar el pipeline de Reportería SQL para tus indicadores clave. ¿Leés si todo esto coincide con tu PRD general?”

________________________________________
Formato de salida

1. Definición Analítica
KPIs definidos, tabla de Hechos/Dimensiones y agrupamientos SQL base.

2. Consultas Complejas SQL o Código Analítico Integrado
Código listo y documentado de VIEWS o funciones SQL listas para despliegue y/o el código python analítico si se solicitó.