// js/database.js - Funciones para interactuar con la base de datos
import { supabase } from './supabase.js';

// Obtener todas las materias
export async function obtenerMaterias() {
    const { data, error } = await supabase
        .from('materias')
        .select('*')
        .order('nombre');
    
    if (error) {
        console.error('Error al obtener materias:', error);
        throw error;
    }
    
    return data;
}

// Insertar nuevas materias (función opcional, normalmente se usa el script SQL)
export async function insertarMaterias(materias) {
    // materias es un array de strings con los nombres de las materias
    const materiasData = materias.map(nombre => ({ nombre }));
    
    const { data, error } = await supabase
        .from('materias')
        .insert(materiasData)
        .select();
    
    if (error) {
        console.error('Error al insertar materias:', error);
        throw error;
    }
    
    return data;
}

// Obtener preguntas de una o más materias
export async function obtenerPreguntas(materiasIds, cantidad = 30) {
    try {
        console.log('obtenerPreguntas: Buscando preguntas para materias:', materiasIds);
        console.log('obtenerPreguntas: Cantidad solicitada:', cantidad);
        
        const { data, error } = await supabase
            .from('preguntas')
            .select('*')
            .in('materia_id', materiasIds);
        
        if (error) {
            console.error('Error al obtener preguntas - Detalles:', error);
            console.error('Error code:', error.code);
            console.error('Error message:', error.message);
            console.error('Error details:', error.details);
            throw error;
        }
        
        console.log('obtenerPreguntas: Total de preguntas encontradas:', data?.length || 0);
        
        if (!data || data.length === 0) {
            console.warn('obtenerPreguntas: No se encontraron preguntas para las materias:', materiasIds);
            // Verificar si las materias existen
            const { data: materiasCheck } = await supabase
                .from('materias')
                .select('id, nombre')
                .in('id', materiasIds);
            
            console.log('obtenerPreguntas: Materias verificadas:', materiasCheck);
            
            return [];
        }
        
        // Validar que las preguntas tengan todos los campos necesarios
        const preguntasValidas = data.filter(p => 
            p.id && 
            p.pregunta && 
            p.opcion_a && 
            p.opcion_b && 
            p.opcion_c && 
            p.opcion_d && 
            p.respuesta_correcta
        );
        
        if (preguntasValidas.length !== data.length) {
            console.warn('obtenerPreguntas: Algunas preguntas no tienen todos los campos necesarios');
            console.warn(`Total: ${data.length}, Válidas: ${preguntasValidas.length}`);
        }
        
        // Mezclar aleatoriamente y seleccionar la cantidad solicitada
        const preguntasMezcladas = preguntasValidas.sort(() => Math.random() - 0.5);
        const preguntasSeleccionadas = preguntasMezcladas.slice(0, cantidad);
        
        console.log('obtenerPreguntas: Preguntas seleccionadas:', preguntasSeleccionadas.length);
        return preguntasSeleccionadas;
    } catch (error) {
        console.error('Error completo en obtenerPreguntas:', error);
        throw error;
    }
}

