# EDIT LOGIC — cómo decide Arthur QUÉ poner, CUÁNDO y CON QUÉ TRANSICIÓN

Fuente: segundo pase fotograma a fotograma de los 20 videos (`references/vNN/edit_logic.json` + `edit_logic.md`),
1 000+ triggers palabra→elemento y 700+ transiciones medidas.

## 1. Sincronía palabra → elemento (lo más importante)
- El elemento entra **en la palabra** que lo nombra: mediana 0.0–0.1 s. Fotos/b-roll 0.1–0.3 s ANTES (v01); la palabra grande 0–0.3 s DESPUÉS de la imagen.
- El **corte cae en la palabra funcional que abre la frase** ("I", "all", "who"); la palabra clave aparece 0.1–0.4 s después (v12).
- Los captions **cruzan el corte**: la frase empieza en un plano y termina en el siguiente sin moverse (v01 34.1, 63.1).
- La palabra grande **entra gris y se enciende** a blanco (o a acento sobre blanco) en 2–4 frames — nunca aparece a opacidad plena (v10, v19).
- **Los efectos hacen lo que dice el verbo**: "separa" → wipe que separa; "eliminar" → lavado a blanco; "detrás" → aparece detrás (v19).

## 2. Qué elemento según lo que se dice
| Lo que se dice | Elemento | Ejemplos |
|---|---|---|
| Anuncia un punto nuevo / transición | A-roll con caption (cara) | todos |
| Describe / cuenta | B-roll de cine con texto fijo encima; varias tomas bajo el mismo texto | v12 57.0 |
| Emoción, idea filosófica | Pintura clásica con textura + texto alrededor del sujeto + slide de cámara | v06 |
| Enumera 2–4 cosas | Índice de franjas (pinturas/fotos) que **vuelve como capítulo** antes de cada punto | v06 1.2/11.6/21.9/40.2 |
| Enumeración conceptual | Diagrama que se construye al ritmo: punto → 3 puntos → triángulo con etiquetas | v12 31–36 |
| Un dato / cifra | Sans bold grande, máquina de escribir; dato malo con punch-in | v11 |
| Una cita / pensamiento interior | Tarjeta de color con comillas; entrada "sándwich" negativo→amarillo→tarjeta | v08 31.8 |
| Contraste antes/después | El MISMO objeto cambia de estado (cerebro rojo "Fear" → verde "Adventure") | v16 33.3 |
| Persona / historia de vida | Foto impresa sobre papel, timeline por edades | v01 |
| Matiz / giro | Corte a fondo de color vacío 0.13–1.4 s con una palabra diminuta | v19 |
| Remate / tesis | Primer plano (punch-in); anécdota = plano medio | v09 |

## 3. Transiciones firma por formato (no editar todo igual)
| Formato | Transiciones (además del corte seco, que es el 70–85 %) | Cámara |
|---|---|---|
| Documental | crossfade, slide, match-cut (timeline), **destello dorado SOLO entre capítulos** | push-in lento, slide |
| Animación VO | slide, wipe, match-cut por elemento compartido (punto de espiral = punto de la "j"), iris, flash blanco, strobe | slide, zoom-out rápido |
| Talking head + minimal | punch-in al inicio de frase, **glitch de bloques**, wipe, inversión de color | punch-in 1.0↔1.3 |
| Clip de podcast | **whip-pan** (smear 4–6 frames) en cada cambio de hablante y A↔B-roll, flash tinte+blanco en cambio de tema, zoom-blur | punch-in en remates |
| Pantalla dividida | crossfades que ocultan jump cuts; solo se corta el panel de arriba | reencuadre digital |

## 4. Ritmo (eventos visuales cada 10 s)
documental 10–12 · animación VO 9–19 · talking head + minimal 6–9 · podcast clip 5–17 · split 1.7–4.
Nunca un efecto en cada corte ("decorar no es editar"): la mayoría son cortes secos.

