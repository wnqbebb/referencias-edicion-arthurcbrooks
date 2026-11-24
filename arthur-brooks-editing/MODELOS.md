# Cómo usar la skill en cada modelo

La skill tiene dos capas:
- **Conocimiento** (reglas, biblioteca de 339 animaciones, 20 videos desglosados, ejemplos, prompts): funciona en cualquier modelo de chat.
- **Sistema** (`system/`: Python + Remotion): transcribe, corta, genera subtítulos, construye y renderiza el video. Necesita un modelo que ejecute código en una máquina (Claude Code, Codex, Gemini CLI) o que lo ejecutes tú.

## Claude
**Claude Code (recomendado, hace todo):**
1. Descomprime el paquete y copia `system/` como tu proyecto (o abre la carpeta del paquete).
2. Copia la carpeta del paquete en `.claude/skills/arthur-brooks-editing/` (o `~/.claude/skills/`). Claude la carga sola cuando pides editar en este estilo.
3. Instala dependencias una vez:
```bash
cd system && pip install -r requirements.txt && cd render && npm install
```
4. Pide la edición con el prompt 2 de `PROMPTS.md`.

**Claude.ai (app/web):** Ajustes → Capacidades → Skills → «Subir skill» → sube el zip. Para videos largos, usa Claude Code.

## ChatGPT
- **GPT personalizado:** Explorar GPTs → Crear → Configurar.
  - Instrucciones: pega el bloque de abajo.
  - Conocimiento: sube los 9 archivos de `knowledge/` y `ANIMACIONES.md`.
  - Activa «Intérprete de código».
- **Proyectos de ChatGPT:** crea un proyecto, sube los mismos archivos y pega las instrucciones en «Instrucciones del proyecto».
- **Codex (CLI):** abre `system/` y di «lee `SKILL.md` y `system/AGENTS.md` y síguelos». Ejecuta todo como Claude Code.

## Gemini
- **Gem:** Gemini → Gems → Nuevo Gem.
  - Instrucciones: pega el bloque de abajo.
  - Conocimiento: sube `knowledge/` y `ANIMACIONES.md`.
- **Gemini CLI:** abre `system/`. `GEMINI.md` ya apunta al contrato `AGENTS.md`. Pide la edición con el prompt 2.

## Instrucciones para pegar (GPT / Gem / Proyecto)
```
Eres editor de video experto en el estilo premium minimal de Arthur Brooks y usas el método de Joseph (Ultimate Editors).
Tu conocimiento son los archivos adjuntos: síguelos al pie de la letra, por encima de tus preferencias.
Orden de lectura: 01_SKILL, 02_METODO_JOSEPH, 03_LOGICA_EDICION, 04_RULEBOOK, 05_FORMATOS, 06_TECNICAS_GENERALES,
07_CONTRATO, 08_EJEMPLOS, 09_PROMPTS y ANIMACIONES (biblioteca con IDs VNN-ANN).
Flujo: transcripción → formato y paleta → plan por beats con 3 diseños A/B/C de la biblioteca (STOP: el humano elige)
→ lista de assets con prompts (STOP: el humano los entrega) → vista previa (STOP: OK) → borrador → revisiones → final.
Reglas: anuncia → cara; describe → se muestra. Todo sincronizado a la palabra. Cortes secos 70–85 %. Subtítulos ≤5
palabras, clave grande en el color de marca, resto al 75 % del ancho arriba/abajo, 2 frames antes de la voz.
Si el humano describe cómo quiere algo, se hace así.
Si no puedes ejecutar código, entrega beats.json, edit_plan.json, los prompts de assets y la hoja de subtítulos en
el formato de 07_CONTRATO para renderizar con system/.
```

## Requisitos del sistema (para renderizar)
Python 3.11+, ffmpeg, Node 18+, Chromium (Remotion lo descarga). Paquetes Python en `system/requirements.txt`.
Música (una vez): `node pipeline/gen/fetch_music.mjs` descarga 25 pistas gratuitas de Mixkit a `assets/music_lib/` (no van en el paquete por licencia y tamaño). Sin música, el sonido se mezcla igual con voz y efectos.
Opcional: clave de Pixabay en la variable `PIXABAY_API_KEY`. **No pegues claves en el chat ni en archivos.**
