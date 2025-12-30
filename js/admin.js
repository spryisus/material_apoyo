// js/admin.js - Panel de Administración
import { supabase } from './supabase.js';
import { obtenerMaterias, crearMateria, actualizarMateria, eliminarMateria, guardarConfiguracionPDF, subirPDF, obtenerConfiguracionPDF, obtenerPDFMateria } from './database.js';
import { esAdmin, getCurrentUser, logout } from './aut.js';
import { obtenerIconoMateria } from './materia-icons.js';

// Verificar autenticación y rol
function verificarAcceso() {
    const user = getCurrentUser();
    
    if (!user) {
        alert('Debes iniciar sesión para acceder al panel de administración.');
        window.location.href = 'index.html';
        return false;
    }
    
    if (!esAdmin()) {
        alert('No tienes permisos para acceder al panel de administración.');
        window.location.href = 'materias.html';
        return false;
    }
    
    return true;
}

// Variables globales
let materias = [];
let temaCounter = 0;
let materiaEditando = null;

// Inicializar página
document.addEventListener('DOMContentLoaded', async () => {
    if (!verificarAcceso()) return;
    
    await cargarMaterias();
    configurarEventListeners();
});

// Cargar lista de materias
async function cargarMaterias() {
    try {
        const materiasList = document.getElementById('materiasList');
        materiasList.innerHTML = '<p>Cargando materias...</p>';
        
        materias = await obtenerMaterias();
        
        if (materias.length === 0) {
            materiasList.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1;">
                    <div class="empty-state-icon">📚</div>
                    <h3>No hay materias registradas</h3>
                    <p>Crea tu primera materia haciendo clic en "Nueva Materia"</p>
                </div>
            `;
            return;
        }
        
        materiasList.innerHTML = materias.map(materia => {
            const icono = obtenerIconoMateria(materia.nombre);
            return `
            <div class="materia-admin-card">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                    <div style="font-size: 2rem;">${icono}</div>
                    <h3 style="margin: 0;">${materia.nombre}</h3>
                </div>
                ${materia.descripcion ? `<p>${materia.descripcion}</p>` : ''}
                <p style="font-size: 0.85rem; color: var(--text-secondary);">
                    ID: ${materia.id}
                </p>
                <div class="materia-actions">
                    <button class="btn btn-primary btn-small" onclick="editarMateria(${materia.id})">
                        ✏️ Editar
                    </button>
                    <button class="btn btn-secondary btn-small" style="background: var(--danger-color);" onclick="eliminarMateriaConfirm(${materia.id})">
                        🗑️ Eliminar
                    </button>
                </div>
            </div>
        `;
        }).join('');
        
    } catch (error) {
        console.error('Error al cargar materias:', error);
        document.getElementById('materiasList').innerHTML = 
            '<p class="error-message">Error al cargar las materias. Por favor, recarga la página.</p>';
    }
}

// Configurar event listeners
function configurarEventListeners() {
    // Botón nueva materia
    document.getElementById('newMateriaBtn').addEventListener('click', () => {
        abrirModalNuevaMateria();
    });
    
    // Botón volver
    document.getElementById('backBtn').addEventListener('click', () => {
        window.location.href = 'materias.html';
    });
    
    // Cerrar modal
    document.getElementById('closeModal').addEventListener('click', cerrarModal);
    document.getElementById('cancelBtn').addEventListener('click', cerrarModal);
    
    // Formulario
    document.getElementById('materiaForm').addEventListener('submit', guardarMateria);
    
    // Agregar tema
    document.getElementById('addTemaBtn').addEventListener('click', agregarTema);
    
    // Subida de PDF
    const pdfUploadArea = document.getElementById('pdfUploadArea');
    const pdfFileInput = document.getElementById('pdfFile');
    
    pdfUploadArea.addEventListener('click', () => {
        pdfFileInput.click();
    });
    
    pdfFileInput.addEventListener('change', (e) => {
        mostrarPreviewPDF(e.target.files[0]);
    });
    
    // Drag and drop
    pdfUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        pdfUploadArea.classList.add('dragover');
    });
    
    pdfUploadArea.addEventListener('dragleave', () => {
        pdfUploadArea.classList.remove('dragover');
    });
    
    pdfUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        pdfUploadArea.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file && file.type === 'application/pdf') {
            pdfFileInput.files = e.dataTransfer.files;
            mostrarPreviewPDF(file);
        } else {
            alert('Por favor, selecciona un archivo PDF válido.');
        }
    });
}

// Abrir modal para nueva materia
function abrirModalNuevaMateria() {
    materiaEditando = null;
    temaCounter = 0;
    document.getElementById('modalTitle').textContent = 'Nueva Materia';
    document.getElementById('materiaForm').reset();
    document.getElementById('materiaId').value = '';
    document.getElementById('temasList').innerHTML = '';
    document.getElementById('pdfPreview').style.display = 'none';
    document.getElementById('pdfFile').required = true;
    
    // Agregar primer tema por defecto
    agregarTema();
    
    document.getElementById('materiaModal').classList.add('active');
}

// Editar materia
window.editarMateria = async function(materiaId) {
    try {
        const materia = materias.find(m => m.id === materiaId);
        if (!materia) {
            alert('Materia no encontrada.');
            return;
        }
        
        materiaEditando = materia;
        temaCounter = 0;
        
        document.getElementById('modalTitle').textContent = 'Editar Materia';
        document.getElementById('materiaId').value = materia.id;
        document.getElementById('materiaNombre').value = materia.nombre;
        document.getElementById('materiaDescripcion').value = materia.descripcion || '';
        document.getElementById('pdfFile').required = false;
        
        // Limpiar lista de temas primero
        document.getElementById('temasList').innerHTML = '';
        
        // Cargar configuración de temas
        let config = [];
        try {
            console.log('Buscando configuración para materia ID:', materiaId);
            console.log('Tipo de materiaId:', typeof materiaId);
            config = await obtenerConfiguracionPDF(materiaId);
            console.log('Configuración cargada:', config);
            console.log('Número de temas encontrados:', config ? config.length : 0);
        } catch (error) {
            console.error('Error al cargar configuración:', error);
            console.error('Detalles del error:', error.message, error.code);
            // Continuar aunque haya error, para que el usuario pueda agregar temas
        }
        
        // Mostrar PDF actual si existe
        try {
            const pdfInfo = await obtenerPDFMateria(materiaId);
            if (pdfInfo) {
                const preview = document.getElementById('pdfPreview');
                const previewName = document.getElementById('pdfPreviewName');
                const fileName = pdfInfo.path.split('/').pop();
                previewName.textContent = `📄 ${fileName} (PDF actual)`;
                preview.style.display = 'block';
            } else {
                document.getElementById('pdfPreview').style.display = 'none';
            }
        } catch (error) {
            console.error('Error al cargar PDF:', error);
            document.getElementById('pdfPreview').style.display = 'none';
        }
        
        // Cargar temas existentes o agregar uno vacío
        if (config && config.length > 0) {
            console.log(`Cargando ${config.length} temas existentes`);
            config.forEach(temaConfig => {
                console.log('Agregando tema:', temaConfig);
                agregarTema({
                    numero: temaConfig.tema_numero,
                    nombre: temaConfig.tema_nombre,
                    paginas: [temaConfig.pagina_inicio, temaConfig.pagina_fin],
                    video_url: temaConfig.video_url || ''
                });
            });
        } else {
            console.log('No hay temas configurados, agregando tema vacío');
            document.getElementById('pdfPreview').style.display = 'none';
            agregarTema();
        }
        
        document.getElementById('materiaModal').classList.add('active');
        
    } catch (error) {
        console.error('Error al cargar materia para editar:', error);
        alert('Error al cargar la materia. Por favor, intenta de nuevo.');
    }
};


// Eliminar materia
window.eliminarMateriaConfirm = function(materiaId) {
    const materia = materias.find(m => m.id === materiaId);
    if (!materia) return;
    
    if (confirm(`¿Estás seguro de que deseas eliminar la materia "${materia.nombre}"?\n\nEsta acción no se puede deshacer.`)) {
        eliminarMateriaAction(materiaId);
    }
};

async function eliminarMateriaAction(materiaId) {
    try {
        await eliminarMateria(materiaId);
        alert('Materia eliminada exitosamente.');
        await cargarMaterias();
    } catch (error) {
        console.error('Error al eliminar materia:', error);
        alert('Error al eliminar la materia. Por favor, intenta de nuevo.');
    }
}

// Agregar tema al formulario
function agregarTema(temaData = null) {
    // Si hay temaData, usar su número; si no, incrementar contador
    const temaId = temaData ? temaData.numero : (++temaCounter);
    
    // Si usamos un tema existente, asegurarnos de que el contador esté al menos en ese número
    if (temaData && temaData.numero >= temaCounter) {
        temaCounter = temaData.numero;
    }
    
    const temaDiv = document.createElement('div');
    temaDiv.className = 'tema-item';
    temaDiv.dataset.temaId = temaId;
    
    temaDiv.innerHTML = `
        <div class="tema-item-header">
            <h4>Tema ${temaId}</h4>
            <button type="button" class="remove-tema" onclick="removerTema(this)">Eliminar</button>
        </div>
        <div class="tema-fields">
            <div class="form-group">
                <label>Nombre del Tema *</label>
                <input type="text" class="tema-nombre" value="${temaData ? temaData.nombre : ''}" 
                       placeholder="Ej: Expresiones algebraicas" required>
            </div>
            <div class="form-group">
                <label>Página Inicio *</label>
                <input type="number" class="tema-pagina-inicio" value="${temaData ? temaData.paginas[0] : ''}" 
                       min="1" required placeholder="1">
            </div>
            <div class="form-group">
                <label>Página Fin *</label>
                <input type="number" class="tema-pagina-fin" value="${temaData ? temaData.paginas[1] || temaData?.paginas[0] : ''}" 
                       min="1" required placeholder="5">
            </div>
            <div class="form-group" style="grid-column: 1 / -1;">
                <label>Video de YouTube (opcional)</label>
                <input type="url" class="tema-video-url" value="${temaData ? (temaData.video_url || '') : ''}" 
                       placeholder="Pega la URL aquí o directamente en el nombre del tema">
                <small style="color: var(--text-secondary); font-size: 0.85rem; display: block; margin-top: 0.25rem;">
                    💡 <strong>Tip:</strong> También puedes pegar la URL directamente en el nombre del tema y se detectará automáticamente
                </small>
            </div>
        </div>
    `;
    
    document.getElementById('temasList').appendChild(temaDiv);
}

// Remover tema
window.removerTema = function(button) {
    const temaItem = button.closest('.tema-item');
    temaItem.remove();
};

// Mostrar preview del PDF
function mostrarPreviewPDF(file) {
    if (!file || file.type !== 'application/pdf') {
        alert('Por favor, selecciona un archivo PDF válido.');
        return;
    }
    
    const preview = document.getElementById('pdfPreview');
    const previewName = document.getElementById('pdfPreviewName');
    
    previewName.textContent = `📄 ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;
    preview.style.display = 'block';
}

// Guardar materia
async function guardarMateria(e) {
    e.preventDefault();
    
    const saveBtn = document.getElementById('saveBtn');
    saveBtn.disabled = true;
    saveBtn.textContent = 'Guardando...';
    
    try {
        const materiaId = document.getElementById('materiaId').value;
        const nombre = document.getElementById('materiaNombre').value.trim();
        const descripcion = document.getElementById('materiaDescripcion').value.trim();
        const pdfFile = document.getElementById('pdfFile').files[0];
        
        // Validar que haya al menos un tema
        const temas = obtenerTemasDelFormulario();
        if (temas.length === 0) {
            alert('Debes agregar al menos un tema para la materia.');
            saveBtn.disabled = false;
            saveBtn.textContent = 'Guardar Materia';
            return;
        }
        
        let materia;
        
        // Crear o actualizar materia
        if (materiaId) {
            materia = await actualizarMateria(materiaId, { nombre, descripcion });
        } else {
            materia = await crearMateria(nombre, descripcion);
        }
        
        // Subir PDF si se proporcionó uno
        let pdfPath = null;
        if (pdfFile) {
            const uploadResult = await subirPDF(materia.id, pdfFile);
            pdfPath = uploadResult.path;
        } else if (materiaId) {
            // Si estamos editando y no hay nuevo PDF, obtener el path existente
            const config = await obtenerConfiguracionPDF(materia.id);
            if (config && config.length > 0) {
                pdfPath = config[0].pdf_path;
            }
        }
        
        if (!pdfPath) {
            throw new Error('Debes subir un PDF para la materia.');
        }
        
        // Guardar configuración de temas
        console.log('Guardando temas:', temas);
        console.log('Para materia ID:', materia.id);
        console.log('PDF Path:', pdfPath);
        const resultado = await guardarConfiguracionPDF(materia.id, pdfPath, temas);
        console.log('Temas guardados exitosamente:', resultado);
        
        alert('Materia guardada exitosamente.');
        cerrarModal();
        await cargarMaterias();
        
    } catch (error) {
        console.error('Error al guardar materia:', error);
        alert(`Error al guardar la materia: ${error.message || 'Error desconocido'}`);
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Guardar Materia';
    }
}

// Obtener temas del formulario
function obtenerTemasDelFormulario() {
    const temasItems = document.querySelectorAll('.tema-item');
    const temas = [];
    
    // Función helper para extraer URL de YouTube de un texto
    function extraerURLYouTube(texto) {
        if (!texto) return { url: null, textoLimpio: texto };
        
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
                    url: match[0].startsWith('http') ? match[0] : `https://${match[0]}`,
                    textoLimpio: textoLimpio
                };
            }
        }
        
        return { url: null, textoLimpio: texto };
    }
    
    temasItems.forEach((item, index) => {
        let nombre = item.querySelector('.tema-nombre').value.trim();
        const paginaInicio = parseInt(item.querySelector('.tema-pagina-inicio').value);
        const paginaFin = parseInt(item.querySelector('.tema-pagina-fin').value);
        let videoUrl = item.querySelector('.tema-video-url')?.value.trim() || '';
        
        // Si no hay video_url en el campo separado, buscar en el nombre
        if (!videoUrl) {
            const videoInfo = extraerURLYouTube(nombre);
            if (videoInfo.url) {
                videoUrl = videoInfo.url;
                nombre = videoInfo.textoLimpio || nombre;
            }
        }
        
        if (nombre && paginaInicio && paginaFin) {
            temas.push({
                numero: index + 1,
                nombre: nombre,
                paginas: [paginaInicio, paginaFin],
                video_url: videoUrl || null
            });
        }
    });
    
    return temas;
}

// Cerrar modal
function cerrarModal() {
    document.getElementById('materiaModal').classList.remove('active');
    document.getElementById('materiaForm').reset();
    materiaEditando = null;
}

// Cerrar modal al hacer clic fuera
document.addEventListener('click', (e) => {
    const modal = document.getElementById('materiaModal');
    if (e.target === modal) {
        cerrarModal();
    }
});

