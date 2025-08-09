-- Crear base de datos (opcional; ejecutar solo si no existe)
-- CREATE DATABASE retosdb;

CREATE TABLE IF NOT EXISTS retos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    categoria VARCHAR(100),
    dificultad VARCHAR(10) CHECK (dificultad IN ('bajo', 'medio', 'alto')),
    estado VARCHAR(15) NOT NULL DEFAULT 'pendiente'
           CHECK (estado IN ('pendiente', 'en proceso', 'completado')),
    creado_en TIMESTAMP DEFAULT NOW(),
    actualizado_en TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_retos_categoria ON retos(categoria);
CREATE INDEX IF NOT EXISTS idx_retos_dificultad ON retos(dificultad);
CREATE INDEX IF NOT EXISTS idx_retos_estado ON retos(estado);

INSERT INTO retos (titulo, descripcion, categoria, dificultad, estado)
VALUES ('Primer reto', 'Descripción de ejemplo', 'general', 'bajo', 'pendiente')
ON CONFLICT DO NOTHING;

