// js/aut.js
import { supabase } from './supabase.js';

// Utilidad para hacer hash de contraseñas usando Web Crypto API
async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hash = await crypto.subtle.digest('SHA-256', data);
    return Array.from(new Uint8Array(hash))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
}

// Verificar si el usuario ya está autenticado
async function checkAuth() {
    try {
        const sessionData = localStorage.getItem('userSession');
        if (!sessionData) {
            console.log('checkAuth: No hay sesión en localStorage');
            return null;
        }
        
        const session = JSON.parse(sessionData);
        console.log('checkAuth: Sesión encontrada en localStorage:', session);
        
        // Validar que la sesión tenga los datos mínimos necesarios
        if (!session || !session.userId || !session.email) {
            console.warn('checkAuth: Sesión inválida - faltan datos necesarios');
            localStorage.removeItem('userSession');
            return null;
        }
        
        // Verificar que la sesión no sea muy antigua (opcional, pero recomendado)
        if (session.loginTime) {
            const loginTime = new Date(session.loginTime);
            const now = new Date();
            const hoursSinceLogin = (now - loginTime) / (1000 * 60 * 60);
            
            // Si la sesión tiene más de 30 días, considerarla expirada
            if (hoursSinceLogin > 24 * 30) {
                console.warn('checkAuth: Sesión expirada por tiempo');
                localStorage.removeItem('userSession');
                return null;
            }
        }
        
        // NO verificar en BD de inmediato para evitar loops y mejorar rendimiento
        // La verificación en BD se puede hacer de forma asíncrona después
        console.log('checkAuth: Sesión válida, retornando sesión local');
        return session;
        
    } catch (error) {
        console.error('checkAuth: Error al verificar sesión:', error);
        // No eliminar la sesión por error de parseo, intentar retornar null
        try {
            localStorage.removeItem('userSession');
        } catch {
            // Ignorar error al limpiar
        }
        return null;
    }
}

// Variable para prevenir múltiples redirecciones
let redirecting = false;

// Verificar si el usuario ya está autenticado (para index.html - redirigir si está logueado)
async function checkAuthAndRedirect() {
    // Solo ejecutar si estamos en index.html
    if (!window.location.pathname.includes('index.html') && !window.location.pathname.endsWith('/')) {
        console.log('checkAuthAndRedirect: No estamos en index.html, ignorando...');
        return;
    }
    
    // Prevenir múltiples redirecciones simultáneas
    if (redirecting) {
        console.log('checkAuthAndRedirect: Ya se está redirigiendo, ignorando...');
        return;
    }
    
    try {
        const session = await checkAuth();
        if (session) {
            redirecting = true;
            console.log('checkAuthAndRedirect: Sesión encontrada, redirigiendo a materias.html...');
            // Usar replace para no crear entrada en el historial
            window.location.replace('materias.html');
        }
    } catch (error) {
        console.error('Error en checkAuthAndRedirect:', error);
        redirecting = false;
    }
}

