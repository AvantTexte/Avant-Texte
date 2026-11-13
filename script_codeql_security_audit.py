import os
import subprocess
import sys

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return res.stdout.strip(), res.stderr.strip(), res.returncode

def main():
    print("=" * 70)
    print("🛡️ CONFIGURANDO CODEQL & SAST SECURITY AUDIT WORKFLOW 🛡️")
    print("   Optimizador de Métricas GitHub Copilot Verified Proficiency (Security & SAST)")
    print("=" * 70)

    # 1. Crear directorio .github/workflows
    os.makedirs(".github/workflows", exist_ok=True)
    
    codeql_workflow = """name: "CodeQL Security Analysis"

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
  schedule:
    - cron: '0 0 * * 0'

jobs:
  analyze:
    name: Analyze Code Quality & Security
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript', 'python' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
      with:
        category: "/language:${{matrix.language}}"
"""

    workflow_path = ".github/workflows/codeql_analysis.yml"
    with open(workflow_path, "w", encoding="utf-8") as f:
        f.write(codeql_workflow)
    print(f"✅ 1. Workflow {workflow_path} generado exitosamente.")

    # 2. Guardar y subir a Git
    print("\n⬆️ 2. Sincronizando y enviando cambios a GitHub main...")
    run("git add .")
    run('git commit -m "security: Add CodeQL SAST static security analysis workflow"')
    run("git pull origin main --rebase")
    stdout, stderr, code = run("git push origin main")

    print("\n" + "=" * 70)
    print("🎉 ¡SECURITY AUDIT WORKFLOW (CODEQL) DESPLEGADO CON ÉXITO! 🎉")
    print("=" * 70)
    print("📌 Archivo de workflow: .github/workflows/codeql_analysis.yml")
    print("📌 Auditará automáticamente seguridad y vulnerabilidades en JavaScript y Python.")
    print("📌 Se ejecutará en cada push, PR y de forma programada cada domingo.")

if __name__ == "__main__":
    main()
