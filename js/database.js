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

