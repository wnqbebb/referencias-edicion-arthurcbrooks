# Técnicas del editor → reglas accionables para VES

Fuente: 6 transcripciones de un editor con más de 10 años de experiencia (Premiere/After Effects + Claude por MCP).
Se ignoró toda la publicidad (Envato, Hostinger, Epidemic, comunidad de pago).
Convención: un número **sin marca** sale de la transcripción; **(sugerido)** = valor nuestro para implementarlo en código.
Destino: reels verticales 1080×1920 de 1–3 min, render con Remotion, audio con ffmpeg y orquestación en Python.

---

## 1. Speed ramps: 8 formas sobre la "value graph" (tiempo de origen vs tiempo de salida)

### Principios
- Un speed ramp es una **curva `src_t = f(out_t)`** (la "value graph" de After Effects), no un multiplicador de velocidad. Esta curva da más control que la gráfica de velocidad: permite congelar, invertir y volver.
- La pendiente de la curva es la velocidad. Si es horizontal, el plano se congela; si es negativa, va en reversa.
- Cuanto más juntos estén los dos keyframes extremos, más rápido es el ramp.
- Los ocho ramps (walkthroughs, edits de coches, transiciones) salen de combinar unas pocas formas.
- Para rematarlo hay que añadir **pixel motion blur** con más muestras: la diferencia es "significativa".

### Las 8 formas (curvas bezier, interpolación tipo "easy ease"/F9)
| # | Forma de `src_t(out_t)` | Efecto visible |
|---|---|---|
| 1 | S invertida: manejadores tirados al máximo (arriba al inicio, abajo al final), simétrica | rápido → lento → rápido |
| 2 | Empieza en 0, sube y **vuelve a 0** | avanza y rebobina hasta el inicio (reverse) |
| 3 | Empieza en 0, sube al frente y baja **sin llegar a 0** | adelante y atrás, termina más adelante que el inicio |
| 4 | Como la #1, más un keyframe a 1 s con el manejador **horizontal** | rápido hasta un punto y se detiene (freeze o hold) |
| 5 | La #1 con 2 keyframes extra para controlar la suavidad del tramo medio | rápido-lento-rápido "domado" |
| 6 | Sube, baja y vuelve a subir (3–4 keyframes, uno con tangente plana) | adelante → atrás → adelante |
| 7 | Sube casi hasta el final y luego se nivela con un tramo plano o casi plano | mucho avance y después una flotación |
| 8 | Espejo de la #7 | flotación y después mucho avance |

### Reglas medibles
- Ventana típica del ramp: los keyframes se juntan a **~2 s** de salida. En el ejemplo, un clip de 10 s se comprime a 2 s.
- El valor máximo de `src_t` nunca supera la duración del clip de origen. Hay que validarlo y recortarlo.
- Los manejadores deben ser simétricos en los dos lados para que la ramp se lea limpia (el autor los iguala "en bloques").
- Siempre se añade motion blur después del ramp.
- Cuándo usarlo según el guion (sugerido): en b-roll de acción, en transiciones entre ideas y en "reveals". En planos de speaker, nunca.

### Flujo del autor
1. Activa time remapping en el clip con un atajo de teclado.
2. Junta los keyframes, los pasa a bezier y abre la value graph.
3. Tira de los manejadores o añade keyframes (Alt + Shift para dejarlos horizontales).
4. Marca el out-point y revisa en reproducción.
5. Aplica pixel motion blur con más muestras.

### Cómo implementarlo en código
- `SpeedRamp` (Remotion): props `{ src, preset: 1..8 | points: [{t_out, t_src, inTan, outTan}], durationOut }`. Para cada frame, `t_src = cubicBezierSpline(points)(frame/fps)` y se aplica `<OffthreadVideo startFrom>` frame a frame, o se pre-renderiza con ffmpeg.
- En ffmpeg o Python: se genera un mapa frame→frame de origen y se renderiza con `select` o un decode en orden. Para reversa hay que extraer los frames antes.
- Presets (sugerido, normalizados 0–1, en formato `(out, src)` con tangentes): `p1=[(0,0,slope 4),(1,1,slope 4)]` con la pendiente central en ~0,25; `p2=[(0,0),(0.5,0.6),(1,0)]`; `p3=[(0,0),(0.45,0.7),(1,0.35)]`; `p4=[(0,0),(0.5,0.8,flat),(1,0.8)]`.
- Motion blur (sugerido): `@remotion/motion-blur` `<CameraMotionBlur samples={10} shutterAngle={180}>` solo dentro del tramo donde `|d src/d out| > 1.5`.

