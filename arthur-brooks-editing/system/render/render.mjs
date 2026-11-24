// node render.mjs props.json out.mp4 [--draft] [--still=SEG]
import { bundle } from "@remotion/bundler";
import { renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const [propsFile, out, ...flags] = process.argv.slice(2);
const draft = flags.includes("--draft");
const still = flags.find((f) => f.startsWith("--still="));
const inputProps = JSON.parse(fs.readFileSync(propsFile, "utf8"));

const CANDIDATES = [
  process.env.VES_CHROME,
  "/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell",
].filter(Boolean);
const browserExecutable = CANDIDATES.find((p) => fs.existsSync(p)) ?? null;

const serveUrl = await bundle({ entryPoint: path.join(here, "src/index.ts"), publicDir: path.join(here, "public") });
const composition = await selectComposition({ serveUrl, id: "Edit", inputProps, browserExecutable });

if (still) {
  // --still=t1,t2,...  → out es una plantilla con {t} (un solo bundle para todos los fotogramas)
  const ts = still.split("=")[1].split(",").map(parseFloat);
  for (const sec of ts) {
    const o = ts.length > 1 || out.includes("{t}") ? out.replace("{t}", sec.toFixed(2).padStart(6, "0")) : out;
    await renderStill({ composition, serveUrl, output: o, inputProps, frame: Math.min(composition.durationInFrames - 1, Math.round(sec * composition.fps)), browserExecutable });
  }
} else {
  let last = -1;
  await renderMedia({
    composition, serveUrl, codec: "h264", outputLocation: out, inputProps, browserExecutable,
    crf: draft ? 28 : 16, scale: draft ? 0.5 : 1, concurrency: Math.max(1, (await import("node:os")).cpus().length - 1),
    onProgress: ({ progress }) => { const p = Math.floor(progress * 20); if (p !== last) { last = p; process.stdout.write(`\r[render] ${Math.round(progress * 100)}%`); } },
  });
  process.stdout.write("\n");
}
fs.rmSync(serveUrl, { recursive: true, force: true }); // no dejar bundles de 600 MB en /tmp
console.log(`[render] ✓ ${out}`);
