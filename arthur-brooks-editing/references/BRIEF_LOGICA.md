# Brief 2: LÓGICA DE EDICIÓN de cada video (segundo pase, más fino)

Ya existe para cada video `references/vNN/`: scenes.json (escenas), evidence.json (palabras con tiempos en "words"),
study/timeline_XX.jpg (1 fotograma cada 1.5 s), breakdown.md. El video está en /home/user/viral-edit-system/refs/arthur/vNN.mp4.
Ahora necesitamos lo que el primer pase NO capturó. Usa Bash + ffmpeg para mirar de cerca, por ejemplo cada transición:
  ffmpeg -v error -ss <t-0.3> -t 0.7 -i refs/arthur/vNN.mp4 -vf "fps=15,scale=160:-1,drawtext=text='%{pts\:hms}':fontsize=12:fontcolor=yellow:x=2:y=2,tile=11x1" -frames:v 1 /tmp/tr_vNN_<t>.jpg
y léelo con Read (ves las imágenes). Mira TODAS las transiciones/cambios de escena y los momentos donde aparece texto o un gráfico.

Escribe `references/vNN/edit_logic.json` con:
{
 "triggers": [ {"t_word": 3.42, "word": "palabra exacta que dispara", "element": "qué aparece (texto/ícono/foto/gráfico/zoom/cambio de color)", "category": "(de scenes.json)", "offset_s": -0.1, "why": "relación palabra→imagen (literal / metáfora / dato / énfasis / cambio de tema)"} ],
 "transitions": [ {"t": 12.3, "from": "aroll|escena X", "to": "...", "type": "corte seco | flash blanco | flash amarillo | inversión de color | zoom-blur | whip-pan | wipe | crossfade | match-cut (elemento compartido) | glitch | slide", "frames": 3, "detail": "..."} ],
 "text_fx": [ {"t": 5.1, "fx": "write-on por palabra | gris→blanco | blur-in | pop | escala | máscara | tracking", "detail": "..."} ],
 "camera": [ {"t": 8.0, "move": "punch-in | zoom-out | pan | slide | push-in lento | shake | rack-focus", "scale_or_dir": "1.0→1.3", "dur_s": 0.0} ],
 "rhythm": {"events_per_10s": [..], "avg_hold_text_s": 0.0, "notes": "..."},
 "typography": "fuentes observadas, pesos, itálica, tamaños relativos, mayúsculas, color de la palabra clave, cuántas palabras por bloque",
 "textures": "papel / tela / pintura / grano / halftone / viñeta, intensidad y dónde",
 "distinct": ["5 cosas que hacen ÚNICO este video frente a los demás de Arthur (para no editar todos igual)"]
}
y `references/vNN/edit_logic.md` (≤ 50 líneas, español): las 10 reglas copiables más importantes de ESTE video con tiempos de ejemplo.
Sé literal y preciso con tiempos (±0.1 s). No modifiques otros archivos. Devuelve solo: por video nº de triggers, transiciones (por tipo) y las 3 rarezas más útiles.
