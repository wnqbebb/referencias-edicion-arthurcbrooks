#!/usr/bin/env python3
"""Paquete de ASSETS por video: todo lo que el editor necesita (fotos, video b-roll, gráficos, texturas, íconos)
con PROMPTS optimizados en el estilo/branding del video, aspect ratio exacto (o el soportado más cercano),
cadena de consistencia (referencias) y alternativa de stock (Pexels/Pixabay) con el mismo grado de color.

  python pipeline/assetpack.py <proyecto>            → projects/<p>/ASSETS_<p>.md + assets_manifest.json
  python pipeline/assetpack.py <proyecto> --ingest X.zip  → valida, normaliza (crop al AR) y copia a media/assets/

El plan (edit_plan.json) declara "assets": [{id, name, kind, ar, use_in, subject, prompt, negative, refs, stock}].
"""
import json, re, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
SUPPORTED = {"9:16": 9 / 16, "2:3": 2 / 3, "3:4": 3 / 4, "4:5": 4 / 5, "1:1": 1.0, "5:4": 1.25, "4:3": 4 / 3, "3:2": 1.5, "16:9": 16 / 9, "21:9": 21 / 9}
RES = {"9:16": "1080x1920", "2:3": "1280x1920", "3:4": "1440x1920", "4:5": "1536x1920", "1:1": "1920x1920", "5:4": "1920x1536", "4:3": "1920x1440", "3:2": "1920x1280", "16:9": "1920x1080", "21:9": "2520x1080"}
KIND = {"location": "Lugar vacío (plate, sin personas)", "photo": "Foto", "video": "Video b-roll", "graphic": "Gráfico / ilustración", "texture": "Textura", "icon": "Ícono", "ui": "UI / mockup", "product": "Producto (hero de referencia)", "model": "Modelo UGC"}
REALISM = ("shot on iPhone 15 Pro, natural window light, true-to-life skin texture with pores and fine hair, slight handheld imperfection, "
           "authentic UGC look, candid moment, no retouching, realistic fabric weave and wrinkles")
PRODUCT_REAL = ("shot on a full-frame camera with a 50mm lens, true-to-life fabric texture, accurate color, subtle natural shadows, "
                "real-world imperfections in the fabric, e-commerce boutique photography, not CGI")
NEG = ("CGI, 3D render, plastic skin, airbrushed, doll face, over-saturated, HDR halo, extra fingers, deformed hands, warped text, "
       "watermark, logo, brand names, cartoonish, uncanny eyes, perfect symmetry, studio glamour retouch")


def closest_ar(ar: str) -> str:
    if ar in SUPPORTED: return ar
    w, h = [float(x) for x in re.split(r"[:x/]", ar)]
    return min(SUPPORTED, key=lambda k: abs(SUPPORTED[k] - w / h))


def brand_block(style, pal):
    c = pal["colors"]
    return (f"Paleta de marca (60/30/10): primario {c['dull_white']} · secundario {c['dull_black']} · acento {c['vibrant_bright']} · acento oscuro {c['vibrant_dark']}. "
            f"Tipografías: {style['fonts']['sans']['family']} + {style['fonts']['special']['family']} {style['fonts']['special'].get('style','')}. "
            f"Textura: {style.get('texture',{}).get('kind','none')}. Look: contraste {style.get('broll_grade',{}).get('contrast',1)}, saturación {style.get('broll_grade',{}).get('saturate',1)}, tinte del acento oscuro.")


# ── Estructura de prompts de Katana (Higgsfield): cada referencia tiene UNA función, y bloqueos finales explícitos ──
OWNS = {"product": "diseño, proporciones, material, color y detalles EXACTOS de la prenda/producto",
        "model": "identidad (cara, pelo, piel, complexión) y la ropa que lleva",
        "location": "arquitectura, materiales y puntos de referencia del lugar (sin personas)",
        "photo": "composición y estilo de la toma", "graphic": "estilo gráfico", "texture": "textura"}


def katana_blocks(a, by_id):
    """devuelve (líneas markdown, frase EN de bloqueo para añadir al prompt)"""
    refs = a.get("refs", [])
    md, locks_en = [], []
    if refs:
        md.append("- **Qué controla cada referencia (adjúntalas en este orden):** " + " · ".join(
            f"`@image{i+1}` = {r} → {OWNS.get(by_id.get(r, {}).get('kind', 'photo'), 'referencia')}" for i, r in enumerate(refs)))
    prod = [i for i, r in enumerate(refs) if by_id.get(r, {}).get("kind") == "product"]
    who = [i for i, r in enumerate(refs) if by_id.get(r, {}).get("kind") == "model"]
    if prod:
        locks_en.append(f"wears/shows exactly the garment from @image{prod[0]+1} in every shot, same color, cut and details")
    if who:
        locks_en.append(f"same person as @image{who[0]+1}, same face, hair and outfit")
    if a["kind"] == "location":
        locks_en.append("empty location plate, no people, no hands, no text")
    elif a["kind"] not in ("graphic", "texture"):
        locks_en.append("no text, no logos, no watermarks in the image")
    bl = ["identidad y ropa del hero bloqueadas" if (prod or who) else None,
          "una sola acción clara por toma" if a["kind"] == "video" else None,
          "cámara: un solo movimiento con dosis y límite" if a["kind"] == "video" else None]
    bl = [x for x in bl if x]
    if bl:
        md.append("- **Bloqueos (Katana):** " + " · ".join(bl))
    if a["kind"] == "video":
        md.append("- **Duración a generar:** el doble de lo que sale en pantalla (mín. 4 s): así se elige el mejor tramo sin manos raras, saltos de cara ni texto parásito.")
    return md, ("; ".join(locks_en) + ".") if locks_en else ""


