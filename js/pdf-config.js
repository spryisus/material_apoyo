// js/pdf-config.js - Configuración de mapeo de materias y temas a páginas del PDF
// Este archivo mapea cada materia y tema a las páginas del PDF que contienen su contenido

// IMPORTANTE: Necesitas configurar:
// 1. El ID de la materia Álgebra (revisa tu base de datos de Supabase)
// 2. Las páginas del PDF que corresponden a cada tema

// Estructura: materia_id -> tema_numero -> { paginas: [inicio, fin], nombre: "Nombre del Tema" }
// Las páginas son 1-indexed (la primera página es 1, no 0)

// Configuración para Álgebra
// ID de la materia: 5
// IMPORTANTE: Ajusta los números de página según tu PDF real

export const pdfConfig = {
    5: {  // ID de Álgebra
        1: {
            paginas: [6, 7],  // AJUSTA: Páginas del PDF para "Expresiones algebraicas"
            nombre: "Expresiones algebraicas"
        },
        2: {
            paginas: [8, 13],  // AJUSTA: Páginas del PDF para "Operaciones básicas"
            nombre: "Operaciones básicas"
        },
        3: {
            paginas: [14, 21],  // AJUSTA: Páginas del PDF para "Factorización"
            nombre: "Factorización"
        },
        4: {
            paginas: [22, 25],  // AJUSTA: Páginas del PDF para "Fracciones algebraicas"
            nombre: "Fracciones algebraicas"
        },
        5: {
            paginas: [26, 28],  // AJUSTA: Páginas del PDF para "Ecuación de primer grado"
            nombre: "Ecuación de primer grado"
        },
        6: {
            paginas: [29, 33],  // AJUSTA: Páginas del PDF para "Ecuación de segundo grado"
            nombre: "Ecuación de segundo grado"
        },
        7: {
            paginas: [34, 39],  // AJUSTA: Páginas del PDF para "Ecuaciones simultaneas"
            nombre: "Ecuaciones simultaneas"
        },
        8: {
            paginas: [40, 45],  // AJUSTA: Páginas del PDF para "Problemas planteados con palabras"
            nombre: "Problemas planteados con palabras"
        }
    }
    
    // NOTA: Si un tema ocupa solo una página, puedes usar: paginas: [5] en lugar de [5, 5]
    // Ejemplo: paginas: [15] mostrará solo la página 15
};

// Ruta al archivo PDF (ajusta según la ubicación de tu PDF)
export const PDF_PATH = 'assets/material-apoyo.pdf';

// Función helper para obtener las páginas de un tema
export function obtenerPaginasTema(materiaId, temaNumero) {
    if (pdfConfig[materiaId] && pdfConfig[materiaId][temaNumero]) {
        const config = pdfConfig[materiaId][temaNumero];
        const paginas = config.paginas || config; // Soporta formato antiguo y nuevo
        
        if (Array.isArray(paginas)) {
            if (paginas.length === 2) {
                return { inicio: paginas[0], fin: paginas[1] };
            } else if (paginas.length === 1) {
                return { inicio: paginas[0], fin: paginas[0] };
            }
        }
    }
    // Si no hay configuración, retornar null
    return null;
}

// Función helper para obtener el nombre personalizado de un tema
export function obtenerNombreTema(materiaId, temaNumero) {
    if (pdfConfig[materiaId] && pdfConfig[materiaId][temaNumero]) {
        const config = pdfConfig[materiaId][temaNumero];
        if (config.nombre) {
            return config.nombre;
        }
    }
    return null; // Retornar null si no hay nombre personalizado
}

