# V2 · Prompts de assets (Clip de podcast)

## Orden de generación y consistencia

Genera en este orden. Cada paso usa como imagen de referencia el archivo indicado, para que la prenda y la persona sean idénticas en todo el video.

1. **A01** Camiseta oversize negra (referencia de consistencia) — primero, es la referencia.
1. **A02** Tienda curada: solo 5 prendas bien puestas — con referencia A01.
1. **A04** Modelo con la pinta completa — con referencia A01.
1. **A06** El mismo modelo de A04 en movimiento — con referencia A04.
1. **A07** Detalles de la pinta (macro) — con referencia A01 + A04.
1. **A03** Rack saturado de camisetas iguales — independiente.
1. **A05** Cliente confundido que se va — independiente.
1. **A08** Textura halftone — independiente.

**Reglas**

- Personas: hiperrealistas tipo UGC (piel con poros, luz de ventana, encuadre de celular). Si se ve a IA, se repite.
- Si tu generador no tiene el formato exacto, usa el más cercano y deja aire alrededor: yo recorto.
- Videos: genera primero el fotograma con el prompt y luego anímalo (image-to-video) con el movimiento indicado.
- No pongas texto dentro de las imágenes salvo donde el prompt lo pide: los textos los anima el sistema encima.
- Al recibirlos aplico el grado de marca a todo: contraste +10 %, saturación −20 %, tinte azul #0A2A8C en sombras (soft-light 15 %), halftone suave, grano medio.

## Prompts de imágenes: producto, modelos y escenas

### A01 · Camiseta oversize negra (referencia de consistencia)

| Campo | Valor |
|---|---|
| Archivo | `A01.png` |
| Tipo | Producto (referencia) |
| Formato | 1:1 · 1920×1920 |
| Dónde sale | referencia de A02, A04, A06, A07 |

**Prompt**

```
Product photo of a heavyweight oversized black cotton t-shirt with dropped shoulders and a thick ribbed collar hanging on a matte black metal hanger against a warm beige wall, soft side light revealing the cotton texture and a few natural creases, no logo, clean streetwear boutique look, centered. shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, real-world imperfections in the fabric, e-commerce boutique photography, not CGI
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

> No sale en el video: solo es la referencia para que la camiseta sea idéntica en todo.

### A02 · Tienda curada: solo 5 prendas bien puestas

| Campo | Valor |
|---|---|
| Archivo | `A02.png` |
| Tipo | Foto |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s05 «5 prendas» |
| Imagen de referencia | `A01` |

**Prompt**

```
Photo of a minimalist men's streetwear store wall with only five pieces displayed on a single black rail with wide spacing: the black oversized tee from the reference, a beige overshirt, washed straight denim jeans, a brown chore jacket and a black cap on a small shelf, warm spotlight on each piece, concrete floor, calm and premium. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

### A04 · Modelo con la pinta completa

| Campo | Valor |
|---|---|
| Archivo | `A04.png` |
| Tipo | Modelo UGC |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s09 «pinta completa» |
| Imagen de referencia | `A01` |

**Prompt**

```
Vertical UGC photo of a 25-year-old Latino man with a short fade haircut wearing the exact black oversized tee from the reference image with beige cargo pants, white leather sneakers and a black cap worn backwards, full outfit head to toe, standing against a warm beige wall in a small studio, confident relaxed pose, face in the upper third. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

## Prompts de ilustraciones, pinturas y texturas

### A08 · Textura halftone

| Campo | Valor |
|---|---|
| Archivo | `A08.png` |
| Tipo | Textura |
| Formato | 1:1 · 1920×1920 |
| Dónde sale | fondos y bloques |

**Prompt**

```
Seamless halftone dot texture, small black dots fading diagonally on off-white (#F9F7FA) paper, offset print look, subtle misregistration, tileable.
```

**Negativo**

```
text, objects, colors, gradients
```

## Prompts de video b-roll y movimiento

### A03 · Rack saturado de camisetas iguales

| Campo | Valor |
|---|---|
| Archivo | `A03.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s02 «100 camisetas» |
| Duración | 5 s |
| Movimiento | Dolly lateral lento; la mano empuja los ganchos a los 2 s. |

**Prompt**

```
Vertical video, slow sideways dolly along an overcrowded clothing rack packed with about one hundred nearly identical gray and black t-shirts squeezed together, a hand pushes the hangers and they barely move, flat harsh fluorescent light, cheap messy store. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

### A05 · Cliente confundido que se va

| Campo | Valor |
|---|---|
| Archivo | `A05.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s04 «se confunde y se va» |
| Duración | 5 s |
| Movimiento | Plano medio fijo; él sale de cuadro por la derecha en el segundo 4. |

**Prompt**

```
Vertical video of a young man browsing a crowded clothing rack, flipping fast through hangers, frowning, then sighing, turning around and walking out of the store, handheld, natural store light. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

### A06 · El mismo modelo de A04 en movimiento

| Campo | Valor |
|---|---|
| Archivo | `A06.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s05 segunda toma |
| Duración | 4 s |
| Imagen de referencia | `A04` |
| Movimiento | Dos pasos hacia cámara + push-in 6 %. |

**Prompt**

```
Image-to-video from the reference image: the same man adjusts his backwards cap, takes two steps towards the camera and stops with a small confident nod, warm beige wall, handheld with a subtle push-in. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

### A07 · Detalles de la pinta (macro)

| Campo | Valor |
|---|---|
| Archivo | `A07.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s09 segunda toma |
| Duración | 3 s |
| Imagen de referencia | `A01` + `A04` |
| Movimiento | Tilt down continuo del cuello a las zapatillas. |

**Prompt**

```
Vertical macro video, three quick details in one continuous move: the ribbed collar of the black oversized tee, the cargo pocket of the beige pants, the white sneaker stepping forward, warm side light, shallow depth of field. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

## Entrega

Mete todos los archivos en un zip llamado **`v2.zip`**, sin carpetas dentro, con estos nombres exactos:

| Archivo | Qué es | Formato |
|---|---|---|
| `A01.png` | Camiseta oversize negra (referencia de consistencia) | 1:1 |
| `A02.png` | Tienda curada: solo 5 prendas bien puestas | 4:5 |
| `A03.mp4` | Rack saturado de camisetas iguales | 9:16 |
| `A04.png` | Modelo con la pinta completa | 9:16 |
| `A05.mp4` | Cliente confundido que se va | 9:16 |
| `A06.mp4` | El mismo modelo de A04 en movimiento | 9:16 |
| `A07.mp4` | Detalles de la pinta (macro) | 9:16 |
| `A08.png` | Textura halftone | 1:1 |

Al recibirlo ejecuto `assetpack.py v2 --ingest v2.zip`: valida que estén todos, recorta al formato, aplica el grado de marca y monta la vista previa con los elementos integrados, el diseño sonoro y la música para tu aprobación antes de renderizar.
