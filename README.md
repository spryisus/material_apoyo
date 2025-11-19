# 📚 Plataforma de Apoyo - Sistema de Exámenes

Plataforma web para estudiar y practicar con exámenes de opción múltiple en 8 materias diferentes.

## 🎯 Características

- **Sistema de Autenticación**: Login y registro de usuarios con Supabase
- **8 Materias Disponibles**: 
  - Matemáticas
  - Español
  - Historia
  - Ciencias Naturales
  - Geografía
  - Inglés
  - Formación Cívica y Ética
  - Tecnología
- **100 Preguntas por Materia**: Divididas en 4 temas de 25 preguntas cada uno
- **Exámenes Personalizados**: Selecciona de 1 a 8 materias para tu examen
- **30 Preguntas Aleatorias**: Cada examen contiene 30 preguntas seleccionadas aleatoriamente del banco
- **Sin Tiempo Límite**: Estudia a tu propio ritmo
- **Resultados Detallados**: Revisa tus respuestas correctas e incorrectas

## 🚀 Configuración

### 1. Configurar Supabase

1. Crea una cuenta en [Supabase](https://supabase.com)
2. Crea un nuevo proyecto
3. Ve a Settings > API
4. Copia tu **Project URL** y **anon public key**
5. Edita el archivo `js/supabase.js` y reemplaza:
   - `TU_PROJECT_URL` con tu Project URL
   - `TU_ANON_PUBLIC_KEY` con tu anon public key

```javascript
export const supabase = createClient(
  'https://tu-proyecto.supabase.co',
  'tu-anon-public-key-aqui'
)
```

### 2. Configurar Autenticación en Supabase

1. Ve a Authentication > Providers en tu panel de Supabase
2. Habilita "Email" provider
3. Configura las opciones según tus necesidades

### 3. Personalizar Preguntas

El archivo `js/preguntas.js` contiene el banco de preguntas. Actualmente tiene preguntas de ejemplo. Puedes personalizarlas editando el objeto `materias` en ese archivo.

Cada materia tiene esta estructura:
```javascript
materia: {
    nombre: 'Nombre de la Materia',
    temas: {
        tema1: {
            nombre: 'Nombre del Tema',
            preguntas: [
                {
                    id: 'id-unico',
                    pregunta: 'Texto de la pregunta',
                    opciones: ['Opción A', 'Opción B', 'Opción C', 'Opción D'],
                    respuestaCorrecta: 0, // Índice de la opción correcta (0-3)
                    materia: 'Nombre Materia',
                    tema: 'Nombre Tema'
                }
            ]
        }
    }
}
```

## 📁 Estructura del Proyecto

```
Plataforma_Apoyo/
├── index.html          # Página de login
├── materias.html       # Selección de materias
├── examen.html         # Página del examen
├── resultado.html      # Resultados del examen
├── css/
│   └── style.css       # Estilos principales
├── js/
│   ├── supabase.js     # Configuración de Supabase
│   ├── aut.js          # Autenticación
│   ├── materias.js     # Lógica de selección de materias
│   ├── preguntas.js    # Banco de preguntas
│   ├── examen.js       # Lógica del examen
│   └── resultado.js    # Lógica de resultados
└── README.md
```

## 🎮 Uso

1. **Iniciar Sesión**: 
   - Abre `index.html` en tu navegador
   - Si no tienes cuenta, haz clic en "Regístrate aquí"
   - Ingresa tu email y contraseña

2. **Seleccionar Materias**:
   - En la pantalla de bienvenida, selecciona las materias que deseas estudiar
   - Puedes seleccionar de 1 a 8 materias
   - Haz clic en "Iniciar Examen"

3. **Realizar el Examen**:
   - Responde las 30 preguntas aleatorias
   - Usa los botones "Anterior" y "Siguiente" para navegar
   - No hay tiempo límite
   - Haz clic en "Finalizar Examen" cuando termines

4. **Ver Resultados**:
   - Revisa tu puntuación y porcentaje
   - Ve el detalle de cada respuesta
   - Puedes iniciar un nuevo examen o revisar las respuestas incorrectas

## 🛠️ Tecnologías Utilizadas

- HTML5
- CSS3 (con variables CSS y diseño responsivo)
- JavaScript (ES6+ con módulos)
- Supabase (para autenticación)

## 📝 Notas

- Las preguntas se seleccionan aleatoriamente del banco de preguntas de las materias seleccionadas
- Las respuestas se guardan en tiempo real mientras navegas por el examen
- Los resultados se almacenan en sessionStorage (se pierden al cerrar el navegador)
- El diseño es completamente responsivo y funciona en dispositivos móviles

## 🔧 Personalización

Puedes personalizar:
- Colores: Edita las variables CSS en `css/style.css`
- Preguntas: Modifica `js/preguntas.js`
- Número de preguntas por examen: Cambia el valor en `js/examen.js` (línea donde se llama `obtenerPreguntasAleatorias`)

## 📄 Licencia

Este proyecto es de uso educativo.

