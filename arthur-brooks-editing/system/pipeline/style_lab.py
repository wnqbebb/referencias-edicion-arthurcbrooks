"""Laboratorio de estilos: crea un estilo de edición nuevo a partir de 10–20 videos de referencia de un creador,
con el mismo proceso que produjo la skill de Arthur Brooks (Joseph + REA + Katana + rea-video).

  python3 pipeline/style_lab.py nuevo <estilo> --refs CARPETA_CON_VIDEOS    → crea el espacio y numera v01…vNN
  python3 pipeline/style_lab.py preparar <estilo> [--rea]                   → planos, palabras, hojas de estudio (+ rea-video)
  python3 pipeline/style_lab.py briefs <estilo>                             → instrucciones para que el modelo analice
  python3 pipeline/style_lab.py sonido <estilo>                             → voz/música/efectos separados y eventos de SFX
  python3 pipeline/style_lab.py energia <estilo>                            → mapa de energía por video (Katana)
  python3 pipeline/style_lab.py biblioteca <estilo>                         → biblioteca de animaciones con ID VNN-ANN
  python3 pipeline/style_lab.py estado <estilo>                             → qué falta por video
  python3 pipeline/style_lab.py empaquetar <estilo> [--titulo "…"]          → dist/<estilo>-editing.zip (la skill del estilo)
"""
import argparse, collections, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TPL = next((d for d in (ROOT / "creator_src" / "plantillas", ROOT.parent / "plantillas") if d.exists()), ROOT / "creator_src" / "plantillas")
VID_EXT = (".mp4", ".mov", ".m4v", ".webm", ".mkv")
CATS = ["captions_text", "broll_text", "imagery_characters", "line_text", "line_illustration", "text_centric", "center_illustration",
        "side_illustration", "object_element", "graph_stats", "ui_screen", "timeline", "split_layout", "aroll_plain", "title_cta"]


def env(estilo):
    return {**os.environ, "VES_STYLE": estilo, "VES_REFS": estilo}


def refdir(estilo):
    return ROOT / "styles" / estilo / "references"


def videos(estilo):
    return sorted((ROOT / "refs" / estilo).glob("v*.mp4"))


def run(cmd, estilo, **kw):
    print("  $", " ".join(str(c) for c in cmd))
    return subprocess.run([str(c) for c in cmd], env=env(estilo), cwd=ROOT, **kw)


def nuevo(a):
    src = Path(a.refs).expanduser()
    vids = sorted(p for p in src.iterdir() if p.suffix.lower() in VID_EXT)
    if not vids:
        sys.exit(f"[lab] no hay videos en {src}")
    dst = ROOT / "refs" / a.estilo; dst.mkdir(parents=True, exist_ok=True)
    mapa = {}
    for i, v in enumerate(vids, 1):
        out = dst / f"v{i:02d}.mp4"
        if v.suffix.lower() == ".mp4":
            shutil.copy2(v, out)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-c:v", "libx264", "-crf", "18", "-c:a", "aac", str(out)], check=True)
        mapa[out.stem] = v.name
    s = ROOT / "styles" / a.estilo
    for d in ("references", "formats", "skill"):
        (s / d).mkdir(parents=True, exist_ok=True)
    (s / "formats" / "labels.json").write_text(json.dumps({k: "?" for k in mapa}, indent=1))
    (s / "refs_map.json").write_text(json.dumps(mapa, ensure_ascii=False, indent=1))
    (s / "task-contract.json").write_text(json.dumps({"estilo": a.estilo, "creador": a.creador or "?", "explicit_locks": [], "creative_freedoms": [],
                                                      "references": [f"refs/{a.estilo}/{k}.mp4" for k in mapa]}, ensure_ascii=False, indent=1))
    print(f"[lab] {len(vids)} videos → refs/{a.estilo}/v01…v{len(vids):02d}.mp4 · espacio styles/{a.estilo}/")
    print("      Siguiente: python3 pipeline/style_lab.py preparar", a.estilo)


