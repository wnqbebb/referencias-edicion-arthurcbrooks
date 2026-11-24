"""Arma el paquete entregable de la skill Arthur Brooks (independiente del modelo) en dist/arthur-brooks-editing/
y su zip. Uso: python3 pipeline/build_skill.py"""
import json, shutil, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "dist_src"
OUT = ROOT / "dist" / "arthur-brooks-editing"
SK = ROOT / "skills/arthur-brooks-style"
REF = ROOT / "styles/arthur-brooks/references"
CAT = {"broll_text": "B-roll + texto", "text_centric": "Texto centrado", "center_illustration": "Ilustración central", "imagery_characters": "Imágenes / personajes",
       "split_layout": "Pantalla dividida", "title_cta": "Título / CTA", "line_illustration": "Línea + ilustraciones", "object_element": "Objeto + texto",
       "timeline": "Línea de tiempo", "graph_stats": "Gráficas", "ui_screen": "UI / pantallas", "side_illustration": "Ilustración lateral", "line_text": "Línea + texto"}


def cp(a, b, ignore=None):
    b.parent.mkdir(parents=True, exist_ok=True)
    if a.is_dir():
        shutil.copytree(a, b, ignore=ignore, dirs_exist_ok=True)
    elif a.exists():
        shutil.copy2(a, b)


