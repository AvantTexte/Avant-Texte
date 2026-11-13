let vocabulary = [];
let filteredVocabulary = [];
let currentIndex = 0;
let isFlipped = false;

document.addEventListener("DOMContentLoaded", () => {
    loadVocabulary();
});

async function loadVocabulary() {
    try {
        const response = await fetch("datos/index.json");
        if (!response.ok) throw new Error("Index no encontrado");
        vocabulary = await response.json();
        
        populateChapterDropdown();
        filterByChapter();
    } catch (error) {
        console.error("Error al cargar el vocabulario:", error);
        document.getElementById("card-fr").innerText = "Guerre";
        document.getElementById("card-es").innerText = "Guerra";
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

function speakWord() {
    if (filteredVocabulary.length === 0) return;
    const item = filteredVocabulary[currentIndex];
    const utterance = new SpeechSynthesisUtterance(item.frances);
    utterance.lang = "fr-FR";
    utterance.rate = 0.9;
    window.speechSynthesis.speak(utterance);
}
