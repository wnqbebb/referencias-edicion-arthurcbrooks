// Busca b-roll en Pexels / Pixabay con navegador real (Playwright). Devuelve candidatos y descarga previews.
// node stock_search.mjs <outdir> <pexels|pixabay> <photos|videos> "<query>" [n]
import { createRequire } from "node:module"; const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "node:fs";
const [out, site, kind, q, nArg] = process.argv.slice(2); const n = +(nArg || 6);
const b = await chromium.launch({ args: ["--disable-blink-features=AutomationControlled"] });
const ctx = await b.newContext({ userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36", viewport: { width: 1400, height: 1000 } });
const pg = await ctx.newPage();
const slug = q.trim().replace(/\s+/g, "-");
const url = site === "pexels" ? `https://www.pexels.com/search/${kind === "videos" ? "videos/" : ""}${encodeURIComponent(q)}/?orientation=portrait`
  : `https://pixabay.com/${kind}/search/${encodeURIComponent(q)}/?orientation=vertical`;
const resp = await pg.goto(url, { waitUntil: "domcontentloaded", timeout: 60000 });
await pg.waitForTimeout(4000);
console.log("status", resp?.status(), await pg.title());
const items = await pg.$$eval(kind === "videos" ? "video source, video" : "img", (els) => els.map((e) => e.getAttribute("src") || e.getAttribute("data-src") || "").filter((s) => s.startsWith("http")));
const uniq = [...new Set(items)].filter((u) => !/avatar|logo|svg|profile|badge/i.test(u)).slice(0, n);
fs.mkdirSync(out, { recursive: true }); const res = [];
for (const [i, u] of uniq.entries()) {
  try { const r = await ctx.request.get(u); if (!r.ok()) continue;
    const ext = kind === "videos" ? "mp4" : "jpg"; const f = `${out}/${site}_${slug}_${i}.${ext}`;
    fs.writeFileSync(f, await r.body()); res.push({ file: f, url: u, page: url, license: site === "pexels" ? "Pexels License" : "Pixabay Content License" });
  } catch {}
}
fs.writeFileSync(`${out}/${site}_${slug}.json`, JSON.stringify(res, null, 1)); console.log(res.length, "descargados");
await b.close();
