import os
import subprocess

def main():
    print("🚀 Construyendo la interfaz de Proyecto Liseur (Duolingo Style)...")

    # 1. Crear index.html
    html_content = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto Liseur - Vocabulaire Français</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <div class="logo">
                <span class="flag">🇫🇷</span>
                <h1>Liseur</h1>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" id="progress-bar"></div>
            </div>
            <div class="score-badge" id="score-badge">0 pts</div>
        </header>

        <!-- Main Card Container -->
        <main class="card-section">
            <div class="flashcard" id="flashcard">
                <div class="card-inner" id="card-inner">
                    <div class="card-front">
                        <span class="category-tag">Vocabulaire • Pilote de guerre</span>
                        <h2 class="french-word" id="word-fr">...</h2>
                        <button class="audio-btn" id="audio-btn" title="Écouter la prononciation">
                            🔊
                        </button>
                        <p class="hint-text">Toca para ver el significado en español</p>
                    </div>
                    <div class="card-back">
                        <span class="category-tag">Español</span>
                        <h3 class="spanish-word" id="word-es">...</h3>
                        <p class="context-sentence" id="context-sentence">...</p>
                    </div>
                </div>
            </div>

            <!-- Controls -->
            <div class="controls">
                <button class="btn btn-secondary" id="prev-btn">⬅️ Anterior</button>
                <button class="btn btn-audio" id="speak-btn">🗣️ Pronunciar</button>
                <button class="btn btn-primary" id="next-btn">Siguiente ➡️</button>
            </div>
        </main>
    </div>

    <script src="app.js"></script>
</body>
</html>
"""

    # 2. Crear styles.css
    css_content = """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Nunito', sans-serif;
}

body {
    background-color: #f7f9fa;
    color: #3c3c3c;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.app-container {
    width: 100%;
    max-width: 500px;
    background: #ffffff;
    border: 2px solid #e5e5e5;
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 32px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 8px;
}

.logo h1 {
    font-size: 1.4rem;
    font-weight: 800;
    color: #58cc02;
}

.progress-bar-container {
    flex: 1;
    height: 14px;
    background: #e5e5e5;
    border-radius: 10px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    width: 0%;
    background: #58cc02;
    transition: width 0.4s ease;
}

.score-badge {
    background: #ffc800;
    color: #fff;
    font-weight: 800;
    padding: 6px 12px;
    border-radius: 12px;
    font-size: 0.9rem;
}

.card-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
}

.flashcard {
    width: 100%;
    height: 280px;
    perspective: 1000px;
    cursor: pointer;
}

.card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    text-align: center;
    transition: transform 0.6s;
    transform-style: preserve-3d;
}

.flashcard.flipped .card-inner {
    transform: rotateY(180deg);
}

.card-front, .card-back {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    border: 2px solid #e5e5e5;
    border-bottom: 6px solid #e5e5e5;
    border-radius: 20px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: white;
}

.card-back {
    transform: rotateY(180deg);
    background: #f0fdf4;
    border-color: #bbf7d0;
    border-bottom-color: #86efac;
}

.category-tag {
    font-size: 0.8rem;
    font-weight: 700;
    color: #afafaf;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.french-word {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1cb0f6;
    margin-bottom: 16px;
}

.spanish-word {
    font-size: 2rem;
    font-weight: 800;
    color: #22c55e;
    margin-bottom: 12px;
}

.context-sentence {
    font-style: italic;
    color: #4b5563;
    font-size: 0.95rem;
}

.audio-btn {
    background: #ddf4ff;
    border: 2px solid #84d8ff;
    border-bottom: 4px solid #84d8ff;
    border-radius: 50%;
    width: 54px;
    height: 54px;
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.1s;
}

.audio-btn:active {
    transform: translateY(2px);
}

.hint-text {
    margin-top: 16px;
    font-size: 0.85rem;
    color: #a0a0a0;
}

.controls {
    display: flex;
    gap: 12px;
    width: 100%;
}

.btn {
    flex: 1;
    padding: 14px;
    border: none;
    border-radius: 16px;
    font-weight: 700;
    font-size: 0.95rem;
    cursor: pointer;
    transition: all 0.1s;
}

.btn-primary {
    background: #58cc02;
    color: white;
    border-bottom: 4px solid #46a302;
}

.btn-primary:active {
    transform: translateY(2px);
    border-bottom: 2px solid #46a302;
}

.btn-secondary {
    background: #e5e5e5;
    color: #4b4b4b;
    border-bottom: 4px solid #cecece;
}

.btn-audio {
    background: #1cb0f6;
    color: white;
    border-bottom: 4px solid #1899d6;
}
"""

    # 3. Crear app.js
    js_content = """let vocabulary = [];
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
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    with open("styles.css", "w", encoding="utf-8") as f:
        f.write(css_content)

    with open("app.js", "w", encoding="utf-8") as f:
        f.write(js_content)

    print("✅ Archivos frontend creados: index.html, styles.css, app.js")

    # Git commit & push
    try:
        subprocess.run(["git", "add", "index.html", "styles.css", "app.js"], check=True)
        subprocess.run(["git", "commit", "-m", "feat: Add interactive Duolingo-style UI for Proyecto Liseur"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("🚀 ¡Sitio subido a GitHub exitosamente!")
    except Exception as e:
        print(f"⚠️ Nota sobre Git/Push: {e}")

if __name__ == "__main__":
    main()