---

## 2. Motion graphics que de verdad sirven (con Claude)

### Principios
- **Regla de 1–3 s** (tomada de un análisis de MrBeast): cada 1–3 s cambia la escena o pasa algo en pantalla. Si no, el espectador se va. Esa regla decide **cuándo** meter un gráfico.
- En reels, el autor **casi no encontró motion graphics de IA** en los creadores que consume: mucho de lo que se hace es "inútil". Donde sí sirven es en long-form.
- La mejor configuración es la que **edita dentro de la herramienta final**, sin ida y vuelta (exportar, reimportar y reaplicar efectos). En VES esto equivale a que el gráfico sea un componente parametrizable del plan, no un MP4 suelto.
- Una **referencia visual** funciona mejor que una descripción en texto.
- Muchas veces **un humano es más rápido**: Claude puede tardar 5–10 min y gastar créditos en una animación de texto simple.

### Reglas medibles
- Densidad: 1 evento visual cada 1–3 s en long-form. En talking head de reel, cada ~1 s (ver sección 3).
- Estilo de entrada recomendado para listas o UI: "estilo Apple", **un elemento aparece después del otro** (stagger).
- Hay que revisar siempre la **alineación** del texto, que es el fallo típico de lo generado.
- Los gráficos con timing atado al guion se generan **después de cerrar el corte**: si se recorta después, los timings se rompen.

### Flujo del autor
1. Exporta la transcripción del editor (Premiere da el texto con tiempos). No usa la transcripción de Claude porque "no es fiable".
2. Pasa una referencia (captura de un frame o un video) con instrucciones de qué quitar. Ejemplo: "quita el botón play, es UI de Instagram".
3. Pide **primero la plantilla estática**. Si está bien, pide la animación.
4. Revisa la alineación y el movimiento de cámara, y corrige por instrucción.
5. Ejemplo de prompt de texto: "composición 1920×1080, 30 fps, 10 s, un círculo con gradiente y glow que recorre las esquinas en bucle".

### Cómo implementarlo en código
- Los gráficos son componentes de `render/src/scenes.tsx` con props (nunca se generan ad hoc, según AGENTS.md).
- `StaggerList` (sugerido): `{ items[], staggerFrames: 4, enter: 'pop'|'slideUp', ease: bezier(0.2,0.8,0.2,1) }`.
- Validador de densidad (sugerido, `ves.py validate`): avisa si hay un hueco de más de 3 s sin evento (corte, zoom, caption especial o gráfico).
- Dos fases en el plan: `layout` y luego `animate`. El storyboard (frame estático) es la "plantilla primero".

---

## 3. Talking head viral (estilo reels de Jordan Belfort)

### Principios (las 6 claves del estilo)
1. **Sin aire muerto**: se cortan todas las pausas y va de frase en frase. "Cada respiración es una puerta de salida".
2. **Algo cambia en pantalla cada ~1 s**: un caption nuevo, un zoom o un gráfico.
3. **Los captions venden**: casi todas las palabras van pequeñas y anchas; las importantes "golpean" en **grande y amarillo debajo**. Solo **~1 palabra cada varios segundos** recibe el tratamiento amarillo.
4. **La cámara nunca está quieta**: el encuadre cambia **cada 2–3 s**. Empuja (push-in) en los remates y vuelve a abrir, así que parece otra cámara aunque sea un solo plano.
5. **Los gráficos van detrás del speaker** (dinero, logos, cifras): parece que está dentro del edit y no que le pegaron stickers encima.
6. **Una sola ruptura de patrón hacia la mitad**: la pantalla se oscurece y pasa a un momento a pantalla completa con la metáfora principal. Se usa **una vez**, y por eso funciona.

