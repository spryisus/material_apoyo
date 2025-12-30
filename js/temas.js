// js/temas.js
import { supabase } from './supabase.js';
import { logout, obtenerUsuario, checkAuth, getCurrentUser } from './aut.js';
import { obtenerTemasPorMateria, obtenerPreguntas, obtenerConfiguracionPDF, obtenerPDFMateria } from './database.js';

// Variable para evitar múltiples verificaciones simultáneas
let checkingAuth = false;
let redirecting = false;

// Verificar autenticación
function verifyAuth() {
    if (checkingAuth || redirecting) {
        return null;
    }
    
    checkingAuth = true;
    
    try {
        const sessionData = localStorage.getItem('userSession');
        
        if (!sessionData) {
            checkingAuth = false;
            if (!redirecting) {
                redirecting = true;
                window.location.replace('index.html');
            }
            return null;
        }
        
        const session = JSON.parse(sessionData);
        
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

// Cargar temas de la materia seleccionada
async function loadTemas() {
    try {
        // Obtener la materia seleccionada del sessionStorage
        const materiaData = sessionStorage.getItem('materiaSeleccionada');
        
        if (!materiaData) {
            // Si no hay materia seleccionada, redirigir a materias
            window.location.href = 'materias.html';
            return;
        }
        
        const materia = JSON.parse(materiaData);
        
        // Mostrar el nombre de la materia
        const materiaTitleElement = document.getElementById('materiaTitle');
        if (materiaTitleElement) {
            materiaTitleElement.textContent = `Temas de ${materia.nombre}`;
        }
        
        // Obtener temas de la materia
        const temas = await obtenerTemasPorMateria(materia.id);
        const temasGrid = document.getElementById('temasGrid');
        
        if (temas.length === 0) {
            temasGrid.innerHTML = '<p>No hay temas disponibles para esta materia.</p>';
            return;
        }
        
        // Crear tarjetas para cada tema
        temas.forEach(tema => {
            const temaCard = document.createElement('div');
            temaCard.className = 'materia-card';
            temaCard.dataset.temaId = tema.id;
            
            temaCard.innerHTML = `
                <div class="materia-label" style="cursor: pointer;">
                    <div class="materia-icon">📖</div>
                    <div class="materia-name">${tema.nombre}</div>
                </div>
            `;
            
            // Al hacer clic en la tarjeta, mostrar el contenido del tema
            temaCard.addEventListener('click', async () => {
                await mostrarContenidoTema(materia.id, tema);
            });
            
            temasGrid.appendChild(temaCard);
        });
        
    } catch (error) {
        console.error('Error al cargar temas:', error);
        const temasGrid = document.getElementById('temasGrid');
        if (temasGrid) {
            temasGrid.innerHTML = 
                '<p class="error-message">Error al cargar los temas. Por favor, recarga la página.</p>';
        }
    }
}

// Mostrar contenido del tema (PDF)
async function mostrarContenidoTema(materiaId, tema) {
    try {
        // Obtener configuración desde la base de datos
        const config = await obtenerConfiguracionPDF(materiaId);
        const temaConfig = config.find(c => c.tema_numero === tema.numero);
        
        if (!temaConfig) {
            alert('No hay configuración de páginas para este tema. Por favor, contacta al administrador.');
            return;
        }
        
        const paginas = {
            inicio: temaConfig.pagina_inicio,
            fin: temaConfig.pagina_fin
        };
        
        // Buscar URL de YouTube en el nombre del tema o en video_url
        let videoUrl = temaConfig.video_url || null;
        let nombreTema = temaConfig.tema_nombre;
        
        // Si no hay video_url pero el nombre contiene una URL de YouTube, extraerla
        if (!videoUrl) {
            const videoInfo = extraerURLYouTube(temaConfig.tema_nombre);
            if (videoInfo.url) {
                videoUrl = videoInfo.url;
                nombreTema = videoInfo.textoLimpio || nombreTema;
            }
        }
        
        // Obtener URL del PDF de la materia
        const pdfInfo = await obtenerPDFMateria(materiaId);
        if (!pdfInfo) {
            alert('No se encontró el PDF para esta materia. Por favor, contacta al administrador.');
            return;
        }
        
        // Mostrar modal con el PDF y video (si existe)
        await mostrarModalPDF({ ...tema, nombre: nombreTema }, paginas, pdfInfo.url, videoUrl);
        
    } catch (error) {
        console.error('Error al obtener contenido del tema:', error);
        alert('Error al cargar el contenido del tema. Por favor, intenta de nuevo.');
    }
}

// Función helper para detectar y extraer URL de YouTube de un texto
function extraerURLYouTube(texto) {
    if (!texto) return { url: null, textoLimpio: texto };
    
    // Patrones para detectar URLs de YouTube
    const patterns = [
        /(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
        /(https?:\/\/)?(www\.)?youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})/
    ];
    
    for (const pattern of patterns) {
        const match = texto.match(pattern);
        if (match) {
            const videoId = match[4] || match[3];
            const urlCompleta = match[0];
            const textoLimpio = texto.replace(urlCompleta, '').trim();
            return {
                url: `https://www.youtube.com/embed/${videoId}`,
                textoLimpio: textoLimpio
            };
        }
    }
    
    return { url: null, textoLimpio: texto };
}

// Función helper para convertir URL de YouTube a formato embed (mantener compatibilidad)
function convertirYouTubeAEmbed(url) {
    if (!url) return null;
    
    // Si ya es una URL embed, retornarla
    if (url.includes('/embed/')) {
        return url;
    }
    
    // Patrones comunes de YouTube
    const patterns = [
        /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
        /youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})/
    ];
    
    for (const pattern of patterns) {
        const match = url.match(pattern);
        if (match && match[1]) {
            return `https://www.youtube.com/embed/${match[1]}`;
        }
    }
    
    return null;
}

