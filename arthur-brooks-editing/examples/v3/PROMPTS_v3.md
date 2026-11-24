# V3 · Prompts de assets (Documental)

## Orden de generación y consistencia

Genera en este orden. Cada paso usa como imagen de referencia el archivo indicado, para que la prenda y la persona sean idénticas en todo el video.

1. **A01** Blusa ganadora (referencia de consistencia) — primero, es la referencia.
1. **A05** Boutique que muestra solo sus 5 ganadoras — con referencia A01.
1. **A08** Flat lay de las 5 prendas ganadoras — con referencia A01.
1. **A09** Macro de la seda lila y su costura — con referencia A01.
1. **A02** Caja con blusas que no se vendieron desde septiembre — independiente.
1. **A03** Clienta exigente revisando costuras — independiente.
1. **A04** La blusa que nadie quiso con -50 % — independiente.
1. **A06** Clienta ve 100 ofertas en el celular — independiente.
1. **A07** Etiquetas de talla con la M sellada «AGOTADA» — independiente.
1. **A10** Papel rugoso con tinte lila — independiente.

**Reglas**

- Personas: hiperrealistas tipo UGC (piel con poros, luz de ventana, encuadre de celular). Si se ve a IA, se repite.
- Si tu generador no tiene el formato exacto, usa el más cercano y deja aire alrededor: yo recorto.
- Videos: genera primero el fotograma con el prompt y luego anímalo (image-to-video) con el movimiento indicado.
- No pongas texto dentro de las imágenes salvo donde el prompt lo pide: los textos los anima el sistema encima.
- Al recibirlos aplico el grado de marca a todo: contraste +6 %, saturación −10 %, tinte violeta #3E1185 en sombras (soft-light 12 %), grano fino, viñeta suave; fotos de archivo con borde de papel.

## Prompts de imágenes: producto, modelos y escenas

### A01 · Blusa ganadora (referencia de consistencia)

| Campo | Valor |
|---|---|
| Archivo | `A01.png` |
| Tipo | Producto (referencia) |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s04, s08 «Ya vendidas», s09 «tus ganadoras» |

**Prompt**

```
Product photo of a lilac silk blouse with a soft bow at the neck on a velvet hanger, against a pale pink plaster wall, soft diffused window light, delicate fabric sheen and fine stitching, elegant feminine boutique aesthetic, small natural creases, centered with negative space around. shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, real-world imperfections in the fabric, e-commerce boutique photography, not CGI
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

> Si ella tiene su prenda más vendida, fotografíala igual y úsala como referencia.

### A02 · Caja con blusas que no se vendieron desde septiembre

| Campo | Valor |
|---|---|
| Archivo | `A02.png` |
| Tipo | Foto |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s01, s02 «desde septiembre» |

**Prompt**

```
Photo of an open cardboard storage box in a dim stockroom with several outdated patterned blouses folded inside, a handwritten paper label 'SEPT' taped on the box, dust in the air, cold light from a small window, slightly faded documentary look. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

### A03 · Clienta exigente revisando costuras

| Campo | Valor |
|---|---|
| Archivo | `A03.png` |
| Tipo | Modelo UGC |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s04 «sabe de telas» |

**Prompt**

```
Vertical UGC photo of a stylish 35-year-old woman with a sleek low bun in a boutique closely inspecting the inside seam of a lilac blouse between her fingers, focused skeptical expression, warm boutique light, shallow depth of field, face in the upper third. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

### A04 · La blusa que nadie quiso con -50 %

| Campo | Valor |
|---|---|
| Archivo | `A04.png` |
| Tipo | Foto |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s01, s05 «¡Ah, saldos!» |

**Prompt**

```
Photo of a slightly wrinkled dated floral blouse on a clearance rack with a big handwritten red '-50%' cardboard tag, cheap overhead lighting, mismatched leftover clothes around it. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

### A08 · Flat lay de las 5 prendas ganadoras

| Campo | Valor |
|---|---|
| Archivo | `A08.png` |
| Tipo | Foto |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s08 «Más preguntadas», s12 cierre «5 ganadoras» |
| Imagen de referencia | `A01` |

**Prompt**

