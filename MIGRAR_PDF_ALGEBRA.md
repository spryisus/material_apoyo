# 📄 Guía para Migrar PDF a Álgebra

## Estructura de Organización

Los PDFs ahora se organizan por materias en la siguiente estructura:
```
material-apoyo/
  └── materias/
      ├── 5/              (ID de Álgebra)
      │   └── material.pdf
      ├── 6/              (ID de otra materia)
      │   └── material.pdf
      └── ...
```

## Opción 1: Migrar desde el Panel de Administración (Recomendado)

1. **Inicia sesión como administrador**
2. **Ve al panel de administración** (botón "⚙️ Administración")
3. **Haz clic en "Editar" en la materia Álgebra**
4. **Sube el PDF** que tienes en `assets/material-apoyo.pdf`
5. **Configura los temas** con las páginas que ya tienes:
   - Tema 1: Expresiones algebraicas - Páginas 6-7
   - Tema 2: Operaciones básicas - Páginas 8-13
   - Tema 3: Factorización - Páginas 14-21
   - Tema 4: Fracciones algebraicas - Páginas 22-25
   - Tema 5: Ecuación de primer grado - Páginas 26-28
   - Tema 6: Ecuación de segundo grado - Páginas 29-33
   - Tema 7: Ecuaciones simultaneas - Páginas 34-39
   - Tema 8: Problemas planteados con palabras - Páginas 40-45
6. **Guarda la materia**

El sistema automáticamente:
- Subirá el PDF a `materias/5/material.pdf`
- Guardará la configuración de temas y páginas
- Eliminará el PDF anterior si existe

## Opción 2: Migración Manual desde Supabase Storage

Si ya tienes el PDF en Supabase Storage en otra ubicación:

1. **Ve a Supabase Dashboard > Storage**
2. **Navega al bucket `material-apoyo`**
3. **Crea la carpeta `materias/5/`** (si no existe)
4. **Mueve o sube el PDF** a `materias/5/material.pdf`
5. **Actualiza la configuración en la base de datos**:
   ```sql
   UPDATE materia_pdf_config 
   SET pdf_path = 'materias/5/material.pdf'
   WHERE materia_id = 5;
   ```

## Opción 3: Usar Script de Migración

Si tienes el PDF en una ubicación específica y quieres migrarlo automáticamente:

1. **Abre la consola del navegador** (F12) en `admin.html`
2. **Ejecuta**:
   ```javascript
   import { migrarPDFAntiguo } from './js/database.js';
   
   // Reemplaza 'assets/material-apoyo.pdf' con la ruta real de tu PDF
   await migrarPDFAntiguo(5, 'assets/material-apoyo.pdf');
   ```

## Verificar la Migración

Después de migrar, verifica que todo funcione:

1. **Ve a la página de materias**
2. **Haz clic en Álgebra**
3. **Haz clic en cualquier tema**
4. **Deberías ver las páginas correctas del PDF**

## Ventajas de esta Estructura

✅ **Organización clara**: Cada materia tiene su propio PDF  
✅ **Fácil mantenimiento**: Fácil encontrar y actualizar PDFs  
✅ **Escalable**: Puedes agregar más materias sin conflictos  
✅ **Mejor rendimiento**: Cada materia carga solo su PDF  

## Notas Importantes

- El sistema automáticamente elimina el PDF anterior cuando subes uno nuevo
- Todos los temas de una materia comparten el mismo PDF
- La estructura `materias/{materia_id}/material.pdf` es automática
- No necesitas crear las carpetas manualmente, el sistema las crea

