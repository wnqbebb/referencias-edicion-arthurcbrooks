# Método Joseph (Ultimate Editors) — cómo se entrena y se usa la skill Arthur Brooks

Fuente: video completo de Joseph «AI edit with only Claude» (21 min), en `research/joseph/`
(transcripción: `transcript.txt`; fotogramas: `sheets/`, `key/`). Esto manda sobre cualquier regla anterior que lo contradiga.

## A. Los 10 principios del estilo (en este orden de frecuencia)

| # | Principio | Receta exacta |
|---|---|---|
| 1 | **Subtítulos en pantalla** | Inter para el texto normal + **Playfair Display Italic** (bold) para la palabra especial. Línea de ≤ 5 palabras. Se elige la palabra (o 2) más importante → **grande y en negrita** (bold sans o bold serif) **al centro**. Las demás palabras van **pequeñas, en sans light, en los huecos arriba/abajo** de la palabra grande. **El texto pequeño ocupa el 75 % del ancho del texto grande.** Variante: palabra serif sobre caja azul («enhance»). |
| 2 | **B-roll + texto** | El guion se parte en segmentos; b-roll que muestra literalmente lo que dice. Encima: **textura de papel clara, bordes oscurecidos y bordes un poco desenfocados** (foco al centro). Texto encima con la lógica del principio 1, describiendo la escena. |
| 3 | **Pinturas** | Pintura que describe la idea + **textura de pintura + papel rugoso** + texto cinematográfico **alrededor del sujeto** + **slide de cámara rápido** para revelarla. La textura se mueve CON la pintura y a media fuerza (revisión 3). |
| 4 | **Línea + texto** | Fondo negro o blanco con papel. **Línea azul de acento que lleva al texto, el texto la interrumpe, y la línea continúa** hacia otro texto relacionado. **La cámara sigue la punta de la línea.** |
| 5 | **Línea + ilustraciones** | Mismo fondo y línea, pero lleva a ilustraciones: (a) línea horizontal con **punto blanco** que marca el objeto + texto + ilustración debajo; (b) texto → **zigzag** con **paneo de cámara** que revela objetos a ambos lados (progresión por fases); (c) la línea llega directo al sujeto. |
| 6 | **Escena centrada en texto** | Fondo **blanco o azul con papel MUY rugoso**, **comillas** alrededor del centro y el texto cinematográfico en medio. |
| 7 | **Ilustración central** | Ilustración de la idea en el centro, **textura pintada, rugosa y con ruido**, ocupa la mitad baja y **sangra hacia el medio**; bordes abstractos. Texto en el resto. Variantes: cerebro cenital, patrón circular de líneas finas, **perfil lateral con textura de tela**. |
| 8 | **Ilustración lateral + texto** | Personaje abstracto a un lado, texto al otro. Variante: **media luna con textura de tela** a la izquierda y texto limpio rotando alrededor. Para mostrar 2 elementos a la vez. |
| 9 | **Objeto + texto** | Un solo elemento de la historia (foto, objeto), fondo papel, texto alrededor, **revelado rugoso**. |
| 10 | **Gráficos / estadísticas** | **Fondo oscuro plano con textura**, **cuadrícula de líneas blancas finas que brillan**, **bola azul** que dibuja la línea y **la cámara la sigue**. Etiquetas de eje en versalitas pequeñas. |

Los 5 pilares de diseño de cada escena: **Tamaño · Composición · Texturas · Formas · Colores** (azul acento, negro, crema/papel, blanco).

## B. Cómo se entrena (lo que ya hicimos y lo que faltaba)
1. 20 videos de referencia → mirarlos como editor: por cada escena «¿por qué este diseño, estos colores, estos efectos, esta animación?».
2. Tablero de inspiración (~130 piezas) categorizado en los 10 principios, con desglose por principio: qué lo compone, fuentes, colores, tamaños y patrones.
3. Prompt de entrenamiento: transcripción palabra a palabra + desglose fotograma a fotograma de cada video para estudiar **(1) dónde van las animaciones respecto al guion, (2) cómo está compuesto el diseño, (3) la lógica de animación: cuánto duran y cómo se sienten**.
4. Resultado: la skill + **225 animaciones extraídas, cada una en su carpeta con el diseño de referencia y la hoja de keyframes** (ID tipo `V10-A02`). → nuestra `library/animations/`.

