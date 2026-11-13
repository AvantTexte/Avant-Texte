let vocabulary = [
    {
        "id": 1,
        "capitulo": "Chapitre I",
        "frances": "camarade",
        "espanol": "camarada / compañero",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Des camarades, auprès de moi, parlent à voix basse.",
        "ejemplo_espanol": "Unos camaradas, cerca de mí, hablan en voz baja."
    },
    {
        "id": 2,
        "capitulo": "Chapitre I",
        "frances": "pilote",
        "espanol": "piloto",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Le pilote se retrouve seul face à la nuit et au ciel.",
        "ejemplo_espanol": "El piloto se encuentra solo ante la noche y el cielo."
    },
    {
        "id": 3,
        "capitulo": "Chapitre II",
        "frances": "solitude",
        "espanol": "soledad",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Enveloppé dans ma solitude bien-aimée pour comprendre.",
        "ejemplo_espanol": "Envuelto en mi amada soledad para comprender."
    }
];

let filteredVocabulary = [];
let currentIndex = 0;
let isFlipped = false;
let currentQuizItem = null;

let userXP = parseInt(localStorage.getItem("liseur_xp") || "0");
let userLevel = Math.floor(userXP / 100) + 1;

document.addEventListener("DOMContentLoaded", () => {
    updateUserStatsUI();
    filteredVocabulary = [...vocabulary];
    populateChapterDropdown();
    showCard();
    loadVocabulary();
});

function updateUserStatsUI() {
    userLevel = Math.floor(userXP / 100) + 1;
    document.getElementById("user-xp").innerText = userXP;
    document.getElementById("user-level").innerText = userLevel;
    localStorage.setItem("liseur_xp", userXP.toString());
}

function addXP(amount) {
    userXP += amount;
    updateUserStatsUI();
}

async function loadVocabulary() {
    try {
        const response = await fetch("datos/index.json");
        if (response.ok) {
            const data = await response.json();
            if (Array.isArray(data) && data.length > 0) {
                vocabulary = data;
                populateChapterDropdown();
                filterByChapter();
            }
        }
    } catch (error) {
        console.log("Usando vocabulario precargado.");
    }
}

function switchMode(mode) {
    document.getElementById("btn-mode-cards").classList.toggle("active", mode === "cards");
    document.getElementById("btn-mode-quiz").classList.toggle("active", mode === "quiz");

    document.getElementById("section-cards").classList.toggle("hidden", mode !== "cards");
    document.getElementById("section-quiz").classList.toggle("hidden", mode !== "quiz");

    if (mode === "quiz") {
        setupNextQuizQuestion();
    }
}

function populateChapterDropdown() {
    const select = document.getElementById("chapter-select");
    const chapters = [...new Set(vocabulary.map(item => item.capitulo || "Chapitre I"))];
    
    select.innerHTML = '<option value="ALL">Todos los Capítulos (' + vocabulary.length + ' palabras)</option>';
    chapters.forEach(chap => {
        const count = vocabulary.filter(i => (i.capitulo || "Chapitre I") === chap).length;
        const opt = document.createElement("option");
        opt.value = chap;
        opt.textContent = `${chap} (${count} palabras)`;
        select.appendChild(opt);
    });
}

function filterByChapter() {
    const selected = document.getElementById("chapter-select").value;
    if (selected === "ALL") {
        filteredVocabulary = [...vocabulary];
    } else {
        filteredVocabulary = vocabulary.filter(item => item.capitulo === selected);
    }
    
    currentIndex = 0;
    isFlipped = false;
    document.getElementById("card-inner").classList.remove("flipped");
    showCard();
    setupNextQuizQuestion();
}

function showCard() {
    if (filteredVocabulary.length === 0) return;
    
    const item = filteredVocabulary[currentIndex];
    
    document.getElementById("card-fr").innerText = item.frances;
    document.getElementById("card-es").innerText = item.espanol;
    document.getElementById("card-type").innerText = item.tipo || "Vocabulario";
    document.getElementById("card-chapter").innerText = item.capitulo || "Pilote de guerre";
    
    document.getElementById("quote-fr").innerText = item.ejemplo_frances ? `"${item.ejemplo_frances}"` : "";
    document.getElementById("quote-es").innerText = item.ejemplo_espanol ? `"${item.ejemplo_espanol}"` : "";
    
    document.getElementById("current-index").innerText = currentIndex + 1;
    document.getElementById("total-cards").innerText = filteredVocabulary.length;
    
    const progressPercent = ((currentIndex + 1) / filteredVocabulary.length) * 100;
    document.getElementById("progress-bar").style.width = `${progressPercent}%`;
}

function flipCard() {
    isFlipped = !isFlipped;
    document.getElementById("card-inner").classList.toggle("flipped", isFlipped);
}

function nextCard(known) {
    if (known) addXP(5);
    if (isFlipped) {
        flipCard();
        setTimeout(() => advanceCard(), 250);
    } else {
        advanceCard();
    }
}

function advanceCard() {
    if (filteredVocabulary.length === 0) return;
    currentIndex = (currentIndex + 1) % filteredVocabulary.length;
    showCard();
}

