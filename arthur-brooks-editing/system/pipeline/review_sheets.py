#!/usr/bin/env python3
"""Hojas de aprobación previas al render:
  palette <p> [--presets rosa,morado]  → out/palette_sheet.jpg (3–5 opciones: del footage + por público)
  music <p> [--folders tag/piano,mood/inspiring] → out/music_preview_N.mp3 (20 s con la voz encima y ducking)
  pick-music <p> N / pick-palette <p> N"""
import colorsys, json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
import ves  # noqa

FONT = str(next((ROOT / "render/public/fonts").glob("Anton.ttf")))


def palette_options(p):
    meta = json.loads((p / "project.json").read_text()); vid = p / meta.get("cut", meta["raw"])
    tmp = p / "media" / "_pal"; tmp.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(vid), "-vf", "fps=1/2,scale=160:-1", str(tmp / "f%03d.png")], check=True)
    px = np.concatenate([np.asarray(Image.open(f).convert("RGB")).reshape(-1, 3) for f in sorted(tmp.glob("*.png"))]) / 255.0
    for f in tmp.glob("*"): f.unlink()
    tmp.rmdir()
    hls = np.array([colorsys.rgb_to_hls(*c) for c in px[:: max(1, len(px) // 50000)]])
    m = (hls[:, 2] > 0.30) & (hls[:, 1] > 0.15) & (hls[:, 1] < 0.85)
    h = hls[m]; hist, edges = np.histogram(h[:, 0], bins=24, range=(0, 1), weights=h[:, 2])
    out = []
    for b in np.argsort(hist)[::-1][:3]:
        sel = (h[:, 0] >= edges[b]) & (h[:, 0] < edges[b + 1])
        out.append(("del video", ves.build_palette(float(np.median(h[sel, 0])), float(np.median(h[sel, 2])))))
    return out


def cmd_palette(name, presets):
    p = ROOT / "projects" / name
    opts = palette_options(p)
    cur = json.loads((p / "palette.json").read_text())["colors"]
    opts = [("actual", cur)] + opts
    pp = json.loads((ROOT / "styles/palette_presets.json").read_text())
    for pr in presets:
        r, g, b = [int(pp[pr][i:i + 2], 16) / 255 for i in (1, 3, 5)]; hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
        opts.append((f"preset {pr}", ves.build_palette(hh, ss)))
    meta = json.loads((p / "project.json").read_text()); vid = p / meta.get("cut", meta["raw"])
    frame = p / "media" / "_frame.jpg"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "3", "-i", str(vid), "-frames:v", "1", "-vf", "scale=270:-2", str(frame)], check=True)
    fr = Image.open(frame); frame.unlink()
    W = 300 + 4 * 150 + 420; sheet = Image.new("RGB", (W, len(opts) * 200 + 20), "#111")
    d = ImageDraw.Draw(sheet); f1 = ImageFont.truetype(FONT, 34); f2 = ImageFont.truetype(FONT, 22)
    for i, (lab, c) in enumerate(opts):
        y = 10 + i * 200
        sheet.paste(fr.crop((0, 120, 270, 300)).resize((270, 180)), (10, y))
        for k, key in enumerate(["vibrant_bright", "vibrant_dark", "dull_white", "dull_black"]):
            x = 300 + k * 150; d.rectangle([x, y, x + 140, y + 140], fill=c[key]); d.text((x, y + 148), c[key], font=f2, fill="#ddd")
        x = 300 + 4 * 150; d.rectangle([x, y, x + 400, y + 180], fill=c["dull_black"])
        d.text((x + 20, y + 30), "Texto normal", font=f2, fill=c["dull_white"]); d.text((x + 20, y + 70), "PALABRA CLAVE", font=f1, fill=c["vibrant_bright"])
        d.text((x + 20, y + 130), f"{i}: {lab}", font=f2, fill="#999")
    out = p / "out"; out.mkdir(exist_ok=True); sheet.save(out / "palette_sheet.jpg", quality=90)
    (out / "palette_options.json").write_text(json.dumps([{"label": l, "colors": c} for l, c in opts], indent=1))
    print(f"[review] {len(opts)} paletas → projects/{name}/out/palette_sheet.jpg")


def cmd_music(name, folders):
    p = ROOT / "projects" / name; lib = ROOT / "assets/music_lib"
    if not lib.exists() or not any(lib.rglob("*.mp3")):
        sys.exit("[music] la biblioteca de música está vacía: descárgala una vez con  node pipeline/gen/fetch_music.mjs  (Mixkit, licencia gratuita; no se redistribuye en el paquete)")
    meta = json.loads((p / "project.json").read_text()); vid = p / meta.get("cut", meta["raw"])
    cands = []
    for fo in folders: cands += sorted((lib / fo).glob("*.mp3"))[:3]
    cands = cands[:5]; out = p / "out"; out.mkdir(exist_ok=True)
    ledger = json.loads((lib / "LEDGER.json").read_text()); lst = []
    for i, m in enumerate(cands, 1):
        o = out / f"music_preview_{i}.mp3"
        # la música es el suelo: -24 dB bajo la voz con sidechain (ducking) — regla del editor
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-t", "20", "-i", str(vid), "-stream_loop", "-1", "-i", str(m), "-filter_complex",
                        "[1:a]volume=0.12,afade=t=in:d=0.8[mm];[mm][0:a]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[m];[0:a][m]amix=inputs=2:normalize=0:duration=first,afade=t=out:st=18.5:d=1.5[a]",
                        "-map", "[a]", "-t", "20", "-b:a", "192k", str(o)], check=True)
        key = str(m.relative_to(lib)); lst.append({"n": i, "file": key, "title": ledger.get(key, {}).get("title", "")})
    (out / "music_options.json").write_text(json.dumps(lst, ensure_ascii=False, indent=1))
    for x in lst: print(f"  {x['n']}: {x['file']} · {x['title']}")


def cmd_pick(name, kind, n):
    p = ROOT / "projects" / name; plan = json.loads((p / "edit_plan.json").read_text())
    if kind == "music":
        x = json.loads((p / "out/music_options.json").read_text())[int(n) - 1]
        plan.setdefault("music", {})["file"] = str(ROOT / "assets/music_lib" / x["file"])
    else:
        c = json.loads((p / "out/palette_options.json").read_text())[int(n)]["colors"]
        (p / "palette.json").write_text(json.dumps({"source": "picked", "colors": c, "options": [c]}, indent=1))
    (p / "edit_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1)); print("ok")


if __name__ == "__main__":
    c, name = sys.argv[1], sys.argv[2]
    arg = lambda k: sys.argv[sys.argv.index(k) + 1].split(",") if k in sys.argv else []
    if c == "palette": cmd_palette(name, arg("--presets"))
    elif c == "music": cmd_music(name, arg("--folders") or ["tag/piano", "mood/inspiring"])
    elif c == "pick-music": cmd_pick(name, "music", sys.argv[3])
    elif c == "pick-palette": cmd_pick(name, "palette", sys.argv[3])
