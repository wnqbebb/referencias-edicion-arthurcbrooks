# Contrato: beats.json → edit_plan.json

El modelo NO escribe código de animación durante una edición: rellena estos dos archivos. El render hace el resto.

## beats.json (plan por beats, lo lee el panel)
```json
{
 "title": "V1 · Talking head + minimal (vino)",
 "beats": [
  {
   "id": "b07",
   "start": 16.28,
   "end": 21.06,
   "script": "Entonces si bajas el precio…",
   "seen": "Consecuencia numérica → gráfico oscuro con bola que cae paso a paso (principio 10).",
   "pick": "A",
   "opts": [
    {
     "title": "Gráfico que cae",
     "cats": "Gráficas · Cut-away",
     "desc": "…",
     "ref": "V19-A14",
     "type": "j_graph",
     "props": {
      "points": [
       {
        "x": 0,
        "y": 0.8,
        "t": 16.4
       },
       {
        "x": 0.2,
        "y": 0.55,
        "t": 17.34,
        "label": "bajas el precio"
       }
      ],
      "small": "pierdes",
      "big": "dos veces.",
      "text_t": 18.66
     },
     "enter": "wipe"
    },
    {
     "title": "…",
     "type": "arthur_blocks"
    },
    {
     "title": "Quedarse en el A-roll",
     "type": null
    }
   ]
  }
 ]
}
```
- `type: null` = quedarse en el A-roll. `t` y los `points[].t` son segundos ABSOLUTOS de la palabra (de `transcript_cut.json`).
- `enter`/`exit` = transición (solo las permitidas por el formato; el render elimina las que sobran).

## edit_plan.json
```json
{
 "style": "arthur-talking-minimal",
 "palette": {
  "vibrant_bright": "#9E1C3A"
 },
 "scenes": [
  {
   "id": "b07a",
   "type": "j_graph",
   "start": 16.28,
   "end": 21.06,
   "props": {},
   "in": "wipe"
  }
 ],
 "assets": [
  {
   "id": "A01",
   "name": "blusa-hero",
   "kind": "product",
   "ar": "4:5",
   "is_ref": true,
   "prompt": "…",
   "negative": "…"
  }
 ],
 "captions": {
  "special_words": [
   "Black Friday"
  ]
 },
 "music": {
  "file": "assets/music_lib/…",
  "volume": 0.16
 }
}
```

## Catálogo de escenas

