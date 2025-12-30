-- Script para restaurar todos los temas de Álgebra con su paginación
-- ID de Álgebra: 5
-- Ejecuta este script en Supabase SQL Editor

-- IMPORTANTE: Asegúrate de que la columna video_url existe
-- Si no existe, ejecuta primero: ALTER TABLE materia_pdf_config ADD COLUMN IF NOT EXISTS video_url TEXT;

-- Insertar todos los temas de Álgebra
-- NOTA: Asegúrate de que el PDF ya esté subido y el pdf_path sea correcto
-- El pdf_path debería ser algo como: 'materias/5/material.pdf'

INSERT INTO materia_pdf_config (materia_id, tema_numero, tema_nombre, pagina_inicio, pagina_fin, pdf_path, video_url)
VALUES 
    (5, 1, 'Expresiones algebraicas', 6, 7, 'materias/5/material.pdf', NULL),
    (5, 2, 'Operaciones básicas', 8, 13, 'materias/5/material.pdf', NULL),
    (5, 3, 'Factorización', 14, 21, 'materias/5/material.pdf', NULL),
    (5, 4, 'Fracciones algebraicas', 22, 25, 'materias/5/material.pdf', NULL),
    (5, 5, 'Ecuación de primer grado', 26, 28, 'materias/5/material.pdf', NULL),
    (5, 6, 'Ecuación de segundo grado', 29, 33, 'materias/5/material.pdf', NULL),
    (5, 7, 'Ecuaciones simultaneas', 34, 39, 'materias/5/material.pdf', NULL),
    (5, 8, 'Problemas planteados con palabras', 40, 45, 'materias/5/material.pdf', NULL)
ON CONFLICT (materia_id, tema_numero) 
DO UPDATE SET
    tema_nombre = EXCLUDED.tema_nombre,
    pagina_inicio = EXCLUDED.pagina_inicio,
    pagina_fin = EXCLUDED.pagina_fin,
    pdf_path = EXCLUDED.pdf_path,
    video_url = COALESCE(EXCLUDED.video_url, materia_pdf_config.video_url),
    updated_at = NOW();

-- Verificar que se insertaron correctamente
SELECT * FROM materia_pdf_config WHERE materia_id = 5 ORDER BY tema_numero;