### Las 3 reglas "nunca" del autor
- Nunca dejar una pausa.
- Nunca poner un efecto en cada corte: "si todo destaca, nada destaca; no estás editando, estás decorando". El zoom se guarda para **la palabra que importa**.
- Nunca dejar que la música le gane a la voz: "la música es el suelo, no el que habla".

### Reglas medibles
- Silencios: se eliminan todos y después se ajusta a mano el **pacing**. Gap máximo entre frases (sugerido): 80–120 ms.
- También se cortan las **repeticiones** (las tomas dobles del speaker).
- Captions normales: pequeños y anchos. Palabra clave: grande, amarilla y en línea aparte debajo. Frecuencia máxima (sugerido): 1 especial cada 3–5 s.
- Zoom o reencuadre: cambio cada 2–3 s. Escalas (sugerido): base 1.0, medio 1.12, punch 1.25–1.35, siempre volviendo a abrir.
- Pattern break: 1 por video, cerca del 50 % de la duración, con fondo oscuro y full-screen. Duración (sugerido): 2–4 s.
- Música bajo la voz: el autor pidió bajarla **~30 dB** y después otros **−10 dB** porque seguía alta. Carácter: "beats serios, sin llegar a thriller".
- Sonido: un SFX en **cada palabra amarilla**.

### Flujo del autor
1. Cortar pausas (en Premiere: panel de texto → pausas → borrar todas), luego repeticiones, luego pacing fino escuchando.
2. Precomponer todo en una sola capa para trabajar encima.
3. Darle a Claude el prompt, el transcript .txt y el **JSON con tiempos palabra por palabra**. Claude pide confirmar palabras dudosas del guion, y se le contesta.
4. Claude genera los captions y los movimientos de cámara. Después se reemplaza la composición en el timeline por la editada.
5. Sonido con prompt: "resalta con SFX las palabras amarillas, música bajo ~30 dB, beats serios". Luego se ajusta el volumen escuchando.
6. Revisión: Claude "comete errores tontos"; el humano escucha música + SFX en solo y corrige. Los cambios globales se piden por instrucción (por ejemplo, "cada palabra de corte en rojo").

### Cómo implementarlo en código
- `rawcut` (Python): elimina silencios con VAD o tiempos de palabra y detecta repeticiones (n-gramas repetidos en una ventana de 5 s, sugerido). Sale `transcript_cut.json`.
- `Captions`: `{ baseSize: 56px (sugerido), baseWeight: 700, special: { color: '#FFD400' (sugerido), size: 2.2×, position: 'below', enter: 'slam' (scale 1.4→1.0 en 6 frames, sugerido) } }`, con un límite de densidad para las especiales.
- `CameraPunch`: genera keyframes de escala cada 2–3 s con el ciclo `push (special word) → hold → pull out`. Ease (sugerido): `bezier(0.33,0,0.2,1)`, 8–10 frames.
- `BehindSubject`: segmentación del speaker (matte por frame con rembg o MediaPipe, sugerido). Orden de capas: fondo → gráfico → speaker recortado → captions.
- `PatternBreak`: escena `fullscreen_metaphor` con `max_per_video: 1` en `style.json` y posición forzada en el 40–60 % de la duración (sugerido).
- Audio: `sfx_on: special_words`; música a −30 dB respecto a la voz y luego −10 dB, con ducking en ffmpeg (`sidechaincompress`).

---

## 4. Sound design automatizado con IA

### Principios
- **Claude no oye**: de un archivo de sonido solo ve el nombre y la duración. Un "swoosh" puede ser una brisa o un jet. Hace falta un analizador ("earshot") que convierta cada sonido en datos legibles: **volumen, duración del golpe y carácter**. Además, **se revisa cada sonido antes de ponerlo** en el timeline.
- Biblioteca **con licencia limpia**: una música cualquiera de internet puede tumbar el video por copyright.
- Música adaptada a la **duración exacta** del video. Si no, se corta en mitad de un compás.
- Claude es **malo eligiendo música** porque es subjetivo. El humano elige la canción y la IA la adapta.
- Lo que se repite se convierte en skill o preset para no volver a escribir las instrucciones.

