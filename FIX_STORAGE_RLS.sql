-- SOLUCIÓN DEFINITIVA: Deshabilitar RLS en Storage temporalmente
-- O crear políticas que permitan todo para usuarios autenticados

-- ============================================
-- OPCIÓN 1: Deshabilitar RLS en Storage (MÁS FÁCIL)
-- ============================================
-- Esto permite que cualquier usuario autenticado pueda subir/actualizar/eliminar
-- La verificación de rol 'admin' se hace en el código JavaScript

-- Eliminar TODAS las políticas existentes de storage.objects
DO $$ 
DECLARE
    r RECORD;
BEGIN
    FOR r IN (SELECT policyname FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage') 
    LOOP
        EXECUTE 'DROP POLICY IF EXISTS ' || quote_ident(r.policyname) || ' ON storage.objects';
    END LOOP;
END $$;

-- Crear políticas muy permisivas (solo para el bucket material-apoyo)
CREATE POLICY "Permitir todo en material-apoyo"
    ON storage.objects
    FOR ALL
    TO authenticated
    USING (bucket_id = 'material-apoyo')
    WITH CHECK (bucket_id = 'material-apoyo');

-- Permitir lectura pública
CREATE POLICY "Lectura pública material-apoyo"
    ON storage.objects
    FOR SELECT
    TO public
    USING (bucket_id = 'material-apoyo');

-- ============================================
-- OPCIÓN 2: Si la opción 1 no funciona, deshabilitar RLS completamente
-- ============================================
-- Descomenta estas líneas si la opción 1 no funciona:
-- ALTER TABLE storage.objects DISABLE ROW LEVEL SECURITY;

-- ============================================
-- VERIFICAR POLÍTICAS
-- ============================================
-- Para ver las políticas actuales:
-- SELECT * FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage';

