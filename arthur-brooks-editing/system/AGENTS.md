# AGENTS.md — Contrato único de VES (Viral Edit System)

Este archivo lo leen **Claude Opus 5.5, ChatGPT 6.2 Sol y Gemini Neon** por igual
(`CLAUDE.md` y `GEMINI.md` solo apuntan aquí). Si sigues este contrato, los tres modelos
producen **el mismo video**, porque el estilo vive en archivos y código, no en tu criterio.

## La regla de oro
**Tú no diseñas. Tú rellenas un contrato.**
- NO escribas componentes de animación nuevos durante una edición.
- NO inventes colores, fuentes, tamaños, curvas ni duraciones de animación.
- SÍ eliges tipos de escena de `schemas/scenes.json` permitidos por `styles/<estilo>/style.json`
  y escribes sus `props` en `projects/<p>/edit_plan.json`.
- El plan creativo lo decide el HUMANO en `plan.html`. Tú lo traduces al JSON.

## Flujo obligatorio (en este orden, sin saltarte pasos)
```bash
python3 pipeline/ves.py new <p> --video RAW.mp4 --style <estilo>
python3 pipeline/ves.py all <p> --lang es           # transcribe → corte (30 ms) → paleta → captions → plan.html
python3 pipeline/fixwords.py <p> "mal=>bien" ...    # corrige la transcripción (los captions muestran estas palabras)
# ⏸ STOP 1 — el humano planifica en plan.html (o aprueba tu propuesta de plan)
# escribes edit_plan.json con "scenes" + "assets" (cada asset con prompt, AR, refs de consistencia)
python3 pipeline/assetpack.py <p>                   # → ASSETS_<p>.md: TODO lo que necesitas, con prompts en el branding del video
python3 pipeline/review_sheets.py palette <p> --presets rosa,morado   # 3–6 paletas para elegir
python3 pipeline/review_sheets.py music <p> --folders tag/piano,mood/inspiring   # 5 muestras de música
python3 pipeline/ves.py captions <p> && python3 pipeline/ves.py captionsheet <p> # hoja de captions (boca = roja)
# ⏸ STOP 2 — PIDE AL HUMANO: el zip <p>.zip con los assets + qué paleta + qué música + OK a la hoja de captions
python3 pipeline/assetpack.py <p> --ingest <p>.zip  # valida, recorta al AR, copia a media/assets
python3 pipeline/review_sheets.py pick-palette <p> N ; python3 pipeline/review_sheets.py pick-music <p> N
python3 pipeline/ves.py validate <p> && python3 pipeline/ves.py storyboard <p>
# ⏸ STOP 3 — el humano aprueba storyboard + hoja de captions. SOLO ÉL ejecuta/ordena:
python3 pipeline/ves.py approve <p>                 # cualquier cambio posterior anula la aprobación
python3 pipeline/ves.py render <p>                  # bloqueado sin aprobación
python3 pipeline/ves.py sound <p>                   # cue sheet + SFX reales (assets/sfx_lib) + música con ducking
```

## Reglas que se aprendieron en revisión (obligatorias)
- **Captions:** grandes (palabras pequeñas ≥ 42 px, palabra clave ≥ 100 px), centradas, y **nunca sobre la boca**: `ves.py captions` detecta la cara y las coloca bajo el mentón (o sobre la cabeza si no caben). Revisa la hoja: la línea roja es la boca.
- **Nunca renderizar sin mostrar antes storyboard + hoja de captions + paleta y recibir el OK.**
- **Nada de imágenes genéricas:** cada escena con imagen usa un asset del paquete (generado con prompt específico o stock de Pexels/Pixabay vía `pipeline/stock_api.py`), y TODO el material externo pasa por el mismo grado de marca (`broll_grade` del estilo = LUT) + textura del estilo. Nunca grado sobre la piel del A-roll.
- **Consistencia:** primero se genera el producto hero (A01), luego todo lo que lo muestra lo usa como referencia; modelos UGC hiperrealistas (sin look de IA).
- **Overlays** (contadores, listicles, listas) nunca sobre la cara: van en la zona media-baja y ocultan el caption mientras están.
- **Ritmo y sonido:** lee `core/tecnicas-editor.md` (speed ramps, algo cambia cada 1–3 s, SFX por evento, música como suelo a −24/−30 dB, sin pausas).

## Cómo traducir el PLAN HUMANO a edit_plan.json
1. Una fila del plan → una o más escenas. Usa los tiempos `start/end` de la fila
   (puedes ajustar a límites de palabra exactos con `transcript_cut.json`).
