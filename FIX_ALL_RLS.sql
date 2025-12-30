-- SOLUCIÓN COMPLETA PARA TODAS LAS POLÍTICAS RLS
-- Ejecuta este script completo en Supabase SQL Editor
-- Este script corrige tanto Storage como materia_pdf_config

-- ============================================
-- PARTE 1: CORREGIR POLÍTICAS DE materia_pdf_config
-- ============================================

-- Eliminar políticas antiguas
DROP POLICY IF EXISTS "Usuarios autenticados pueden leer configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Solo administradores pueden modificar configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Lectura pública de configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Usuarios pueden modificar configuración PDF" ON materia_pdf_config;

-- Crear políticas permisivas para materia_pdf_config
-- Permitir lectura pública
CREATE POLICY "Lectura pública materia_pdf_config"
    ON materia_pdf_config
    FOR SELECT
    TO public
    USING (true);

-- Permitir inserción a todos (la verificación de admin se hace en código)
CREATE POLICY "Inserción materia_pdf_config"
    ON materia_pdf_config
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (true);

-- Permitir actualización a todos
CREATE POLICY "Actualización materia_pdf_config"
    ON materia_pdf_config
    FOR UPDATE
    TO anon, authenticated
    USING (true)
    WITH CHECK (true);

-- Permitir eliminación a todos
CREATE POLICY "Eliminación materia_pdf_config"
    ON materia_pdf_config
    FOR DELETE
    TO anon, authenticated
    USING (true);

-- ============================================
-- PARTE 2: CORREGIR POLÍTICAS DE STORAGE
-- ============================================

-- Eliminar políticas existentes del bucket material-apoyo
DROP POLICY IF EXISTS "Lectura pública de PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Usuarios autenticados pueden subir PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Usuarios autenticados pueden actualizar PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Usuarios autenticados pueden eliminar PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Solo administradores pueden subir PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Solo administradores pueden actualizar PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Solo administradores pueden eliminar PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Permitir todo en material-apoyo" ON storage.objects;
DROP POLICY IF EXISTS "Permitir todo material-apoyo" ON storage.objects;
DROP POLICY IF EXISTS "Lectura pública material-apoyo" ON storage.objects;
DROP POLICY IF EXISTS "Inserción material-apoyo" ON storage.objects;
DROP POLICY IF EXISTS "Actualización material-apoyo" ON storage.objects;
DROP POLICY IF EXISTS "Eliminación material-apoyo" ON storage.objects;

-- Crear políticas permisivas para Storage
-- Permitir lectura pública
CREATE POLICY "Lectura pública material-apoyo"
    ON storage.objects
    FOR SELECT
    TO public
    USING (bucket_id = 'material-apoyo');

-- Permitir inserción
CREATE POLICY "Inserción material-apoyo"
    ON storage.objects
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (bucket_id = 'material-apoyo');

-- Permitir actualización
CREATE POLICY "Actualización material-apoyo"
    ON storage.objects
    FOR UPDATE
    TO anon, authenticated
    USING (bucket_id = 'material-apoyo')
    WITH CHECK (bucket_id = 'material-apoyo');

-- Permitir eliminación
CREATE POLICY "Eliminación material-apoyo"
    ON storage.objects
    FOR DELETE
    TO anon, authenticated
    USING (bucket_id = 'material-apoyo');

-- ============================================
-- VERIFICACIÓN
-- ============================================
-- Para verificar las políticas creadas, ejecuta:
-- SELECT * FROM pg_policies WHERE tablename = 'materia_pdf_config';
-- SELECT * FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage' AND policyname LIKE '%material-apoyo%';

