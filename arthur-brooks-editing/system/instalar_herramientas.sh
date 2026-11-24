#!/usr/bin/env bash
# Instala todo lo que la skill necesita para renderizar y buscar material (ejecútalo dentro de system/).
set -e
echo "→ Python"
pip install -r requirements.txt yt-dlp gallery-dl
echo "→ Render (Remotion)"
(cd render && npm install)
echo "→ Plugin Edit Studio (incluido en el paquete) → .claude/skills"
mkdir -p .claude/skills && cp -r ../plugins/edit-studio/skills/* .claude/skills/ 2>/dev/null || true
echo "→ Skills complementarias para Claude Code"
npx -y skills add remotion-dev/skills -a claude-code -y || true
npx -y skills add heygen-com/hyperframes -a claude-code -y || true
npx -y skills add digitalsamba/claude-code-video-toolkit --skill ffmpeg -a claude-code -y || true
npx -y skills add terminalskills/skills --skill gallery-dl -a claude-code -y || true
echo "→ Navegador para Playwright (si no hay uno instalado)"
npx -y playwright install chromium || true
echo "→ Música y efectos (Mixkit, gratis)"
node pipeline/gen/fetch_music.mjs || echo "  (puedes descargar la música más tarde)"
node pipeline/gen/fetch_sfx.mjs || true
command -v ffmpeg >/dev/null || echo "⚠ Falta ffmpeg: instálalo (brew install ffmpeg / apt install ffmpeg / winget install ffmpeg)"
echo "✓ Listo. El MCP de Playwright ya está en .mcp.json. Clave de Pixabay: export PIXABAY_API_KEY=… (no la pegues en archivos)"
