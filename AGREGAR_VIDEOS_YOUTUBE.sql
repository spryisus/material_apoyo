-- Script SQL para agregar soporte de videos de YouTube
-- Ejecuta este script en Supabase SQL Editor

-- Agregar columna video_url a la tabla materia_pdf_config
ALTER TABLE materia_pdf_config 
ADD COLUMN IF NOT EXISTS video_url TEXT;

-- Comentario: El campo video_url almacenará URLs completas de YouTube
-- Ejemplo: https://www.youtube.com/watch?v=VIDEO_ID
-- o: https://youtu.be/VIDEO_ID
-- El código JavaScript convertirá automáticamente estas URLs a formato embed

