-- Esquema de base de datos para consultorio de salud
-- Cumple mejores prácticas PostgreSQL

CREATE TABLE paciente (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    rut TEXT NOT NULL UNIQUE,
    telefono TEXT,
    correo TEXT,
    sexo TEXT,
    fecha_nacimiento DATE,
    prevision TEXT
);

CREATE TABLE cita (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    paciente_id BIGINT NOT NULL,
    fecha TIMESTAMPTZ NOT NULL,
    razon TEXT,
    CONSTRAINT fk_paciente FOREIGN KEY(paciente_id) REFERENCES paciente(id) ON DELETE CASCADE
);

-- Índice para búsquedas por rut
CREATE INDEX idx_paciente_rut ON paciente(rut);
-- Índice para filtrar citas por fecha
CREATE INDEX idx_cita_fecha ON cita(fecha);
-- Índice explícito para la FK
CREATE INDEX idx_cita_paciente_id ON cita(paciente_id);