// Mostrar modal con el PDF del tema y video (si existe)
async function mostrarModalPDF(tema, paginas, pdfUrl, videoUrl = null) {
    // Verificar que PDF.js esté cargado
    if (typeof pdfjsLib === 'undefined') {
        alert('Error: PDF.js no está cargado. Por favor, recarga la página.');
        return;
    }
    
    // Configurar PDF.js worker
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    
    // Crear overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        padding: 1rem;
    `;
    
    // Crear modal
    const modal = document.createElement('div');
    modal.className = 'modal-content';
    modal.style.cssText = `
        background: white;
        border-radius: 1rem;
        padding: 1.5rem;
        max-width: 95%;
        width: 100%;
        max-height: 95vh;
        display: flex;
        flex-direction: column;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    `;
    
    // Header del modal
    const header = document.createElement('div');
    header.style.cssText = `
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--border-color);
    `;
    header.innerHTML = `
        <h2 style="margin: 0; color: var(--primary-color);">${tema.nombre}</h2>
        <button id="closeModalBtn" class="btn btn-secondary" style="padding: 0.5rem 1rem;">Cerrar</button>
    `;
    
    // Contenedor principal del contenido
    const contentContainer = document.createElement('div');
    contentContainer.style.cssText = `
        flex: 1;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 2rem;
        padding: 1rem 0;
    `;
    
    // Contenedor para el video (si existe)
    if (videoUrl) {
        const videoEmbedUrl = convertirYouTubeAEmbed(videoUrl);
        if (videoEmbedUrl) {
            const videoSection = document.createElement('div');
            videoSection.style.cssText = `
                width: 100%;
                margin-bottom: 1rem;
            `;
            
            const videoTitle = document.createElement('h3');
            videoTitle.textContent = '📹 Video de Apoyo';
            videoTitle.style.cssText = `
                margin: 0 0 1rem 0;
                color: var(--primary-color);
                font-size: 1.2rem;
            `;
            
            const videoWrapper = document.createElement('div');
            videoWrapper.style.cssText = `
                position: relative;
                padding-bottom: 56.25%; /* 16:9 aspect ratio */
                height: 0;
                overflow: hidden;
                border-radius: 0.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            `;
            
            const iframe = document.createElement('iframe');
            iframe.src = videoEmbedUrl;
            iframe.style.cssText = `
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                border: none;
            `;
            iframe.setAttribute('allow', 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
            iframe.setAttribute('allowfullscreen', 'true');
            
            videoWrapper.appendChild(iframe);
            videoSection.appendChild(videoTitle);
            videoSection.appendChild(videoWrapper);
            contentContainer.appendChild(videoSection);
        }
    }
    
    // Contenedor del PDF
    const pdfSection = document.createElement('div');
    pdfSection.style.cssText = `
        width: 100%;
    `;
    
    // Título de la sección PDF (solo si hay video)
    if (videoUrl) {
        const pdfTitle = document.createElement('h3');
        pdfTitle.textContent = '📄 Material de Estudio';
        pdfTitle.style.cssText = `
            margin: 0 0 1rem 0;
            color: var(--primary-color);
            font-size: 1.2rem;
        `;
        pdfSection.appendChild(pdfTitle);
    }
    
    const pdfContainer = document.createElement('div');
    pdfContainer.id = 'pdfContainer';
    pdfContainer.style.cssText = `
        width: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    `;
    
    // Mensaje de carga
    pdfContainer.innerHTML = `
        <div style="text-align: center; padding: 2rem;">
            <p style="color: var(--text-secondary);">Cargando contenido...</p>
        </div>
    `;
    
    pdfSection.appendChild(pdfContainer);
    contentContainer.appendChild(pdfSection);
    modal.appendChild(header);
    modal.appendChild(contentContainer);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    
    // Cargar y mostrar las páginas del PDF
    try {
        await cargarPaginasPDF(pdfContainer, paginas, pdfUrl);
    } catch (error) {
        console.error('Error al cargar PDF:', error);
        pdfContainer.innerHTML = `
            <div style="text-align: center; padding: 2rem;">
                <p style="color: var(--danger-color);">Error al cargar el PDF. Por favor, verifica que el archivo existe.</p>
            </div>
        `;
    }
    
    // Cerrar modal al hacer clic en el botón
    const closeBtn = header.querySelector('#closeModalBtn');
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(overlay);
    });
    
    // Cerrar modal al hacer clic fuera del contenido
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            document.body.removeChild(overlay);
        }
    });
    
    // Cerrar con ESC
    const closeHandler = (e) => {
        if (e.key === 'Escape') {
            document.body.removeChild(overlay);
            document.removeEventListener('keydown', closeHandler);
        }
    };
    document.addEventListener('keydown', closeHandler);
}

// Cargar y renderizar las páginas del PDF
async function cargarPaginasPDF(container, paginas, pdfUrl) {
    if (typeof pdfjsLib === 'undefined') {
        throw new Error('PDF.js no está cargado');
    }
    
    try {
        // Cargar el PDF desde la URL
        const loadingTask = pdfjsLib.getDocument(pdfUrl);
        const pdf = await loadingTask.promise;
        
        // Limpiar contenedor
        container.innerHTML = '';
        
        // Renderizar cada página en el rango
        for (let pageNum = paginas.inicio; pageNum <= paginas.fin; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const viewport = page.getViewport({ scale: 1.5 });
            
            // Crear canvas para la página
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;
            canvas.style.cssText = `
                max-width: 100%;
                height: auto;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
                border: 1px solid var(--border-color);
            `;
            
            // Renderizar la página
            const renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            
            await page.render(renderContext).promise;
            
            // Agregar etiqueta de página
            const pageWrapper = document.createElement('div');
            pageWrapper.style.cssText = `
                display: flex;
                flex-direction: column;
                align-items: center;
                margin-bottom: 1.5rem;
            `;
            
            const pageLabel = document.createElement('p');
            pageLabel.textContent = `Página ${pageNum}`;
            pageLabel.style.cssText = `
                color: var(--text-secondary);
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            `;
            
            pageWrapper.appendChild(pageLabel);
            pageWrapper.appendChild(canvas);
            container.appendChild(pageWrapper);
        }
    } catch (error) {
        console.error('Error al cargar páginas del PDF:', error);
        throw error;
    }
}

// Variable para evitar múltiples inicializaciones
let pageInitialized = false;

// Event listeners
document.addEventListener('DOMContentLoaded', async () => {
    if (pageInitialized) {
        console.log('temas.js: Página ya inicializada, ignorando...');
        return;
    }
    
    pageInitialized = true;
    console.log('temas.js: Inicializando página...');
    
    try {
        // Verificar autenticación
        const session = verifyAuth();
        if (!session) {
            return;
        }
        
        // Cargar temas
        await loadTemas();
        
        // Botón para volver a materias
        const backBtn = document.getElementById('backBtn');
        if (backBtn) {
            backBtn.addEventListener('click', () => {
                window.location.href = 'materias.html';
            });
        }
    } catch (error) {
        console.error('Error al inicializar página:', error);
        pageInitialized = false;
    }
});

