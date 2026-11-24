---
name: ves-train-style
description: Crear un estilo de edición nuevo en VES haciendo ingeniería inversa de videos de referencia (método REA de evidencia). Úsalo cuando el usuario traiga 10-20 videos de un creador/estilo y quiera que el sistema lo replique.
---

# Entrenar un estilo nuevo (ingeniería inversa con evidencia)

Inspirado en el flujo "carpeta de referencias + tablero Figma → skill", pero con la
disciplina de REA: **cada regla del estilo debe citar evidencia**.

## Niveles de evidencia (de REA)
- `observed`: medido por herramienta (cortes, paleta, duración de planos, texto dicho).
- `derived`: calculado de observaciones (ASL, cortes/min, cuota de animación).
- `inferred`: interpretación (tipo de escena, por qué está ahí). Requiere confirmación humana.
- `unknown`: lo que no se puede saber (curva exacta, fuente exacta) — se declara, no se inventa.

## Pasos
1. Carpeta `refs/` con 10–20 videos del estilo (descargados por el usuario).
2. Por cada uno: `python3 reverse/breakdown.py refs/X.mp4 --style-id <nuevo> --transcribe`
3. Abre cada `board.html` y `cards.md`. Para cada plano rellena ASSETS / EFFECTS / ANIMATION / ¿por qué aquí?
   Mira los `shots/NNN.jpg` (5 keyframes) para medir duración de entradas (frames entre keyframes).
4. Agrupa los planos en tipos de escena (máx ~10 "principios" del estilo). Mapea cada uno a un tipo
   de `schemas/scenes.json`. Si no existe → propón un componente nuevo en `render/src/scenes.tsx` (cambio de sistema).
5. Escribe `styles/<nuevo>/style.json` (copia uno existente) y `rulebook.md`, citando ids de plano como evidencia:
   `"enter_ms": 600  // derivado: refs/A planos 3,7,12 (18 frames @30fps)`.
6. Valida con un clip real: `ves.py all` → plan → `validate` → `preview`. Compara stills lado a lado con los keyframes de referencia.
7. Itera hasta que un humano no distinga. Recién entonces el estilo es "estable" y sirve para los 3 modelos.

## Dónde entra REA (rea-agents) de verdad
REA analiza binarios, apps JS/Electron y **sitios web**, no archivos de video. Úsalo para:
- Extraer curvas y duraciones EXACTAS de animaciones web que quieras copiar (landing pages SaaS,
  portfolios motion, players de Lottie): `capture_browser_scenario` / exportar scripts del sitio y leer
  los `cubic-bezier`, `duration`, keyframes CSS/GSAP/Lottie JSON → pásalos al `style.json`.
- Inspeccionar plantillas de apps de edición de escritorio que uses (si son JS/Electron) para entender
  sus presets. Solo software que tengas derecho a analizar.