### Reglas medibles
- **Regla de SFX**: cada movimiento de motion graphics, grande o pequeño, lleva un sonido (swooshes, pops, sonidos de UI). **Si en pantalla solo está la persona, no lleva sonido.**
- Análisis visual: con 18 s a 30 fps salen 540 frames. El agente tomó 52 capturas (**1 cada 10 frames**) y se puede forzar a cada frame. Duración total: ~6–7 min.
- Revisión del autor: "un poco alto". Bajó **el SFX más fuerte 15 dB y el resto 5–10 dB**.
- Música: la IA la dejó y luego se bajó **25 dB** (en el video 3 fueron ~30 dB más 10).
- En esta tanda solo se hicieron SFX, sin música. La música se pone **en una segunda pasada**.

### Flujo del autor
1. Instalar tres piezas: el analizador de audio (oídos), el conector al editor (manos) y la biblioteca con licencia (material).
2. Prompt: "sonoriza 0–18 s; analiza cada frame; por cada movimiento de gráfico añade un sonido (swoosh, pop, UI); donde solo hay persona, nada; solo SFX, sin música; usa solo la biblioteca X y verifica cada sonido con el analizador".
3. Escuchar y ajustar dB por instrucción.
4. Música: una canción concreta elegida por el humano, adaptada (recortada o reestructurada) a la duración de la intro.
5. Escuchar la mezcla sin la voz para comprobar que fluye.
6. Convertir las instrucciones en una skill reutilizable.

### Cómo implementarlo en código
- `sfx_index.json` (Python, offline): para cada SFX se calcula `peak_dbfs`, `lufs`, `attack_ms` (tiempo al pico), `duration_ms`, `spectral_centroid` y etiqueta (`whoosh|pop|ui|riser|impact`). Se hace con librosa o pyloudnorm (sugerido). Así el agente "oye".
- `cue_sheet` desde el `edit_plan`: cada evento de animación (entrada o salida de una escena, zoom, pop de un caption especial o un gráfico) genera una cue `{t, type, intensity}`. Las escenas `speaker-only` no generan cues.
- Mapa evento → SFX (los dos primeros los da el autor; el resto es sugerido):
  - `zoom_out` / cambio de escala grande → whoosh
  - `text_pop` / aparición de UI → UI click o pop
  - `special_word` → impacto corto
  - `scene_transition` / cambio de tema → riser + whoosh
  - `pattern_break` → sub-drop o impacto grave
- Niveles: el SFX más fuerte se fija 15 dB por debajo de lo que dejó la IA y el resto 5–10 dB, así que en la práctica la tabla de la sección 7 manda. Hay que alinear el pico del SFX (`attack_ms`) con el frame del evento, no con su inicio.
- Música: `fit_music(track, duration)` corta en el límite de un compás (beat tracking) y empalma intro y final (ver sección 6). Nunca corta a mitad de beat.

---

## 5. Estilo "pixel" (minimal, contraste alto, cinemático)

### Principios
- **Limpio**: el sujeto se ve siempre de inmediato. Texto y animación solo lo apoyan.
- **Muy contrastado** (negros muy negros, sombras profundas) y **saturado** (nada lavado).
- **Líneas guía como en fotografía**: cada movimiento lleva al siguiente, así que todo parece **un único movimiento**. Un elemento aparece justo cuando termina el anterior.
- El detalle "premium" son **píxeles que recorren la pantalla** en el **mismo color de acento** que la palabra clave: ese color une todo el frame.
- Sin sonido se siente plano: "**todo lo que se mueve lleva sonido**".

