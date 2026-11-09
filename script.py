import json
import os
import subprocess
import time

# Configuración de tu cuenta secundaria (AvantTexte)
COAUTHOR_NAME = "AvantTexte"
COAUTHOR_EMAIL = "thegithubfrenchproyect@gmail.com"

JSON_FILE_PATH = "datos/pilote-de-guerre-ch1.json"
BASE_BRANCH = "main"
DELAY_SECONDS = 4

# Vocabulario extraído de Pilote de guerre
VOCABULARIO = [
    {"id": 1, "frances": "guerre", "espanol": "guerra", "tipo": "Sustantivo"},
    {"id": 2, "frances": "pilote", "espanol": "piloto", "tipo": "Sustantivo"},
    {"id": 3, "frances": "vol", "espanol": "vuelo", "tipo": "Sustantivo"},
    {"id": 4, "frances": "avion", "espanol": "avión", "tipo": "Sustantivo"},
    {"id": 5, "frances": "mission", "espanol": "misión", "tipo": "Sustantivo"},
    {"id": 6, "frances": "ciel", "espanol": "cielo", "tipo": "Sustantivo"},
    {"id": 7, "frances": "nuit", "espanol": "noche", "tipo": "Sustantivo"},
    {"id": 8, "frances": "camarade", "espanol": "camarada", "tipo": "Sustantivo"}
]

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.returncode != 0:
        print(f"Aviso: {res.stderr.strip()}")
    return res.stdout.strip()

def main():
    print("🚀 Iniciando envío de Pull Requests...")

    for item in VOCABULARIO:
        word_fr = item["frances"]
        branch_name = f"vocab/{word_fr.lower()}-{item['id']}"

        print(f"\n--------------------------------------------------")
        print(f"📦 Procesando: {word_fr} ({item['espanol']})")

        # Volver a main y crear rama
        run(f"git checkout {BASE_BRANCH}")
        run(f"git checkout -b {branch_name}")

        # Guardar en archivo JSON
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
        commit_msg = f"Add word: {word_fr}"
        coauthor_line = f"Co-authored-by: {COAUTHOR_NAME} <{COAUTHOR_EMAIL}>"
        run(f'git commit -m "{commit_msg}" -m "{coauthor_line}"')

        # Subir y crear Pull Request
        print("⬆️ Subiendo rama a GitHub...")
        run(f"git push origin {branch_name}")

        print("🔀 Abriendo Pull Request...")
        pr_title = f"Vocabulario: {word_fr}"
        pr_body = f"Añade {word_fr} al vocabulario."
        run(f'gh pr create --title "{pr_title}" --body "{pr_body}" --base {BASE_BRANCH} --head {branch_name}')

        run(f"git checkout {BASE_BRANCH}")
        time.sleep(DELAY_SECONDS)

    print("\n🎉 ¡Todos los Pull Requests han sido enviados!")

if __name__ == "__main__":
    main()
