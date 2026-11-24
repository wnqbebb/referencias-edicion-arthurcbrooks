#!/usr/bin/env python3
"""B-roll de stock por API oficial (Pexels y Pixabay: licencia libre, uso comercial, sin atribución obligatoria).
Requiere PEXELS_API_KEY y/o PIXABAY_API_KEY (gratis). Vertical primero; descarga a projects/<p>/media/stock/.
  python pipeline/stock_api.py <proyecto> <photos|videos> "<consulta en inglés>" [n]
Luego el render les aplica el MISMO grado de marca del video (BrandGrade = LUT del estilo)."""
import json, os, sys, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
name, kind, q = sys.argv[1], sys.argv[2], sys.argv[3]; n = int(sys.argv[4]) if len(sys.argv) > 4 else 6
out = ROOT / "projects" / name / "media" / "stock"; out.mkdir(parents=True, exist_ok=True)
led_f = out / "LEDGER.json"; led = json.loads(led_f.read_text()) if led_f.exists() else {}
slug = "-".join(q.lower().split())[:40]
def get(url, headers=None):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ves-editor/1.0", **(headers or {})}), timeout=60).read()
got = 0
if os.environ.get("PEXELS_API_KEY"):
    h = {"Authorization": os.environ["PEXELS_API_KEY"]}
    base = "https://api.pexels.com/videos/search?" if kind == "videos" else "https://api.pexels.com/v1/search?"
    d = json.loads(get(base + urllib.parse.urlencode({"query": q, "orientation": "portrait", "per_page": n}), h))
    for i, it in enumerate(d.get("videos" if kind == "videos" else "photos", [])):
        if kind == "videos":
            fs = sorted([f for f in it["video_files"] if f.get("height", 0) >= 1280], key=lambda f: f["height"]) or it["video_files"]
            url, ext = fs[0]["link"], "mp4"
        else:
            url, ext = it["src"]["large2x"], "jpg"
        f = out / f"pexels_{slug}_{i}.{ext}"; f.write_bytes(get(url)); got += 1
        led[f.name] = {"source": it.get("url"), "author": (it.get("user") or {}).get("name") or it.get("photographer"), "license": "Pexels License"}
if os.environ.get("PIXABAY_API_KEY"):
    base = "https://pixabay.com/api/videos/?" if kind == "videos" else "https://pixabay.com/api/?"
    d = json.loads(get(base + urllib.parse.urlencode({"key": os.environ["PIXABAY_API_KEY"], "q": q, "per_page": max(3, n), "orientation": "vertical", "safesearch": "true"})))
    for i, it in enumerate(d.get("hits", [])[:n]):
        url, ext = (it["videos"]["large"]["url"] or it["videos"]["medium"]["url"], "mp4") if kind == "videos" else (it["largeImageURL"], "jpg")
        f = out / f"pixabay_{slug}_{i}.{ext}"; f.write_bytes(get(url)); got += 1
        led[f.name] = {"source": it.get("pageURL"), "author": it.get("user"), "license": "Pixabay Content License"}
if not (os.environ.get("PEXELS_API_KEY") or os.environ.get("PIXABAY_API_KEY")):
    sys.exit("[stock] falta PEXELS_API_KEY / PIXABAY_API_KEY (gratis en pexels.com/api y pixabay.com/api/docs)")
led_f.write_text(json.dumps(led, ensure_ascii=False, indent=1)); print(f"[stock] {got} archivos → {out.relative_to(ROOT)}")
