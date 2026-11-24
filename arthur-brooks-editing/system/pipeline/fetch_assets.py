#!/usr/bin/env python3
"""Busca imágenes con licencia libre (Openverse: CC0, PDM, CC-BY, CC-BY-SA) y las descarga como candidatas.
uso: fetch_assets.py <proyecto> "<slug>=<búsqueda en inglés>" ... [--n 6]
Guarda media/cand/<slug>_<k>.jpg y apunta autor/licencia/URL en credits.json (obligatorio para CC-BY)."""
import json, subprocess, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
proj = ROOT / "projects" / sys.argv[1]; cand = proj / "media" / "cand"; cand.mkdir(parents=True, exist_ok=True)
n = 6
args = [a for a in sys.argv[2:]]
if "--n" in args:
    i = args.index("--n"); n = int(args[i + 1]); del args[i:i + 2]
cf = proj / "credits.json"; credits = json.loads(cf.read_text()) if cf.exists() else {}
for spec in args:
    slug, q = spec.split("=", 1)
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm,by,by-sa", "page_size": n * 2, "size": "large"})
    import time
    res = []
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ves-editor/1.0"})
            res = json.loads(urllib.request.urlopen(req, timeout=30).read())["results"]; break
        except urllib.error.HTTPError as e:
            print("  openverse", e.code, "reintento en", 15 * (attempt + 1), "s"); time.sleep(15 * (attempt + 1))
    time.sleep(4)
    k = 0
    for r in res:
        if k >= n: break
        out = cand / f"{slug}_{k}.jpg"
        try:
            raw = urllib.request.urlopen(urllib.request.Request(r["url"], headers={"User-Agent": "ves-editor/1.0"}), timeout=30).read()
        except Exception as e:
            continue
        tmp = cand / "_tmp"; tmp.write_bytes(raw)
        ok = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp), "-vf", "scale='min(1600,iw)':-2", "-q:v", "3", str(out)]).returncode == 0
        tmp.unlink(missing_ok=True)
        if not ok: continue
        credits[out.name] = {"title": r.get("title"), "creator": r.get("creator"), "license": r.get("license"), "license_version": r.get("license_version"), "source": r.get("foreign_landing_url")}
        k += 1
    print(slug, k, "imágenes")
cf.write_text(json.dumps(credits, ensure_ascii=False, indent=1))