def preparar(a):
    vs = videos(a.estilo)
    for v in vs:
        run(["python3", "reverse/breakdown.py", v, "--style-id", a.estilo, "--transcribe"], a.estilo, check=True)
    run(["python3", "reverse/sheets.py"], a.estilo, check=True)
    if a.rea:
        if shutil.which("rea-video") is None:
            print("[lab] rea-video no está instalado: pip install git+https://github.com/JuneYaooo/rea-video  (sigo sin él)")
        else:
            for v in vs:   # rea-video escribe en inglés o chino: usamos inglés y el modelo traduce al analizar
                run(["rea-video", "decompose", v, "-o", refdir(a.estilo) / v.stem / "rea", "--lang", "en"], a.estilo)
    ok_rea = [v.stem for v in vs if (refdir(a.estilo) / v.stem / "rea" / "VIDEO.md").exists()]
    print(f"[lab] {len(vs)} videos preparados (evidence.json, shots/, study/, .srt)"
          + (f" · rea-video OK en {len(ok_rea)}/{len(vs)}: {ok_rea}" if a.rea else "") + ".")
    if a.rea and len(ok_rea) < len(vs):
        print("      ⚠ rea-video falló en algunos videos: el análisis sigue con evidence.json y las hojas de estudio.")
    print("      Siguiente: python3 pipeline/style_lab.py briefs", a.estilo)


def briefs(a):
    r = refdir(a.estilo)
    for name in ("BRIEF_ANALISIS.md", "BRIEF_LOGICA.md"):
        t = (TPL / name).read_text().replace("{ESTILO}", a.estilo).replace("{REFS}", f"refs/{a.estilo}").replace("{ROOT}", str(ROOT))
        (r / name).write_text(t)
    print(f"[lab] briefs → styles/{a.estilo}/references/BRIEF_ANALISIS.md y BRIEF_LOGICA.md")
    print("      El modelo los sigue video por video (o con subagentes en paralelo, 4–5 videos cada uno).")


def sonido(a):
    run(["python3", "reverse/audio_sfx.py"] + [v.stem for v in videos(a.estilo)], a.estilo, check=True)


def energia(a):
    tot = collections.Counter(); dur_tot = 0.0
    for d in sorted(refdir(a.estilo).glob("v??")):
        el, sc = d / "edit_logic.json", d / "scenes.json"
        if not el.exists() or not sc.exists():
            print(f"  · {d.name}: falta edit_logic.json o scenes.json"); continue
        L, S = json.loads(el.read_text()), json.loads(sc.read_text())
        dur = max((s["end"] for s in S), default=1.0)
        c = collections.Counter()
        for t in L.get("transitions", []):
            c["corte_seco" if "seco" in t.get("type", "") else "transicion"] += 1
        c["texto"] = len(L.get("text_fx", [])); c["camara"] = len(L.get("camera", [])); c["disparadores"] = len(L.get("triggers", []))
        c["escenas"] = len(S)
        en = {"duracion_s": round(dur, 2), "por_segundo": {k: round(v / dur, 3) for k, v in c.items()}, "conteo": dict(c),
              "tipos_transicion": dict(collections.Counter(t.get("type", "?") for t in L.get("transitions", [])))}
        (d / "energy.json").write_text(json.dumps(en, ensure_ascii=False, indent=1))
        tot.update(c); dur_tot += dur
        print(f"  ✓ {d.name}: {en['por_segundo']}")
    if dur_tot:
        res = {k: round(v / dur_tot, 3) for k, v in tot.items()}
        (refdir(a.estilo) / "ENERGY_SUMMARY.json").write_text(json.dumps({"por_segundo_media": res, "duracion_total_s": round(dur_tot, 1)}, indent=1))
        print("[lab] energía media por segundo:", res)


