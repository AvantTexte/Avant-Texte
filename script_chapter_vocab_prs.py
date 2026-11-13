import json
import os
import subprocess
import time

COAUTHOR_NAME = "AvantTexte"
COAUTHOR_EMAIL = "thegithubfrenchproyect@gmail.com"
BASE_BRANCH = "main"
DELAY_SECONDS = 2

# Vocabulario real de Pilote de guerre extraído por capítulos con frases literales
VOCABULARY_DATASET = [
    # Chapitre I
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
        "frances": "compas",
        "espanol": "compás / brújula",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Je me sers sagement du compas, de la règle, du rapporteur.",
        "ejemplo_espanol": "Me sirvo sabiamiente del compás, de la regla, del transportador."
    },
    {
        "id": 3,
        "capitulo": "Chapitre I",
        "frances": "enfance",
        "espanol": "infancia",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Je m'enferme avec tant de joie dans cette enfance bien protégée !",
        "ejemplo_espanol": "¡Me encierro con tanta alegría en esta infancia bien protegida!"
    },
    {
        "id": 4,
        "capitulo": "Chapitre I",
        "frances": "désastre",
        "espanol": "desastre",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Nous sommes fin mai, en pleine retraite, en plein désastre.",
        "ejemplo_espanol": "Estamos a fines de mayo, en plena retirada, en pleno desastre."
    },
    {
        "id": 5,
        "capitulo": "Chapitre I",
        "frances": "reconnaissance",
        "espanol": "reconocimiento / exploración",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Nous sommes encore cinquante équipages de Grande Reconnaissance.",
        "ejemplo_espanol": "Aún somos cincuenta tripulaciones de Gran Reconocimiento."
    },
    {
        "id": 6,
        "capitulo": "Chapitre I",
        "frances": "absurde",
        "espanol": "absurdo",
        "tipo": "Adjetivo",
        "ejemplo_frances": "C'est celle de l'absurde. Tout craque autour de nous.",
        "ejemplo_espanol": "Es la impresión de lo absurdo. Todo cruje a nuestro alrededor."
    },

    # Chapitre II
    {
        "id": 7,
        "capitulo": "Chapitre II",
        "frances": "prudence",
        "espanol": "prudencia",
        "tipo": "Sustantivo",
        "ejemplo_frances": "On lui avait tellement parlé de la prudence juive.",
        "ejemplo_espanol": "Le habían hablado tanto de la prudencia judía."
    },
    {
        "id": 8,
        "capitulo": "Chapitre II",
        "frances": "angoisse",
        "espanol": "angustia",
        "tipo": "Sustantivo",
        "ejemplo_frances": "L'angoisse commençait de répandre sur son visage une clarté égale.",
        "ejemplo_espanol": "La angustia comenzaba a extender sobre su rostro una claridad pareja."
    },
    {
        "id": 9,
        "capitulo": "Chapitre II",
        "frances": "esprit",
        "espanol": "espíritu / mente",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Je suis choqué par une évidence: la vie de l'Esprit est intermittente.",
        "ejemplo_espanol": "Me choca una evidencia: la vida del Espíritu es intermitente."
    },
    {
        "id": 10,
        "capitulo": "Chapitre II",
        "frances": "solitude",
        "espanol": "soledad",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Enveloppé dans ma solitude bien-aimée, afin d'y reconnaître pourquoi je dois mourir.",
        "ejemplo_espanol": "Envuelto en mi amada soledad, para reconocer en ella por qué debo morir."
    },

    # Chapitre III
    {
        "id": 11,
        "capitulo": "Chapitre III",
        "frances": "harnacher",
        "espanol": "equiparse / arnesarse",
        "tipo": "Verbo",
        "ejemplo_frances": "On se harnache avec tant de soin pour griller vif.",
        "ejemplo_espanol": "Uno se equipa con tanto cuidado para asarse vivo."
    },
    {
        "id": 12,
        "capitulo": "Chapitre III",
        "frances": "oxygène",
        "espanol": "oxígeno",
        "tipo": "Sustantivo",
        "ejemplo_frances": "D'organiser le circuit d'oxygène, le circuit de chauffage.",
        "ejemplo_espanol": "Organizar el circuito de oxígeno, el circuito de calefacción."
    },
    {
        "id": 13,
        "capitulo": "Chapitre III",
        "frances": "laryngophone",
        "espanol": "laringófono",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Reste à essayer les laryngophones... M'entendez bien ?",
        "ejemplo_espanol": "Falta probar los laringófonos... ¿Me oye bien?"
    },

    # Chapitre IV & V
    {
        "id": 14,
        "capitulo": "Chapitre V",
        "frances": "altitude",
        "espanol": "altitud",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Nous montons vite : six mille sept cents mètres d'altitude.",
        "ejemplo_espanol": "Subimos rápido: seis mil setecientos metros de altitud."
    },
    {
        "id": 15,
        "capitulo": "Chapitre V",
        "frances": "mitrailleuse",
        "espanol": "ametralladora",
        "tipo": "Sustantivo",
        "ejemplo_frances": "J'appuie le bouton en vue du contrôle de mes mitrailleuses.",
        "ejemplo_espanol": "Presiono el botón para controlar mis ametralladoras."
    },
    {
        "id": 16,
        "capitulo": "Chapitre V",
        "frances": "palonnier",
        "espanol": "pedal de dirección (timón)",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Le volant est dur ; quant au palonnier, il est entièrement coincé !",
        "ejemplo_espanol": "¡El volante está duro; en cuanto al pedal del timón, está totalmente atascado!"
    },

    # Chapitre VI & VII
    {
        "id": 17,
        "capitulo": "Chapitre VI",
        "frances": "obstacle",
        "espanol": "obstáculo",
        "tipo": "Sustantivo",
        "ejemplo_frances": "A la façon d'un vieux cheval qui se méfierait de l'obstacle.",
        "ejemplo_espanol": "A la manera de un caballo viejo que recelaría del obstáculo."
    },
    {
        "id": 18,
        "capitulo": "Chapitre VII",
        "frances": "exaltation",
        "espanol": "exaltación",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Il n'est, dans la défaite, aucun espoir d'exaltation.",
        "ejemplo_espanol": "En la derrota no hay ninguna esperanza de exaltación."
    },
    {
        "id": 19,
        "capitulo": "Chapitre VII",
        "frances": "sourire",
        "espanol": "sonrisa / sonreír",
        "tipo": "Sustantivo / Verbo",
        "ejemplo_frances": "Je la vois sourire, tout simplement.",
        "ejemplo_espanol": "La veo sonreír, simplemente."
    },

    # Chapitre VIII & IX
    {
        "id": 20,
        "capitulo": "Chapitre VIII",
        "frances": "chasseur",
        "espanol": "caza (avión de combate)",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Six chasseurs, six, à l'avant-gauche !",
        "ejemplo_espanol": "¡Seis cazas, seis, al frente a la izquierda!"
    },
    {
        "id": 21,
        "capitulo": "Chapitre VIII",
        "frances": "évanouissement",
        "espanol": "desmayo / desvanecimiento",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Elle se traduit par une euphorie vague qui aboutit à l'évanouissement.",
        "ejemplo_espanol": "Se traduce en una euforia vaga que desemboca en el desmayo."
    },
    {
        "id": 22,
        "capitulo": "Chapitre IX",
        "frances": "parachute",
        "espanol": "paracaídas",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Mon genou a été accroché au cours du saut en parachute.",
        "ejemplo_espanol": "Mi rodilla se enganchó durante el salto en paracaídas."
    },

    # Chapitre X & XI
    {
        "id": 23,
        "capitulo": "Chapitre X",
        "frances": "brouillard",
        "espanol": "niebla",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Ces étages de bulles lumineuses qui montent avec la lenteur de voiles de brouillard.",
        "ejemplo_espanol": "Esa sucesión de burbujas luminosas que suben con la lentitud de velos de niebla."
    },
    {
        "id": 24,
        "capitulo": "Chapitre XI",
        "frances": "fécondité",
        "espanol": "fecundidad / calor fecundo",
        "tipo": "Sustantivo",
        "ejemplo_frances": "J'y goûtais la béatitude du repos après les journées dures.",
        "ejemplo_espanol": "Apaladeaba allí la beatitud del descanso tras las jornadas duras."
    },

    # Chapitre XII & XIII
    {
        "id": 25,
        "capitulo": "Chapitre XII",
        "frances": "administration",
        "espanol": "administración",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Nous vivons dans le ventre aveugle d'une administration.",
        "ejemplo_espanol": "Vivimos en el vientre ciego de una administración."
    },
    {
        "id": 26,
        "capitulo": "Chapitre XIII",
        "frances": "incendie",
        "espanol": "incendio",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Il faut que la signification de l'incendie du village équilibre la signification du village.",
        "ejemplo_espanol": "Es preciso que el significado del incendio del pueblo equilibre el significado del pueblo."
    },

    # Chapitre XIV & XV
    {
        "id": 27,
        "capitulo": "Chapitre XIV",
        "frances": "civilisation",
        "espanol": "civilización",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Une civilisation est un héritage de croyances, de coutumes et de connaissances.",
        "ejemplo_espanol": "Una civilización es un legado de creencias, costumbres y conocimientos."
    },
    {
        "id": 28,
        "capitulo": "Chapitre XV",
        "frances": "exode",
        "espanol": "éxodo / evacuación",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Il est une contagion démente dans cet exode.",
        "ejemplo_espanol": "Hay una contagio demente en este éxodo."
    },

    # Chapitre XVI & XVII
    {
        "id": 29,
        "capitulo": "Chapitre XVI",
        "frances": "caravane",
        "espanol": "caravana",
        "tipo": "Sustantivo",
        "ejemplo_frances": "C'est ainsi que commence de se mettre en marche cette caravane condamnée !",
        "ejemplo_espanol": "¡Así comienza a ponerse en marcha esta caravana condenada!"
    },
    {
        "id": 30,
        "capitulo": "Chapitre XVII",
        "frances": "résistance",
        "espanol": "resistencia",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Le premier acte de résistance, s'il survient trop tard, est toujours perdant.",
        "ejemplo_espanol": "El primer acto de resistencia, si ocurre demasiado tarde, siempre es perdedor."
    },

    # Chapitre XVIII & XIX
    {
        "id": 31,
        "capitulo": "Chapitre XVIII",
        "frances": "sacrifice",
        "espanol": "sacrificio",
        "tipo": "Sustantivo",
        "ejemplo_frances": "C'est, à certain heures, pour le combattant, l'acceptation pure et simple de la mort.",
        "ejemplo_espanol": "Es, a ciertas horas, para el combatiente, la aceptación pura y simple de la muerte."
    },
    {
        "id": 32,
        "capitulo": "Chapitre XIX",
        "frances": "Arras",
        "espanol": "Arras (Ciudad escenario del vuelo de reconocimiento)",
        "tipo": "Nombre propio",
        "ejemplo_frances": "Arras n'est rien d'autre qu'une mèche rouge sur fond bleu de nuit.",
        "ejemplo_espanol": "Arras no es otra cosa que una mecha roja sobre fondo azul noche."
    },

    # Chapitre XX - XXVIII
    {
        "id": 33,
        "capitulo": "Chapitre XX",
        "frances": "invulnérable",
        "espanol": "invulnerable",
        "tipo": "Adjetivo",
        "ejemplo_frances": "Je me découvre invulnérable. Je me sens comme vainqueur !",
        "ejemplo_espanol": "Me descubro invulnerable. ¡Me siento como vencedor!"
    },
    {
        "id": 34,
        "capitulo": "Chapitre XXII",
        "frances": "fraternité",
        "espanol": "fraternidad",
        "tipo": "Sustantivo",
        "ejemplo_frances": "Rien n'abîmera cette fraternité. Je suis de mon Groupe plus que jamais.",
        "ejemplo_espanol": "Nada arruinará esta fraternidad. Soy de mi Grupo más que nunca."
    },
    {
        "id": 35,
        "capitulo": "Chapitre XXIV",
        "frances": "pain",
        "espanol": "pan",
        "tipo": "Sustantivo",
        "ejemplo_frances": "La saveur du pain partagé n'a point d'égale.",
        "ejemplo_espanol": "El sabor del pan compartido no tiene igual."
    },
    {
        "id": 36,
        "capitulo": "Chapitre XXVII",
        "frances": "cathédrale",
        "espanol": "catedral",
        "tipo": "Sustantivo",
        "ejemplo_frances": "On meurt pour une cathédrale. Non pour des pierres.",
        "ejemplo_espanol": "Uno muere por una catedral. No por piedras."
    }
]

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.returncode != 0 and "Aviso" not in res.stderr:
        print(f"  [Info/Git]: {res.stderr.strip()}")
    return res.stdout.strip()