| Tipo | Capa | Cuándo usarla | Props |
|---|---|---|---|
| `aroll` | base | Transiciones, presentar un punto nuevo, descanso visual, conexión con el speaker. Nunca más de pacing.max_aroll_streak_s seguido. | {"zoom": "number 1.0-1.3 (punch-in)", "desaturate": "bool (romper patrón)"} |
| `fullscreen_text` | fullscreen | Frase clave / tesis que el viewer debe leer. Fondo y texto contrastan. | {"text": "string <= 8 palabras", "special": "array de palabras dentro de text (1-2)"} |
| `quote` | fullscreen | Cita textual o cierre filosófico. Comillas alrededor del texto. | {"text": "string <= 14 palabras", "special": "array", "author": "string opcional"} |
| `listicle` | overlay | Videos por capítulos: mostrar los N pasos temprano; reusar al mencionar cada capítulo con active=i. | {"items": "array de 2-5 strings cortos", "active": "int índice resaltado o -1", "title": "string opcional"} |
| `notification` | overlay | Mención de software, marca, evento, dinero (ej. pago de Stripe). Pop-up de UI con fondo blur. | {"app": "string", "title": "string", "body": "string", "icon": "emoji o ruta a logo"} |
| `counter_ring` | overlay | Timers, porcentajes, contadores, cifras. | {"from": "number", "to": "number", "suffix": "string ej. % o s", "label": "string corto", "max": "number valor que llena el anillo"} |
| `before_after` | fullscreen | Comparar dos cosas: antes/después, A vs B. Balance horizontal con flecha. | {"left": "{label, image?}", "right": "{label, image?}", "arrow": "bool"} |
| `two_object` | fullscreen | Speaker/persona en mitad inferior + texto/pregunta en mitad superior (balance vertical). | {"text": "string", "special": "array", "image": "ruta opcional (si no: frame del A-roll)"} |
| `list_card` | overlay | Enumerar varias cosas en secuencia sobre un cuadro con blur. | {"title": "string", "items": "array 2-6 strings"} |
| `bar_graph` | fullscreen | Dos o más magnitudes que suben/bajan (productividad vs contratación). | {"bars": "array {label, value 0-100}", "title": "string opcional"} |
| `line_graph` | fullscreen | Progresión en el tiempo; 'sube y sube' = escalones; 'lento y constante' = línea plana. Bola de acento sigue la línea. | {"points": "array de números 0-100", "steps": "bool (escalonado)", "label": "string opcional", "sync_words": "array de tiempos (s) donde avanza cada punto, opcional"} |
| `broll_text` | fullscreen | Momentos emocionales o con personajes. B-roll con viñeta, blur de bordes, textura y texto cinematográfico encima. | {"media": "ruta imagen/video", "text": "string", "special": "array"} |
| `painting` | fullscreen | Puntos filosóficos / historias: pintura clásica (dominio público) + textura + texto alrededor del sujeto + slide-in de cámara. | {"media": "ruta imagen", "text": "string", "special": "array"} |
| `line_text` | fullscreen | Encadenar conceptos: una línea de acento se dibuja, es interrumpida por texto, y continúa al siguiente concepto. Cámara sigue la línea. | {"words": "array 2-4 conceptos (cada uno 1-3 palabras)"} |
| `center_illustration` | fullscreen | Idea principal visualizada en el centro (espiral, cerebro, persona) con texto alrededor. | {"media": "ruta imagen opcional", "shape": "spiral/circle/none", "text": "string", "special": "array"} |
| `object_callout` | fullscreen | Un objeto/persona con texto alrededor como parte de la historia (one-object scene: punto focal + color de acento). | {"media": "ruta imagen", "label": "string", "text": "string opcional"} |
| `lower_third` | overlay | Presentar quién habla (nombre + cargo) al aparecer un speaker nuevo. | {"name": "string", "role": "string"} |
| `name_card` | fullscreen | Presentación del protagonista al inicio (v01 0:01): 'Me llamo' + nombre en serif azul sobre estudio blanco. | {"kicker": "string", "name": "string", "media": "foto/video recortado opcional"} |
| `paper_collage` | fullscreen | Enumerar roles/identidades o momentos con fotos impresas sobre papel blanco (v01 0:03 'escribo / hablo / enseño'). | {"images": "1-3 rutas", "labels": "[{small, word}] 1-3"} |
| `timeline` | fullscreen | Historia por edades/etapas: línea con hitos, marcador azul avanza al hito activo; fotos caen encima. Con over_aroll=true va sobre el A-roll (v01 2:07). | {"milestones": "[{label, age}]", "active": "int", "images": "rutas opcionales", "over_aroll": "bool"} |
| `archival_photo` | fullscreen | Recuerdo/pasado: foto de archivo a sangre con scanlines y aro de resaltado sobre la persona (v01 0:24). Caption sigue visible. | {"media": "ruta", "bw": "bool", "ring": "{x,y,r} opcional (x,y en 0-1)", "scanlines": "bool"} |
| `video_card` | fullscreen | B-roll como tarjeta redondeada sobre negro (v01 0:45, 1:34). Caption visible. | {"media": "ruta", "size": "small/tall"} |
| `split_layout` | base | Podcast pantalla dividida: close-up arriba + plano abierto abajo (v05, v14, v20). | {"ratio": "0.6-0.75", "zoom": "1.5-2.2", "face_x": "0-1", "face_y": "0-1", "top_media": "opcional", "bottom_media": "opcional"} |
| `kinetic_type` | fullscreen | Tipografía cinética manuscrita palabra por palabra (v04). | {"lines": "[{text,size,at}]", "dark": "bool"} |
| `blue_quote` | fullscreen | Cita interna/pensamiento en fondo azul radial con comilla (v01 1:24). | {"text": "string"} |
| `arthur_text` | fullscreen | Frase clave/tesis/cita: fondo acento (texto blanco) o blanco (texto acento), write-on por palabra; alternar bg entre escenas consecutivas (inversión de marca). | {"bg": "accent/white/black", "lines": "[{t, size:'s'/'l', align, italic, accentWord}]", "quote": "bool", "flash": "in/out/both"} |
| `arthur_icons` | fullscreen | Idea concreta con objetos (prendas, etiquetas, celular, caja, persona): mancha blanca con íconos de línea que aparecen en secuencia + texto arriba. | {"bg": "accent/white", "icons": "[tshirt,hanger,tag,phone,box,person,eye,heart,bag,camera,star,calendar,sun,cart]", "highlight": "int", "lines": "[...]"} |
| `arthur_orbit` | fullscreen | Una persona/cliente/producto como centro de la idea: círculo con ícono o foto y anillos orbitales. | {"bg": "accent/white", "icon": "nombre", "media": "ruta opcional", "lines": "[...]"} |
| `arthur_stripes` | fullscreen | ENUMERAR (2–4 cosas): pantalla dividida en franjas numeradas con imagen/video en cada una; se ilumina la que se nombra. | {"items": "[{label, media?}]", "active_at": "[segundos relativos]"} |
| `arthur_blocks` | fullscreen | Comparar/dividir un todo (2 o 4 partes): bloque de acento que se divide. | {"bg": "white/accent", "labels": "[2/4 textos cortos]", "highlight": "int", "lines": "[...]"} |
| `arthur_broll` | fullscreen | Momento emocional/descriptivo: b-roll oscuro de cine (varias tomas cambiando) con texto fijo encima. | {"media": "[rutas]", "lines": "[...]"} |
| `arthur_number` | overlay | Una cifra protagonista (100 camisetas, 5 prendas, 50 %): número gigante que cae desde arriba + etiqueta en mayúsculas. | {"value": "string", "label": "string", "px": "int"} |
| `j_graph` | fullscreen | Principio 10: cifra/consecuencia/tendencia. Fondo oscuro, cuadrícula brillante, bola de acento que avanza un punto por palabra; la cámara la sigue y al final zoom-out. | {"small": "str", "big": "str", "after": "str", "sans": "bool", "t": "seg absoluto de la palabra que enciende el texto", "px": "int", "points": "[{x,y (0-1), t, label}]", "x_label": "str", "y_label": "str", "text_t": "seg"} |
| `j_line` | fullscreen | Principios 4/5: progresión, fases, enumeración. Línea gruesa de acento que el texto interrumpe; la cámara sigue la punta; zigzag con fotos a los lados. | {"bg": "white/black/accent", "shape": "zigzag/down/arc", "stops": "[{small,big,after,sans,t,img}]", "dot": "bool", "px": "int"} |
| `j_quote` | fullscreen | Principio 6: tesis/regla/pensamiento interior. Papel muy rugoso blanco o de acento, comillas alrededor del texto. | {"small": "str", "big": "str", "after": "str", "sans": "bool", "t": "seg absoluto de la palabra que enciende el texto", "px": "int", "bg": "white/accent"} |
| `j_illus` | fullscreen | Principios 7/8/9: persona u objeto como ilustración rugosa (recorte PNG de pipeline/cutout.py). | {"small": "str", "big": "str", "after": "str", "sans": "bool", "t": "seg absoluto de la palabra que enciende el texto", "px": "int", "media": "*_cut.png", "mode": "center/side", "bg": "white/accent/black", "keep_color": "bool (objeto a color)", "fill": "color de silueta"} |
| `j_half` | fullscreen | Principio 8: dos elementos a la vez. Media luna con textura de tela y palabras rotando alrededor. | {"small": "str", "big": "str", "after": "str", "sans": "bool", "t": "seg absoluto de la palabra que enciende el texto", "px": "int", "ring": "[str]", "bg": "white/accent"} |
| `j_painting` | fullscreen | Principio 3: emoción/belleza/idea filosófica. Pintura de dominio público, slide de cámara, textura de pintura que se mueve con ella. | {"small": "str", "big": "str", "after": "str", "sans": "bool", "t": "seg absoluto de la palabra que enciende el texto", "px": "int", "media": "png", "text_pos": "top/bottom"} |
| `j_broll` | fullscreen | Principio 2: describe una escena. B-roll literal con papel, bordes oscuros y desenfocados, texto fijo encima; varias tomas bajo el mismo texto. | {"small": "str", "big": "str", "after": "str", "sans": "bool", "t": "seg absoluto de la palabra que enciende el texto", "px": "int", "media": "[ruta]", "cuts": "[seg]"} |
