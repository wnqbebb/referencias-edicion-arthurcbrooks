# ASSETS · v2

Estilo: **Arthur Brooks · Clip de podcast (zooms + cambios de cámara)** · Formato del video: 9:16 (1080×1920).

**Branding:** Paleta de marca (60/30/10): primario #F9F7FA · secundario #0B0B0D · acento #1B54F8 · acento oscuro #0A2A8C. Tipografías: Inter + Playfair Display italic. Textura: paper. Look: contraste 1.05, saturación 0.95, tinte del acento oscuro.

## Cómo entregarlo
1. Genera (o descarga) cada asset **en el orden de la lista**: los marcados con *referencia* se usan como imagen de referencia de los siguientes (consistencia de producto, modelo y estilo).
2. Nombra cada archivo exactamente como dice **Archivo** (la extensión puede ser .png/.jpg/.webp o .mp4/.mov).
3. Mete todo en un zip llamado **`v2.zip`** y pásamelo. Yo lo valido, recorto al aspect ratio y aplico el grado de color del video.

| # | Archivo | Tipo | AR | Escena | Referencias |
|---|---|---|---|---|---|
| A01 | `A01_camiseta-hero` | Producto (hero de referencia) | 1:1 | referencia de A02, A04, A06, A07 | — |
| A02 | `A02_tienda-curada-5` | Foto | 4:5 | s05 «5 prendas» | A01 |
| A03 | `A03_rack-saturado` | Video b-roll | 9:16 | s02 «100 camisetas» | — |
| A04 | `A04_modelo-pinta` | Modelo UGC | 9:16 | s09 «pinta completa» | A01 |
| A05 | `A05_cliente-se-va` | Video b-roll | 9:16 | s04 «se confunde y se va» | — |
| A06 | `A06_modelo-pinta-video` | Video b-roll | 9:16 | s05 segunda toma | A04 |
| A07 | `A07_detalle-pinta` | Video b-roll | 9:16 | s09 segunda toma | A01, A04 |
| A08 | `A08_halftone` | Textura | 1:1 | fondos y bloques | — |

## A01 · Camiseta oversize negra (referencia de consistencia)
- **Archivo:** `A01_camiseta-hero.png` · **Tipo:** Producto (hero de referencia) · **Aspect ratio:** 1:1 (1920x1920)
- **Se usa en:** referencia de A02, A04, A06, A07 · **Duración:** —
- **Referencias de consistencia:** ninguna (este asset ES referencia)
- **Prompt (EN):**

```
Product photo of a heavyweight oversized black cotton t-shirt with dropped shoulders and a thick ribbed collar hanging on a matte black metal hanger against a warm beige wall, soft side light revealing the cotton texture and a few natural creases, no logo, clean streetwear boutique look, centered. shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, real-world imperfections in the fabric, e-commerce boutique photography, not CGI
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`
- **Nota para el editor:** No sale en el video: solo es la referencia para que la camiseta sea idéntica en todo.

## A02 · Tienda curada: solo 5 prendas bien puestas
- **Archivo:** `A02_tienda-curada-5.png` · **Tipo:** Foto · **Aspect ratio:** 4:5 (1536x1920)
- **Se usa en:** s05 «5 prendas» · **Duración:** —
- **Referencias de consistencia:** A01
- **Prompt (EN):**

```
Photo of a minimalist men's streetwear store wall with only five pieces displayed on a single black rail with wide spacing: the black oversized tee from the reference, a beige overshirt, washed straight denim jeans, a brown chore jacket and a black cap on a small shelf, warm spotlight on each piece, concrete floor, calm and premium. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`

## A03 · Rack saturado de camisetas iguales
- **Archivo:** `A03_rack-saturado.mp4` · **Tipo:** Video b-roll · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s02 «100 camisetas» · **Duración:** 5 s
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Vertical video, slow sideways dolly along an overcrowded clothing rack packed with about one hundred nearly identical gray and black t-shirts squeezed together, a hand pushes the hangers and they barely move, flat harsh fluorescent light, cheap messy store. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays`
- **Movimiento de cámara / animación (video):** Dolly lateral lento; la mano empuja los ganchos a los 2 s.

## A04 · Modelo con la pinta completa
- **Archivo:** `A04_modelo-pinta.png` · **Tipo:** Modelo UGC · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s09 «pinta completa» · **Duración:** —
- **Referencias de consistencia:** A01
- **Prompt (EN):**

```
Vertical UGC photo of a 25-year-old Latino man with a short fade haircut wearing the exact black oversized tee from the reference image with beige cargo pants, white leather sneakers and a black cap worn backwards, full outfit head to toe, standing against a warm beige wall in a small studio, confident relaxed pose, face in the upper third. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch`

## A05 · Cliente confundido que se va
- **Archivo:** `A05_cliente-se-va.mp4` · **Tipo:** Video b-roll · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s04 «se confunde y se va» · **Duración:** 5 s
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Vertical video of a young man browsing a crowded clothing rack, flipping fast through hangers, frowning, then sighing, turning around and walking out of the store, handheld, natural store light. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays`
- **Movimiento de cámara / animación (video):** Plano medio fijo; él sale de cuadro por la derecha en el segundo 4.

## A06 · El mismo modelo de A04 en movimiento
- **Archivo:** `A06_modelo-pinta-video.mp4` · **Tipo:** Video b-roll · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s05 segunda toma · **Duración:** 4 s
- **Referencias de consistencia:** A04
- **Prompt (EN):**

```
Image-to-video from the reference image: the same man adjusts his backwards cap, takes two steps towards the camera and stops with a small confident nod, warm beige wall, handheld with a subtle push-in. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays`
- **Movimiento de cámara / animación (video):** Dos pasos hacia cámara + push-in 6 %.

## A07 · Detalles de la pinta (macro)
- **Archivo:** `A07_detalle-pinta.mp4` · **Tipo:** Video b-roll · **Aspect ratio:** 9:16 (1080x1920)
- **Se usa en:** s09 segunda toma · **Duración:** 3 s
- **Referencias de consistencia:** A01, A04
- **Prompt (EN):**

```
Vertical macro video, three quick details in one continuous move: the ribbed collar of the black oversized tee, the cargo pocket of the beige pants, the white sneaker stepping forward, warm side light, shallow depth of field. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```
- **Negative prompt:** `CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays`
- **Movimiento de cámara / animación (video):** Tilt down continuo del cuello a las zapatillas.

## A08 · Textura halftone
- **Archivo:** `A08_halftone.png` · **Tipo:** Textura · **Aspect ratio:** 1:1 (1920x1920)
- **Se usa en:** fondos y bloques · **Duración:** —
- **Referencias de consistencia:** —
- **Prompt (EN):**

```
Seamless halftone dot texture, small black dots fading diagonally on off-white (#F9F7FA) paper, offset print look, subtle misregistration, tileable.
```
- **Negative prompt:** `text, objects, colors, gradients`
