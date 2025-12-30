// js/materias.js
import { supabase } from './supabase.js';
import { logout, obtenerUsuario, checkAuth, getCurrentUser, esAdmin } from './aut.js';
import { obtenerMaterias } from './database.js';
import { obtenerIconoMateria } from './materia-icons.js';

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
        
        if (materias.length === 0) {
            materiasGrid.innerHTML = '<p>No hay materias disponibles. Por favor, contacta al administrador.</p>';
            return;
        }
        
        materias.forEach(materia => {
            const materiaCard = document.createElement('div');
            materiaCard.className = 'materia-card';
            materiaCard.dataset.materiaId = materia.id;
            
            // Obtener icono específico para la materia
            const icono = obtenerIconoMateria(materia.nombre);
            
            materiaCard.innerHTML = `
                <div class="materia-label" style="cursor: pointer;">
                    <div class="materia-icon">${icono}</div>
                    <div class="materia-name">${materia.nombre}</div>
                </div>
            `;
            
            // Al hacer clic en la tarjeta, redirigir a la página de temas
            materiaCard.addEventListener('click', () => {
                // Guardar el ID de la materia seleccionada en sessionStorage
                sessionStorage.setItem('materiaSeleccionada', JSON.stringify({
                    id: materia.id,
                    nombre: materia.nombre
                }));
                window.location.href = 'temas.html';
            });
            
            materiasGrid.appendChild(materiaCard);
        });
    } catch (error) {
        console.error('Error al cargar materias:', error);
        document.getElementById('materiasGrid').innerHTML = 
            '<p class="error-message">Error al cargar las materias. Por favor, recarga la página.</p>';
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
        
        // Botón de administración (solo para admins)
        const adminBtn = document.getElementById('adminBtn');
        if (adminBtn) {
            if (esAdmin()) {
                adminBtn.style.display = 'inline-block';
                adminBtn.addEventListener('click', () => {
                    window.location.href = 'admin.html';
                });
            } else {
                adminBtn.style.display = 'none';
            }
        }
        
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

