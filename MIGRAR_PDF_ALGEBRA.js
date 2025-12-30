// Script para migrar el PDF antiguo a Álgebra
// Ejecuta este script en la consola del navegador después de iniciar sesión como admin
// O úsalo como referencia para crear una función de migración

import { migrarPDFAntiguo } from './js/database.js';

// ID de Álgebra (ajustar según tu base de datos)
const ALGEBRA_ID = 5;

// Ruta del PDF antiguo (ajustar según tu estructura)
const PDF_ANTIGUO = 'assets/material-apoyo.pdf'; // O la ruta que tengas en Storage

async function migrarPDF() {
    try {
        console.log('Iniciando migración del PDF a Álgebra...');
        
        const resultado = await migrarPDFAntiguo(ALGEBRA_ID, PDF_ANTIGUO);
        
        console.log('✅ PDF migrado exitosamente:', resultado);
        alert('PDF migrado exitosamente a Álgebra');
        
        return resultado;
    } catch (error) {
        console.error('❌ Error al migrar PDF:', error);
        alert(`Error al migrar PDF: ${error.message}`);
        throw error;
    }
}

// Para ejecutar: migrarPDF();

