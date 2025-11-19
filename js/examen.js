// js/examen.js
import { supabase } from './supabase.js';
import { checkAuth, getCurrentUser } from './aut.js';
import { obtenerPreguntas, crearExamen, guardarRespuestas, actualizarCalificacion, obtenerMaterias } from './database.js';

let preguntasExamen = [];
let respuestasUsuario = {};
let preguntaActual = 0;
let examenId = null;
let materiasIds = [];

// Verificar autenticación
async function checkAuthAndRedirect() {
    const session = await checkAuth();
    if (!session) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Inicializar examen
async function initExam() {
    const isAuthenticated = await checkAuthAndRedirect();
    if (!isAuthenticated) return;
    
    // Obtener materias seleccionadas
    const materiasSeleccionadasStr = sessionStorage.getItem('materiasSeleccionadas');
    if (!materiasSeleccionadasStr) {
        alert('No hay materias seleccionadas. Redirigiendo...');
        window.location.href = 'materias.html';
        return;
    }
    
    materiasIds = JSON.parse(materiasSeleccionadasStr);
    
    try {
        console.log('Iniciando carga de examen...');
        console.log('Materias seleccionadas (IDs):', materiasIds);
        
        // Obtener 30 preguntas aleatorias desde la base de datos
        console.log('Obteniendo preguntas...');
        preguntasExamen = await obtenerPreguntas(materiasIds, 30);
        console.log('Preguntas obtenidas:', preguntasExamen.length);
        
        if (preguntasExamen.length === 0) {
            console.error('No se encontraron preguntas para las materias seleccionadas');
            alert('No se encontraron preguntas para las materias seleccionadas. Asegúrate de que existan preguntas en la base de datos. Redirigiendo...');
            window.location.href = 'materias.html';
            return;
        }
        
        // Obtener nombres de materias para mostrar
        console.log('Obteniendo nombres de materias...');
        const materias = await obtenerMaterias();
        console.log('Materias obtenidas:', materias);
        const materiasNombres = materias
            .filter(m => materiasIds.includes(m.id))
            .map(m => m.nombre)
            .join(', ');
        
        const materiasBadgeElement = document.getElementById('materiasBadge');
        if (materiasBadgeElement) {
            materiasBadgeElement.textContent = materiasNombres;
        }
        
        // Crear examen en la base de datos
        console.log('Obteniendo usuario actual...');
        const user = getCurrentUser();
        if (!user || !user.userId) {
            console.error('No se pudo obtener información del usuario');
            alert('Error: No se pudo obtener información del usuario. Redirigiendo...');
            window.location.href = 'index.html';
            return;
        }
        
        console.log('Creando examen en BD...');
        const examen = await crearExamen(user.userId, materiasIds, preguntasExamen.length);
        console.log('Examen creado:', examen);
        examenId = examen.id;
        
        // Inicializar respuestas
        preguntasExamen.forEach((pregunta, index) => {
            respuestasUsuario[index] = null;
        });
        
        // Mostrar primera pregunta
        mostrarPregunta(0);
        
        // Event listeners
        document.getElementById('prevBtn').addEventListener('click', () => {
            if (preguntaActual > 0) {
                guardarRespuesta();
                mostrarPregunta(preguntaActual - 1);
            }
        });
        
        document.getElementById('nextBtn').addEventListener('click', () => {
            guardarRespuesta();
            if (preguntaActual < preguntasExamen.length - 1) {
                mostrarPregunta(preguntaActual + 1);
            } else {
                finalizarExamen();
            }
        });
        
        document.getElementById('finishBtn').addEventListener('click', () => {
            guardarRespuesta();
            finalizarExamen();
        });
    } catch (error) {
        console.error('Error al inicializar examen:', error);
        console.error('Error completo:', JSON.stringify(error, null, 2));
        console.error('Stack trace:', error.stack);
        
        let mensajeError = 'Error al cargar el examen. Por favor, intenta de nuevo.';
        
        if (error.message) {
            if (error.message.includes('No se encontraron preguntas')) {
                mensajeError = 'No se encontraron preguntas para las materias seleccionadas. Verifica que existan preguntas en la base de datos.';
            } else if (error.message.includes('permission') || error.message.includes('policy')) {
                mensajeError = 'Error de permisos: No tienes acceso para crear exámenes. Verifica las políticas RLS en Supabase.';
            } else {
                mensajeError = `Error: ${error.message}`;
            }
        }
        
        alert(mensajeError);
        console.error('Redirigiendo a materias.html debido al error...');
        window.location.href = 'materias.html';
    }
}

function guardarRespuesta() {
    const opciones = document.querySelectorAll('.option-radio:checked');
    if (opciones.length > 0) {
        respuestasUsuario[preguntaActual] = opciones[0].value; // Guardar 'A', 'B', 'C', o 'D'
    }
}

function mostrarPregunta(index) {
    preguntaActual = index;
    const pregunta = preguntasExamen[index];
    
    // Extraer el tema de la pregunta si está en el formato "Pregunta-Tema X: ..."
    let temaTexto = '';
    let textoPregunta = pregunta.pregunta;
    
    if (pregunta.pregunta && pregunta.pregunta.includes('Pregunta-Tema')) {
        // Extraer el tema (ej: "Pregunta-Tema 1: ..." -> "Tema 1")
        const matchTema = pregunta.pregunta.match(/Pregunta-Tema\s*(\d+)/i);
        if (matchTema) {
            temaTexto = `Tema ${matchTema[1]}`;
            // Remover el prefijo del tema del texto de la pregunta
            textoPregunta = pregunta.pregunta.replace(/Pregunta-Tema\s*\d+:\s*/i, '').trim();
        }
    }
    
    // Actualizar información
    document.getElementById('currentQuestion').textContent = index + 1;
    document.getElementById('totalQuestions').textContent = preguntasExamen.length;
    document.getElementById('questionNumber').textContent = index + 1;
    
    // Mostrar el tema si existe
    const questionTopicElement = document.getElementById('questionTopic');
    if (questionTopicElement) {
        if (temaTexto) {
            questionTopicElement.textContent = temaTexto;
            questionTopicElement.style.display = 'inline-block';
        } else {
            questionTopicElement.style.display = 'none';
        }
    }
    
    // Mostrar el texto de la pregunta (sin el prefijo del tema)
    document.getElementById('questionText').textContent = textoPregunta || pregunta.pregunta;
    
    // Mostrar opciones (convertir respuesta_correcta a índice si es texto)
    const optionsContainer = document.getElementById('optionsContainer');
    optionsContainer.innerHTML = '';
    
    const opciones = [
        pregunta.opcion_a,
        pregunta.opcion_b,
        pregunta.opcion_c,
        pregunta.opcion_d
    ];
    
    // Convertir respuesta_correcta de texto ('A', 'B', 'C', 'D') a índice (0, 1, 2, 3)
    const respuestaCorrectaIndex = pregunta.respuesta_correcta.toUpperCase().charCodeAt(0) - 65;
    
    opciones.forEach((opcion, i) => {
        const optionDiv = document.createElement('div');
        optionDiv.className = 'option-item';
        
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'opcion';
        radio.value = String.fromCharCode(65 + i); // 'A', 'B', 'C', 'D'
        radio.id = `opcion-${i}`;
        radio.className = 'option-radio';
        
        // Guardar el índice correcto en la pregunta para comparación
        if (!pregunta.respuestaCorrectaIndex) {
            pregunta.respuestaCorrectaIndex = respuestaCorrectaIndex;
        }
        
        if (respuestasUsuario[index] === radio.value) {
            radio.checked = true;
        }
        
        const label = document.createElement('label');
        label.htmlFor = `opcion-${i}`;
        label.textContent = opcion;
        
        optionDiv.appendChild(radio);
        optionDiv.appendChild(label);
        optionsContainer.appendChild(optionDiv);
    });
    
    // Actualizar botones
    document.getElementById('prevBtn').disabled = index === 0;
    
    if (index === preguntasExamen.length - 1) {
        document.getElementById('nextBtn').style.display = 'none';
        document.getElementById('finishBtn').style.display = 'inline-block';
    } else {
        document.getElementById('nextBtn').style.display = 'inline-block';
        document.getElementById('finishBtn').style.display = 'none';
    }
    
    // Actualizar barra de progreso
    const progress = ((index + 1) / preguntasExamen.length) * 100;
    document.getElementById('progressFill').style.width = `${progress}%`;
}

async function finalizarExamen() {
    guardarRespuesta();
    
    try {
        // Preparar respuestas para guardar en la base de datos
        const respuestasParaGuardar = preguntasExamen.map((pregunta, index) => ({
            pregunta_id: pregunta.id,
            respuesta_usuario: respuestasUsuario[index] || null
        }));
        
        // Guardar respuestas en la base de datos
        await guardarRespuestas(examenId, respuestasParaGuardar);
        
        // Calcular resultados
        let correctas = 0;
        const resultados = [];
        
        preguntasExamen.forEach((pregunta, index) => {
            const respuestaUsuario = respuestasUsuario[index];
            const respuestaCorrecta = pregunta.respuesta_correcta.toUpperCase();
            const esCorrecta = respuestaUsuario && respuestaUsuario.toUpperCase() === respuestaCorrecta;
            
            if (esCorrecta) {
                correctas++;
            }
            
            resultados.push({
                pregunta: pregunta.pregunta,
                opciones: {
                    A: pregunta.opcion_a,
                    B: pregunta.opcion_b,
                    C: pregunta.opcion_c,
                    D: pregunta.opcion_d
                },
                respuestaCorrecta: respuestaCorrecta,
                respuestaUsuario: respuestaUsuario || null,
                esCorrecta: esCorrecta,
                materia_id: pregunta.materia_id
            });
        });
        
        const porcentaje = Math.round((correctas / preguntasExamen.length) * 100);
        
        // Actualizar calificación en la base de datos
        await actualizarCalificacion(examenId, porcentaje);
        
        // Guardar resultados en sessionStorage para mostrar en la página de resultados
        sessionStorage.setItem('resultadosExamen', JSON.stringify({
            examenId: examenId,
            total: preguntasExamen.length,
            correctas: correctas,
            incorrectas: preguntasExamen.length - correctas,
            porcentaje: porcentaje,
            resultados: resultados
        }));
        
        // Redirigir a resultados
        window.location.href = 'resultado.html';
    } catch (error) {
        console.error('Error al finalizar examen:', error);
        alert('Error al guardar el examen. Por favor, intenta de nuevo.');
    }
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', initExam);

