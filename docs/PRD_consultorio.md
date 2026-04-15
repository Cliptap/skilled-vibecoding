PRD – Repositorio de Información para Consultorio de Salud

1. Propósito
• Problema: Necesidad de registrar y organizar las citas de los pacientes en el consultorio.
• Objetivo: Facilitar el manejo y organización de las citas de los pacientes.

2. Usuarios
• Tipos: Recepcionistas
• Uso: Generar, modificar y cancelar citas para pacientes en fechas y horas determinadas.

3. Datos
• Tipo: Estructurados
• Dominio: Datos personales de pacientes (nombre, apellido, rut, teléfono, correo, sexo, fecha de nacimiento, previsión) y datos de citas.
• Volumen: Aproximadamente 15 pacientes al día.

4. Fuentes
• Origen: Ingreso manual por el/la recepcionista.

5. Arquitectura
• Base de datos: SQL
• Infraestructura: Local

6. Procesamiento de datos
• Extracción: Ingreso manual
• Frecuencia: Diaria
• Transformación: Validación del rut

7. Gobernanza
• Nivel: Bajo (validaciones básicas, sin control de acceso, sin logs ni auditoría)
