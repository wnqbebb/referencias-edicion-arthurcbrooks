"""Plan por beats (método Joseph) para CUALQUIER proyecto.
  python3 pipeline/beats.py apply <p> [--picks plan.json]   → aplica la opción elegida de cada beat a edit_plan.json
  python3 pipeline/beats.py panel <p1> [<p2> ...] --out DIR   → genera el panel (index.html + panel_data.json + clips)
beats.json (lo escribe el modelo en el STOP 1):
  {"title": "...", "beats": [{"id":"b01","start":0.0,"end":4.7,"script":"...","seen":"patrón de Arthur",
     "pick":"A","opts":[{"title","cats","desc","ref":"V10-A02","type":"j_graph|aroll|null|...","props":{...},
                          "start"?,"end"?,"enter"?,"exit"?,"then"?}, x3]}]}
El texto que copia el panel («Copiar plan») es {"picks":{"<p>":{"b01":"B"}},"notes":{...}} → --picks."""
import base64, io, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# la biblioteca está en skills/… (repositorio) o en ../library (paquete de la skill descomprimido)
_LIBS = [ROOT / "skills/arthur-brooks-style/library", ROOT.parent / "library"]
LIBDIR = next((d for d in _LIBS if (d / "ANIMATIONS.json").exists()), _LIBS[0])
LIB = LIBDIR / "ANIMATIONS.json"


def sheet_path(rel):
    """ruta de la hoja de keyframes sea cual sea la ubicación de la biblioteca"""
    rel = str(rel).replace("skills/arthur-brooks-style/library/", "")
    return LIBDIR / rel


def scenes_from(beats, picks):
    out = []
    for b in beats:
        k = picks.get(b["id"], b.get("pick", "A"))
        opt = b["opts"]["ABC".index(k)]
        if not opt.get("type"):
            continue
        s = {"id": f"{b['id']}{k.lower()}", "type": opt["type"], "start": opt.get("start", b["start"]), "end": opt.get("end", b["end"]), "props": opt.get("props", {})}
        if opt.get("enter"): s["in"] = opt["enter"]
        if opt.get("exit"): s["out"] = opt["exit"]
        out.append(s)
        if opt.get("then"):
            out.append({"id": f"{b['id']}{k.lower()}2", **opt["then"]})
    return out


def apply(p, picks_all):
    pr = ROOT / "projects" / p
    bj = json.loads((pr / "beats.json").read_text())
    plan = json.loads((pr / "edit_plan.json").read_text())
    plan["scenes"] = scenes_from(bj["beats"], picks_all.get("picks", picks_all).get(p, {}))
    plan.setdefault("notes", {}).update(picks_all.get("notes", {}).get(p, {}))
    (pr / "edit_plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(f"[beats] {p}: {len(plan['scenes'])} escenas aplicadas")


def panel(projects, out):
    from PIL import Image
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    A = {a["aid"]: a for a in json.loads(LIB.read_text())}
    data, refs = {}, set()
    for p in projects:
        pr = ROOT / "projects" / p
        bj = json.loads((pr / "beats.json").read_text())
        for b in bj["beats"]:
            for o in b["opts"]:
                refs.add(o["ref"]); o.pop("props", None); o.pop("then", None)
        data[p] = {"title": bj["title"], "beats": bj["beats"]}
        meta = json.loads((pr / "project.json").read_text())
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(pr / meta.get("cut", meta["raw"])), "-vf", "scale=360:-2", "-c:v", "libx264", "-crf", "30",
                        "-preset", "veryfast", "-c:a", "aac", "-b:a", "64k", "-movflags", "+faststart", str(out / f"{p}.mp4")], check=True)
    thumbs = {}
    for r in refs:
        a = A.get(r)
        if not a or not sheet_path(a["sheet"]).exists():
            continue
        s = Image.open(sheet_path(a["sheet"])).convert("RGB"); W, H = s.size
        fr = s.crop((int(W * 2 / 5), 0, int(W * 3 / 5), H)); fr.thumbnail((180, 320))
        bio = io.BytesIO(); fr.save(bio, "WEBP", quality=62)
        thumbs[r] = "data:image/webp;base64," + base64.b64encode(bio.getvalue()).decode()
    (out / "panel_data.json").write_text(json.dumps({"videos": data, "thumbs": thumbs}, ensure_ascii=False))
    tpl = ROOT / "panel" / "index.html"
    shutil.copy(tpl if tpl.exists() else ROOT.parent / "panel" / "index.html", out / "index.html")
    print(f"[beats] panel → {out}/index.html (publícalo como página o ábrelo con un servidor local: python3 -m http.server)")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "apply":
        raw = Path(sys.argv[sys.argv.index("--picks") + 1]).read_text() if "--picks" in sys.argv else "{}"
        picks = json.loads(raw[raw.index("{"):])
        apply(sys.argv[2], picks)
    elif cmd == "panel":
        o = sys.argv[sys.argv.index("--out") + 1]
        panel([x for x in sys.argv[2:sys.argv.index("--out")]], o)
