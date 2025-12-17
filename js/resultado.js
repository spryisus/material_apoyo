// js/resultado.js
import { supabase } from './supabase.js';
import { checkAuth } from './aut.js';

// Verificar autenticación
async function checkAuthAndRedirect() {
    const session = await checkAuth();
    if (!session) {
        window.location.href = 'index.html';
        return false;
    }
    return true;
}

// Cargar resultados
function loadResults() {
    const resultadosStr = sessionStorage.getItem('resultadosExamen');
    if (!resultadosStr) {
        alert('No hay resultados disponibles. Redirigiendo...');
        window.location.href = 'materias.html';
        return;
    }
    
    const resultados = JSON.parse(resultadosStr);
    
    // Mostrar estadísticas
    document.getElementById('score').textContent = `${resultados.correctas}/${resultados.total}`;
    document.getElementById('correct').textContent = resultados.correctas;
    document.getElementById('incorrect').textContent = resultados.incorrectas;
    document.getElementById('percentage').textContent = `${resultados.porcentaje}%`;
    
    // Mostrar detalles
    const resultDetails = document.getElementById('resultDetails');
    resultDetails.innerHTML = '<h3>Detalle de Respuestas</h3>';
    
    resultados.resultados.forEach((resultado, index) => {
        const detailCard = document.createElement('div');
        detailCard.className = `detail-card ${resultado.esCorrecta ? 'correct' : 'incorrect'}`;
        
        const icon = resultado.esCorrecta ? '✅' : '❌';
        const status = resultado.esCorrecta ? 'Correcta' : 'Incorrecta';
        
        detailCard.innerHTML = `
            <div class="detail-header">
                <span class="detail-icon">${icon}</span>
                <span class="detail-status">${status}</span>
                <span class="detail-number">Pregunta ${index + 1}</span>
            </div>
            <div class="detail-question">${resultado.pregunta}</div>
            <div class="detail-info">
                ${resultado.materia_id ? `<div class="detail-materia">Materia ID: ${resultado.materia_id}</div>` : ''}
                <div class="detail-answers">
                    <div class="answer-item ${!resultado.esCorrecta ? 'selected' : ''}">
                        <strong>Tu respuesta:</strong> ${resultado.respuestaUsuario !== null ? (resultado.opciones[resultado.respuestaUsuario] || 'Sin responder') : 'Sin responder'}
                    </div>
                    ${!resultado.esCorrecta ? `
                        <div class="answer-item correct-answer">
                            <strong>Respuesta correcta:</strong> ${resultado.opciones[resultado.respuestaCorrecta]}
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
        
        resultDetails.appendChild(detailCard);
    });
    
    // Event listeners
    // Función para volver a selección de materias
    function volverAMaterias() {
        sessionStorage.removeItem('resultadosExamen');
        window.location.href = 'materias.html';
    }
    
    // Botón en el header
    const backToMateriasBtn = document.getElementById('backToMateriasBtn');
    if (backToMateriasBtn) {
        backToMateriasBtn.addEventListener('click', volverAMaterias);
    }
    
    // Botón en actions (cambiar el texto)
    document.getElementById('newExamBtn').addEventListener('click', volverAMaterias);
    
    // Botón de revisar respuestas
    document.getElementById('reviewBtn').addEventListener('click', () => {
        // Scroll a la primera pregunta incorrecta
        const firstIncorrect = document.querySelector('.detail-card.incorrect');
        if (firstIncorrect) {
            firstIncorrect.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            // Si no hay incorrectas, mostrar un mensaje
            alert('¡Felicitaciones! Respondiste todas las preguntas correctamente. 🎉');
        }
    });
}

// Inicializar
document.addEventListener('DOMContentLoaded', async () => {
    const isAuthenticated = await checkAuthAndRedirect();
    if (isAuthenticated) {
        loadResults();
    }
});