def update_web_app_code():
    """Actualiza la interfaz HTML/JS para dar soporte a la selección por Capítulos."""
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proyecto Liseur - Francés con Pilote de guerre</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <div class="logo">
                <span class="flag">🇫🇷</span>
                <h1>Proyecto Liseur</h1>
            </div>
            <!-- Filtro de Capítulos -->
            <div class="chapter-filter-container">
                <label for="chapter-select">📖 Capítulo:</label>
                <select id="chapter-select" onchange="filterByChapter()">
                    <option value="ALL">Todos los Capítulos</option>
                </select>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar" id="progress-bar"></div>
            </div>
        </header>

        <!-- Main Content Area -->
        <main class="flashcard-section">
            <div class="card-container" id="card-container" onclick="flipCard()">
                <div class="card-inner" id="card-inner">
                    <!-- Frente (Francés) -->
                    <div class="card-front">
                        <span class="chapter-badge" id="card-chapter">Chapitre I</span>
                        <span class="badge" id="card-type">Sustantivo</span>
                        <h2 class="word-fr" id="card-fr">Chargement...</h2>
                        <p class="click-hint">Haz clic para ver traducción 🔄</p>
                        <button class="audio-btn" onclick="event.stopPropagation(); speakWord();">
                            🔊 Escuchar
                        </button>
                    </div>
                    <!-- Reverso (Español + Frase de la novela) -->
                    <div class="card-back">
                        <h3 class="word-es" id="card-es">Cargando...</h3>
                        <div class="quote-box">
                            <p class="quote-fr" id="quote-fr">""</p>
                            <p class="quote-es" id="quote-es">""</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Botones de Acción -->
            <div class="action-buttons">
                <button class="btn btn-again" onclick="nextCard(false)">❌ Repasar luego</button>
                <button class="btn btn-know" onclick="nextCard(true)">✅ La conozco</button>
            </div>
        </main>

        <!-- Footer Stats -->
        <footer class="app-footer">
            <p>Ficha <span id="current-index">1</span> de <span id="total-cards">0</span> | <span id="chapter-name">Pilote de guerre</span></p>
        </footer>
    </div>

    <script src="app.js"></script>
