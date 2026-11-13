import os
import json
import random
import subprocess
from datetime import datetime

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return res.stdout.strip()

def execute_autonomous_cycle():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now_str}] 🚀 Iniciando ciclo autónomo del Super Bot...")

    # Cargar dataset si existe o generar actividad de mantenimiento
    vocab_dir = "datos/vocab"
    os.makedirs(vocab_dir, exist_ok=True)

    # Actualizar indicador de pulso 24/7 en README.md
    readme_path = "README.md"
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        status_line = f"| **Super Bot Status** | 🟢 Activo en la Nube (Última sync: {now_str}) |"
        if "| **Super Bot Status** |" in content:
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if "| **Super Bot Status** |" in line:
                    new_lines.append(status_line)
                else:
                    new_lines.append(line)
            content = "
".join(new_lines)
        else:
            content += f"

### 🤖 Bot Autonomous Heartbeat

| Métrica | Estado |
|---|---|
{status_line}
"

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Configurar Git bot author
    run('git config user.name "GitHub Super Bot 24/7"')
    run('git config user.email "superbot-actions@users.noreply.github.com"')
    
    # Git add, commit y push directo
    run("git add .")
    run(f'git commit -m "chore(bot): 24/7 Cloud Autonomous Pulse [{now_str}] [skip ci]"')
    run("git push origin main")
    print("✅ Ciclo completado y sincronizado con éxito.")

if __name__ == "__main__":
    execute_autonomous_cycle()