## C. Cómo se usa (flujo de una edición)
1. Prompt: usar la skill + **transcripción al milisegundo, cortar silencios dejando 30 ms**, + **documento de planificación**.
2. **Documento de plan por beats**: guion a la derecha con el clip, a la izquierda **3 diseños recomendados (A/B/C) sacados de la biblioteca de Arthur** con miniatura, categoría, descripción concreta del beat y referencia (`Ref V10-A02`), + nota «Visto en los reels» (qué patrón de Arthur es) + caja para notas propias. El humano elige uno por beat → «Copiar plan».
3. Reglas de planificación del humano: **cuando anuncia algo nuevo → cara (A-roll con captions); cuando lo describe → se muestra**. Abrir con A-roll para conectar. Se balancean las escenas para que fluya.
4. Claude construye: busca las referencias elegidas, hace la **lista de assets** y los consigue (pinturas de Wikipedia, stock, fotos), captions primero, luego escena por escena, render.
5. **El primer borrador está al 60–70 %**: revisiones concretas con tiempo (ej.: «el texto de la escena 1 no está bien», «corte brusco entre el gráfico y el siguiente plano», «textura de pintura demasiado fuerte y no se mueve con la pintura», «mal corte en 0:24», «la espiral debe durar más», «comillas en la escena final»).
6. Diseño sonoro basado en las 20 referencias: **música cinematográfica, clics para texto, highlighter para gráficos, whooshes para transiciones**.

Tiempos de Joseph: corte + plan 15 min · planificar 15 min · crear edición 60 min · revisiones 10 min · sonido 15 min.

## D. Reglas del cliente (revisión 24-nov)
- **Palabra clave de los subtítulos en el color de marca del video** (la grande: «Black Friday», «menos», «telas»…). Si el acento es muy oscuro para leerse sobre el A-roll, se aclara lo justo; el resto del caption en blanco.
- **También se permiten gráficos en color sólido** (sin textura) cuando la escena lo pide: bloques, números, fondos planos de marca.
- **Si el cliente describe cómo quiere algo, se construye así**, aunque no siga estas reglas al pie de la letra: las reglas guían, la descripción del cliente manda.


---

# Higgsfield Katana + Edit Studio dentro de la skill

## 0. Regla número uno: no se genera nada
**La skill nunca genera imágenes, video, voz ni música con herramientas de pago** (Higgsfield, Katana, edit-gen, Seedance,
Soul, etc.). Siempre:
1. Escribe los **prompts** de todo lo que falta (con la estructura de Katana de la sección 3).
2. Tú generas y entregas un **zip** con los nombres de archivo de la lista.
3. La skill lo ingiere (`assetpack.py --ingest`), lo recorta, le aplica el color de marca y lo usa.

Katana y edit-gen se usan **solo como método**: cómo analizan, planifican, escriben prompts y verifican. Sus pasos de
generación, sus créditos y su modo «autónomo sin preguntar» quedan **desactivados**. Prevalecen nuestras 3 pausas
(plan → assets → vista previa).