### Reglas medibles
- Lienzo de 1080×1920 a 30 fps. Fuente **Inter** (similar a la de Apple).
- Tres líneas de texto centradas en **composición triangular**: la línea central es la más grande y la de abajo, más pequeña.
- Animación de texto **por palabras** (no por caracteres):
  - Línea 1: posición desde arriba y opacidad 0→100.
  - Palabra clave: escala 0 → **overshoot** → ligero rebote por debajo → 100 (keyframes con ease y graph suavizada). Va en **rojo** con glow cuya exposición sube al máximo y vuelve a 0.
  - Línea 3: posición desde la izquierda, opacidad 0→100 y **blur 20 → 0**.
- Tarjetas de video: rectángulo con esquinas muy redondeadas y un duplicado más grande y desenfocado detrás (halo).
  - Hay **3 tarjetas** (son precomps distintas: si duplicas mal animas lo mismo 3 veces).
  - Entrada: escala 0→100 con ease, desfasadas **unos frames** entre sí.
  - En la entrada, Gaussian blur de máximo a 0 y **exposición 2 → 0**.
  - Van **detrás del texto** y entran **justo después** de la palabra clave.
- Píxeles: un trazo (path) en rojo de acento con trim paths (`end` 0→100 y luego `start` 0→100, solapados), más turbulent displace y mosaic, que los vuelven bloques irregulares. Uno por cada lado del encuadre y **detrás** de las tarjetas.
- Cámara global: un null padre de todo. Zoom-in **muy rápido al inicio que luego desacelera** (keyframes separados para que sea dramático).
- Fondo: sólido del color del fondo con máscara con feather para que no haya bordes duros al alejarse.
- Al final, un trazo guía que acompaña a las tarjetas, glow opcional ("puede ser demasiado") y **motion blur** en todo.

### Flujo del autor
1. Texto (timing en el waveform: cada línea entra cuando se dice).
2. Palabra clave (escala con rebote y glow).
3. Tarjetas.
4. Píxeles.
5. Null con zoom.
6. Fondo y trazo guía.
7. Motion blur.
8. Volver al editor para el sonido: zoom out → whoosh y popups de texto → sonidos de UI. La música se busca describiéndola a un asistente.

### Cómo implementarlo en código
- Estilo `pixel-minimal` en `style.json`: `font: Inter`, `accent: #E5242B (sugerido)` y `grade: { contrast: +20, blacks: -15, saturation: +15 } (sugerido)`, aplicado con el filtro `eq` de ffmpeg o una LUT.
- `WordReveal`: `{ by: 'word', from: 'top'|'left', distance: 40px (sugerido), opacity: [0,1], blur: [20,0], stagger: 3f (sugerido), dur: 10f (sugerido) }`.
- `KeywordPop`: escala `[0, 1.25, 0.95, 1.0]` en frames `[0, 8, 13, 18]` (sugerido), color de acento y `glow` con intensidad `[0, max, 0]`.
- `VideoCards`: `{ count: 3, radius: 48px (sugerido), haloBlur: 30px (sugerido), enterOffset: 4f (sugerido), enterBlur: [max,0], enterExposure: [2,0], startAfter: keywordEnd }`.
- `PixelTrail`: un SVG path con `strokeDasharray` animado (trim de start y end) y rasterizado a una rejilla de bloques de 8–12 px (sugerido) con ruido de desplazamiento (simplex). Usa el color de acento y z-index por debajo de las tarjetas.
- `CameraRig`: un wrapper con `scale/translate` y la curva `easeOutExpo` (sugerido) de 1.0 a 1.15 en 1–1.5 s.
- Encadenado: el planificador fuerza `start(next) = end(prev) - overlap(2–4f, sugerido)` para mantener la "línea guía" temporal.

---

## 6. Assets de edición (b-roll, fotos, IA, LUTs, plantillas, captions, música)

