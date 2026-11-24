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