// Crear un nuevo examen
export async function crearExamen(usuarioId, materiasIds, totalPreguntas) {
    // Primero verificar si existe la tabla examen_materias
    // Si no existe, crear examen sin relaciones (compatibilidad con esquema original)
    let examen;
    
    try {
        // Insertar examen (total_preguntas es opcional, solo incluirlo si la columna existe)
        // Por ahora, solo insertamos usuario_id ya que total_preguntas puede no existir
        const examenData = {
            usuario_id: usuarioId
            // total_preguntas es opcional - no lo incluimos para evitar errores
            // Si necesitas esta columna, agrégala primero a la tabla examenes en Supabase
        };
        
        console.log('crearExamen: Datos del examen a insertar:', examenData);
        
        const { data, error: errorExamen } = await supabase
            .from('examenes')
            .insert(examenData)
            .select()
            .single();
        
        if (errorExamen) {
            console.error('Error al crear examen:', errorExamen);
            console.error('Error code:', errorExamen.code);
            console.error('Error message:', errorExamen.message);
            
            // Si el error es por columnas faltantes, intentar sin total_preguntas
            if (errorExamen.message && errorExamen.message.includes('total_preguntas')) {
                console.warn('La columna total_preguntas no existe, continuando sin ella...');
                // Ya no incluimos total_preguntas arriba, así que este error no debería ocurrir
            }
            
            throw errorExamen;
        }
        
        examen = data;
        console.log('crearExamen: Examen creado exitosamente:', examen);
        
        // Intentar crear relaciones examen-materias (si la tabla existe)
        try {
            const relaciones = materiasIds.map(materiaId => ({
                examen_id: examen.id,
                materia_id: materiaId
            }));
            
            const { error: errorRelaciones } = await supabase
                .from('examen_materias')
                .insert(relaciones);
            
            if (errorRelaciones) {
                console.warn('No se pudieron crear relaciones examen-materias (tabla puede no existir):', errorRelaciones);
                // No lanzar error, el examen se creó correctamente
            }
        } catch (e) {
            console.warn('Tabla examen_materias no disponible, usando esquema original');
        }
        
        return examen;
    } catch (error) {
        throw error;
    }
}

// Guardar respuestas del usuario
export async function guardarRespuestas(examenId, respuestas) {
    // respuestas es un array de objetos: [{ pregunta_id, respuesta_usuario }, ...]
    const respuestasData = respuestas.map(resp => ({
        examen_id: examenId,
        pregunta_id: resp.pregunta_id,
        respuesta_usuario: resp.respuesta_usuario
    }));
    
    const { data, error } = await supabase
        .from('respuestas_usuario')
        .insert(respuestasData)
        .select();
    
    if (error) {
        console.error('Error al guardar respuestas:', error);
        throw error;
    }
    
    return data;
}

// Actualizar calificación del examen
export async function actualizarCalificacion(examenId, calificacion) {
    const { data, error } = await supabase
        .from('examenes')
        .update({ calificacion: calificacion })
        .eq('id', examenId)
        .select()
        .single();
    
    if (error) {
        console.error('Error al actualizar calificación:', error);
        throw error;
    }
    
    return data;
}

// Obtener examen con sus detalles
export async function obtenerExamen(examenId) {
    try {
        const { data, error } = await supabase
            .from('examenes')
            .select(`
                *,
                examen_materias (
                    materias (*)
                ),
                respuestas_usuario (
                    *,
                    preguntas (*)
                )
            `)
            .eq('id', examenId)
            .single();
        
        if (error) {
            console.error('Error al obtener examen:', error);
            throw error;
        }
        
        return data;
    } catch (error) {
        // Si falla por la relación, intentar sin ella
        const { data, error: errorSimple } = await supabase
            .from('examenes')
            .select('*')
            .eq('id', examenId)
            .single();
        
        if (errorSimple) {
            throw errorSimple;
        }
        
        return data;
    }
}

// Obtener historial de exámenes del usuario
export async function obtenerHistorialExamenes(usuarioId) {
    try {
        const { data, error } = await supabase
            .from('examenes')
            .select(`
                *,
                examen_materias (
                    materias (*)
                )
            `)
            .eq('usuario_id', usuarioId)
            .order('fecha', { ascending: false });
        
        if (error) {
            console.error('Error al obtener historial:', error);
            throw error;
        }
        
        return data;
    } catch (error) {
        // Si falla por la relación, intentar sin ella
        const { data, error: errorSimple } = await supabase
            .from('examenes')
            .select('*')
            .eq('usuario_id', usuarioId)
            .order('fecha', { ascending: false });
        
        if (errorSimple) {
            throw errorSimple;
        }
        
        return data;
    }
}