/* QUIZ SYSTEM */
function setupNextQuizQuestion() {
    if (filteredVocabulary.length === 0) return;
    
    currentQuizItem = filteredVocabulary[Math.floor(Math.random() * filteredVocabulary.length)];
    
    document.getElementById("quiz-fr").innerText = currentQuizItem.frances;
    document.getElementById("quiz-chapter").innerText = currentQuizItem.capitulo || "Pilote de guerre";
    document.getElementById("quiz-feedback").classList.add("hidden");

    // Generar 4 opciones (1 correcta + 3 distractores)
    let options = [currentQuizItem.espanol];
    let pool = vocabulary.map(v => v.espanol).filter(e => e !== currentQuizItem.espanol);
    
    // Mezclar distractores
    pool.sort(() => 0.5 - Math.random());
    options.push(...pool.slice(0, 3));
    options.sort(() => 0.5 - Math.random());

    const container = document.getElementById("quiz-options");
    container.innerHTML = "";

    options.forEach(opt => {
        const btn = document.createElement("button");
        btn.className = "option-btn";
        btn.innerText = opt;
        btn.onclick = () => checkQuizAnswer(btn, opt);
        container.appendChild(btn);
    });
}

function checkQuizAnswer(selectedBtn, chosenText) {
    const allBtns = document.querySelectorAll(".option-btn");
    allBtns.forEach(b => b.disabled = true);

    const isCorrect = chosenText === currentQuizItem.espanol;
    const feedbackText = document.getElementById("feedback-text");

    if (isCorrect) {
        selectedBtn.classList.add("correct");
        feedbackText.innerText = "🎉 ¡Excelente! +10 XP";
        feedbackText.style.color = "#58cc02";
        addXP(10);
    } else {
        selectedBtn.classList.add("incorrect");
        allBtns.forEach(b => {
            if (b.innerText === currentQuizItem.espanol) b.classList.add("correct");
        });
        feedbackText.innerText = `❌ Respuesta correcta: ${currentQuizItem.espanol}`;
        feedbackText.style.color = "#ff4b4b";
    }

    document.getElementById("quiz-feedback").classList.remove("hidden");
    speakWordText(currentQuizItem.frances);
}

function nextQuizQuestion() {
    setupNextQuizQuestion();
}

function speakWord() {
    if (filteredVocabulary.length === 0) return;
    speakWordText(filteredVocabulary[currentIndex].frances);
}

function speakQuizWord() {
    if (currentQuizItem) speakWordText(currentQuizItem.frances);
}

function speakWordText(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "fr-FR";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
}


// === LÓGICA DE NAVEGACIÓN Y DASHBOARD DE ESTADÍSTICAS ===
document.addEventListener('DOMContentLoaded', () => {
    const tabCards = document.getElementById('tab-cards');
    const tabQuiz = document.getElementById('tab-quiz');
    const tabStats = document.getElementById('tab-stats');

    const flashcardView = document.getElementById('flashcard-view') || document.querySelector('.card-container');
    const quizView = document.getElementById('quiz-view');
    const statsView = document.getElementById('stats-view');

    function switchTab(activeTab, activeView) {
        [tabCards, tabQuiz, tabStats].forEach(t => t && t.classList.remove('active'));
        [flashcardView, quizView, statsView].forEach(v => v && (v.style.display = 'none'));

        if (activeTab) activeTab.classList.add('active');
        if (activeView) activeView.style.display = 'block';

        if (activeView === statsView) {
            updateStatsView();
        }
    }

    if (tabCards) tabCards.addEventListener('click', () => switchTab(tabCards, flashcardView));
    if (tabQuiz) tabQuiz.addEventListener('click', () => switchTab(tabQuiz, quizView));
    if (tabStats) tabStats.addEventListener('click', () => switchTab(tabStats, statsView));

    const btnReset = document.getElementById('btn-reset-stats');
    if (btnReset) {
        btnReset.addEventListener('click', () => {
            if (confirm('¿Deseas reiniciar todas tus estadísticas de estudio?')) {
                localStorage.removeItem('user_xp');
                localStorage.removeItem('cards_seen_count');
                localStorage.removeItem('quiz_correct_count');
                localStorage.removeItem('quiz_total_count');
                updateStatsView();
            }
        });
    }
});

function updateStatsView() {
    const xp = parseInt(localStorage.getItem('user_xp') || '0');
    const cardsSeen = parseInt(localStorage.getItem('cards_seen_count') || '0');
    const quizCorrect = parseInt(localStorage.getItem('quiz_correct_count') || '0');
    const quizTotal = parseInt(localStorage.getItem('quiz_total_count') || '0');

    const elCards = document.getElementById('stat-cards-learned');
    const elXp = document.getElementById('stat-total-xp');
    const elAccuracy = document.getElementById('stat-accuracy');
    const elTime = document.getElementById('stat-study-time');
    const elFill = document.getElementById('global-progress-fill');
    const elProgressText = document.getElementById('progress-percentage-text');

    const totalCards = 1024;
    const progressPct = Math.min(100, Math.round((cardsSeen / totalCards) * 100));

    if (elCards) elCards.textContent = `${cardsSeen} / ${totalCards}`;
    if (elXp) elXp.textContent = `${xp} XP`;
    
    const accuracyPct = quizTotal > 0 ? Math.round((quizCorrect / quizTotal) * 100) : 0;
    if (elAccuracy) elAccuracy.textContent = `${accuracyPct}%`;

    const estMinutes = Math.round((cardsSeen * 0.5) + (quizTotal * 0.8));
    if (elTime) elTime.textContent = `${estMinutes} min`;

    if (elFill) elFill.style.width = `${progressPct}%`;
    if (elProgressText) elProgressText.textContent = `${progressPct}% del vocabulario del libro completado`;
}