def biblioteca(a):
    sc = []
    for d in sorted(refdir(a.estilo).glob("v??")):
        if (d / "scenes.json").exists():
            for s in json.loads((d / "scenes.json").read_text()):
                s.setdefault("video", d.name); sc.append(s)
    if not sc:
        sys.exit("[lab] no hay scenes.json: primero el análisis con BRIEF_ANALISIS.md")
    run(["python3", "reverse/build_library.py"], a.estilo, check=True)
    lib = ROOT / "skills" / f"{a.estilo}-style" / "library"
    jp = {p.stem: str(p.relative_to(ROOT)) for p in lib.glob("*/*.jpg")}
    out, cnt = [], collections.Counter()
    for s in sc:
        if s.get("category") in ("captions_text", "aroll_plain"):
            continue
        v = int(s["id"][1:3]); cnt[v] += 1
        out.append({"aid": f"V{v:02d}-A{cnt[v]:02d}", "scene": s["id"], "category": s.get("category"), "start": s["start"], "end": s["end"],
                    "dur": round(s["end"] - s["start"], 2), **{k: s.get(k, "") for k in ("script", "what", "design", "effects", "animation", "why")},
                    "quality": s.get("quality"), "sheet": jp.get(s["id"], "")})
    (lib / "ANIMATIONS.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"[lab] {len(sc)} escenas · {len(out)} animaciones con ID → {lib.relative_to(ROOT)}/ANIMATIONS.json")
    print("      por categoría:", dict(collections.Counter(o["category"] for o in out).most_common()))


def estado(a):
    need = ["evidence.json", "study", "scenes.json", "breakdown.md", "edit_logic.json", "edit_logic.md", "energy.json", "sfx_events.json"]
    print(f"{'video':6} " + " ".join(f"{n[:10]:>10}" for n in need))
    for d in sorted(refdir(a.estilo).glob("v??")):
        print(f"{d.name:6} " + " ".join(f"{'✓' if (d / n).exists() else '·':>10}" for n in need))
    s = ROOT / "styles" / a.estilo / "skill"
    for f in ("SKILL.md", "RULEBOOK.md", "EDIT_LOGIC.md", "FORMATOS.md"):
        print(f"skill/{f:14} {'✓' if (s / f).exists() else '· (lo escribe el modelo con plantillas/' + f + ')'}")
    print(f"biblioteca    {'✓' if (ROOT / 'skills' / f'{a.estilo}-style' / 'library' / 'ANIMATIONS.json').exists() else '·'}")
    print(f"style.json    {'✓' if (ROOT / 'styles' / a.estilo / 'style.json').exists() else '· (plantillas/style.json)'}")


def empaquetar(a):
    """Arma la skill del estilo con la misma estructura que la de Arthur."""
    st = ROOT / "styles" / a.estilo
    sk = st / "skill"
    miss = [f for f in ("SKILL.md", "RULEBOOK.md", "EDIT_LOGIC.md") if not (sk / f).exists()]
    if miss:
        sys.exit(f"[lab] faltan documentos del estilo en styles/{a.estilo}/skill/: {miss} (escríbelos con creator_src/plantillas/)")
    name = f"{a.estilo}-editing"
    out = ROOT / "dist" / name
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    def cp(x, y, **kw):
        y.parent.mkdir(parents=True, exist_ok=True)
        (shutil.copytree(x, y, dirs_exist_ok=True, **kw) if x.is_dir() else shutil.copy2(x, y)) if x.exists() else None
    for f in sk.iterdir():
        cp(f, out / "SKILL.md" if f.name == "SKILL.md" else out / "docs" / f.name)
    jm = next((p for p in (ROOT / "skills/arthur-brooks-style/JOSEPH_METODO.md", ROOT.parent / "metodo/JOSEPH_METODO.md") if p.exists()), None)
    if jm: cp(jm, out / "docs/JOSEPH_METODO.md")
    for f in ("tecnicas-editor.md", "principios-diseno.md", "psicologia.md"):
        cp(ROOT / "core" / f, out / "docs" / f)
    gen = next((d for d in (ROOT / "dist_src", ROOT.parent / "editing_docs") if d.exists()), ROOT / "dist_src")
    for f in ("PROMPTS.md", "MODELOS.md", "HERRAMIENTAS.md"):
        cp(gen / f, out / f)
    cp(gen / "KATANA_EDITSTUDIO.md", out / "docs/KATANA_EDITSTUDIO.md")
    lib = ROOT / "skills" / f"{a.estilo}-style" / "library"
    cp(lib, out / "library")
    keep = ("scenes.json", "edit_logic.json", "edit_logic.md", "breakdown.md", "transcript.txt", "sfx_events.json", "energy.json", "evidence.json")
    for v in sorted(refdir(a.estilo).glob("v??")):
        for f in keep:
            cp(v / f, out / "references" / v.name / f)
        for s in v.glob("*.srt"):
            cp(s, out / "references" / v.name / s.name)
        cp(v / "study", out / "references" / v.name / "study")
        cp(v / "rea" / "VIDEO.md", out / "references" / v.name / "VIDEO.md")
    cp(refdir(a.estilo) / "ENERGY_SUMMARY.json", out / "references/ENERGY_SUMMARY.json")
    # tabla de animaciones
    A = json.loads((lib / "ANIMATIONS.json").read_text()) if (lib / "ANIMATIONS.json").exists() else []
    L = [f"# Biblioteca de animaciones · {a.titulo or a.estilo} ({len(A)})", "", "| Ref | Categoría | Dur. | Guion | Qué se ve | Animación | Hoja |", "|---|---|---|---|---|---|---|"]
    for x in A:
        c = lambda s: str(s).replace("|", "/").replace("\n", " ")[:140]
        L.append(f"| {x['aid']} | {x['category']} | {x['dur']} s | {c(x['script'])} | {c(x['what'])} | {c(x['animation'])} | `{Path(x['sheet']).name if x['sheet'] else ''}` |")
    (out / "ANIMACIONES.md").write_text("\n".join(L) + "\n")
    # sistema (render) + estilo
    s = out / "system"
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".mcp.json"):
        cp(ROOT / f, s / f)
    cp(ROOT / "pipeline", s / "pipeline", ignore=shutil.ignore_patterns("__pycache__", "*_v123.py"))
    cp(ROOT / "reverse", s / "reverse", ignore=shutil.ignore_patterns("__pycache__"))
    cp(ROOT / "styles", s / "styles", ignore=shutil.ignore_patterns("references", "*.html", "refs_map.json"))
    cp(ROOT / "schemas", s / "schemas"); cp(ROOT / "core", s / "core"); cp(ROOT / "panel", s / "panel")
    for f in ("package.json", "package-lock.json", "render.mjs"):
        cp(ROOT / "render" / f, s / "render" / f)
    for d in ("src", "public/fonts", "public/textures"):
        cp(ROOT / "render" / d, s / "render" / d)
    cp(ROOT / "assets/sfx", s / "assets/sfx")
    (s / "requirements.txt").write_text("faster-whisper\nfonttools\nopencv-python-headless==4.10.0.84\nnumpy\npillow\nlibrosa\nrembg[cpu]\nonnxruntime\nrequests\n")
    (out / "README.md").write_text(f"# Skill de edición · {a.titulo or a.estilo}\n\nEmpieza por `SKILL.md`. Instalación en cada modelo: `MODELOS.md`. Prompts: `PROMPTS.md`.\n"
                                   f"Creada con la skill «crear-estilo-edicion» a partir de {len(list(refdir(a.estilo).glob('v??')))} videos de referencia.\n")
    # ── SIEMPRE incluido en cada skill de estilo: reglas generales, plugin Edit Studio (Higgsfield), método Katana,
    #    instalador de herramientas y knowledge para GPT/Gem ─────────────────────────────────────────────────────
    first = lambda *ps: next((p for p in ps if p.exists()), ps[0])
    reglas = first(ROOT / "dist_src/REGLAS_GENERALES.md", ROOT.parent / "REGLAS_GENERALES.md", gen / "REGLAS_GENERALES.md")
    cp(reglas, out / "REGLAS_GENERALES.md")
    plug = first(ROOT / "plugins/edit-studio", ROOT.parent / "plugins/edit-studio")
    cp(plug, out / "plugins/edit-studio", ignore=shutil.ignore_patterns("__pycache__"))
    kat = first(ROOT / "research/katana", ROOT.parent / "metodo/katana")
    for kf in ("creative-quality.md", "generation.md", "katana-SKILL.md"):
        cp(kat / kf, out / "docs/katana" / kf)
    cp(first(ROOT / "dist_src/instalar_herramientas.sh", gen / "instalar_herramientas.sh"), s / "instalar_herramientas.sh")
    if (s / "instalar_herramientas.sh").exists():
        (s / "instalar_herramientas.sh").chmod(0o755)
    cp(first(ROOT / "skills-lock.json", gen / "skills-lock.json"), s / "skills-lock.json")
    falta = [x for x in ("REGLAS_GENERALES.md", "plugins/edit-studio/skills/edit-director/SKILL.md", "docs/katana/katana-SKILL.md") if not (out / x).exists()]
    if falta:
        sys.exit(f"[lab] ⛔ no se puede empaquetar sin lo obligatorio: {falta}")
    sk_md = (out / "SKILL.md").read_text()
    if "REGLAS_GENERALES" not in sk_md:   # la skill del estilo siempre remite a las reglas generales
        sk_md = sk_md.replace("\n# ", "\n> **Obligatorio:** `REGLAS_GENERALES.md` + plugin Edit Studio (`plugins/edit-studio/`) + método Katana (`docs/katana/`).\n\n# ", 1)
        (out / "SKILL.md").write_text(sk_md)
    (out / "EMPIEZA_AQUI.md").write_text(
        f"# Empieza aquí · {a.titulo or a.estilo}\n\n1. Lee `REGLAS_GENERALES.md` (obligatorias) y `SKILL.md`.\n"
        "2. Instala: copia la carpeta a `.claude/skills/` y ejecuta `bash system/instalar_herramientas.sh` dentro de `system/` (incluye el plugin Edit Studio).\n"
        "3. ChatGPT / Gemini: sube `knowledge/` a un GPT, Proyecto o Gem con las instrucciones de `MODELOS.md`.\n4. Primer mensaje: el prompt 2 de `PROMPTS.md` con tu video.\n")
    k = out / "knowledge"; k.mkdir(exist_ok=True)
    def merge(name, files):
        (k / name).write_text("\n\n---\n\n".join(p.read_text() for p in files if p.exists()))
    merge("01_SKILL_Y_REGLAS.md", [out / "SKILL.md", out / "REGLAS_GENERALES.md"])
    merge("02_RULEBOOK.md", [out / "docs/RULEBOOK.md"])
    merge("03_LOGICA_Y_FORMATOS.md", [out / "docs/EDIT_LOGIC.md", out / "docs/FORMATOS.md"])
    merge("04_METODO.md", [out / "docs/JOSEPH_METODO.md", out / "docs/KATANA_EDITSTUDIO.md"])
    merge("05_PROMPTS_Y_HERRAMIENTAS.md", [out / "PROMPTS.md", out / "MODELOS.md", out / "HERRAMIENTAS.md"])
    merge("06_ANIMACIONES.md", [out / "ANIMACIONES.md"])
    z = shutil.make_archive(str(out), "zip", out.parent, out.name)
    print(f"[lab] skill del estilo → {z} (con reglas generales, Edit Studio y Katana)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("nuevo"); p.add_argument("estilo"); p.add_argument("--refs", required=True); p.add_argument("--creador", default=None); p.set_defaults(f=nuevo)
    p = sp.add_parser("preparar"); p.add_argument("estilo"); p.add_argument("--rea", action="store_true"); p.set_defaults(f=preparar)
    for n, fn in (("briefs", briefs), ("sonido", sonido), ("energia", energia), ("biblioteca", biblioteca), ("estado", estado)):
        p = sp.add_parser(n); p.add_argument("estilo"); p.set_defaults(f=fn)
    p = sp.add_parser("empaquetar"); p.add_argument("estilo"); p.add_argument("--titulo", default=None); p.set_defaults(f=empaquetar)
    a = ap.parse_args(); a.f(a)