// Obtener temas únicos de una materia desde las preguntas
export async function obtenerTemasPorMateria(materiaId) {
    try {
        // Importar funciones de configuración de PDF
        const { obtenerNombreTema, pdfConfig } = await import('./pdf-config.js');
        
        // Si hay configuración de temas en pdfConfig, usar esos temas
        if (pdfConfig[materiaId]) {
            const temasConfigurados = Object.keys(pdfConfig[materiaId])
                .map(num => parseInt(num))
                .sort((a, b) => a - b)
                .map(numero => {
                    const nombrePersonalizado = obtenerNombreTema(materiaId, numero);
                    return {
                        id: numero,
                        nombre: nombrePersonalizado || `Tema ${numero}`,
                        numero: numero
                    };
                });
            
            if (temasConfigurados.length > 0) {
                return temasConfigurados;
            }
        }
        
        // Si no hay configuración en BD, retornar array vacío
        // (Los temas deben configurarse desde el panel de administración)
        return [];
    } catch (error) {
        console.error('Error al obtener temas por materia:', error);
        throw error;
    }
}

// ========== FUNCIONES DE ADMINISTRACIÓN ==========

// Crear nueva materia
export async function crearMateria(nombre, descripcion = '') {
    try {
        const { data, error } = await supabase
            .from('materias')
            .insert({ nombre, descripcion })
            .select()
            .single();
        
        if (error) {
            console.error('Error al crear materia:', error);
            throw error;
        }
        
        return data;
    } catch (error) {
        console.error('Error completo en crearMateria:', error);
        throw error;
    }
}

// Actualizar materia
export async function actualizarMateria(materiaId, datos) {
    try {
        const { data, error } = await supabase
            .from('materias')
            .update(datos)
            .eq('id', materiaId)
            .select()
            .single();
        
        if (error) {
            console.error('Error al actualizar materia:', error);
            throw error;
        }
        
        return data;
    } catch (error) {
        console.error('Error completo en actualizarMateria:', error);
        throw error;
    }
}

// Eliminar materia
export async function eliminarMateria(materiaId) {
    try {
        const { error } = await supabase
            .from('materias')
            .delete()
            .eq('id', materiaId);
        
        if (error) {
            console.error('Error al eliminar materia:', error);
            throw error;
        }
        
        return true;
    } catch (error) {
        console.error('Error completo en eliminarMateria:', error);
        throw error;
    }
}

// Guardar configuración de PDF para una materia
export async function guardarConfiguracionPDF(materiaId, pdfPath, temas) {
    // temas es un array: [{ numero: 1, nombre: "Tema 1", paginas: [1, 5] }, ...]
    try {
        // Verificar que el usuario sea admin (verificación en código)
        const { esAdmin } = await import('./aut.js');
        if (!esAdmin()) {
            throw new Error('Solo los administradores pueden guardar configuración de PDFs');
        }
        
        // Primero, eliminar configuración anterior si existe
        const { error: deleteError } = await supabase
            .from('materia_pdf_config')
            .delete()
            .eq('materia_id', materiaId);
        
        if (deleteError) {
            console.warn('Error al eliminar configuración anterior (puede que no exista):', deleteError);
        }
        
        // Insertar nueva configuración
        const configData = temas.map(tema => ({
            materia_id: materiaId,
            tema_numero: tema.numero,
            tema_nombre: tema.nombre,
            pagina_inicio: tema.paginas[0],
            pagina_fin: tema.paginas[1] || tema.paginas[0],
            pdf_path: pdfPath,
            video_url: tema.video_url || null
        }));
        
        const { data, error } = await supabase
            .from('materia_pdf_config')
            .insert(configData)
            .select();
        
        if (error) {
            console.error('Error al guardar configuración PDF:', error);
            throw error;
        }
        
        return data;
    } catch (error) {
        console.error('Error completo en guardarConfiguracionPDF:', error);
        throw error;
    }
}

// Obtener configuración de PDF de una materia
export async function obtenerConfiguracionPDF(materiaId) {
    try {
        // Convertir materiaId a número si es string
        const id = typeof materiaId === 'string' ? parseInt(materiaId) : materiaId;
        console.log('obtenerConfiguracionPDF: Buscando para materia_id =', id);
        
        const { data, error } = await supabase
            .from('materia_pdf_config')
            .select('*')
            .eq('materia_id', id)
            .order('tema_numero');
        
        if (error) {
            console.error('Error al obtener configuración PDF:', error);
            console.error('Código de error:', error.code);
            console.error('Mensaje:', error.message);
            throw error;
        }
        
        console.log('obtenerConfiguracionPDF: Resultados encontrados:', data ? data.length : 0);
        if (data && data.length > 0) {
            console.log('Primer tema encontrado:', data[0]);
        }
        
        return data || [];
    } catch (error) {
        console.error('Error completo en obtenerConfiguracionPDF:', error);
        throw error;
    }
}

