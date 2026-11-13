# 🇫🇷 Proyecto Liseur - Aprendizaje de Francés con *Pilote de guerre*

![Build Status](https://github.com/AvantTexte/Avant-Texte/actions/workflows/test_and_badge.yml/badge.svg)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20App-58CC02?style=flat&logo=github)
![Vocabulary Count](https://img.shields.io/badge/Vocabulario-1024%20Fichas-1CB0F6?style=flat&logo=duolingo)
![Level](https://img.shields.io/badge/Nivel-B1%20--%20B2-orange)
![License](https://img.shields.io/badge/Licencia-MIT-green)

**Proyecto Liseur** es una aplicación web interactiva estilo Duolingo diseñada para aprender vocabulario en francés extraído directamente de la novela clásica ***Pilote de guerre*** de Antoine de Saint-Exupéry.

---

## 🌟 Características Principales

- 📖 **Organización por Capítulos:** Explora el vocabulario de forma estructurada desde el *Chapitre I* hasta el *Chapitre XXVIII*.
- 🔄 **Tarjetas Interactivas 3D:** Voltea las fichas para descubrir la traducción al español, el tipo de palabra y la cita textual literal del libro.
- 🔊 **Audio Nativo en Francés:** Pronunciación integrada utilizando el motor de síntesis de voz nativo del navegador (`fr-FR`).
- ⚡ **Validación Automática de Datos:** CI/CD configurado en GitHub Actions para asegurar la validez de los esquemas JSON.

---

## 🚀 Probar la Aplicación Web

La aplicación se encuentra desplegada de forma pública en **GitHub Pages**:

👉 **[Ver Aplicación en Vivo](https://AvantTexte.github.io/Avant-Texte/)**

---

## ⚙️ Estructura del Proyecto

```text
Avant-Texte/
├── index.html                  # Interfaz principal responsive
├── styles.css                  # Estilos visuales inspiración Duolingo
├── app.js                      # Lógica interactiva y motor de audio
├── datos/
│   ├── index.json              # Índice general de 1.024 palabras
│   └── vocab/                  # Fichas JSON por palabra
├── tests/
│   └── test_vocab.py           # Pruebas unitarias de validación
└── .github/
    └── workflows/              # Automatización CI/CD con GitHub Actions
```

---

## 🧪 Pruebas Unitarias

Para ejecutar las pruebas en tu máquina local:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## ✒️ Licencia & Coautoría

Desarrollado en colaboración por **Diego Juliáni** y la cuenta **AvantTexte** bajo licencia MIT.
