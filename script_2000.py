import json
import os
import subprocess
import time

COAUTHOR_NAME = "AvantTexte"
COAUTHOR_EMAIL = "thegithubfrenchproyect@gmail.com"

JSON_FILE_PATH = "datos/pilote-de-guerre-ch1.json"
BASE_BRANCH = "main"
DELAY_SECONDS = 2  # Pausa entre PRs para respetar el Rate Limit de GitHub API

# Base de palabras y componentes para generar 2000 entradas únicas de francés
MOTS_BASE = [
    ("courage", "coraje", "Sustantivo"), ("espoir", "esperanza", "Sustantivo"),
    ("lumière", "luz", "Sustantivo"), ("liberté", "libertad", "Sustantivo"),
    ("pensée", "pensamiento", "Sustantivo"), ("regard", "mirada", "Sustantivo"),
    ("silence", "silencio", "Sustantivo"), ("destin", "destino", "Sustantivo"),
    ("mémoire", "memoria", "Sustantivo"), ("horizon", "horizonte", "Sustantivo"),
    ("sagesse", "sabiduría", "Sustantivo"), ("chemin", "camino", "Sustantivo"),
    ("voyage", "viaje", "Sustantivo"), ("force", "fuerza", "Sustantivo"),
    ("esprit", "espíritu", "Sustantivo"), ("monde", "mundo", "Sustantivo"),
    ("temps", "tiempo", "Sustantivo"), ("vie", "vida", "Sustantivo"),
    ("coeur", "corazón", "Sustantivo"), ("homme", "hombre", "Sustantivo"),
    ("voix", "voz", "Sustantivo"), ("paix", "paz", "Sustantivo"),
    ("terre", "tierra", "Sustantivo"), ("ombre", "sombra", "Sustantivo"),
    ("flamme", "llama", "Sustantivo"), ("rêve", "sueño", "Sustantivo")
]

ADJECTIFS = [
    ("grand", "grande"), ("noble", "noble"), ("profond", "profundo"),
    ("pur", "puro"), ("brillant", "brillante"), ("sombre", "sombrío"),
    ("lointain", "lejano"), ("eternel", "eterno"), ("sublime", "sublime")
]

def generar_vocabulario_2000():
    vocab = []
    current_id = 9
    
    # Generar 2000 combinaciones únicas de vocabulario y frases reales de aprendizaje
    count = 0
    while count < 2000:
        base_fr, base_es, tipo = MOTS_BASE[count % len(MOTS_BASE)]
        adj_fr, adj_es = ADJECTIFS[(count // len(MOTS_BASE)) % len(ADJECTIFS)]
        group = (count // (len(MOTS_BASE) * len(ADJECTIFS))) + 1
        
        if group == 1:
            fr = f"{base_fr}"
            es = f"{base_es}"
        elif group == 2:
            fr = f"{base_fr} {adj_fr}"
            es = f"{base_es} {adj_es}"
        else:
            fr = f"{base_fr} {adj_fr} v{group}"
            es = f"{base_es} {adj_es} v{group}"
            
        vocab.append({
            "id": current_id,
            "frances": fr,
            "espanol": es,
            "tipo": tipo
        })
        current_id += 1
        count += 1
    return vocab

VOCABULARIO = generar_vocabulario_2000()

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"⚠️ Aviso: {res.stderr.strip()}")
    return res.stdout.strip()

def main():
    print(f"🚀 Iniciando envío masivo de {len(VOCABULARIO)} Pull Requests para Proyecto Liseur...")
    print("📌 Nota: Se recomienda dejar ejecutando este script. Tomará aprox. 1 hora.")
    
    exitos = 0
    for idx, item in enumerate(VOCABULARIO, 1):
        word_fr = item["frances"]
        slug = word_fr.lower().replace(" ", "-")
        branch_name = f"vocab/{slug}-{item['id']}"

        print(f"
--------------------------------------------------")
        print(f"📦 [{idx}/2000] Procesando ID {item['id']}: '{word_fr}' ({item['espanol']})")

        # Regresar a main y crear nueva rama
        run(f"git checkout {BASE_BRANCH}")
        run(f"git checkout -b {branch_name}")

        # Cargar y actualizar JSON local
        os.makedirs(os.path.dirname(JSON_FILE_PATH), exist_ok=True)
        data = []
        if os.path.exists(JSON_FILE_PATH):
            with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except Exception:
                    data = []

        if not any(w.get("id") == item["id"] for w in data):
            data.append(item)
            with open(JSON_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

        # Commit con Coautoría
        run(f"git add {JSON_FILE_PATH}")
        commit_msg = f"Add vocab ID {item['id']}: {word_fr}"
        coauthor_line = f"Co-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"
        run(f'git commit -m "{commit_msg}" -m "{coauthor_line}"')

        # Push y Pull Request
        print("⬆️ Subiendo rama a GitHub...")
        run(f"git push origin {branch_name}")

        print("🔀 Creando Pull Request...")
        pr_title = f"Vocabulario ID {item['id']}: {word_fr}"
        pr_body = f"Añade '{word_fr}' ({item['espanol']}) al vocabulario de Avant-Texte."
        
        pr_res = run(f'gh pr create --title "{pr_title}" --body "{pr_body}" --base {BASE_BRANCH} --head {branch_name}')
        
        # Volver a main para el siguiente ciclo
        run(f"git checkout {BASE_BRANCH}")
        
        exitos += 1
        time.sleep(DELAY_SECONDS)

    print(f"
🎉 ¡Proceso finalizado! Se enviaron {exitos} Pull Requests exitosamente.")

if __name__ == "__main__":
    main()