```
Top-down flat lay of five neatly folded best-selling women's garments on a pale pink linen surface, the lilac silk blouse from the reference image at the center, a cream knit cardigan, wide-leg beige trousers, a black slip skirt and a white shirt, small dried flowers, soft daylight, elegant boutique styling. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

### A09 · Macro de la seda lila y su costura

| Campo | Valor |
|---|---|
| Archivo | `A09.png` |
| Tipo | Foto |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s04 «telas», s07 segunda toma |
| Imagen de referencia | `A01` |

**Prompt**

```
Extreme macro photo of the lilac silk from the reference blouse: the fine weave, a neat French seam and the soft sheen of light on the fabric, shallow depth of field, warm side light. shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, real-world imperfections in the fabric, e-commerce boutique photography, not CGI
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch
```

## Prompts de ilustraciones, pinturas y texturas

### A07 · Etiquetas de talla con la M sellada «AGOTADA»

| Campo | Valor |
|---|---|
| Archivo | `A07.png` |
| Tipo | Ilustración |
| Formato | 4:5 · 1536×1920 |
| Dónde sale | s08 «Agotadas en M» |

**Prompt**

```
Flat editorial illustration of a row of clothing size tags XS S M L XL hanging from strings on a rough lilac paper background, the 'M' tag stamped diagonally with a violet (#7B2FF0) rubber stamp reading 'AGOTADA', visible paper fibers, slightly misregistered ink, soft shadows, minimal.
```

**Negativo**

```
photorealistic, 3D, gradients, glossy, drop shadows, people, logos, watermark, misspelled text, extra letters
```

### A10 · Papel rugoso con tinte lila

| Campo | Valor |
|---|---|
| Archivo | `A10.png` |
| Tipo | Textura |
| Formato | 1:1 · 1920×1920 |
| Dónde sale | fondos, collages y marcos de fotos |

**Prompt**

```
Seamless rough watercolor paper texture with a very subtle lilac tint (#F8F5FB), visible fibers and grain, flat even scan, tileable.
```

**Negativo**

```
text, objects, strong colors, vignette
```

## Prompts de video b-roll y movimiento

### A05 · Boutique que muestra solo sus 5 ganadoras

| Campo | Valor |
|---|---|
| Archivo | `A05.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s07 «hacen lo contrario» |
| Duración | 5 s |
| Imagen de referencia | `A01` |
| Movimiento | Push-in lento 8 %; la mano entra a los 2 s. Genera primero el fotograma y luego image-to-video. |

**Prompt**

```
Vertical video, slow push-in on an elegant small women's boutique table and rail showing only five best-selling pieces, the lilac silk blouse from the reference image as the hero in the center, a saleswoman's hand straightens the bow, soft warm light, violet (#7B2FF0) and pink accents in the decor. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

### A06 · Clienta ve 100 ofertas en el celular

| Campo | Valor |
|---|---|
| Archivo | `A06.mp4` |
| Tipo | Video |
| Formato | 9:16 · 1080×1920 |
| Dónde sale | s03 «cien ofertas» |
| Duración | 5 s |
| Movimiento | Primer plano del pulgar → tilt up a su cara iluminada por la pantalla. |

**Prompt**

```
Vertical close-up video of a woman's thumb scrolling very fast through a phone feed full of red and yellow sale banners and discount posts, screen glow on her face in a dark bedroom at night, she looks tired. shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles
```

**Negativo**

```
CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch, morphing fabric, flickering, face distortion, sudden camera jumps, slow motion, text overlays
```

## Entrega

Mete todos los archivos en un zip llamado **`v3.zip`**, sin carpetas dentro, con estos nombres exactos:

| Archivo | Qué es | Formato |
|---|---|---|
| `A01.png` | Blusa ganadora (referencia de consistencia) | 4:5 |
| `A02.png` | Caja con blusas que no se vendieron desde septiembre | 4:5 |
| `A03.png` | Clienta exigente revisando costuras | 9:16 |
| `A04.png` | La blusa que nadie quiso con -50 % | 4:5 |
| `A05.mp4` | Boutique que muestra solo sus 5 ganadoras | 9:16 |
| `A06.mp4` | Clienta ve 100 ofertas en el celular | 9:16 |
| `A07.png` | Etiquetas de talla con la M sellada «AGOTADA» | 4:5 |
| `A08.png` | Flat lay de las 5 prendas ganadoras | 4:5 |
| `A09.png` | Macro de la seda lila y su costura | 4:5 |
| `A10.png` | Papel rugoso con tinte lila | 1:1 |

Al recibirlo ejecuto `assetpack.py v3 --ingest v3.zip`: valida que estén todos, recorta al formato, aplica el grado de marca y monta la vista previa con los elementos integrados, el diseño sonoro y la música para tu aprobación antes de renderizar.
