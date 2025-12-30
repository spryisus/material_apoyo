-- Script para corregir las políticas RLS
-- Ejecuta este script completo en Supabase SQL Editor

-- ============================================
-- 1. CORREGIR POLÍTICAS DE materia_pdf_config
-- ============================================

-- Eliminar políticas antiguas
DROP POLICY IF EXISTS "Usuarios autenticados pueden leer configuración PDF" ON materia_pdf_config;
DROP POLICY IF EXISTS "Solo administradores pueden modificar configuración PDF" ON materia_pdf_config;

-- Crear nuevas políticas (más permisivas porque la verificación de rol se hace en código)
CREATE POLICY "Lectura pública de configuración PDF"
    ON materia_pdf_config
    FOR SELECT
    TO public
    USING (true);

CREATE POLICY "Usuarios pueden modificar configuración PDF"
    ON materia_pdf_config
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- ============================================
-- 2. CORREGIR POLÍTICAS DE STORAGE
-- ============================================

-- Eliminar políticas antiguas
DROP POLICY IF EXISTS "Lectura pública de PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Solo administradores pueden subir PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Solo administradores pueden actualizar PDFs" ON storage.objects;
DROP POLICY IF EXISTS "Solo administradores pueden eliminar PDFs" ON storage.objects;

-- Crear nuevas políticas
CREATE POLICY "Lectura pública de PDFs"
    ON storage.objects
    FOR SELECT
    TO public
    USING (bucket_id = 'material-apoyo');

CREATE POLICY "Usuarios autenticados pueden subir PDFs"
    ON storage.objects
    FOR INSERT
    TO authenticated
    WITH CHECK (bucket_id = 'material-apoyo');

CREATE POLICY "Usuarios autenticados pueden actualizar PDFs"
    ON storage.objects
    FOR UPDATE
    TO authenticated
    USING (bucket_id = 'material-apoyo')
    WITH CHECK (bucket_id = 'material-apoyo');

CREATE POLICY "Usuarios autenticados pueden eliminar PDFs"
    ON storage.objects
    FOR DELETE
    TO authenticated
    USING (bucket_id = 'material-apoyo');

-- ============================================
-- 3. VERIFICAR QUE TU USUARIO SEA ADMIN
-- ============================================

-- Reemplaza 'tu-email@ejemplo.com' con tu email real
-- Descomenta la siguiente línea y ejecuta:
-- UPDATE usuarios SET rol = 'admin' WHERE email = 'tu-email@ejemplo.com';

-- Para verificar tu rol actual:
-- SELECT id, email, rol FROM usuarios WHERE email = 'tu-email@ejemplo.com';

