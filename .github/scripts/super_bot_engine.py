import os
import subprocess
from datetime import datetime

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    print(f"Executing: {cmd}")
    if res.stdout:
        print(f"STDOUT: {res.stdout.strip()}")
    if res.stderr:
        print(f"STDERR: {res.stderr.strip()}")
    return res

def execute_autonomous_cycle():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now_str}] 🚀 Iniciando ciclo autónomo del Super Bot...")

    # Asegurar rama main y pull previo
    run("git checkout main")
    run("git pull origin main --rebase")

    # Actualizar indicador de pulso en README.md
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
            content = "\n".join(new_lines)
        else:
            content += f"\n\n### 🤖 Bot Autonomous Heartbeat\n\n| Métrica | Estado |\n|---|---|\n{status_line}\n"

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

    # Configurar Git bot author
    run('git config user.name "github-actions[bot]"')
    run('git config user.email "github-actions[bot]@users.noreply.github.com"')
    
    # Comprobar si hay cambios pendientes antes de hacer commit
    status_res = run("git status --porcelain")
    if status_res.stdout.strip():
        run("git add .")
        commit_res = run(f'git commit -m "chore(bot): 24/7 Cloud Autonomous Pulse [{now_str}] [skip ci]"')
        if commit_res.returncode == 0:
            push_res = run("git push origin main")
            if push_res.returncode == 0:
                print("✅ Ciclo completado y sincronizado exitosamente con GitHub main.")
            else:
                print("⚠️ Falló el push. Reintentando rebase...")
                run("git pull origin main --rebase")
                run("git push origin main")
    else:
        print("ℹ️ No hay cambios que confirmar en este ciclo.")

if __name__ == "__main__":
    execute_autonomous_cycle()