2. `type` = el elegido por el humano. Si es inválido para el estilo, elige el más cercano
   de `scenes_allowed` y explícalo en tu respuesta.
3. `props`: textos CORTOS (menos texto = más premium). Las palabras `special` deben existir
   literalmente en `text`. Máx 1–2 especiales.
4. Notas del humano mandan sobre tus preferencias.
5. Assets (imágenes, logos, b-roll): haz una **lista de assets** primero, guárdalos en
   `projects/<p>/media/` y referencia rutas relativas al proyecto. Pinturas: solo dominio público.
6. `captions.special_words`: las palabras que el humano destacó.

## Psicología de edición (cuándo usar qué) — ver core/psicologia.md
- **A-roll**: transiciones, presentar un punto nuevo, descanso visual, conexión con el speaker.
- **B-roll / pintura**: momentos emocionales, personajes, historias.
- **Animación**: momentos de valor que deben visualizarse (cifras, comparaciones, listas).
- **Hook (0–3 s)**: speaker visible (ojos en tercio superior) + texto que dice por qué quedarse + visual que lo apoya.
- Cuando anuncia algo nuevo → cara. Cuando lo describe → muéstralo.

## Zona segura (innegociable)
Reels/TikTok/Shorts tapan arriba (~14 %), abajo (~26 %) y la columna derecha (~15 %).
Todo texto y elemento importante va **centrado y cerca de la mitad** de la pantalla, dentro del
rectángulo verde del storyboard. Los fondos pueden ir a sangre completa; el contenido, nunca.
Si en el storyboard algo cae en zona roja, el plan NO se renderiza: acorta el texto o cambia la escena.

## Color por público / marca
Misma estructura de estilo, distinto acento: `ves.py palette <p> --preset rosa|morado|azul|…`
o `--accent #HEX` (presets en `styles/palette_presets.json`). Ej.: marca femenina → rosa/morado.
El acento cambia; las reglas 60/30/10, fuentes y animaciones del estilo NO.

## 3 estilos del mismo video
`ves.py fork <p> <p>-min --style minimal-cinematic` reutiliza el mismo corte y transcripción
para producir otra versión del mismo material en otro estilo.

## Revisiones
Aplica las revisiones del humano editando SOLO `edit_plan.json` (o `palette.json`).
Si una revisión exige un componente o parámetro que no existe, **no improvises en el render**:
propón el cambio a `render/src/scenes.tsx` o al `style.json` como cambio de sistema, aparte,
para que quede disponible para los 3 modelos.

## Formatos de Arthur Brooks
Para clasificar un video o editar en uno de los 5 formatos (documental, animación con voz en off, talking head + minimal,
clip de podcast, pantalla dividida), sigue `skills/ves-arthur-formats/SKILL.md`. La referencia maestra es
`styles/arthur-brooks/formats/ANATOMIA_v01_my_life.md`.

## Crear un estilo nuevo
Sigue `skills/ves-train-style/SKILL.md` (ingeniería inversa con `reverse/breakdown.py`).

## Método Joseph (manda sobre lo anterior) — ver skills/arthur-brooks-style/JOSEPH_METODO.md
- **STOP 1 = panel por beats:** escribe `projects/<p>/beats.json` (cada beat: guion, "visto en los reels", 3 opciones A/B/C
  de `skills/arthur-brooks-style/library/ANIMATIONS.json` con `ref`, `type`, `props`), genera el panel con
  `python3 pipeline/beats.py panel <p> --out projects/<p>/out/panel`, y cuando el humano pegue su plan:
  `python3 pipeline/beats.py apply <p> --picks plan.txt`.
- **Escenas `j_*`** (render/src/scenes_joseph.tsx): j_graph, j_line, j_quote, j_illus, j_half, j_painting, j_broll. Props con
  tiempos ABSOLUTOS de palabra. Ilustraciones: `python3 pipeline/cutout.py <p> A02 o:A01` (h = persona, o = objeto).
- **Fluidez automática** al renderizar (`fluidity()` en ves.py): escenas ajustadas a palabra, sin destellos de A-roll < 0.6 s,
  transiciones solo las de `style.transitions.allowed` separadas ≥ `min_gap_s`. No pongas transición en cada escena.
- **Subtítulos modo `arthur`:** ≤5 palabras por sentido, clave grande en color de marca, resto al 75 %, 2 frames antes de la voz.
- **Borrador:** `ves.py render <p> --draft` + `ves.py sound <p> --draft` (no necesita aprobación). Final solo con `approve`.
- **Entregar el paquete de la skill:** `python3 pipeline/build_skill.py` → `dist/arthur-brooks-editing.zip`.