// Subir PDF a Supabase Storage (organizado por materias)
export async function subirPDF(materiaId, archivo) {
    try {
        const fileExt = archivo.name.split('.').pop();
        const fileName = `material.${fileExt}`;
        // Organizar por materias: materias/{materiaId}/material.pdf
        const filePath = `materias/${materiaId}/${fileName}`;
        
        // Si ya existe un PDF para esta materia, eliminarlo primero
        try {
            const { data: existingFiles } = await supabase.storage
                .from('material-apoyo')
                .list(`materias/${materiaId}/`);
            
            if (existingFiles && existingFiles.length > 0) {
                const filesToDelete = existingFiles.map(f => `materias/${materiaId}/${f.name}`);
                await supabase.storage
                    .from('material-apoyo')
                    .remove(filesToDelete);
            }
        } catch (deleteError) {
            // Si no existe, no hay problema
            console.log('No hay PDF anterior para eliminar o error al eliminar:', deleteError);
        }
        
        const { data, error } = await supabase.storage
            .from('material-apoyo')
            .upload(filePath, archivo, {
                cacheControl: '3600',
                upsert: true // Permitir sobrescribir si existe
            });
        
        if (error) {
            console.error('Error al subir PDF:', error);
            throw error;
        }
        
        // Obtener URL pública
        const { data: urlData } = supabase.storage
            .from('material-apoyo')
            .getPublicUrl(filePath);
        
        return {
            path: filePath,
            url: urlData.publicUrl,
            fileName: fileName
        };
    } catch (error) {
        console.error('Error completo en subirPDF:', error);
        throw error;
    }
}

// Obtener URL del PDF de una materia
export async function obtenerPDFMateria(materiaId) {
    try {
        const config = await obtenerConfiguracionPDF(materiaId);
        if (!config || config.length === 0) {
            return null;
        }
        
        // Todos los temas de una materia usan el mismo PDF
        const pdfPath = config[0].pdf_path;
        
        // Obtener URL pública
        const { data: urlData } = supabase.storage
            .from('material-apoyo')
            .getPublicUrl(pdfPath);
        
        return {
            path: pdfPath,
            url: urlData.publicUrl
        };
    } catch (error) {
        console.error('Error al obtener PDF de materia:', error);
        return null;
    }
}

// Migrar PDF antiguo a estructura por materias
export async function migrarPDFAntiguo(materiaId, pdfPathAntiguo) {
    try {
        // Leer el archivo antiguo
        const { data: fileData, error: downloadError } = await supabase.storage
            .from('material-apoyo')
            .download(pdfPathAntiguo);
        
        if (downloadError) {
            throw new Error(`No se pudo leer el archivo antiguo: ${downloadError.message}`);
        }
        
        // Determinar extensión del archivo
        const fileExt = pdfPathAntiguo.split('.').pop() || 'pdf';
        const newFileName = `material.${fileExt}`;
        const newPath = `materias/${materiaId}/${newFileName}`;
        
        // Subir a la nueva ubicación
        const { data: uploadData, error: uploadError } = await supabase.storage
            .from('material-apoyo')
            .upload(newPath, fileData, {
                cacheControl: '3600',
                upsert: true
            });
        
        if (uploadError) {
            throw new Error(`No se pudo subir el archivo: ${uploadError.message}`);
        }
        
        // Actualizar todas las configuraciones de PDF de esta materia
        const { error: updateError } = await supabase
            .from('materia_pdf_config')
            .update({ pdf_path: newPath })
            .eq('materia_id', materiaId);
        
        if (updateError) {
            console.warn('Error al actualizar configuración, pero el archivo se migró:', updateError);
        }
        
        return {
            path: newPath,
            success: true
        };
    } catch (error) {
        console.error('Error al migrar PDF:', error);
        throw error;
    }
}