### Principios
- El A-roll es el speaker. El **B-roll** (foto o video de lo que se dice) entra encima cuando se habla de algo concreto. **Mejor video que foto.**
- Las fotos fijas se "animan" con un paneo lento o un zoom leve. Si el zoom queda exagerado, se baja.
- Lo que no existe en stock (por ejemplo "publiqué más de 1000 videos") se **genera con IA**: 9:16, sin audio, 5 s y 1080p.
- Si una foto está casi bien, **se corrige con IA** (de nublado a soleado) en vez de buscar otra.
- LUTs: el autor casi no los usa porque "no aportan". **No se aplican sobre personas** (la piel se pone amarilla). Sí sobre paisajes y drones, donde el naranja-azul es el contraste más cinemático. Se aplican en intensidad parcial y después de la corrección de color base.
- Las plantillas de UI (mensaje o email) se ponen **a pantalla completa sobre un fondo abstracto**, no encima de la cara.
- Fuente de captions: elige una buena, **guárdala como estilo** y no la cambies en cada video.
- La música se usa por secciones: entra en un beat concreto en un punto de cambio y **el video termina con el final de la canción**.

### Reglas medibles
- Descarga en 1080, no en 4K: el ejemplo pesaba 610 MB contra 15 MB, y el 4K tiene 4 veces los píxeles.
- Imagen generada por IA: 9:16, 5 s, 1080, sin audio.
- Intensidad de la LUT: el ejemplo bajó a **~20 %**.
- Captions de reel: **una sola línea**, con estilo guardado (con sombra si así se guardó).
- Música: **−30 dB**. Arranca en un beat marcado, al principio si el video no tiene intro.
- Empalme de música (intro y final de la canción): crossfade por defecto, cubierto con **riser + whoosh a −15 dB** cada uno (el riser se acorta y bajó "otros −15").
- Risers y whooshes **solo en transiciones reales** (cambio de tema o de sección), "si no, es aleatorio".

### Flujo del autor
1. Ver el transcript y marcar qué frase pide visual.
2. Buscar video (preferido) o foto y colocarla exactamente cuando se nombra.
3. Animar con paneo o escala.
4. Generar con IA lo que no exista.
5. Plantilla de UI sobre fondo abstracto a pantalla completa para el momento de "envié 80 mensajes".
6. Captions con estilo guardado.
7. Música a −30 dB recortada al beat, empalme intro→final con crossfade + riser + whoosh.
8. Corregir assets con IA si algo no encaja.

### Cómo implementarlo en código
- `BRoll`: `{ src, kind: 'video'|'photo', at: wordStart, motion: 'panLR'|'zoomIn', panPx: 80 (sugerido), zoom: [1.0,1.08] (sugerido) }`. Una foto siempre lleva motion; un video, ninguno o uno leve.
- `asset_list` en el plan: `{ phrase, need: 'stock'|'generate'|'template', query, aspect:'9:16', dur:5 }` (encaja con la regla 5 de AGENTS.md).
- `ingest.py`: transcodifica todo a 1080×1920 H.264 (por ejemplo `ffmpeg -vf scale=-2:1920,crop=1080:1920`) y nunca trabaja en 4K.
- `grade`: `lut: {file, mix: 0.2}` solo en escenas sin persona (flag `has_person` del plan o de la detección de caras). En el speaker, solo la corrección base.
- `UITemplateScene`: `{ template, bg: 'abstract_loop.mp4', scale: 0.8 (sugerido) }`, a pantalla completa con el speaker oculto.
- `music.py`: detecta beats (librosa), elige un `in_beat` y alinea el `track_end` con el final del video. Para el empalme usa `acrossfade=d=1 (sugerido)`, con riser + whoosh a −15 dB y el pico del whoosh en el punto de corte.

---

## 7. Tabla maestra de niveles de audio (consolidada)

| Capa | Valor de la transcripción | Implementación (sugerido) |
|---|---|---|
| Voz | (referencia) | −14 LUFS integrado del master, voz en −16 a −14 LUFS |
| Música bajo voz | −30 dB, a veces otros −10 dB extra, o −25 dB | ducking: música en −30 LU respecto a la voz. Sin voz, se sube +6 dB |
| SFX (whoosh, riser) en transiciones | −15 dB | pico en −18 dBFS |
| SFX tras la revisión | el más fuerte −15 dB y el resto −5 a −10 dB | normalizar cada SFX a −20 dBFS de pico y los "hero" a −16 dBFS |
| Regla dura | "la música nunca gana a la voz" | QA automático: la RMS de la música por debajo de la de la voz −20 dB en todo tramo con voz |

