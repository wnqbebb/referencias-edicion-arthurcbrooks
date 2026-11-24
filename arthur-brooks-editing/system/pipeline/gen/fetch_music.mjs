// Descarga efectos de sonido reales de Mixkit (Mixkit Stock Music Free License: uso comercial sin atribución)
// node fetch_sfx.mjs <outdir> cat1 cat2 ...   (cat = slug de mixkit.co/free-sound-effects/<cat>/)
import { createRequire } from "node:module"; const { chromium } = createRequire(import.meta.url)("playwright");
import fs from "node:fs";
const [out, ...cats] = process.argv.slice(2);
const b = await chromium.launch(); const pg = await b.newPage();
const ledger = {};
for (const cat of cats) {
  await pg.goto(`https://mixkit.co/free-stock-music/${cat}/`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await pg.waitForTimeout(2500);
  const items = await pg.$$eval("[data-audio-player-preview-url-value]", (els) => els.map((e) => {
    const card = e.closest(".item-grid-card") || e.parentElement?.parentElement;
    return { url: e.getAttribute("data-audio-player-preview-url-value"), title: (card?.querySelector("h2,.item-grid-card__title")?.textContent || "").trim() };
  }));
  fs.mkdirSync(`${out}/${cat}`, { recursive: true });
  let k = 0;
  for (const it of items.slice(0, 5)) {
    const r = await fetch(it.url); if (!r.ok) continue;
    const f = `${out}/${cat}/${String(k).padStart(2, "0")}.mp3`; fs.writeFileSync(f, Buffer.from(await r.arrayBuffer()));
    ledger[f.replace(out + "/", "")] = { title: it.title, source: it.url, license: "Mixkit Stock Music Free License" }; k++;
  }
  console.log(cat, k);
}
fs.writeFileSync(`${out}/LEDGER.json`, JSON.stringify(ledger, null, 1));
await b.close();
