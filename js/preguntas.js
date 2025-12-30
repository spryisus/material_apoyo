// js/preguntas.js - Banco de preguntas para 8 materias
// Cada materia tiene 100 preguntas divididas en 4 temas de 25 preguntas cada uno

export const materias = {
    matemáticas: {
        nombre: 'Matemáticas',
        temas: {
            algebra: {
                nombre: 'Álgebra',
                preguntas: generateQuestions('Matemáticas - Álgebra', 25)
            },
            geometria: {
                nombre: 'Geometría',
                preguntas: generateQuestions('Matemáticas - Geometría', 25)
            },
            calculo: {
                nombre: 'Cálculo',
                preguntas: generateQuestions('Matemáticas - Cálculo', 25)
            },
            estadistica: {
                nombre: 'Estadística',
                preguntas: generateQuestions('Matemáticas - Estadística', 25)
            }
        }
    },
    español: {
        nombre: 'Español',
        temas: {
            gramatica: {
                nombre: 'Gramática',
                preguntas: generateQuestions('Español - Gramática', 25)
            },
            literatura: {
                nombre: 'Literatura',
                preguntas: generateQuestions('Español - Literatura', 25)
            },
            ortografia: {
                nombre: 'Ortografía',
                preguntas: generateQuestions('Español - Ortografía', 25)
            },
            redaccion: {
                nombre: 'Redacción',
                preguntas: generateQuestions('Español - Redacción', 25)
            }
        }
    },
    historia: {
        nombre: 'Historia',
        temas: {
            mexicana: {
                nombre: 'Historia de México',
                preguntas: generateQuestions('Historia - Historia de México', 25)
            },
            universal: {
                nombre: 'Historia Universal',
                preguntas: generateQuestions('Historia - Historia Universal', 25)
            },
            prehispanica: {
                nombre: 'Época Prehispánica',
                preguntas: generateQuestions('Historia - Época Prehispánica', 25)
            },
            contemporanea: {
                nombre: 'Historia Contemporánea',
                preguntas: generateQuestions('Historia - Historia Contemporánea', 25)
            }
        }
    },
    ciencias: {
        nombre: 'Ciencias Naturales',
        temas: {
            biologia: {
                nombre: 'Biología',
                preguntas: generateQuestions('Ciencias - Biología', 25)
            },
            quimica: {
                nombre: 'Química',
                preguntas: generateQuestions('Ciencias - Química', 25)
            },
            fisica: {
                nombre: 'Física',
                preguntas: generateQuestions('Ciencias - Física', 25)
            },
            ecologia: {
                nombre: 'Ecología',
                preguntas: generateQuestions('Ciencias - Ecología', 25)
            }
        }
    },
    geografia: {
        nombre: 'Geografía',
        temas: {
            fisica: {
                nombre: 'Geografía Física',
                preguntas: generateQuestions('Geografía - Geografía Física', 25)
            },
            humana: {
                nombre: 'Geografía Humana',
                preguntas: generateQuestions('Geografía - Geografía Humana', 25)
            },
            mexico: {
                nombre: 'Geografía de México',
                preguntas: generateQuestions('Geografía - Geografía de México', 25)
            },
            mundial: {
                nombre: 'Geografía Mundial',
                preguntas: generateQuestions('Geografía - Geografía Mundial', 25)
            }
        }
    },
    ingles: {
        nombre: 'Inglés',
        temas: {
            gramatica: {
                nombre: 'Gramática',
                preguntas: generateQuestions('Inglés - Gramática', 25)
            },
            vocabulario: {
                nombre: 'Vocabulario',
                preguntas: generateQuestions('Inglés - Vocabulario', 25)
            },
            comprension: {
                nombre: 'Comprensión Lectora',
                preguntas: generateQuestions('Inglés - Comprensión Lectora', 25)
            },
            conversacion: {
                nombre: 'Conversación',
                preguntas: generateQuestions('Inglés - Conversación', 25)
            }
        }
    },
    civica: {
        nombre: 'Formación Cívica y Ética',
        temas: {
            valores: {
                nombre: 'Valores',
                preguntas: generateQuestions('Formación Cívica - Valores', 25)
            },
            derechos: {
                nombre: 'Derechos Humanos',
                preguntas: generateQuestions('Formación Cívica - Derechos Humanos', 25)
            },
            gobierno: {
                nombre: 'Gobierno y Estado',
                preguntas: generateQuestions('Formación Cívica - Gobierno y Estado', 25)
            },
            participacion: {
                nombre: 'Participación Ciudadana',
                preguntas: generateQuestions('Formación Cívica - Participación Ciudadana', 25)
            }
        }
    },
    tecnologia: {
        nombre: 'Tecnología',
        temas: {
            computacion: {
                nombre: 'Computación',
                preguntas: generateQuestions('Tecnología - Computación', 25)
            },
            programacion: {
                nombre: 'Programación',
                preguntas: generateQuestions('Tecnología - Programación', 25)
            },
            internet: {
                nombre: 'Internet y Redes',
                preguntas: generateQuestions('Tecnología - Internet y Redes', 25)
            },
            seguridad: {
                nombre: 'Seguridad Informática',
                preguntas: generateQuestions('Tecnología - Seguridad Informática', 25)
            }
        }
    }
};

// Función para generar preguntas de ejemplo
function generateQuestions(tema, cantidad) {
    const preguntas = [];
    for (let i = 1; i <= cantidad; i++) {
        preguntas.push({
            id: `${tema}-${i}`,
            pregunta: `Pregunta ${i} de ${tema}: ¿Cuál es la respuesta correcta?`,
            opciones: [
                `Opción A - Respuesta ${i}`,
                `Opción B - Respuesta ${i}`,
                `Opción C - Respuesta ${i}`,
                `Opción D - Respuesta ${i}`
            ],
            respuestaCorrecta: Math.floor(Math.random() * 4), // 0-3
            materia: tema.split(' - ')[0],
            tema: tema.split(' - ')[1]
        });
    }
    return preguntas;
}

// Función para obtener todas las preguntas de las materias seleccionadas
export function obtenerPreguntasAleatorias(materiasSeleccionadas, cantidad = 30) {
    const todasLasPreguntas = [];
    
    // Recopilar todas las preguntas de las materias seleccionadas
    materiasSeleccionadas.forEach(materiaKey => {
        const materia = materias[materiaKey];
        if (materia) {
            Object.values(materia.temas).forEach(tema => {
                todasLasPreguntas.push(...tema.preguntas);
            });
        }
    });
    
    // Mezclar las preguntas aleatoriamente
    const preguntasMezcladas = todasLasPreguntas.sort(() => Math.random() - 0.5);
    
    // Seleccionar la cantidad solicitada
    return preguntasMezcladas.slice(0, cantidad);
}

// Función para obtener la lista de materias disponibles
export function obtenerListaMaterias() {
    return Object.keys(materias).map(key => ({
        key: key,
        nombre: materias[key].nombre
    }));
}


