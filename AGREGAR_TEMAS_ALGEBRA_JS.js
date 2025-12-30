// Script JavaScript para agregar todos los temas de Álgebra
// Ejecuta esto en la consola del navegador después de iniciar sesión como admin
// O úsalo como referencia para crear una función de administración

import { supabase } from './js/supabase.js';
import { obtenerConfiguracionPDF, guardarConfiguracionPDF } from './js/database.js';

async function agregarTodosLosTemasAlgebra() {
    const ALGEBRA_ID = 5;
    
    // Verificar si ya existe configuración
    const configExistente = await obtenerConfiguracionPDF(ALGEBRA_ID);
    let pdfPath = 'materias/5/material.pdf';
    
    if (configExistente && configExistente.length > 0) {
        pdfPath = configExistente[0].pdf_path;
    }
    
    // Definir todos los temas con su paginación
    const temas = [
        { numero: 1, nombre: 'Expresiones algebraicas', paginas: [6, 7] },
        { numero: 2, nombre: 'Operaciones básicas', paginas: [8, 13] },
        { numero: 3, nombre: 'Factorización', paginas: [14, 21] },
        { numero: 4, nombre: 'Fracciones algebraicas', paginas: [22, 25] },
        { numero: 5, nombre: 'Ecuación de primer grado', paginas: [26, 28] },
        { numero: 6, nombre: 'Ecuación de segundo grado', paginas: [29, 33] },
        { numero: 7, nombre: 'Ecuaciones simultaneas', paginas: [34, 39] },
        { numero: 8, nombre: 'Problemas planteados con palabras', paginas: [40, 45] }
    ];
    
    try {
        console.log('Agregando temas de Álgebra...');
        await guardarConfiguracionPDF(ALGEBRA_ID, pdfPath, temas);
        console.log('✅ Todos los temas de Álgebra agregados exitosamente!');
        alert('Temas agregados exitosamente. Recarga la página para ver los cambios.');
    } catch (error) {
        console.error('❌ Error al agregar temas:', error);
        alert(`Error: ${error.message}`);
    }
}

// Para ejecutar: agregarTodosLosTemasAlgebra();

