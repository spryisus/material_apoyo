# 🪣 Crear Bucket de Almacenamiento en Supabase

## Error: "Bucket not found"

Este error ocurre porque el bucket `material-apoyo` no existe en Supabase Storage. Sigue estos pasos para crearlo:

## Método 1: Desde la Interfaz de Supabase (Más Fácil)

1. **Ve a tu proyecto en Supabase Dashboard**
   - Abre https://supabase.com/dashboard
   - Selecciona tu proyecto

2. **Navega a Storage**
   - En el menú lateral, haz clic en **"Storage"**

3. **Crea un nuevo bucket**
   - Haz clic en el botón **"New bucket"** o **"Crear bucket"**
   - Nombre del bucket: `material-apoyo`
   - Marca la casilla **"Public bucket"** (para que los PDFs sean accesibles públicamente)
   - Haz clic en **"Create bucket"**

4. **Configura las políticas (opcional pero recomendado)**
   - Ve a la pestaña **"Policies"** del bucket
   - O ejecuta el script SQL que está en `SETUP_ADMIN.sql` (líneas 56-76)

## Método 2: Desde SQL Editor (Alternativo)

Si prefieres crear el bucket desde SQL:

1. **Ve a SQL Editor en Supabase**
2. **Ejecuta este comando**:

```sql
-- Crear el bucket
INSERT INTO storage.buckets (id, name, public)
VALUES ('material-apoyo', 'material-apoyo', true)
ON CONFLICT (id) DO NOTHING;
```

3. **Verifica que se creó**:
   - Ve a Storage y deberías ver el bucket `material-apoyo`

## Configurar Políticas de Acceso

Después de crear el bucket, ejecuta estas políticas en SQL Editor:

```sql
-- Permitir lectura pública de PDFs
CREATE POLICY "Lectura pública de PDFs"
    ON storage.objects
    FOR SELECT
    TO public
    USING (bucket_id = 'material-apoyo');

-- Permitir subida solo a administradores
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
```

## Verificar que Funciona

1. **Recarga la página de administración**
2. **Intenta subir el PDF de nuevo**
3. **Debería funcionar sin errores**

## Notas Importantes

- El bucket debe llamarse exactamente `material-apoyo` (con guión)
- Debe ser público para que los usuarios puedan ver los PDFs
- Las políticas aseguran que solo los administradores puedan modificar archivos

## Solución Rápida

Si quieres una solución rápida sin políticas (solo para probar):

1. Crea el bucket como público desde la interfaz
2. Temporalmente puedes deshabilitar RLS en Storage si tienes problemas
3. Una vez que funcione, configura las políticas correctamente

