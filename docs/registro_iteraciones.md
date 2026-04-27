# Registro de Iteraciones y Gobernanza

Este documento registra la evolución de la arquitectura, el nivel de gobernanza y las skills aplicadas en cada iteración del Consultorio (repositorio de procesamiento de datos).

## Iteración 1: MVP Pacientes (Gobernanza Baja)
**Estado:** Completado
**Objetivo:** Crear un repositorio funcional rápido para la gestión de pacientes y visualización de KPIs.

**Nivel de Gobernanza:**
* **Arquitectura:** Monolito local modular.
* **Backend:** FastAPI con almacenamiento en memoria (diccionarios), preparado para migrar a PostgreSQL.
* **Frontend:** Vanilla JS + HTML5 + Tailwind CSS (Vía CDN, sin build step).
* **Seguridad:** Filtrado IP estático simple (solo localhost `127.0.0.1`). Identidad única (Recepcionista).
* **Calidad:** Tests unitarios básicos en Pytest para los endpoints CRUD.

**Skills Utilizadas del Pipeline:**
1. `prd.md`: Para definir el alcance inicial del consultorio.
2. `db_schema.md`: Para diseñar los esquemas de PostgreSQL (`01_patients.sql`, `02_analytics_views.sql`).
3. `api_endpoints.md`: Para estructurar la API REST y las validaciones con Pydantic.
4. `frontend_ui.md`: Para garantizar el diseño responsivo y sin frameworks pesados.
5. `data_reporting.md`: Para crear el dashboard de KPIs y filtros temporales.

---

## Iteración 2: Médicos y Citas (Gobernanza Media) - *Próximo*
**Estado:** En Planificación
**Objetivo:** Introducir complejidad relacional y lógica de negocio agregando las entidades de Médico y Cita.

**Evolución Esperada de Gobernanza:**
* **Datos:** Relaciones foráneas (Cita pertenece a Paciente y Médico). Prevención de colisiones de horarios.
* **Skills:** Se reutilizarán las skills de la Iteración 1. Si se requieren reglas estrictas de validación de horarios, se actualizarán las skills de Backend/PRD para exigir siempre control de concurrencia.
