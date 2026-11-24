# Brief: análisis escena por escena de un video de referencia (Arthur Brooks, Reels 9:16)

Eres un editor de video senior haciendo ingeniería inversa. Para CADA video asignado, en
`/home/user/viral-edit-system/styles/arthur-brooks/references/vNN/`:

Material (léelo con la herramienta Read; las imágenes se ven):
- `study/timeline_XX.jpg` — un fotograma cada 1.5 s con el tiempo impreso (8x3 por hoja). ES LA FUENTE PRINCIPAL.
- `study/shots_XX.jpg` + `study/shots.txt` — planos detectados por corte (id, inicio-fin, lo que se dice).
- `transcript.txt`, `vNN.srt` — lo que se dice (palabra a palabra con tiempos en evidence.json → "words").
- `../../formats/labels.json` — formato del video (documental_bio, animacion_vo, talking_head_minimal, podcast_clip, podcast_split).

Divide el video en ESCENAS (beats visuales: cambia el diseño/la composición, no solo la cámara). Típicamente 1 escena cada 1.5–4 s.
Para cada escena clasifica `category` en UNA de:
  captions_text (texto en pantalla sobre A-roll) · broll_text · imagery_characters (pinturas/fotos/personajes + texto) ·
  line_text · line_illustration · text_centric (solo texto / citas con comillas) · center_illustration ·
  side_illustration · object_element · graph_stats · ui_screen (interfaz/redes) · timeline · split_layout ·
  aroll_plain (A-roll sin texto destacado) · title_cta (título de inicio / cierre / CTA)

Escribe `scenes.json` (lista JSON, español) con, por escena:
{
 "id": "vNN_s01", "start": 0.0, "end": 2.4, "category": "...",
 "script": "lo que se dice en ese tramo",
 "what": "qué se ve, concreto",
 "design": "fuentes (sans vs serif itálica, peso, mayúsculas), tamaños relativos, posición en pantalla (tercios, centro), colores (hex aproximado si se puede), forma/bordes",
 "effects": "texturas (papel, tela, halftone, grano), blur, viñeta, desaturación, glow, scanlines…",
 "animation": "cómo entra/sale y se mueve: pop+blur+fade, write-on por palabra, slide de cámara, línea que se dibuja, zoom, duración estimada en segundos y sensación (suave/seca)",
 "why": "por qué el editor usó esta escena AQUÍ respecto al guion (psicología: anunciar vs describir, emoción, dato, transición, hook)",
 "quality": 1-5 (5 = escena de inspiración top que copiarías),
 "best_t": segundo exacto del fotograma más representativo (de las hojas)
}
Y `breakdown.md` (español, ≤ 60 líneas): formato, estructura del guion (hook → … → cierre), ritmo (seg/escena),
sistema de captions (fuentes, posición, palabra destacada), paleta, texturas, 5–8 técnicas destacables con tiempos,
y "reglas copiables" en viñetas.

Sé literal con lo que ves: no inventes fuentes si no puedes saberlo ("serif itálica tipo Playfair" está bien).
Escribe los archivos con la herramienta Write. No modifiques nada más. Al terminar devuelve solo: por video, nº de escenas,
conteo por categoría y nº de escenas con quality ≥ 4.
