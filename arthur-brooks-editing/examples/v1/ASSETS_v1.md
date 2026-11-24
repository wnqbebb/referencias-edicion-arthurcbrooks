# ASSETS · v1

Estilo: **Arthur Brooks · Talking head + minimal** · Formato del video: 9:16 (1080×1920).

**Branding:** Paleta de marca (60/30/10): primario #F7F3F2 · secundario #120A0C · acento #9E1C3A · acento oscuro #5A0F21. Tipografías: Inter + Playfair Display italic. Textura: paper. Look: contraste 1.08, saturación 0.8, tinte del acento oscuro.

## Cómo entregarlo
1. Genera (o descarga) cada asset **en el orden de la lista**: los marcados con *referencia* se usan como imagen de referencia de los siguientes (consistencia de producto, modelo y estilo).
2. Nombra cada archivo exactamente como dice **Archivo** (la extensión puede ser .png/.jpg/.webp o .mp4/.mov).
3. Mete todo en un zip llamado **`v1.zip`** y pásamelo. Yo lo valido, recorto al aspect ratio y aplico el grado de color del video.

| # | Archivo | Tipo | AR | Escena | Referencias |
|---|---|---|---|---|---|
| A01 | `A01_blusa-hero` | Producto (hero de referencia) | 4:5 | s09, s07 | — |
| A02 | `A02_modelo-ugc-blusa` | Modelo UGC | 9:16 | s07 | A01 |
| A03 | `A03_foto-mala-blusa` | Foto | 4:5 | s07b | A01 |
| A04 | `A04_blackfriday-tienda` | Video b-roll | 9:16 | s02 | — |
| A05 | `A05_etiquetas-iguales` | Gráfico / ilustración | 9:16 | s03 | — |
| A06 | `A06_devolucion-paquete` | Video b-roll | 9:16 | s08b | — |
| A07 | `A07_bodega-vacia-enero` | Foto | 9:16 | s06 | — |
| A08 | `A08_textura-papel` | Textura | 1:1 | todas las escenas de fondo | — |

## A01 · Producto hero (referencia de consistencia)
- **Archivo:** `A01_blusa-hero.png` · **Tipo:** Producto (hero de referencia) · **Aspect ratio:** 4:5 (1536x1920)
- **Se usa en:** s09, s07 · **Duración:** —
- **Referencias de consistencia:** ninguna (este asset ES referencia)
- **Prompt (EN):**

```
Product photo of a deep wine-red (#5A0F21) satin wrap blouse with long sleeves on a slim wooden hanger, hanging against a warm off-white plaster wall, soft directional window light from the left, gentle fabric folds and realistic satin sheen, small visible stitching, minimalist boutique aesthetic, centered, generous negative space above. shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, real-world imperfections in the fabric, e-commerce boutique photography, not CGI
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`
- **Nota para el editor:** Este es el producto de referencia: TODOS los assets con la blusa deben usar este archivo como imagen de referencia.

## A02 · Modelo UGC con la blusa puesta (look completo, buena luz)
- **Archivo:** `A02_modelo-ugc-blusa.png` · **Tipo:** Modelo UGC · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s07 · **Duración:** —
- **Referencias de consistencia:** A01
- **Prompt (EN):**

```
Vertical UGC photo of a 28-year-old Latina woman wearing the exact wine-red satin wrap blouse from the reference image, tucked into high-waisted black tailored trousers, gold hoop earrings, standing in a small warm boutique fitting area, full outfit visible head to knees, soft daylight from a large window, natural relaxed pose with one hand in pocket, looking slightly off camera, real skin texture, phone-camera framing. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`

## A03 · La misma blusa mal fotografiada (contraste antes/después)
- **Archivo:** `A03_foto-mala-blusa.png` · **Tipo:** Foto · **Aspect ratio:** 4:5 (1536x1920)
- **Se usa en:** s07b · **Duración:** —
- **Referencias de consistencia:** A01
- **Prompt (EN):**

```
Amateur phone photo of the same wine-red satin blouse from the reference image lying crumpled on an unmade bed, dim yellow tungsten room light, harsh on-camera flash reflection, slightly tilted framing, cluttered background with a phone charger and a mug, colors look dull and wrong. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`
- **Nota para el editor:** Debe verse MAL a propósito: es el 'antes'.

## A04 · Tiendas con descuentos iguales
- **Archivo:** `A04_blackfriday-tienda.mp4` · **Tipo:** Video b-roll · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s02 · **Duración:** 5 s
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Vertical handheld video walking past several clothing store windows in a mall, each window with the same generic red 'SALE -30%' signs, shoppers passing by blurred, evening mall lighting, slight motion blur, realistic. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`
- **Movimiento de cámara / animación (video):** travelling lateral lento a pie, 0.5 m/s
- **Alternativa stock (Pexels/Pixabay):** buscar `black friday sale store window` → yo le aplico el mismo grado/LUT del video.

## A05 · 20 etiquetas de descuento idénticas (gráfico)
- **Archivo:** `A05_etiquetas-iguales.png` · **Tipo:** Gráfico / ilustración · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s03 · **Duración:** —
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Flat editorial illustration, top-down grid of 20 identical paper price tags with string, each printed '-30%' in bold black sans-serif, tags on an off-white #F4F1F1 rough paper background, subtle paper grain texture, one single tag slightly highlighted in #9E1C3A, soft shadows, minimal, high contrast, vertical composition with breathing room at top and bottom.
```
- **Negative prompt:** `photorealistic people, faces, logos, brand names, 3D render, clutter, gradients`

## A06 · Clienta abre paquete y la prenda no es igual
- **Archivo:** `A06_devolucion-paquete.mp4` · **Tipo:** Video b-roll · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s08b · **Duración:** 5 s
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Vertical UGC video, close-up of a woman's hands opening a plain cardboard delivery box on a kitchen table, pulling out a red blouse that looks noticeably different in color, she pauses and folds it back, daylight, realistic hands with natural nails. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`
- **Movimiento de cámara / animación (video):** cámara fija en mano, leve temblor
- **Alternativa stock (Pexels/Pixabay):** buscar `woman opening package clothes` → yo le aplico el mismo grado/LUT del video.

## A07 · Bodega con estantes vacíos en enero
- **Archivo:** `A07_bodega-vacia-enero.png` · **Tipo:** Foto · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s06 · **Duración:** —
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Vertical photo of a small boutique stockroom with mostly empty white shelves and a few lonely folded garments, cold gray January daylight, a calendar on the wall, quiet and sad mood, realistic. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`
- **Alternativa stock (Pexels/Pixabay):** buscar `empty shelves store` → yo le aplico el mismo grado/LUT del video.

## A08 · Textura de papel de la marca
- **Archivo:** `A08_textura-papel.png` · **Tipo:** Textura · **Aspect ratio:** 1:1 (1920x1920)
- **Se usa en:** todas las escenas de fondo · **Duración:** —
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Seamless high-resolution texture of light off-white #F4F1F1 cotton paper, subtle fibers and grain, very soft uneven lighting, no folds, no text, flat scan, tileable.
```
- **Negative prompt:** `text, objects, shadows, wrinkles, color tint`
