# GitHub Copilot & Agent Configuration Guidelines

## Project Overview
Proyecto Liseur is an interactive web application for learning French vocabulary based on literary texts like *Pilote de guerre* and *Le Petit Prince*.

## Coding Standards & Schema Rules
1. **JSON Data Format**: All vocabulary files in `datos/vocab/` must follow the strict schema:
   ```json
   {
     "id": int,
     "frances": "word_in_french",
     "espanol": "translation_in_spanish",
     "tipo": "Sustantivo | Verbo | Adjetivo | Expresión",
     "contexto_original": "sample sentence from text",
     "dominado": false
   }
   ```
2. **Co-authorship**: All automated commits and code suggestions MUST include co-authorship metadata:
   `Co-authored-by: AvantTexte <thegithubfrenchproyect@gmail.com>`

3. **Frontend**: Pure Vanilla JS, HTML5, CSS3. No heavy frameworks. Utilize native Web Speech API (`window.speechSynthesis`) for French pronunciation.
