# 📄 Instrucciones para Configurar el PDF de Apoyo

## Pasos para Configurar el PDF

### 1. Colocar el archivo PDF

1. Coloca tu archivo PDF en la carpeta `assets/`
2. Asegúrate de que el nombre del archivo coincida con el valor en `js/pdf-config.js`
   - Por defecto: `material-apoyo.pdf`
   - Puedes cambiar la ruta en la variable `PDF_PATH` en `js/pdf-config.js`

### 2. Configurar el Mapeo de Páginas

Edita el archivo `js/pdf-config.js` y configura el mapeo de materias y temas a páginas del PDF.

#### Estructura de Configuración

```javascript
export const pdfConfig = {
    // materia_id: {
    //     tema_numero: [página_inicio, página_fin]
    // }
    
    // Ejemplo:
    1: {  // ID de la materia (Álgebra)
        1: [1, 3],   // Tema 1: páginas 1-3
        2: [4, 6],   // Tema 2: páginas 4-6
        3: [7, 9],   // Tema 3: páginas 7-9
        4: [10, 12]  // Tema 4: páginas 10-12
    },
    2: {  // ID de otra materia
        1: [13, 15],
        2: [16, 18],
        // ...
    }
};
```

#### Cómo Obtener el ID de la Materia

1. Abre la consola del navegador (F12)
2. Ve a la página de materias
3. En la consola, ejecuta:
```javascript
// Ver todas las materias con sus IDs
const materias = await obtenerMaterias();
console.log(materias);
```

O revisa directamente en tu base de datos de Supabase en la tabla `materias`.

#### Ejemplo Completo

Si tienes 4 materias con IDs 1, 2, 3, 4, y cada una tiene 4 temas:

```javascript
export const pdfConfig = {
    1: {  // Álgebra
        1: [1, 5],    // Tema 1: páginas 1-5
        2: [6, 10],   // Tema 2: páginas 6-10
        3: [11, 15],  // Tema 3: páginas 11-15
        4: [16, 20]   // Tema 4: páginas 16-20
    },
    2: {  // Cómputo
        1: [21, 25],
        2: [26, 30],
        3: [31, 35],
        4: [36, 40]
    },
    3: {  // Electricidad
        1: [41, 45],
        2: [46, 50],
        3: [51, 55],
        4: [56, 60]
    },
    4: {  // Electrónica
        1: [61, 65],
        2: [66, 70],
        3: [71, 75],
        4: [76, 80]
    }
};
```

### 3. Verificar la Configuración

1. Abre la aplicación en el navegador
2. Inicia sesión
3. Selecciona una materia
4. Haz clic en un tema
5. Deberías ver las páginas del PDF correspondientes a ese tema

### 4. Solución de Problemas

#### El PDF no se carga
- Verifica que el archivo PDF existe en la ruta especificada
- Verifica que la ruta en `PDF_PATH` es correcta
- Abre la consola del navegador (F12) para ver errores

#### Se muestran páginas incorrectas
- Verifica que los números de página en `pdfConfig` son correctos
- Recuerda que las páginas son 1-indexed (la primera página es 1, no 0)

#### No se muestra nada al hacer clic en un tema
- Verifica que el `materia_id` y `tema_numero` coinciden con los de tu base de datos
- Verifica que hay una entrada en `pdfConfig` para esa materia y tema

### Notas Importantes

- Las páginas del PDF son **1-indexed** (la primera página es 1)
- Puedes especificar un rango de páginas `[inicio, fin]` o una sola página `[página]`
- El visor de PDF usa PDF.js desde CDN, así que necesitas conexión a internet
- El PDF se carga completamente, pero solo se muestran las páginas configuradas

