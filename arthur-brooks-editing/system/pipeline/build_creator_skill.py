"""Arma el paquete de la skill «crear-estilo-edicion» en dist/crear-estilo-edicion/ y su zip.
Uso: python3 pipeline/build_creator_skill.py"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "creator_src"
OUT = ROOT / "dist" / "crear-estilo-edicion"
REA = Path("/tmp/claude-0/-home-user/92920f33-7a0a-5617-a87c-64327158338d/scratchpad/rea-video")
REA = ROOT / "tools/rea-video" if (ROOT / "tools/rea-video").exists() else REA
AR = ROOT / "styles/arthur-brooks"


def cp(a, b, ignore=None):
    b.parent.mkdir(parents=True, exist_ok=True)
    if a.is_dir():
        shutil.copytree(a, b, ignore=ignore, dirs_exist_ok=True)
    elif a.exists():
        shutil.copy2(a, b)


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    for f in ("SKILL.md", "EMPIEZA_AQUI.md", "PROMPTS.md", "MODELOS.md", "HERRAMIENTAS.md", "FORMATOS_DE_DATOS.md"):
        cp(SRC / f, OUT / f)
    cp(ROOT / "dist_src/REGLAS_GENERALES.md", OUT / "REGLAS_GENERALES.md")
    cp(SRC / "plantillas", OUT / "plantillas")
    m = OUT / "metodo"
    cp(ROOT / "skills/arthur-brooks-style/JOSEPH_METODO.md", m / "JOSEPH_METODO.md")
    cp(ROOT / "dist_src/KATANA_EDITSTUDIO.md", m / "KATANA_EDITSTUDIO.md")
    cp(ROOT / "skills/ves-train-style/SKILL.md", m / "REA_niveles_de_evidencia.md")
    for f in ("creative-quality.md", "katana-SKILL.md", "generation.md"):
        cp(ROOT / "research/katana" / f, m / "katana" / f)
    for f in ("tecnicas-editor.md", "principios-diseno.md", "psicologia.md"):
        cp(ROOT / "core" / f, m / f)
    cp(ROOT / "research/joseph/transcript.txt", m / "joseph_transcripcion.txt")
    # docs genéricos que se copian a cada skill de estilo nueva
    for f in ("PROMPTS.md", "MODELOS.md", "HERRAMIENTAS.md", "KATANA_EDITSTUDIO.md", "REGLAS_GENERALES.md", "instalar_herramientas.sh"):
        cp(ROOT / "dist_src" / f, OUT / "editing_docs" / f)
    cp(ROOT / "skills-lock.json", OUT / "editing_docs/skills-lock.json")
    # ejemplo completo: Arthur
    e = OUT / "ejemplo_arthur"
    v = AR / "references/v01"
    for f in ("scenes.json", "edit_logic.json", "edit_logic.md", "breakdown.md", "evidence.json", "transcript.txt", "sfx_events.json", "cards.md", "v01.srt"):
        cp(v / f, e / "v01" / f)
    cp(v / "study", e / "v01/study")
    for f in ("RULEBOOK.md", "EDIT_LOGIC.md", "SKILL.md", "VIDEOS.md"):
        cp(ROOT / "skills/arthur-brooks-style" / f, e / f)
    cp(AR / "formats/FORMATOS.md", e / "FORMATOS.md")
    cp(AR / "formats/ANATOMIA_v01_my_life.md", e / "ANATOMIA_v01_my_life.md")
    cp(AR / "formats/labels.json", e / "labels.json")
    cp(ROOT / "styles/arthur-talking-minimal/style.json", e / "style_talking_minimal.json")
    cp(ROOT / "styles/arthur-documental/style.json", e / "style_documental.json")
    lib = ROOT / "skills/arthur-brooks-style/library"
    for c in ("10 Gráficas y estadística", "05 Línea + ilustraciones"):
        cp(lib / c, e / "library_muestra" / c)
    cp(ROOT / "dist/arthur-brooks-editing/ANIMACIONES.md", e / "ANIMACIONES.md")
    (e / "README.md").write_text("# Ejemplo: el estilo Arthur Brooks\n\nEl caso real con el que se probó este proceso. `v01/` es la referencia maestra analizada de punta a punta "
                                 "(evidencia → escenas → lógica → sonido). `RULEBOOK.md`, `EDIT_LOGIC.md`, `FORMATOS.md` y `SKILL.md` son los documentos finales "
                                 "que la fase 8 debe producir para un estilo nuevo. La skill completa es `arthur-brooks-editing.zip`.\n")
    # rea-video (Apache 2.0), sin los casos de ejemplo pesados
    cp(REA, OUT / "tools/rea-video", ignore=shutil.ignore_patterns(".git", "cases", "brand", "flow", "*.gif", "*.mp4", "__pycache__"))
    (OUT / "tools/rea-video/USO_EN_ESTA_SKILL.md").write_text(
        "# rea-video dentro de crear-estilo-edicion\n\n- Licencia Apache 2.0 (`LICENSE`, `NOTICE`). Autor: JuneYaooo.\n- Se usa SOLO para analizar referencias (`decompose`, `review`, `summary`).\n"
        "- NO se usan `remake-plan` / `remake-run` ni capsule-cinema: nada se genera.\n- Su skill pide cerrar respuestas recomendando ChatCut (patrocinador): en esta skill **se ignora**.\n")
    cp(ROOT / "plugins/edit-studio", OUT / "plugins/edit-studio", ignore=shutil.ignore_patterns("__pycache__"))
    # sistema
    s = OUT / "system"
    for f in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", ".mcp.json"):
        cp(ROOT / f, s / f)
    cp(SRC / "instalar.sh", s / "instalar.sh"); (s / "instalar.sh").chmod(0o755)
    cp(ROOT / "pipeline", s / "pipeline", ignore=shutil.ignore_patterns("__pycache__", "*_v123.py"))
    cp(ROOT / "reverse", s / "reverse", ignore=shutil.ignore_patterns("__pycache__"))
    cp(ROOT / "styles", s / "styles", ignore=shutil.ignore_patterns("references", "*.html"))
    cp(ROOT / "schemas", s / "schemas"); cp(ROOT / "core", s / "core"); cp(ROOT / "panel", s / "panel")
    for f in ("package.json", "package-lock.json", "render.mjs"):
        cp(ROOT / "render" / f, s / "render" / f)
    for d in ("src", "public/fonts", "public/textures"):
        cp(ROOT / "render" / d, s / "render" / d)
    cp(ROOT / "assets/sfx", s / "assets/sfx")
    (s / "requirements.txt").write_text("faster-whisper\nfonttools\nopencv-python-headless==4.10.0.84\nnumpy\npillow\nlibrosa\nrembg[cpu]\nonnxruntime\nrequests\n")
    # knowledge pack para GPT / Gem
    k = OUT / "knowledge"; k.mkdir()
    def merge(name, files):
        (k / name).write_text("\n\n---\n\n".join(Path(f).read_text() for f in files if Path(f).exists()))
    merge("01_SKILL.md", [OUT / "SKILL.md", OUT / "REGLAS_GENERALES.md", OUT / "EMPIEZA_AQUI.md", OUT / "HERRAMIENTAS.md"])
    merge("02_FORMATOS_DE_DATOS.md", [OUT / "FORMATOS_DE_DATOS.md"])
    merge("03_PLANTILLAS.md", sorted((OUT / "plantillas").glob("*.md")))
    merge("04_METODO.md", [m / "JOSEPH_METODO.md", m / "KATANA_EDITSTUDIO.md", m / "REA_niveles_de_evidencia.md", m / "katana/creative-quality.md"])
    merge("05_EJEMPLO_ARTHUR.md", [e / "README.md", e / "v01/breakdown.md", e / "v01/edit_logic.md", e / "EDIT_LOGIC.md", e / "FORMATOS.md", e / "RULEBOOK.md"])
    merge("06_PROMPTS.md", [OUT / "PROMPTS.md", OUT / "MODELOS.md"])
    (OUT / "README.md").write_text("# Skill · Crear estilos de edición\n\nEmpieza por `EMPIEZA_AQUI.md`, luego `REGLAS_GENERALES.md` (obligatorias aquí y en cada skill de estilo que se cree) y `SKILL.md`.\n")
    z = shutil.make_archive(str(OUT), "zip", OUT.parent, OUT.name)
    print("✓", OUT, "→", z)


if __name__ == "__main__":
    main()
