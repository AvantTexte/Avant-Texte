import os
import subprocess
import json
import re
from datetime import datetime

BASE_BRANCH = "main"

def run(cmd):
    res = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    return res.stdout.strip()

def main():
    print("=" * 70)
    print("📊 AGREGANDO PESTAÑA DE ESTADÍSTICAS DE ESTUDIO Y PROGRESO (WEB APP) 📊")
    print("   Proyecto Liseur - Francés & GitHub Badges")
    print("=" * 70)

    # 1. Verificar archivos principales
    if not os.path.exists("index.html") or not os.path.exists("app.js"):
        print("❌ Error: No se encontraron index.html o app.js en el directorio actual.")
        print("   Asegúrate de ejecutar este script dentro de ~/Avant-Texte/")
        return

    print("\n📝 1. Actualizando index.html con navegación a Estadísticas...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Añadir botón de navegación si no existe
    if 'id="tab-stats"' not in html:
        nav_target = '<button class="nav-btn" id="tab-quiz">🎮 Quiz XP</button>'
        nav_replacement = nav_target + '\n      <button class="nav-btn" id="tab-stats">📊 Progreso</button>'
        if nav_target in html:
            html = html.replace(nav_target, nav_replacement)
        else:
            # Fallback en caso de estructura distinta
            html = html.replace('</nav>', '  <button class="nav-btn" id="tab-stats">📊 Progreso</button>\n</nav>')

    # Añadir sección del Dashboard de Stats si no existe
    if 'id="stats-view"' not in html:
        stats_section_html = """
    <!-- VISTA DE ESTADÍSTICAS Y PROGRESO -->
    <section id="stats-view" class="view-section" style="display: none;">
      <div class="stats-container">
        <h2>📊 Tu Panel de Progreso & Métricas</h2>
        <p class="stats-subtitle">Seguimiento de vocabulario de <em>Pilote de guerre</em></p>
        
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">🎴</div>
            <div class="stat-value" id="stat-cards-learned">0 / 1024</div>
            <div class="stat-label">Tarjetas Vistas</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-value" id="stat-total-xp">0 XP</div>
            <div class="stat-label">Experiencia Acumulada</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-value" id="stat-accuracy">0%</div>
            <div class="stat-label">Precisión en Quiz</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-value" id="stat-study-time">0 min</div>
            <div class="stat-label">Tiempo Estimado</div>
          </div>
        </div>

        <div class="chapter-progress-section">
          <h3>📖 Progreso General por Capítulos (I - XXVII)</h3>
          <div class="progress-bar-container">
            <div class="progress-bar-fill" id="global-progress-fill" style="width: 0%;"></div>
          </div>
          <p id="progress-percentage-text">0% del vocabulario del libro completado</p>
        </div>

        <div class="stats-actions">
          <button id="btn-reset-stats" class="btn-secondary-danger">🔄 Reiniciar Métricas</button>
        </div>
      </div>
    </section>
"""
        html = html.replace('</main>', stats_section_html + '\n  </main>')

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("  ✅ index.html actualizado.")

    print("\n🎨 2. Añadiendo estilos CSS para el Dashboard...")
    with open("styles.css", "r", encoding="utf-8") as f:
        css = f.read()

    if '.stats-container' not in css:
        extra_css = """

/* === ESTILOS DASHBOARD DE ESTADÍSTICAS === */
.stats-container {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: 20px;
}
.stats-subtitle {
  color: #a0aec0;
  margin-bottom: 24px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin-bottom: 28px;
}
.stat-card {
  background: rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}
.stat-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}
.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #6366f1;
}
.stat-label {
  font-size: 0.85rem;
  color: #cbd5e1;
  margin-top: 4px;
}
.chapter-progress-section {
  background: rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 20px;
}
.progress-bar-container {
  background: #334155;
  height: 16px;
  border-radius: 8px;
  overflow: hidden;
  margin: 12px 0;
}
.progress-bar-fill {
  background: linear-gradient(90deg, #6366f1, #a855f7);
  height: 100%;
  transition: width 0.5s ease-in-out;
}
.btn-secondary-danger {
  background: transparent;
  border: 1px solid #ef4444;
  color: #f87171;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-secondary-danger:hover {
  background: #ef4444;
  color: #fff;
}
"""
        css += extra_css
        with open("styles.css", "w", encoding="utf-8") as f:
            f.write(css)
    print("  ✅ styles.css actualizado.")

    print("\n⚙️ 3. Integrando lógica en app.js para cálculo en tiempo real...")
    with open("app.js", "r", encoding="utf-8") as f:
        js = f.read()

    if 'function updateStatsView()' not in js:
        stats_js = """

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
"""
        js += stats_js
        with open("app.js", "w", encoding="utf-8") as f:
            f.write(js)
    print("  ✅ app.js actualizado.")

    print("\n⬆️ 4. Subiendo actualización a GitHub main...")
    run("git add .")
    run('git commit -m "feat(web): Add Study Statistics & Progress Dashboard tab"')
    run(f"git pull origin {BASE_BRANCH} --rebase >/dev/null 2>&1")
    push_res = run(f"git push origin {BASE_BRANCH}")
    print(f"  Result: {push_res}")

    print("\n" + "=" * 70)
    print("🎉 ¡DASHBOARD DE ESTADÍSTICAS Y PROGRESO DESPLEGADO CON ÉXITO! 🎉")
    print("=" * 70)
    print("📌 Nueva pestaña: 📊 Progreso en tu aplicación web.")
    print("📌 Métricas en tiempo real: Tarjetas vistas, XP, % de precisión y tiempo de estudio.")
    print("📌 Persistencia automática mediante LocalStorage.")

if __name__ == "__main__":
    main()
