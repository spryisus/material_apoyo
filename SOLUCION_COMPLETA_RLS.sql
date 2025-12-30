-- ============================================
-- SOLUCIÓN COMPLETA PARA RLS - EJECUTA ESTE SCRIPT
-- ============================================
-- Este script corrige TODAS las políticas RLS necesarias
-- Ejecuta TODO el script de una vez

-- ============================================
-- PARTE 1: materia_pdf_config
-- ============================================

-- Eliminar TODAS las políticas existentes
DROP POLICY IF EXISTS "Usuarios autenticados pueden leer configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Solo administradores pueden modificar configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Lectura pública de configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Usuarios pueden modificar configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Lectura pública materia_pdf_config" ON materia_pdf_config;
DROP POLICY IF EXISTS "Inserción materia_pdf_config" ON materia_pdf_config;
DROP POLICY IF EXISTS "Actualización materia_pdf_config" ON materia_pdf_config;
DROP POLICY IF EXISTS "Eliminación materia_pdf_config" ON materia_pdf_config;

-- Crear políticas que permitan operaciones a usuarios anónimos también
CREATE POLICY "Lectura pública materia_pdf_config"
    ON materia_pdf_config
    FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Inserción materia_pdf_config"
    ON materia_pdf_config
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (true);

CREATE POLICY "Actualización materia_pdf_config"
    ON materia_pdf_config
    FOR UPDATE
    TO anon, authenticated
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Eliminación materia_pdf_config"
    ON materia_pdf_config
    FOR DELETE
    TO anon, authenticated
    USING (true);

-- ============================================
-- PARTE 2: STORAGE (material-apoyo bucket)
-- ============================================

-- Eliminar TODAS las políticas existentes
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
CREATE POLICY "Lectura pública material-apoyo"
    ON storage.objects
    FOR SELECT
    TO public
    USING (bucket_id = 'material-apoyo');

CREATE POLICY "Inserción material-apoyo"
    ON storage.objects
    FOR INSERT
    TO anon, authenticated
    WITH CHECK (bucket_id = 'material-apoyo');

CREATE POLICY "Actualización material-apoyo"
    ON storage.objects
    FOR UPDATE
    TO anon, authenticated
    USING (bucket_id = 'material-apoyo')
    WITH CHECK (bucket_id = 'material-apoyo');

CREATE POLICY "Eliminación material-apoyo"
    ON storage.objects
    FOR DELETE
    TO anon, authenticated
    USING (bucket_id = 'material-apoyo');

-- ============================================
-- VERIFICACIÓN (Opcional - ejecuta para verificar)
-- ============================================
-- SELECT 'Políticas de materia_pdf_config:' as info;
-- SELECT * FROM pg_policies WHERE tablename = 'materia_pdf_config';
-- 
-- SELECT 'Políticas de storage.objects:' as info;
-- SELECT * FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage' AND policyname LIKE '%material-apoyo%';