---

## Errores comunes que el autor dice evitar
1. Dejar pausas o respiraciones. Cada una es una puerta de salida.
2. Poner un efecto en cada corte. Eso es decorar, no editar. El zoom se guarda para la palabra que importa.
3. Dejar que la música tape la voz. La música es el suelo.
4. Usar la ruptura de patrón más de una vez. Funciona porque es única.
5. Pegar gráficos "encima" del speaker como stickers en lugar de ponerlos detrás.
6. Marcar demasiadas palabras clave: solo ~1 cada varios segundos.
7. Motion graphics de IA "porque sí". En reels casi nadie los usa. Antes de pedirlos, comprueba si a mano o con un componente es más rápido.
8. Hacer gráficos con timing y **luego** recortar el video, porque los tiempos se rompen.
9. Fiarse de la transcripción o la alineación que hace la IA. Hay que usar los tiempos del editor y revisar la alineación del texto.
10. Dejar que la IA elija la música. La elige el humano.
11. Usar música o SFX sin licencia. Un claim tumba el video.
12. Cortar la música a mitad de un beat o de una frase musical.
13. Poner SFX en planos donde solo habla la persona, o risers en puntos aleatorios sin transición real.
14. Aceptar el nivel de SFX o música que deja la IA sin escucharlo (siempre quedó alto).
15. Aplicar LUTs sobre piel humana.
16. Descargar o trabajar en 4K sin necesidad.
17. Poner una plantilla de UI encima de la cara en lugar de a pantalla completa.
18. Duplicar mal las precomps de las tarjetas y acabar animando 3 veces lo mismo.
19. Olvidar el motion blur en ramps y animaciones, que se notan baratas sin él.
20. Cambiar de fuente en cada video en vez de usar un estilo guardado.

## Checklist de calidad antes de entregar
- [ ] No queda ningún silencio de más de 120 ms (sugerido) ni ninguna repetición de toma.
- [ ] Hay un evento visual cada 1–3 s, y en talking head cada ~1 s. No hay huecos de más de 3 s sin cambio.
- [ ] El encuadre cambia cada 2–3 s, el push-in cae en los remates y luego vuelve a abrir.
- [ ] Las palabras especiales (amarillas o de acento) son como máximo ~1 cada varios segundos y cada una tiene SFX.
- [ ] Hay 0 o 1 ruptura de patrón, cerca de la mitad.
- [ ] Los gráficos van detrás del speaker cuando comparten plano. Las plantillas de UI van a pantalla completa sobre fondo.
- [ ] El texto está alineado y centrado dentro de la zona segura del storyboard.
- [ ] Hay un único color de acento repetido (palabra clave, píxeles y trazos). El contraste es alto y no hay nada lavado.
- [ ] Las animaciones están encadenadas (cada una arranca cuando termina la anterior) y tienen motion blur.
- [ ] Los speed ramps no superan la duración del clip de origen y llevan motion blur.
- [ ] El b-roll entra exactamente en la palabra que nombra. Las fotos llevan paneo o zoom suave.
- [ ] No hay LUT sobre personas. Si hay LUT, está en mezcla parcial (~20 %).
- [ ] Cada movimiento de gráfico tiene su SFX y los planos de solo speaker no tienen SFX.
- [ ] Hay risers y whooshes solo en las transiciones reales.
- [ ] La música está a −25/−30 dB bajo la voz, entra en un beat y termina con el final del video.
- [ ] Música y SFX tienen licencia limpia.
- [ ] Se escuchó la mezcla en solo (música + SFX) y con voz: nada tapa la voz y no hay SFX que piten.
- [ ] Se vio el video en mute: se entiende y no se siente plano.
- [ ] Se vio el video con sonido: no hay ningún efecto "decorativo" que no apoye una palabra o un movimiento.