// Iniciar sesión
async function login(email, password) {
    try {
        // Limpiar email
        const emailLimpio = email.trim().toLowerCase();
        
        // Buscar usuario por email
        const { data: usuario, error: selectError } = await supabase
            .from('usuarios')
            .select('*')
            .eq('email', emailLimpio)
            .single();
        
        if (selectError || !usuario) {
            throw new Error('Email o contraseña incorrectos.');
        }
        
        // Verificar contraseña
        const passwordHash = await hashPassword(password);
        
        if (usuario.password_hash !== passwordHash) {
            // Si la contraseña está en texto plano (migración), compararla y actualizar
            if (usuario.password && usuario.password === password) {
                // Actualizar a hash
                await supabase
                    .from('usuarios')
                    .update({ password_hash: passwordHash })
                    .eq('id', usuario.id);
            } else {
                throw new Error('Email o contraseña incorrectos.');
            }
        }
        
        // Actualizar fecha de último acceso
        await supabase
            .from('usuarios')
            .update({ fecha_ultimo_acceso: new Date().toISOString() })
            .eq('id', usuario.id);
        
        // Crear sesión en localStorage
        const sessionData = {
            userId: usuario.id,
            email: usuario.email,
            nombre: usuario.nombre || null,
            apellido: usuario.apellido || null,
            loginTime: new Date().toISOString()
        };
        
        // Guardar sesión en localStorage
        try {
            localStorage.setItem('userSession', JSON.stringify(sessionData));
            console.log('Sesión guardada en localStorage:', sessionData);
            
            // Verificar que se guardó correctamente
            const verify = localStorage.getItem('userSession');
            if (!verify) {
                throw new Error('No se pudo guardar la sesión en localStorage');
            }
        } catch (storageError) {
            console.error('Error al guardar sesión en localStorage:', storageError);
            throw new Error('Error al guardar la sesión. Por favor, verifica que localStorage esté habilitado.');
        }
        
        return { user: usuario, session: sessionData };
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
}

// Registrar nuevo usuario
async function register(email, password, nombre = '', apellido = '') {
    try {
        // Limpiar email
        const emailLimpio = email.trim().toLowerCase();
        
        // Verificar si el email ya existe
        const { data: existingUser, error: checkError } = await supabase
            .from('usuarios')
            .select('id')
            .eq('email', emailLimpio)
            .maybeSingle(); // Usar maybeSingle en lugar de single para evitar error si no existe
        
        if (checkError && checkError.code !== 'PGRST116') {
            // Si hay un error que NO es "no se encontraron resultados", lanzar error
            console.error('Error al verificar email existente:', checkError);
            throw new Error(`Error al verificar email: ${checkError.message || 'Desconocido'}. Revisa la consola para más detalles.`);
        }
        
        if (existingUser) {
            throw new Error('Este email ya está registrado. Por favor, inicia sesión o usa otro email.');
        }
        
        // Hashear contraseña
        const passwordHash = await hashPassword(password);
        
        // Generar ID único (UUID v4 simplificado)
        const userId = crypto.randomUUID ? crypto.randomUUID() : 
            'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                const r = Math.random() * 16 | 0;
                const v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        
        // Insertar usuario en la tabla usuarios
        const { data, error } = await supabase
            .from('usuarios')
            .insert({
                id: userId,
                email: emailLimpio,
                password_hash: passwordHash,
                nombre: nombre || null,
                apellido: apellido || null,
                fecha_registro: new Date().toISOString(),
                fecha_ultimo_acceso: new Date().toISOString()
            })
            .select()
            .single();
        
        if (error) {
            console.error('Error al crear usuario - Detalles completos:', error);
            console.error('Error code:', error.code);
            console.error('Error message:', error.message);
            console.error('Error details:', error.details);
            console.error('Error hint:', error.hint);
            
            // Mejorar mensajes de error específicos
            if (error.code === 'PGRST116' || error.message?.includes('does not exist') || error.message?.includes('column') && error.message?.includes('password_hash')) {
                throw new Error('Error: La tabla usuarios no tiene la columna password_hash. Por favor, ejecuta el script SQL ACTUALIZAR_TABLA_USUARIOS.sql en Supabase.');
            } else if (error.code === '42501' || error.message?.includes('permission denied') || error.message?.includes('policy')) {
                throw new Error('Error de permisos: Las políticas RLS no permiten registro. Ejecuta el script SQL ACTUALIZAR_TABLA_USUARIOS.sql para corregir las políticas.');
            } else if (error.code === '23505' || error.message?.includes('duplicate') || error.message?.includes('unique constraint')) {
                throw new Error('Este email ya está registrado. Por favor, inicia sesión o usa otro email.');
            } else if (error.message) {
                throw new Error(`Error al registrar: ${error.message}. Revisa la consola para más detalles.`);
            }
            throw new Error(`Error al registrar usuario: ${error.code || 'Desconocido'}. Revisa la consola del navegador (F12) para más detalles.`);
        }
        
        console.log('Usuario registrado exitosamente:', data);
        return { user: data };
    } catch (error) {
        console.error('Error completo en register:', error);
        throw error;
    }
}

// Actualizar fecha de último acceso
async function actualizarUltimoAcceso() {
    try {
        const session = await checkAuth();
        if (session && session.userId) {
            await supabase
                .from('usuarios')
                .update({ fecha_ultimo_acceso: new Date().toISOString() })
                .eq('id', session.userId);
        }
    } catch (error) {
        console.warn('Error al actualizar último acceso:', error);
    }
}

// Obtener información del usuario actual
async function obtenerUsuario() {
    try {
        const session = await checkAuth();
        if (!session) return null;
        
        const { data, error } = await supabase
            .from('usuarios')
            .select('id, email, nombre, apellido, fecha_registro, fecha_ultimo_acceso')
            .eq('id', session.userId)
            .single();
        
        if (error) {
            console.error('Error al obtener usuario:', error);
            return null;
        }
        
        return data;
    } catch (error) {
        console.error('Error en obtenerUsuario:', error);
        return null;
    }
}

// Obtener usuario actual (más simple, devuelve datos de sesión)
function getCurrentUser() {
    try {
        const sessionData = localStorage.getItem('userSession');
        if (sessionData) {
            return JSON.parse(sessionData);
        }
        return null;
    } catch (error) {
        console.error('Error al obtener usuario actual:', error);
        return null;
    }
}

// Actualizar información del usuario
async function actualizarUsuario(datos) {
    try {
        const session = await checkAuth();
        if (!session) throw new Error('Usuario no autenticado');
        
        // No permitir actualizar ID o email directamente
        const { id, email, password_hash, ...datosPermitidos } = datos;
        
        const { data, error } = await supabase
            .from('usuarios')
            .update(datosPermitidos)
            .eq('id', session.userId)
            .select()
            .single();
        
        if (error) {
            throw error;
        }
        
        // Actualizar sesión si se actualizó nombre o apellido
        if (datosPermitidos.nombre || datosPermitidos.apellido) {
            const updatedSession = { ...session };
            if (datosPermitidos.nombre !== undefined) updatedSession.nombre = datosPermitidos.nombre;
            if (datosPermitidos.apellido !== undefined) updatedSession.apellido = datosPermitidos.apellido;
            localStorage.setItem('userSession', JSON.stringify(updatedSession));
        }
        
        return data;
    } catch (error) {
        console.error('Error en actualizarUsuario:', error);
        throw error;
    }
}

// Cerrar sesión
async function logout() {
    try {
        localStorage.removeItem('userSession');
        return true;
    } catch (error) {
        console.error('Error en logout:', error);
        throw error;
    }
}

// Variable para prevenir múltiples inicializaciones
let autInitialized = false;

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Prevenir múltiples inicializaciones
    if (autInitialized) {
        console.log('aut.js: Ya inicializado, ignorando...');
        return;
    }
    
    autInitialized = true;
    
    // Solo verificar autenticación si estamos en index.html
    if (window.location.pathname.includes('index.html') || window.location.pathname.endsWith('/')) {
        checkAuthAndRedirect();
    }
    
    const loginForm = document.getElementById('loginForm');
    const registerLink = document.getElementById('registerLink');
    const errorMessage = document.getElementById('errorMessage');
    
    let isRegisterMode = false;
    
    // Función para validar email
    function validarEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMessage.style.display = 'none';
        errorMessage.style.color = ''; // Resetear color
        
        // Obtener el botón de submit
        const submitButton = loginForm.querySelector('button[type="submit"]');
        const originalButtonText = submitButton.textContent;
        
        // Limpiar y obtener valores
        const email = document.getElementById('email').value.trim().toLowerCase();
        const password = document.getElementById('password').value;
        
        // Validar email
        if (!validarEmail(email)) {
            errorMessage.textContent = 'Por favor, ingresa un email válido.';
            errorMessage.style.display = 'block';
            return;
        }
        
        // Validar contraseña
        if (password.length < 6) {
            errorMessage.textContent = 'La contraseña debe tener al menos 6 caracteres.';
            errorMessage.style.display = 'block';
            return;
        }
        
        // Mostrar indicador de carga
        submitButton.disabled = true;
        submitButton.textContent = 'Cargando...';
        submitButton.style.opacity = '0.7';
        submitButton.style.cursor = 'not-allowed';
        
        try {
            if (isRegisterMode) {
                const nombre = document.getElementById('nombre').value.trim();
                const apellido = document.getElementById('apellido').value.trim();
                
                console.log('Iniciando registro...');
                const result = await register(email, password, nombre, apellido);
                console.log('Registro completado:', result);
                
                errorMessage.textContent = '¡Registro exitoso! Por favor inicia sesión.';
                errorMessage.style.display = 'block';
                errorMessage.style.color = 'green';
                isRegisterMode = false;
                registerLink.textContent = 'Regístrate aquí';
                submitButton.textContent = 'Iniciar Sesión';
                document.getElementById('nombreGroup').style.display = 'none';
                document.getElementById('apellidoGroup').style.display = 'none';
                // Limpiar formulario
                loginForm.reset();
            } else {
                console.log('Iniciando login...');
                const loginResult = await login(email, password);
                console.log('Login exitoso:', loginResult);
                
                // Verificar que la sesión se guardó correctamente
                const sessionCheck = localStorage.getItem('userSession');
                if (!sessionCheck) {
                    throw new Error('Error: La sesión no se guardó correctamente. Por favor, intenta nuevamente.');
                }
                
                console.log('Sesión guardada en localStorage, verificando...');
                const parsedSession = JSON.parse(sessionCheck);
                console.log('Sesión verificada:', parsedSession);
                
                // Pequeño delay para asegurar que localStorage se haya actualizado
                await new Promise(resolve => setTimeout(resolve, 100));
                
                console.log('Redirigiendo a materias.html...');
                window.location.href = 'materias.html';
                return; // No restaurar el botón porque estamos redirigiendo
            }
        } catch (error) {
            console.error('Error en autenticación:', error);
            console.error('Error completo:', JSON.stringify(error, null, 2));
            // Mejorar mensajes de error
            let mensajeError = 'Error al autenticar. Por favor, intenta nuevamente.';
            
            if (error && error.message) {
                // Si el mensaje ya es específico (de nuestras validaciones), usarlo directamente
                if (error.message.includes('password_hash') || error.message.includes('RLS') || error.message.includes('política')) {
                    mensajeError = error.message;
                } else if (error.message.includes('already registered') || error.message.includes('already exists')) {
                    mensajeError = 'Este email ya está registrado. Por favor, inicia sesión.';
                } else if (error.message.includes('invalid') && error.message.includes('email')) {
                    mensajeError = 'El formato del email no es válido. Por favor, verifica tu email.';
                } else if (error.message.includes('Invalid login credentials')) {
                    mensajeError = 'Email o contraseña incorrectos.';
                } else if (error.message.includes('Password')) {
                    mensajeError = 'La contraseña debe tener al menos 6 caracteres.';
                } else if (error.message.includes('network') || error.message.includes('fetch')) {
                    mensajeError = 'Error de conexión. Por favor, verifica tu internet e intenta nuevamente.';
                } else {
                    mensajeError = error.message || 'Error desconocido. Por favor, intenta nuevamente.';
                }
            } else if (error && typeof error === 'object') {
                // Mostrar información útil del error
                mensajeError = error.message || JSON.stringify(error);
            }
            
            errorMessage.textContent = mensajeError;
            errorMessage.style.display = 'block';
            errorMessage.style.color = 'red';
        } finally {
            // Restaurar el botón
            submitButton.disabled = false;
            submitButton.textContent = originalButtonText;
            submitButton.style.opacity = '1';
            submitButton.style.cursor = 'pointer';
        }
    });
    
    registerLink.addEventListener('click', (e) => {
        e.preventDefault();
        isRegisterMode = !isRegisterMode;
        if (isRegisterMode) {
            registerLink.textContent = 'Iniciar sesión';
            loginForm.querySelector('button').textContent = 'Registrarse';
            document.getElementById('nombreGroup').style.display = 'block';
            document.getElementById('apellidoGroup').style.display = 'block';
        } else {
            registerLink.textContent = 'Regístrate aquí';
            loginForm.querySelector('button').textContent = 'Iniciar Sesión';
            document.getElementById('nombreGroup').style.display = 'none';
            document.getElementById('apellidoGroup').style.display = 'none';
        }
    });
});

export { login, logout, checkAuth, checkAuthAndRedirect, register, obtenerUsuario, getCurrentUser, actualizarUsuario, actualizarUltimoAcceso };

