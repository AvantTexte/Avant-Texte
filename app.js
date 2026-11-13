let vocabulary = [];
let currentIndex = 0;
let points = 0;

// Carga vocabulario dinámicamente desde datos/vocab/ o fallback
async function loadVocabulary() {
    try {
        // Intentar cargar índice o fichas individuales
        const sampleWords = [
            { fr: "guerre", es: "guerra", context: "Pilote de guerre est un récit de 1942." },
            { fr: "camarade", es: "camarada", context: "Mes camarades de l'escadrille 2/33." },
            { fr: "vol", es: "vuelo", context: "Le vol au-dessus de Arras." },
            { fr: "espoir", es: "esperanza", context: "Garder l'espoir malgré la défaite." },
            { fr: "devoir", es: "deber", context: "Accomplir son devoir jusqu'au bout." }
        ];

        // Cargar desde JSONs si existen
        for (let i = 1; i <= 20; i++) {
            try {
                const res = await fetch(`datos/vocab/word_${i}.json`);
                if (res.ok) {
                    const data = await res.json();
                    if (data && data.palabra_frances) {
                        vocabulary.push({
                            fr: data.palabra_frances,
                            es: data.traduccion_espanol || data.significado,
                            context: data.contexto || ""
                        });
                    }
                }
            } catch (e) {}
        }

        if (vocabulary.length === 0) {
            vocabulary = sampleWords;
        }
    } catch (err) {
        console.warn("Usando datos de respaldo:", err);
    }
    
    renderCard();
}

function renderCard() {
    if (vocabulary.length === 0) return;
    const current = vocabulary[currentIndex];
    
    document.getElementById('word-fr').textContent = current.fr;
    document.getElementById('word-es').textContent = current.es;
    document.getElementById('context-sentence').textContent = current.context ? `"${current.context}"` : '';
    
    const card = document.getElementById('flashcard');
    card.classList.remove('flipped');

    // Actualizar barra de progreso
    const progressPercent = ((currentIndex + 1) / vocabulary.length) * 100;
    document.getElementById('progress-bar').style.width = `${progressPercent}%`;
}

function speakWord() {
    if (vocabulary.length === 0) return;
    const currentWord = vocabulary[currentIndex].fr;
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(currentWord);
        utterance.lang = 'fr-FR';
        utterance.rate = 0.9;
        window.speechSynthesis.speak(utterance);
    }
}

// Event Listeners
document.getElementById('flashcard').addEventListener('click', () => {
    document.getElementById('flashcard').classList.toggle('flipped');
});

document.getElementById('audio-btn').addEventListener('click', (e) => {
    e.stopPropagation();
    speakWord();
});

document.getElementById('speak-btn').addEventListener('click', () => {
    speakWord();
});

document.getElementById('next-btn').addEventListener('click', () => {
    if (currentIndex < vocabulary.length - 1) {
        currentIndex++;
        points += 10;
        document.getElementById('score-badge').textContent = `${points} pts`;
        renderCard();
    }
});

document.getElementById('prev-btn').addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        renderCard();
    }
});

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', loadVocabulary);