</body>
</html>'''

    js_content = '''let vocabulary = [];
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
'''

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open("app.js", "w", encoding="utf-8") as f:
        f.write(js_content)

def main():
    print("🚀 Iniciando generación de fichas por capítulo y ejecutor de Pull Requests...")

    # 1. Asegurar la estructura frontend
    update_web_app_code()

    # 2. Generar fichas individuales y ejecutarlas como PRs
    for item in VOCABULARY_DATASET:
        item_id = item["id"]
        word_fr = item["frances"]
        word_es = item["espanol"]
        capitulo = item["capitulo"]

        file_path = f"datos/vocab/word_{item_id}.json"
        branch_name = f"vocab/chapter-word-{item_id}"

        print(f"\n--------------------------------------------------")
        print(f"📦 [{capitulo}] Ficha #{item_id}: {word_fr} ({word_es})")

        run(f"git checkout {BASE_BRANCH}")
        run("git pull origin main")

        run(f"git checkout -b {branch_name}")

        # Guardar archivo individual
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=2)

        # Actualizar índice general
        index_items = []
        for i_item in VOCABULARY_DATASET:
            if i_item["id"] <= item_id:
                index_items.append(i_item)
        with open("datos/index.json", "w", encoding="utf-8") as f:
            json.dump(index_items, f, ensure_ascii=False, indent=2)

        # Commit con coautoría
        run("git add .")
        commit_msg = f"feat({capitulo}): Add vocab #{item_id} {word_fr} with literal sentence"
        coauthor_line = f"Co-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"
        run(f'git commit -m "{commit_msg}" -m "{coauthor_line}"')

        # Push y Pull Request
        print("⬆️ Subiendo rama...")
        run(f"git push origin {branch_name}")

        print("🔀 Abriendo Pull Request...")
        pr_title = f"Vocabulario [{capitulo}] #{item_id}: {word_fr}"
        pr_body = f"Añade la ficha #{item_id} de {capitulo} ({word_fr} - {word_es}) con cita textual de Pilote de guerre."
        run(f'gh pr create --title "{pr_title}" --body "{pr_body}" --base {BASE_BRANCH} --head {branch_name}')

        print("⚡ Fusionando Pull Request automáticamente...")
        run(f"gh pr merge {branch_name} --merge --delete-branch")

        run(f"git checkout {BASE_BRANCH}")
        run("git pull origin main")

        time.sleep(DELAY_SECONDS)

    print("\n🎉 ¡Todas las fichas por capítulo han sido creadas y fusionadas con éxito!")

if __name__ == "__main__":
    main()
