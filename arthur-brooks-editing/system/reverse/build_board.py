#!/usr/bin/env python3
"""Genera los elementos del tablero (pizarra) a partir de ALL_SCENES.json + blobs.json {scene_id: url}.
Salida: un directorio con eN.json + meta.json + lotes de escrituras (batch_XX.json) para ArtifactData."""
import os
import json, math, sys
from pathlib import Path
from build_library import CAT_NAMES
ROOT = Path(__file__).resolve().parent.parent
STYLE = os.environ.get("VES_STYLE", "arthur-brooks")   # estilo que se está entrenando
REFS = ROOT / "refs" / os.environ.get("VES_REFS", "arthur")  # carpeta con los videos de referencia vNN.mp4
sc = json.loads((ROOT / "styles" / STYLE / "references/ALL_SCENES.json").read_text())
blobs = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
for f in out.glob("*.json"): f.unlink()
picked = [s for s in sc if s["id"] in blobs and s.get("category") != "aroll_plain"]
E = []
def add(d):
    E.append(d); return f"e{len(E)}"
def h_text(txt, wrap, px=14):
    per = max(1, int(wrap / (px * 0.5)))
    return sum(math.ceil(max(1, len(l)) / per) for l in txt.split("\n")) * px * 1.5 + 8
add({"type": "text", "x": 0, "y": -230, "text": "Arthur Brooks — Tablero de inspiración (20 videos)", "size": "title"})
add({"type": "text", "x": 0, "y": -160, "text": f"{len(picked)} escenas top, ordenadas en los principios del estilo.", "size": "large"})
# ── Full inspiration board
cols, pw, ph = 12, 100, 176
rows = math.ceil(len(picked) / cols)
add({"type": "container", "x": 0, "y": 0, "w": 24 + cols * pw + 14, "h": 24 + rows * ph + 10, "color": "white", "text": "Tablero completo de inspiración"})
order = sorted(picked, key=lambda s: (s["video"], s["start"]))
for i, s in enumerate(order):
    add({"type": "image", "x": 24 + (i % cols) * pw, "y": 24 + (i // cols) * ph, "w": 90, "h": 160, "src": blobs[s["id"]]})
# ── categorías
cats = [c for c in CAT_NAMES if any(s["category"] == c for s in picked)]
colx = [1400, 2560]; coly = [0, 0]
for ci, c in enumerate(cats):
    items = sorted([s for s in picked if s["category"] == c], key=lambda s: -(s.get("quality") or 0))
    top = items[0]
    grid = items[:12]
    gh = math.ceil(len(grid) / 4) * 158
    notes = [("¿Por qué este *diseño*?", top.get("design", "")), ("¿Por qué estos *efectos*?", top.get("effects", "")),
             ("¿Por qué esta *animación*?", top.get("animation", "")), ("¿Por qué *aquí*?", top.get("why", ""))]
    th = sum(h_text(f"**{a}**\n{b}", 300) + 14 for a, b in notes)
    H = 24 + max(gh, 372, th) + 24
    k = 0 if coly[0] <= coly[1] else 1
    X, Y = colx[k], coly[k]
    add({"type": "container", "x": X, "y": Y, "w": 1100, "h": H, "color": "white", "text": f"{CAT_NAMES[c]} · {sum(1 for s in picked if s['category']==c)} escenas"})
    for i, s in enumerate(grid):
        add({"type": "image", "x": X + 24 + (i % 4) * 92, "y": Y + 24 + (i // 4) * 158, "w": 82, "h": 146, "src": blobs[s["id"]]})
    add({"type": "image", "x": X + 410, "y": Y + 24, "w": 200, "h": 356, "src": blobs.get(top["id"] + "_L", blobs[top["id"]])})
    add({"type": "text", "x": X + 410, "y": Y + 388, "wrap": 200, "size": "small", "color": "blue", "text": f"{top['id']} · {top['start']:.1f}s\n“{(top.get('script') or '')[:70]}”"})
    ty = Y + 24
    for a, b in notes:
        t = f"**{a}**\n{b}"
        add({"type": "text", "x": X + 640, "y": ty, "wrap": 430, "size": "small", "text": t})
        ty += h_text(t, 430) + 14
    coly[k] = Y + max(H, ty - Y + 24, 430) + 90
ids = [f"e{i+1}" for i in range(len(E))]
for i, d in enumerate(E):
    (out / f"e{i+1}.json").write_text(json.dumps(d, ensure_ascii=False))
(out / "meta.json").write_text(json.dumps({"v": 1, "title": "Tablero de inspiración Arthur Brooks", "order": ids}, ensure_ascii=False))
w = [{"op": "set", "collection": "board", "doc_id": "meta", "file_path": str(out / "meta.json")}] + \
    [{"op": "set", "collection": "elements", "doc_id": x, "file_path": str(out / f"{x}.json")} for x in ids]
for b in range(0, len(w), 50):
    (out / f"batch_{b // 50:02d}.json").write_text(json.dumps(w[b:b + 50]))
print(len(E), "elementos,", math.ceil(len(w) / 50), "lotes; alto col:", coly)
