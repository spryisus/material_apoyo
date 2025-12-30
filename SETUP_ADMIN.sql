-- Script SQL para configurar el sistema de administración
-- Ejecuta este script en Supabase SQL Editor

-- 1. Agregar columna 'rol' a la tabla usuarios (si no existe)
ALTER TABLE usuarios 
ADD COLUMN IF NOT EXISTS rol VARCHAR(20) DEFAULT 'alumno' CHECK (rol IN ('admin', 'profesor', 'alumno'));

-- 2. Crear tabla para configuración de PDFs de materias
CREATE TABLE IF NOT EXISTS materia_pdf_config (
    id BIGSERIAL PRIMARY KEY,
    materia_id BIGINT NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
    tema_numero INTEGER NOT NULL,
    tema_nombre VARCHAR(255) NOT NULL,
    pagina_inicio INTEGER NOT NULL,
    pagina_fin INTEGER NOT NULL,
    pdf_path TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(materia_id, tema_numero)
);

-- 3. Crear índice para mejorar búsquedas
CREATE INDEX IF NOT EXISTS idx_materia_pdf_config_materia_id ON materia_pdf_config(materia_id);

-- 4. Habilitar RLS (Row Level Security) en la nueva tabla
ALTER TABLE materia_pdf_config ENABLE ROW LEVEL SECURITY;

-- 5. Políticas RLS para materia_pdf_config
-- NOTA: Como el sistema usa autenticación personalizada (no Supabase Auth),
-- las políticas se simplifican. La verificación de rol se hace en el código JavaScript.

-- Permitir lectura a todos (público, ya que los usuarios necesitan ver los temas)
DROP POLICY IF EXISTS "Lectura pública de configuración PDF" ON materia_pdf_config;
CREATE POLICY "Lectura pública de configuración PDF"
    ON materia_pdf_config
    FOR SELECT
    TO public
    USING (true);

-- Permitir inserción/actualización/eliminación a todos los usuarios autenticados
-- (La verificación de rol 'admin' se hace en el código JavaScript antes de llamar estas funciones)
DROP POLICY IF EXISTS "Usuarios pueden modificar configuración PDF" ON materia_pdf_config;
CREATE POLICY "Usuarios pueden modificar configuración PDF"
    ON materia_pdf_config
    FOR ALL
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- 6. Crear bucket de almacenamiento para PDFs
-- IMPORTANTE: Primero crea el bucket desde la interfaz de Supabase Storage
-- Ve a Storage > New bucket > Nombre: 'material-apoyo' > Marca "Public bucket"
-- O ejecuta esto en SQL Editor si tienes permisos:
INSERT INTO storage.buckets (id, name, public) 
VALUES ('material-apoyo', 'material-apoyo', true)
ON CONFLICT (id) DO NOTHING;

-- NOTA: Los PDFs se organizan por materias en la estructura:
-- materias/{materia_id}/material.pdf
-- Esto permite tener un PDF por materia y mantener mejor organización

-- 7. Políticas de almacenamiento para el bucket
-- IMPORTANTE: Solo ejecuta estas políticas DESPUÉS de crear el bucket

-- Permitir lectura pública de PDFs
DROP POLICY IF EXISTS "Lectura pública de PDFs" ON storage.objects;
CREATE POLICY "Lectura pública de PDFs"
    ON storage.objects
    FOR SELECT
    TO public
    USING (bucket_id = 'material-apoyo');

-- Permitir subida solo a administradores
DROP POLICY IF EXISTS "Solo administradores pueden subir PDFs" ON storage.objects;
CREATE POLICY "Solo administradores pueden subir PDFs"
    ON storage.objects
    FOR INSERT
    TO authenticated
    WITH CHECK (
        bucket_id = 'material-apoyo' AND
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.id = auth.uid() 
            AND usuarios.rol = 'admin'
        )
    );

-- Permitir actualización solo a administradores
DROP POLICY IF EXISTS "Solo administradores pueden actualizar PDFs" ON storage.objects;
CREATE POLICY "Solo administradores pueden actualizar PDFs"
    ON storage.objects
    FOR UPDATE
    TO authenticated
    USING (
        bucket_id = 'material-apoyo' AND
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.id = auth.uid() 
            AND usuarios.rol = 'admin'
        )
    );

-- Permitir eliminación solo a administradores
DROP POLICY IF EXISTS "Solo administradores pueden eliminar PDFs" ON storage.objects;
CREATE POLICY "Solo administradores pueden eliminar PDFs"
    ON storage.objects
    FOR DELETE
    TO authenticated
    USING (
        bucket_id = 'material-apoyo' AND
        EXISTS (
            SELECT 1 FROM usuarios 
            WHERE usuarios.id = auth.uid() 
            AND usuarios.rol = 'admin'
        )
    );

-- 8. Actualizar un usuario existente a administrador (opcional)
-- Reemplaza 'tu-email@ejemplo.com' con tu email
-- UPDATE usuarios SET rol = 'admin' WHERE email = 'tu-email@ejemplo.com';

-- 9. Agregar columna descripcion a materias (si no existe)
ALTER TABLE materias 
ADD COLUMN IF NOT EXISTS descripcion TEXT;

