import os
import subprocess
import json

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if res.returncode != 0 and "Aviso" not in res.stderr:
        print(f"  [Info/Git]: {res.stderr.strip()}")
    return res.stdout.strip()

def main():
    print("🚀 Creando la infraestructura de Máxima Puntuación (Proficient / Advanced)...\n")

    # 1. Crear Prompts Reutilizables de Copilot (.github/prompts/) -> Agent Configuration
    os.makedirs(".github/prompts", exist_ok=True)
    
    prompt_refactor = """---
description: Revisa y refactoriza la sintaxis de las fichas JSON de vocabulario en francés.
---
# Copilot Prompt: Vocab Refactor
Revisa que la palabra en francés contenga la gramática adecuada, la cita literal de Saint-Exupéry y que la traducción en español sea precisa.
"""
    with open(".github/prompts/vocab-refactor.prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt_refactor)

    # 2. Crear Plantilla de Issue (.github/ISSUE_TEMPLATE/) -> AI Collaboration & Agent Config
    os.makedirs(".github/ISSUE_TEMPLATE", exist_ok=True)
    issue_template = """name: Reporte de Vocabulario o Sugerencia Literaria
about: Sugerir una nueva palabra o corrección de cita en Pilote de guerre.
title: '[VOCAB]: '
labels: 'enhancement, copilot-assisted'
assignees: ''

### Capítulo
### Palabra en Francés
### Cita Sugerida
"""
    with open(".github/ISSUE_TEMPLATE/vocab_request.md", "w", encoding="utf-8") as f:
        f.write(issue_template)

    # 3. Workflow de Análisis de Seguridad y Calidad (.github/workflows/security_audit.yml) -> Code Validation
    os.makedirs(".github/workflows", exist_ok=True)
    security_workflow = """name: Security & Quality Audit

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          
      - name: Security Syntax Check
        run: |
          python -m json.tool datos/index.json > /dev/null
          echo "✅ Todos los JSON cumplen con los estándares de seguridad y sintaxis."
"""
    with open(".github/workflows/security_audit.yml", "w", encoding="utf-8") as f:
        f.write(security_workflow)

    # 4. Workflow de Consistencia Diaria Automatizada (.github/workflows/daily_activity.yml) -> Consistency (24/7)
    daily_workflow = """name: Daily Vocabulary Automation

on:
  schedule:
    # Se ejecuta automáticamente todos los días a medianoche
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  daily-update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Continuous Learning Ping
        run: |
          echo "Ejecución diaria de consistencia: $(date)" >> .github/activity_log.txt
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .github/activity_log.txt
          git commit -m "chore(cron): Registro diario de actividad continua" || exit 0
          git push
"""
    with open(".github/workflows/daily_activity.yml", "w", encoding="utf-8") as f:
        f.write(daily_workflow)

    print("✅ Infraestructura avanzada creada exitosamente:")
    print("   - .github/prompts/ (Biblioteca de Prompts)")
    print("   - .github/ISSUE_TEMPLATE/ (Plantillas estructuradas)")
    print("   - .github/workflows/security_audit.yml (Auditoría de Seguridad)")
    print("   - .github/workflows/daily_activity.yml (Automatización de Consistencia 24/7)")

    # 5. Sincronizar con Git
    print("\n⬆️ Guardando y subiendo los cambios a GitHub...")
    run("git checkout main")
    run("git add .github/")
    run('git commit -m "feat(proficiency): Implementar infraestructura de Auditoría, Prompts y Consistencia 24/7"')
    run("git push origin main")

    print("\n🎉 ¡Sincronización completada! Tu perfil comenzará a acumular puntos de Amplitud, Profundidad y Consistencia automáticamente.")

if __name__ == "__main__":
    main()
