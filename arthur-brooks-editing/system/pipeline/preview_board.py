#!/usr/bin/env python3
"""Vista previa del video COMPLETO en UNA imagen (para aprobar antes del render): cada tramo en orden
(escenas + A-roll con su caption), con tiempo, tipo y lo que se dice; cabecera con estilo y paleta."""
import json, subprocess, sys, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline")); import ves
name = sys.argv[1]; p = ROOT / "projects" / name
meta = json.loads((p / "project.json").read_text()); plan = json.loads((p / "edit_plan.json").read_text())
style = ves.load_style(plan["style"]); dur = meta["cut_probe"]["duration"]
words = json.loads((p / "transcript_cut.json").read_text())["words"]
scenes = sorted([s for s in plan["scenes"] if s["type"] != "aroll"], key=lambda s: s["start"])
segs, t = [], 0.0
for s in scenes:
    if s["start"] - t > 0.6: segs.append({"type": "A-roll", "start": t, "end": s["start"]})
    segs.append(s); t = max(t, s["end"])
if dur - t > 0.6: segs.append({"type": "A-roll", "start": t, "end": dur})
times = [round(min(s["end"] - 0.15, s["start"] + max(0.7, 0.6 * (s["end"] - s["start"]))), 2) for s in segs]
ves.cmd_render(argparse.Namespace(name=name, at=",".join(map(str, times)), force=True, draft=False))
F = lambda n: ImageFont.truetype(str(ROOT / "render/public/fonts/Anton.ttf"), n)
TW, TH, cols = 240, 427, 8
rows = (len(segs) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (TW + 12) + 12, 150 + rows * (TH + 120)), "#0d0d10")
d = ImageDraw.Draw(sheet)
d.text((14, 14), f"{name.upper()} · {style['name']}", font=F(40), fill="#fff")
pal = plan.get("palette") or json.loads((p / "palette.json").read_text())["colors"]
for i, k in enumerate(["vibrant_bright", "vibrant_dark", "dull_white", "dull_black"]):
    d.rectangle([14 + i * 130, 76, 134 + i * 130, 126], fill=pal[k]); d.text((18 + i * 130, 128), pal[k], font=F(14), fill="#aaa")
d.text((560, 86), f"{dur:.1f} s · {len(segs)} tramos · {sum(1 for s in segs if s['type']!='A-roll')} escenas", font=F(26), fill="#bbb")
for i, (s, tt) in enumerate(zip(segs, times)):
    x, y = 12 + (i % cols) * (TW + 12), 150 + (i // cols) * (TH + 120)
    im = Image.open(p / "out" / f"still_{tt:06.2f}.png").convert("RGB").resize((TW, TH)); sheet.paste(im, (x, y))
    said = " ".join(w["w"] for w in words if s["start"] <= w["start"] < s["end"])
    col = "#7fe3b8" if s["type"] == "A-roll" else pal["vibrant_bright"]
    d.text((x, y + TH + 4), f"{s['start']:.1f}–{s['end']:.1f}s · {s['type']}", font=F(17), fill=col)
    line, out = "", []
    for w in said.split():
        if len(line) + len(w) > 30: out.append(line); line = ""
        line += w + " "
    out.append(line)
    d.text((x, y + TH + 28), "\n".join(out[:4]), font=F(14), fill="#ccc", spacing=2)
o = p / "out" / f"PREVIEW_{name}.jpg"; sheet.save(o, quality=88); print("[preview]", o.relative_to(ROOT))