## 5. Tipografía (principio 1 + medición)
Tres voces: **Playfair Display Bold Italic** para la emoción/palabra clave · **Inter Bold/Heavy** para el dato · Inter pequeña como "super/subíndice" de enlace.
La palabra clave al centro, el resto pequeño en los huecos arriba/abajo. Sobre blanco: serif en acento o negro.

## 6. Texturas
Papel rugoso en todos los fondos planos · pintura + papel en pinturas · tela rugosa en siluetas/perfiles · grano y viñeta en b-roll · halftone en podcasts.

## 7. Sonido (medido con Demucs: voz separada de música+SFX, `reverse/audio_sfx.py`)
- SFX **escasos**: v01 2 eventos · v02 3 · v03 0 · v04 1 · v05 2 · v06 8 (el más animado). Media ≈ 1 cada 15–30 s.
- Tipos: pop suave cuando aparece una foto/elemento, golpe grave (hit/boom) en una revelación o cambio de capítulo, clic en una cifra. Nunca un whoosh en cada corte.
- La **música es el suelo**: entra desde el segundo 0, ~10 dB bajo la voz, con ducking; sube un poco en los tramos sin voz.
- Los captions NO llevan clic. El silencio también edita: en la cita/tesis se baja la música 2–3 dB.
- En el sistema: `style.json → sfx.min_gap_s` (6 s documental/minimal, 4 s podcast) y sin `caption_special`; recortes de referencia en `references/vNN/audio/sfx/` (solo estudio, no para publicar).


---

# Desglose por video

| Video | Formato | Escenas | Archivos |
|---|---|---|---|
| v01 | documental_bio | 66 | `references/v01/breakdown.md` · `scenes.json` · `v01.srt` · `study/` |
| v02 | podcast_split | 16 | `references/v02/breakdown.md` · `scenes.json` · `v02.srt` · `study/` |
| v03 | animacion_vo | 5 | `references/v03/breakdown.md` · `scenes.json` · `v03.srt` · `study/` |
| v04 | animacion_vo | 20 | `references/v04/breakdown.md` · `scenes.json` · `v04.srt` · `study/` |
| v05 | podcast_split | 18 | `references/v05/breakdown.md` · `scenes.json` · `v05.srt` · `study/` |
| v06 | talking_head_minimal | 30 | `references/v06/breakdown.md` · `scenes.json` · `v06.srt` · `study/` |
| v07 | podcast_clip | 11 | `references/v07/breakdown.md` · `scenes.json` · `v07.srt` · `study/` |
| v08 | talking_head_minimal | 24 | `references/v08/breakdown.md` · `scenes.json` · `v08.srt` · `study/` |
| v09 | podcast_clip | 11 | `references/v09/breakdown.md` · `scenes.json` · `v09.srt` · `study/` |
| v10 | animacion_vo | 59 | `references/v10/breakdown.md` · `scenes.json` · `v10.srt` · `study/` |
| v11 | documental_bio | 36 | `references/v11/breakdown.md` · `scenes.json` · `v11.srt` · `study/` |
| v12 | animacion_vo | 44 | `references/v12/breakdown.md` · `scenes.json` · `v12.srt` · `study/` |
| v13 | podcast_clip | 15 | `references/v13/breakdown.md` · `scenes.json` · `v13.srt` · `study/` |
| v14 | podcast_split | 11 | `references/v14/breakdown.md` · `scenes.json` · `v14.srt` · `study/` |
| v15 | podcast_split | 9 | `references/v15/breakdown.md` · `scenes.json` · `v15.srt` · `study/` |
| v16 | talking_head_minimal | 36 | `references/v16/breakdown.md` · `scenes.json` · `v16.srt` · `study/` |
| v17 | podcast_clip | 16 | `references/v17/breakdown.md` · `scenes.json` · `v17.srt` · `study/` |
| v18 | podcast_clip | 16 | `references/v18/breakdown.md` · `scenes.json` · `v18.srt` · `study/` |
| v19 | animacion_vo | 53 | `references/v19/breakdown.md` · `scenes.json` · `v19.srt` · `study/` |
| v20 | podcast_split | 10 | `references/v20/breakdown.md` · `scenes.json` · `v20.srt` · `study/` |