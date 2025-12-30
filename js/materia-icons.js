// js/materia-icons.js - Iconos para cada materia

// Función para obtener el icono de una materia según su nombre
export function obtenerIconoMateria(nombreMateria) {
    if (!nombreMateria) return '📚';
    
    const nombre = nombreMateria.toLowerCase().trim();
    
    // Mapeo de iconos por materia
    const iconos = {
        // Matemáticas
        'álgebra': '🔢',
        'algebra': '🔢',
        'matemáticas': '📐',
        'matematicas': '📐',
        'matematica': '📐',
        
        // Computación/Tecnología
        'cómputo': '💻',
        'computo': '💻',
        'computación': '💻',
        'computacion': '💻',
        'informática': '💻',
        'informatica': '💻',
        'programación': '💻',
        'programacion': '💻',
        'tecnología': '💻',
        'tecnologia': '💻',
        
        // Electricidad
        'electricidad': '⚡',
        
        // Electrónica
        'electrónica': '🔌',
        'electronica': '🔌',
        
        // Ciencias
        'ciencias': '🔬',
        'ciencias naturales': '🔬',
        'física': '⚛️',
        'fisica': '⚛️',
        'química': '🧪',
        'quimica': '🧪',
        'biología': '🧬',
        'biologia': '🧬',
        
        // Lenguaje
        'español': '📝',
        'espanol': '📝',
        'lenguaje': '📝',
        'comunicación': '📝',
        'comunicacion': '📝',
        
        // Historia
        'historia': '📜',
        'historia de méxico': '🇲🇽',
        
        // Geografía
        'geografía': '🌍',
        'geografia': '🌍',
        
        // Inglés
        'inglés': '🇬🇧',
        'ingles': '🇬🇧',
        
        // Formación Cívica
        'formación cívica': '⚖️',
        'formacion civica': '⚖️',
        'cívica': '⚖️',
        'civica': '⚖️',
        'ética': '⚖️',
        'etica': '⚖️',
    };
    
    // Buscar coincidencia exacta o parcial
    for (const [key, icono] of Object.entries(iconos)) {
        if (nombre.includes(key) || key.includes(nombre)) {
            return icono;
        }
    }
    
    // Si no encuentra coincidencia, retornar icono por defecto
    return '📚';
}

// Función para obtener icono de tema (genérico)
export function obtenerIconoTema() {
    return '📖';
}

