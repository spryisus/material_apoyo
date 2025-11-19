// js/materias.js
import { supabase } from './supabase.js';
import { logout, obtenerUsuario, checkAuth, getCurrentUser } from './aut.js';
import { obtenerMaterias } from './database.js';

// Variable para evitar múltiples verificaciones simultáneas
let checkingAuth = false;
let redirecting = false;

// Verificar autenticación (versión simplificada para materias.html)
function verifyAuth() {
    // Prevenir múltiples verificaciones
    if (checkingAuth || redirecting) {
        return null;
    }
    
    checkingAuth = true;
    
    try {
        // Verificar localStorage directamente (síncrono, más rápido)
        const sessionData = localStorage.getItem('userSession');
        
        if (!sessionData) {
            checkingAuth = false;
            if (!redirecting) {
                redirecting = true;
                window.location.replace('index.html');
            }
            return null;
        }
        
        // Parsear sesión
        const session = JSON.parse(sessionData);
        
        // Validar sesión básica
        if (!session || !session.userId || !session.email) {
            localStorage.removeItem('userSession');
            checkingAuth = false;
            if (!redirecting) {
                redirecting = true;
                window.location.replace('index.html');
            }
            return null;
        }
        
        checkingAuth = false;
        return session;
        
    } catch (error) {
        console.error('Error al verificar autenticación:', error);
        localStorage.removeItem('userSession');
        checkingAuth = false;
        if (!redirecting) {
            redirecting = true;
            window.location.replace('index.html');
        }
        return null;
    }
}

// Cargar información del usuario
async function loadUserInfo() {
    try {
        // Verificar autenticación de forma síncrona primero
        const session = verifyAuth();
        if (!session) {
            // Si no hay sesión, verifyAuth ya redirigió
            return;
        }
        
        // Mostrar nombre desde la sesión directamente (más rápido)
        const userNameElement = document.getElementById('userName');
        if (userNameElement) {
            let userName = '';
            if (session.nombre || session.apellido) {
                userName = ` ${session.nombre || ''} ${session.apellido || ''}`.trim();
            } else {
                userName = ` ${session.email?.split('@')[0] || 'Usuario'}`;
            }
            userNameElement.textContent = userName;
        }
        
        // Intentar actualizar con datos más recientes de la BD (async, no bloquea)
        try {
            const usuario = await obtenerUsuario();
            if (usuario && userNameElement) {
                let userName = '';
                if (usuario.nombre || usuario.apellido) {
                    userName = ` ${usuario.nombre || ''} ${usuario.apellido || ''}`.trim();
                } else {
                    userName = ` ${usuario.email?.split('@')[0] || session.email?.split('@')[0] || 'Usuario'}`;
                }
                userNameElement.textContent = userName;
            }
        } catch (error) {
            // Si falla obtener de BD, usar datos de sesión (ya se mostraron arriba)
            console.warn('No se pudo obtener datos actualizados de BD, usando sesión local:', error);
        }
    } catch (error) {
        console.error('Error al cargar información del usuario:', error);
    }
}

// Cargar materias disponibles desde la base de datos
async function loadMaterias() {
    try {
        const materias = await obtenerMaterias();
        const materiasGrid = document.getElementById('materiasGrid');
        const selectedMaterias = new Set();
        
        // Actualizar el total de materias dinámicamente
        const totalMateriasElement = document.getElementById('totalMaterias');
        if (totalMateriasElement) {
            totalMateriasElement.textContent = materias.length;
        }
        
        if (materias.length === 0) {
            materiasGrid.innerHTML = '<p>No hay materias disponibles. Por favor, contacta al administrador.</p>';
            if (totalMateriasElement) {
                totalMateriasElement.textContent = '0';
            }
            return;
        }
        
        materias.forEach(materia => {
            const materiaCard = document.createElement('div');
            materiaCard.className = 'materia-card';
            materiaCard.dataset.materiaId = materia.id;
            
            materiaCard.innerHTML = `
                <input type="checkbox" id="materia-${materia.id}" class="materia-checkbox">
                <label for="materia-${materia.id}" class="materia-label">
                    <div class="materia-icon">📚</div>
                    <div class="materia-name">${materia.nombre}</div>
                </label>
            `;
            
            const checkbox = materiaCard.querySelector('.materia-checkbox');
            checkbox.addEventListener('change', (e) => {
                if (e.target.checked) {
                    selectedMaterias.add(materia.id);
                    materiaCard.classList.add('selected');
                } else {
                    selectedMaterias.delete(materia.id);
                    materiaCard.classList.remove('selected');
                }
                
                updateSelectionInfo(selectedMaterias.size);
            });
            
            materiasGrid.appendChild(materiaCard);
        });
        
        // Botón para iniciar examen
        document.getElementById('startExamBtn').addEventListener('click', () => {
            if (selectedMaterias.size > 0) {
                // Guardar IDs de materias seleccionadas en sessionStorage
                sessionStorage.setItem('materiasSeleccionadas', JSON.stringify(Array.from(selectedMaterias)));
                window.location.href = 'examen.html';
            }
        });
    } catch (error) {
        console.error('Error al cargar materias:', error);
        document.getElementById('materiasGrid').innerHTML = 
            '<p class="error-message">Error al cargar las materias. Por favor, recarga la página.</p>';
        
        // Si hay error, mostrar 0 en el total
        const totalMateriasElement = document.getElementById('totalMaterias');
        if (totalMateriasElement) {
            totalMateriasElement.textContent = '0';
        }
    }
}

function updateSelectionInfo(count) {
    document.getElementById('selectedCount').textContent = count;
    const startBtn = document.getElementById('startExamBtn');
    if (count > 0) {
        startBtn.disabled = false;
    } else {
        startBtn.disabled = true;
    }
}

// Variable para evitar múltiples inicializaciones
let pageInitialized = false;

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
    // Evitar múltiples inicializaciones
    if (pageInitialized) {
        console.log('materias.js: Página ya inicializada, ignorando...');
        return;
    }
    
    pageInitialized = true;
    console.log('materias.js: Inicializando página...');
    
    try {
        await loadUserInfo();
        loadMaterias();
        
        // Botón de cerrar sesión
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', async () => {
                try {
                    await logout();
                    window.location.replace('index.html');
                } catch (error) {
                    console.error('Error al cerrar sesión:', error);
                }
            });
        }
    } catch (error) {
        console.error('Error al inicializar página:', error);
        pageInitialized = false;
    }
});