def build(name):
    p = ROOT / "projects" / name
    plan = json.loads((p / "edit_plan.json").read_text())
    meta = json.loads((p / "project.json").read_text())
    style = json.loads((ROOT / "styles" / plan.get("style", meta["style"]) / "style.json").read_text())
    pal = json.loads((p / "palette.json").read_text())
    acc = pal["colors"]["vibrant_bright"]
    assets = plan.get("assets", [])
    man, md = [], [f"# ASSETS · {name}\n",
        f"Estilo: **{style['name']}** · Formato del video: 9:16 (1080×1920).",
        f"\n**Branding:** {brand_block(style, pal)}\n",
        "## Cómo entregarlo",
        f"1. Genera (o descarga) cada asset **en el orden de la lista**: los marcados con *referencia* se usan como imagen de referencia de los siguientes (consistencia de producto, modelo y estilo).",
        f"2. Nombra cada archivo exactamente como dice **Archivo** (la extensión puede ser .png/.jpg/.webp o .mp4/.mov).",
        f"3. Mete todo en un zip llamado **`{name}.zip`** y pásamelo. Yo lo valido, recorto al aspect ratio y aplico el grado de color del video.\n",
        "| # | Archivo | Tipo | AR | Escena | Referencias |", "|---|---|---|---|---|---|"]
    for a in assets:
        ar = closest_ar(a.get("ar", "9:16"))
        fn = f"{a['id']}_{a['name']}"
        refs = a.get("refs", [])
        md.append(f"| {a['id']} | `{fn}` | {KIND.get(a['kind'], a['kind'])} | {ar} | {', '.join(a.get('use_in', []))} | {', '.join(refs) or '—'} |")
    md.append("")
    for a in assets:
        ar = closest_ar(a.get("ar", "9:16")); fn = f"{a['id']}_{a['name']}"
        realism = PRODUCT_REAL if a["kind"] == "product" else (REALISM if a["kind"] in ("photo", "model", "video") else "")
        prompt = a["prompt"].replace("{ACCENT}", acc).replace("{ACCENT_DARK}", pal["colors"]["vibrant_dark"]).replace("{REALISM}", realism)
        neg = a.get("negative", NEG if realism else "photorealistic photo, people, faces, text, watermark, clutter, gradients banding")
        kb, lock_en = katana_blocks(a, {x["id"]: x for x in assets})
        if lock_en and lock_en.lower() not in prompt.lower():
            prompt = prompt.rstrip(" .") + ". " + lock_en[0].upper() + lock_en[1:]
        md += [f"## {a['id']} · {a.get('subject', a['name'])}",
               f"- **Archivo:** `{fn}.{ 'mp4' if a['kind']=='video' else 'png'}` · **Tipo:** {KIND.get(a['kind'], a['kind'])} · **Aspect ratio:** {ar} ({RES[ar]})"
               + (f" · pedido {a['ar']} → más cercano soportado {ar}" if a.get('ar', ar) != ar else ""),
               f"- **Se usa en:** {', '.join(a.get('use_in', []))} · **Duración:** {a.get('duration', '5 s') if a['kind']=='video' else '—'}",
               f"- **Referencias de consistencia:** {', '.join(a.get('refs', [])) or 'ninguna (este asset ES referencia)' if a.get('is_ref') else ', '.join(a.get('refs', [])) or '—'}",
               f"- **Prompt (EN):**\n\n```\n{prompt}\n```",
               f"- **Negative prompt:** `{neg}`"] + kb
        if a.get("motion"): md.append(f"- **Movimiento de cámara / animación (video):** {a['motion']}")
        if a.get("stock"): md.append(f"- **Alternativa stock (Pexels/Pixabay):** buscar `{a['stock']}` → yo le aplico el mismo grado/LUT del video.")
        if a.get("note"): md.append(f"- **Nota para el editor:** {a['note']}")
        md.append("")
        man.append({**a, "ar": ar, "resolution": RES[ar], "file": fn, "prompt": prompt, "negative": neg})
    (p / f"ASSETS_{name}.md").write_text("\n".join(md))
    (p / "assets_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1))
    print(f"[assets] {len(assets)} assets → projects/{name}/ASSETS_{name}.md")


def ingest(name, zpath):
    p = ROOT / "projects" / name; man = json.loads((p / "assets_manifest.json").read_text())
    dst = p / "media" / "assets"; dst.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp()); zipfile.ZipFile(zpath).extractall(tmp)
    files = {f.name.split("_")[0]: f for f in tmp.rglob("*") if f.is_file() and not f.name.startswith(".")}
    missing = []
    for a in man:
        f = files.get(a["id"])
        if not f: missing.append(a["id"]); continue
        W, H = [int(x) for x in a["resolution"].split("x")]
        out = dst / (a["id"] + (".mp4" if a["kind"] == "video" else ".png"))
        vf = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(f), "-vf", vf] + (["-an", "-c:v", "libx264", "-crf", "18"] if a["kind"] == "video" else []) + [str(out)], check=True)
        print(f"  ✓ {a['id']} → {out.relative_to(ROOT)}")
    shutil.rmtree(tmp)
    print("[assets] faltan:", missing or "nada ✓")


if __name__ == "__main__":
    if "--ingest" in sys.argv: ingest(sys.argv[1], sys.argv[sys.argv.index("--ingest") + 1])
    else: build(sys.argv[1])