def md_cell(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def animaciones():
    A = json.loads((SK / "library/ANIMATIONS.json").read_text())
    by = {}
    for a in A:
        by.setdefault(a["category"], []).append(a)
    L = ["# Biblioteca de animaciones de Arthur (339)", "",
         "Cada animación tiene ID `VNN-ANN` (video NN, animación NN), una hoja de 5 keyframes en `library/<categoría>/<escena>.jpg` y su ficha `.md`.",
         "Úsala para recomendar los diseños A/B/C de cada beat (columna «Ref» del panel).", "",
         "| Categoría | Cantidad | Escena del render que la recrea |", "|---|---|---|"]
    rmap = {"broll_text": "j_broll", "text_centric": "j_quote / arthur_text", "center_illustration": "j_illus", "imagery_characters": "paper_collage / archival_photo / j_painting",
            "split_layout": "split_layout", "title_cta": "arthur_text / name_card", "line_illustration": "j_line (img) / j_illus", "object_element": "j_illus keep_color",
            "timeline": "timeline", "graph_stats": "j_graph / arthur_number / arthur_blocks", "ui_screen": "ui_*", "side_illustration": "j_half / j_illus side", "line_text": "j_line"}
    for c, l in sorted(by.items(), key=lambda x: -len(x[1])):
        L.append(f"| {CAT.get(c, c)} | {len(l)} | `{rmap.get(c, '')}` |")
    for c, l in sorted(by.items(), key=lambda x: -len(x[1])):
        L += ["", f"## {CAT.get(c, c)} ({len(l)})", "", "| Ref | Dur. | Guion | Qué se ve | Diseño | Animación | Hoja |", "|---|---|---|---|---|---|---|"]
        for a in l:
            sheet = str(Path(a["sheet"]).relative_to("skills/arthur-brooks-style")) if a["sheet"] else ""
            L.append(f"| {a['aid']} | {a['dur']} s | {md_cell(a['script'][:90])} | {md_cell(a['what'][:160])} | {md_cell(a['design'][:140])} | {md_cell(a['animation'][:140])} | `{sheet}` |")
    return "\n".join(L) + "\n"


def ejemplos():
    L = ["# Ejemplos completos (3 ediciones reales)", "",
         "Tres videos de moda en español, cada uno en un formato distinto de Arthur para que no se vean iguales.",
         "Por cada beat: guion, patrón de Arthur, las 3 opciones (★ = la elegida) y su referencia. Archivos completos en `examples/<p>/`.", ""]
    for p in ("v1", "v2", "v3"):
        pr = ROOT / "projects" / p
        bj = json.loads((pr / "beats.json").read_text())
        pal = json.loads((pr / "palette.json").read_text())["colors"] if (pr / "palette.json").exists() else {}
        plan = json.loads((pr / "edit_plan.json").read_text())
        L += [f"## {bj['title']}", "", f"Estilo `{plan.get('style')}` · paleta: " + " · ".join(f"{k} {v}" for k, v in pal.items() if isinstance(v, str) and v.startswith("#")), "",
              "| Beat | Tiempo | Guion | Visto en los reels | A | B | C |", "|---|---|---|---|---|---|---|"]
        for b in bj["beats"]:
            cells = []
            for j, o in enumerate(b["opts"]):
                star = "★ " if "ABC"[j] == b.get("pick", "A") else ""
                cells.append(f"{star}**{md_cell(o['title'])}** ({md_cell(o['cats'])}) {md_cell(o.get('desc', ''))} · `{o.get('type') or 'A-roll'}` · Ref {o['ref']}")
            L.append(f"| {b['id']} | {b['start']:.2f}–{b['end']:.2f} | {md_cell(b['script'])} | {md_cell(b['seen'])} | " + " | ".join(cells) + " |")
        assets = plan.get("assets", [])
        if assets:
            L += ["", "**Assets del video**", "", "| ID | Qué es | Formato | Referencia |", "|---|---|---|---|"]
            for a in assets:
                L.append(f"| {a['id']} | {md_cell(a.get('subject', ''))} | {a.get('ar', '')} | {', '.join(a.get('refs', [])) or ('hero' if a.get('is_ref') else '—')} |")
        L.append("")
    return "\n".join(L)


def contrato():
    sch = json.loads((ROOT / "schemas/scenes.json").read_text())
    L = ["# Contrato: beats.json → edit_plan.json", "",
         "El modelo NO escribe código de animación durante una edición: rellena estos dos archivos. El render hace el resto.", "",
         "## beats.json (plan por beats, lo lee el panel)", "```json",
         json.dumps({"title": "V1 · Talking head + minimal (vino)", "beats": [{"id": "b07", "start": 16.28, "end": 21.06, "script": "Entonces si bajas el precio…",
                     "seen": "Consecuencia numérica → gráfico oscuro con bola que cae paso a paso (principio 10).", "pick": "A",
                     "opts": [{"title": "Gráfico que cae", "cats": "Gráficas · Cut-away", "desc": "…", "ref": "V19-A14", "type": "j_graph",
                               "props": {"points": [{"x": 0, "y": 0.8, "t": 16.4}, {"x": 0.2, "y": 0.55, "t": 17.34, "label": "bajas el precio"}], "small": "pierdes", "big": "dos veces.", "text_t": 18.66},
                               "enter": "wipe"}, {"title": "…", "type": "arthur_blocks"}, {"title": "Quedarse en el A-roll", "type": None}]}]}, ensure_ascii=False, indent=1),
         "```", "- `type: null` = quedarse en el A-roll. `t` y los `points[].t` son segundos ABSOLUTOS de la palabra (de `transcript_cut.json`).",
         "- `enter`/`exit` = transición (solo las permitidas por el formato; el render elimina las que sobran).", "",
         "## edit_plan.json", "```json",
         json.dumps({"style": "arthur-talking-minimal", "palette": {"vibrant_bright": "#9E1C3A"}, "scenes": [{"id": "b07a", "type": "j_graph", "start": 16.28, "end": 21.06, "props": {}, "in": "wipe"}],
                     "assets": [{"id": "A01", "name": "blusa-hero", "kind": "product", "ar": "4:5", "is_ref": True, "prompt": "…", "negative": "…"}],
                     "captions": {"special_words": ["Black Friday"]}, "music": {"file": "assets/music_lib/…", "volume": 0.16}}, ensure_ascii=False, indent=1),
         "```", "", "## Catálogo de escenas", "", "| Tipo | Capa | Cuándo usarla | Props |", "|---|---|---|---|"]
    for k, v in sch.items():
        if k.startswith("_") or not isinstance(v, dict):
            continue
        L.append(f"| `{k}` | {v.get('layer', '')} | {md_cell(v.get('use_when', ''))} | {md_cell(json.dumps(v.get('props', {}), ensure_ascii=False))[:300]} |")
    return "\n".join(L) + "\n"


def readme():
    n_ref = len([d for d in REF.iterdir() if d.is_dir()])
    return f"""# Skill de edición · Arthur Brooks (método Joseph)

Edita videos verticales en el estilo premium minimal de Arthur Brooks con cualquier modelo (Claude, ChatGPT, Gemini).

**Empieza por `EMPIEZA_AQUI.md`, luego `REGLAS_GENERALES.md` (obligatorias) y `SKILL.md`.** Para instalarla, lee `MODELOS.md`. Para usarla, copia los prompts de `PROMPTS.md`.

| Qué | Dónde |
|---|---|
| Reglas y flujo | `SKILL.md` |
| Método de Joseph (10 principios, entrenamiento, uso) | `docs/JOSEPH_METODO.md` |
| Biblioteca de 339 animaciones con hojas de keyframes | `ANIMACIONES.md`, `library/` |
| {n_ref} videos de referencia desglosados | `references/vNN/` |
| Panel de planificación por beats | `panel/` (abre `panel/demo/index.html` con un servidor local) |
| 3 ediciones de ejemplo completas | `EJEMPLOS.md`, `examples/` |
| Contrato de datos y catálogo de escenas | `CONTRATO.md` |
| Código del sistema (pipeline + render) | `system/` |
| Paquete para GPT / Gem | `knowledge/` |
| Herramientas necesarias (MCP, skills, búsqueda en internet) | `HERRAMIENTAS.md` |
| Crear un estilo nuevo (con rea-video) | `CREAR_ESTILO_NUEVO.md` |
| Katana + Edit Studio (reglas generales, prompts en 7 bloques, plugin) | `KATANA_EDITSTUDIO.md`, `plugins/edit-studio/`, `docs/katana/` |

Panel de ejemplo publicado: https://claude.ai/artifact/RGC9S9Asz46akbjhmvAKeQ
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for f in ("SKILL.md", "PROMPTS.md", "MODELOS.md", "EMPIEZA_AQUI.md", "HERRAMIENTAS.md", "KATANA_EDITSTUDIO.md", "CREAR_ESTILO_NUEVO.md", "REGLAS_GENERALES.md"):
        cp(SRC / f, OUT / f)
    (OUT / "README.md").write_text(readme())
    (OUT / "ANIMACIONES.md").write_text(animaciones())
    (OUT / "EJEMPLOS.md").write_text(ejemplos())
    (OUT / "CONTRATO.md").write_text(contrato())
    d = OUT / "docs"
    for f in ("JOSEPH_METODO.md", "RULEBOOK.md", "EDIT_LOGIC.md", "VIDEOS.md"):
        cp(SK / f, d / f)
    cp(ROOT / "styles/arthur-brooks/formats/FORMATOS.md", d / "FORMATOS.md")
    cp(ROOT / "styles/arthur-brooks/formats/ANATOMIA_v01_my_life.md", d / "ANATOMIA_v01_my_life.md")
    for f in ("tecnicas-editor.md", "principios-diseno.md", "psicologia.md"):
        cp(ROOT / "core" / f, d / f)
    cp(ROOT / "research/joseph/transcript.txt", d / "joseph_transcripcion.txt")
    cp(ROOT / "skills/ves-train-style/SKILL.md", d / "ves-train-style.md")
    for g in ("g0.jpg", "g1.jpg", "g2.jpg", "g3.jpg", "g4.jpg", "g5.jpg", "cap_rule.jpg"):
        cp(ROOT / "research/joseph/key" / g, d / "joseph_fotogramas" / g)
    cp(SK / "library", OUT / "library")
    cp(ROOT / "plugins/edit-studio", OUT / "plugins/edit-studio", ignore=shutil.ignore_patterns("__pycache__"))
    for kf in ("creative-quality.md", "generation.md", "katana-SKILL.md"):
        cp(ROOT / "research/katana" / kf, d / "katana" / kf)
    keep = ("scenes.json", "edit_logic.json", "edit_logic.md", "breakdown.md", "cards.md", "transcript.txt", "sfx_events.json", "evidence.json")
    for v in sorted(REF.iterdir()):
        if not v.is_dir():
            continue
        for f in keep:
            cp(v / f, OUT / "references" / v.name / f)
        for s in v.glob("*.srt"):
            cp(s, OUT / "references" / v.name / s.name)
        cp(v / "study", OUT / "references" / v.name / "study")
    for f in ("ALL_SCENES.json", "BRIEF_ANALISIS.md", "BRIEF_LOGICA.md"):
        cp(REF / f, OUT / "references" / f)
    # panel: plantilla + demo con los 3 ejemplos
    cp(ROOT / "panel/index.html", OUT / "panel/index.html")
    subprocess.run(["python3", str(ROOT / "pipeline/beats.py"), "panel", "v1", "v2", "v3", "--out", str(OUT / "panel/demo")], check=True)
    # ejemplos
    for p in ("v1", "v2", "v3"):
        pr = ROOT / "projects" / p
        for f in ("beats.json", "edit_plan.json", "captions.json", "palette.json", "cue_sheet.json", f"ASSETS_{p}.md", f"PROMPTS_{p}.md", "assets_manifest.json"):
            cp(pr / f, OUT / "examples" / p / f)
        cp(pr / "out" / f"PREVIEW_{p}.jpg", OUT / "examples" / p / f"PREVIEW_{p}.jpg")
    # sistema
    s = OUT / "system"
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".mcp.json", "skills-lock.json"):
        cp(ROOT / f, s / f)
    cp(SRC / "instalar_herramientas.sh", s / "instalar_herramientas.sh")
    (s / "instalar_herramientas.sh").chmod(0o755)
    cp(ROOT / "reverse", s / "reverse", ignore=shutil.ignore_patterns("__pycache__", "*.wav", "*.mp4"))
    cp(ROOT / "pipeline", s / "pipeline", ignore=shutil.ignore_patterns("__pycache__", "assets_v123.py", "beats_v123.py"))
    cp(ROOT / "styles", s / "styles", ignore=shutil.ignore_patterns("references", "*.html"))
    cp(ROOT / "schemas", s / "schemas")
    cp(ROOT / "core", s / "core")
    cp(ROOT / "panel", s / "panel")
    r = s / "render"
    for f in ("package.json", "package-lock.json", "render.mjs", "tsconfig.json", "remotion.config.ts"):
        cp(ROOT / "render" / f, r / f)
    cp(ROOT / "render/src", r / "src")
    cp(ROOT / "render/public/fonts", r / "public/fonts")
    cp(ROOT / "render/public/textures", r / "public/textures")
    cp(ROOT / "assets/sfx", s / "assets/sfx")
    (s / "requirements.txt").write_text("faster-whisper\nfonttools\nopencv-python-headless==4.10.0.84\nnumpy\npillow\nlibrosa\nrembg[cpu]\nonnxruntime\nrequests\n")
    # knowledge pack (GPT / Gem): 9 archivos fusionados
    k = OUT / "knowledge"; k.mkdir()
    def merge(name, files):
        (k / name).write_text("\n\n---\n\n".join(Path(f).read_text() for f in files))
    merge("01_SKILL.md", [OUT / "SKILL.md", OUT / "REGLAS_GENERALES.md"])
    merge("02_METODO_JOSEPH.md", [d / "JOSEPH_METODO.md", OUT / "KATANA_EDITSTUDIO.md"])
    merge("03_LOGICA_EDICION.md", [d / "EDIT_LOGIC.md", d / "VIDEOS.md"])
    merge("04_RULEBOOK.md", [d / "RULEBOOK.md"])
    merge("05_FORMATOS.md", [d / "FORMATOS.md", d / "ANATOMIA_v01_my_life.md"])
    merge("06_TECNICAS_GENERALES.md", [d / "tecnicas-editor.md", d / "principios-diseno.md", d / "psicologia.md"])
    merge("07_CONTRATO.md", [OUT / "CONTRATO.md"])
    merge("08_EJEMPLOS.md", [OUT / "EJEMPLOS.md"])
    merge("09_PROMPTS.md", [OUT / "PROMPTS.md", OUT / "MODELOS.md", OUT / "HERRAMIENTAS.md", OUT / "CREAR_ESTILO_NUEVO.md"])
    z = shutil.make_archive(str(OUT), "zip", OUT.parent, OUT.name)
    print("✓", OUT, "→", z)


if __name__ == "__main__":
    main()