## 1. Qué es cada cosa
| | Qué es | Qué trae que nos sirve | Qué NO usamos |
|---|---|---|---|
| **Katana** (flujo de Higgsfield) | Rehace un video de referencia con tu sujeto: analiza cada fotograma, planifica, genera escenas nuevas y monta | Lectura fotograma a fotograma con mapa de energía; contrato de bloqueos y libertades; roles de toma; **prompts en 7 bloques con una función por referencia**; lugares vacíos reutilizables; 3 revisiones de movimiento; control de calidad (lógica cada 0.5 s, sin fotogramas repetidos) | La generación con Seedance/Soul, el gasto de créditos y el modo sin pausas |
| **Edit Studio** (plugin `edit-studio`) | Edición en código (Python + ffmpeg) con 3 skills: director, voz y generación | **Biblioteca de 268 movimientos** (`moves/*.yaml`: zoom, whip, crash, speed ramp, freeze, flash…); **15 géneros** con estructura y ritmo (fashion, ugc, product, explainer, viral…); presets de estilo por palabras; ediciones puntuales por voz («crash zoom en 0:07», «whip entre #4 y #5»); vista previa con clips numerados; versiones que no se repiten; medir un efecto de un clip de ejemplo; QA medido (cortes en el beat, LUFS) | `edit-gen` (de pago) y descargar de YouTube o TikTok |

Va incluido en `plugins/edit-studio/`. Las instrucciones de Katana (método) están en `docs/katana/`.

## 2. Reglas generales que adopta la skill (todas las ediciones)
1. **Plan en 5 líneas antes de trabajar** (Edit Studio): partes en orden, puntos de corte (tiempos o palabras citadas), duración, formato y estilo. Luego se ejecuta.
2. **Contrato de bloqueos y libertades** (Katana): `analysis/task-contract.json` con lo que NO puede cambiar (la prenda, la palabra del CTA, la canción…) y lo que es libre. Cada pedido tuyo es un bloqueo.
3. **Analizar la referencia entera** (Katana): todos los fotogramas, notas por segundo, cortes corregidos a mano, y un **mapa de energía**: cuántos cortes, flashes, sacudidas, movimientos de cámara y golpes por segundo. **La edición nueva repite esas tasas.** Si baja la energía, el video se siente plano.
4. **Roles de toma** (Katana): cada escena tiene una función: gancho, contexto, héroe, acción, detalle, contraste, revelación, clímax, pausa o remate. El concepto lleva planteamiento y remate.
5. **Ritmo por género** (Edit Studio): para moda se aplica `genres/fashion.md` (gancho tipo portada de revista, detalles de tela, un cambio de look por beat, flash de foto con congelado). Para UGC y producto, sus géneros. Se combinan con el formato Arthur, que manda.
6. **Movimientos con nombre** (Edit Studio): las transiciones y efectos se eligen de `moves/` (`find_move.py crash zoom`), respetando los permitidos y prohibidos de cada género y de cada formato Arthur.
7. **Prompts de assets en 7 bloques** (Katana, sección 3), con la referencia de identidad y ropa siempre primero.
8. **Lugares vacíos** (Katana): cada lugar que aparezca en varias tomas generadas tiene un «plate» propio **sin personas** (tipo `location`), que se reutiliza en todas sus tomas. Así el fondo no cambia entre tomas.
9. **La ropa del hero está bloqueada**: en todas las tomas lleva exactamente la prenda de tu foto. Nunca la del video de referencia ni una inventada.
10. **Duración a generar = el doble de lo que sale en pantalla** (mín. 4 s; Seedance: Σ por toma de clamp(2 × segundos en pantalla, 2, 4)). Así se elige el mejor tramo.
11. **Nunca se retocan caras con código**: ni pegar, ni deformar, ni «embellecer». Si una cara sale mal, se pide otra generación (prompt nuevo) o se usa otra toma.
12. **3 revisiones de movimiento** (Katana), antes de renderizar y sobre el borrador: (1) tiempo y ritmo; (2) movimiento en el espacio y continuidad entre cortes (dirección, escala); (3) detalle y pulido (energía, easing, tipografía, acentos de sonido).
13. **Control de calidad del material que entregas** (Katana): un fotograma cada 0.5 s de cada video generado. Se revisan manos, objetos que se funden, identidad, ropa y texto parásito, y se usa solo el tramo limpio.
14. **Ediciones puntuales por voz** (Edit Studio): «#5» (el número del clip en la vista previa), «0:07» o «donde dice …» + qué hacer («crash zoom», «whip», «quita», «más fuerte»).
15. **Versiones que no se repiten** (Edit Studio): una segunda versión evita las transiciones, movimientos y tomas de la anterior.
16. **Sonido de bibliotecas reales** (Katana/Edit Studio): música y efectos grabados (Mixkit, YouTube Audio Library, CC0). Nunca sintetizados por código.

## 3. Prompts de assets en 7 bloques (Katana)
Cada prompt de imagen o video incluye solo los bloques que aclaran la toma:

| # | Bloque | Qué escribir | Ejemplo |
|---|---|---|---|
| 1 | **Función de cada referencia** | Qué controla cada imagen adjunta, en orden | `@image1` = A01 (diseño exacto de la blusa) · `@image2` = A02 (identidad de la modelo) · `@image3` = L01 (lugar vacío) |
| 2 | **Contexto** (opcional) | Qué pasó antes y su huella; estado inicial → estado final | «acaba de abrir la caja; la blusa sale doblada → la sostiene frente al espejo» |
| 3 | **Mapa espacial** | Primer plano, plano medio y fondo; posiciones; dirección del movimiento | «ella a la izquierda en plano medio, ventana al fondo a la derecha» |
| 4 | **Una sola acción clara** | Un cambio de estado por toma | «gira ¼ hacia la ventana» |
| 5 | **Cámara** | Encuadre y ángulo; si se mueve: un movimiento, su dosis y su límite | «push-in lento del 5 %, termina antes de cortar la cabeza» |
| 6 | **Luz y textura** | La gramática visual elegida + luz motivada | «luz dorada de ventana, satén con brillo real, grano fino» |
| 7 | **Bloqueos finales** | Identidad, la ropa de tu foto, sin texto, continuidad | «lleva exactamente la blusa de @image1 en toda la toma; sin texto ni logos» |

Más la ficha técnica: formato (más cercano soportado) y resolución, duración a generar, negativo, nombre de archivo y zip.
`pipeline/assetpack.py` ya añade solo los bloques 1 y 7, la función de cada referencia y la duración a generar.

## 4. El plus, en concreto
| Antes | Ahora |
|---|---|
| Prompts sueltos: la blusa podía cambiar de color entre tomas | Cada referencia controla una sola cosa y la ropa está bloqueada en todas las tomas |
| Fondos distintos en cada toma generada | Un lugar vacío reutilizable por cada sitio |
| La energía se elegía a ojo | Se mide la de la referencia (cortes, flashes y movimientos por segundo) y se iguala |
| Transiciones de una lista corta | 268 movimientos con nombre, filtrados por género |
| Revisión general | 3 revisiones de movimiento + control cada 0.5 s del material generado |
| «Cámbialo» | Ediciones puntuales con #clip, tiempo o palabra |
