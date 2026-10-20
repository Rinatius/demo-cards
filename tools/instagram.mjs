// Render a topic's cards as 1080x1350 Instagram carousel slides (PNG).
// Usage: NODE_PATH=$(npm root -g) node tools/instagram.mjs cards/<topic>/cards.json <out-dir> ["Cover title"]
import { createRequire } from 'node:module';
import { readFileSync, mkdirSync } from 'node:fs';
import { resolve, dirname, extname } from 'node:path';
// require() honours NODE_PATH, so a globally installed Playwright works too.
const { chromium } = createRequire(import.meta.url)('playwright');

const [input, outDir, coverTitle = 'Starshield explained'] = process.argv.slice(2);
if (!input || !outDir) { console.error('usage: instagram.mjs <cards.json> <out-dir> [cover title]'); process.exit(1); }
const cards = JSON.parse(readFileSync(input, 'utf8'));
mkdirSync(outDir, { recursive: true });

const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
// Optional photo: card.image may be a URL/path string or { url | src, credit }.
const photo = c => {
  const img = typeof c.image === 'string' ? { url: c.image } : c.image && { ...c.image, url: c.image.url ?? c.image.src };
  if (!img?.url) return null;
  // setContent pages can't read file:// URLs, so local photos are inlined.
  const url = /^https?:|^data:/.test(img.url) ? img.url
    : `data:image/${extname(img.url).slice(1).replace('jpg', 'jpeg').replace('svg', 'svg+xml')};base64,${readFileSync(resolve(dirname(input), img.url)).toString('base64')}`;
  return { url, credit: img.credit };
};
const total = cards.length + 1;

const css = `
  * { box-sizing: border-box; margin: 0; }
  body { width: 1080px; height: 1350px; background: #161615; color: #ecebe6;
    font-family: Inter, system-ui, sans-serif; display: flex; flex-direction: column; overflow: hidden; }
  .pad { padding: 72px 80px; display: flex; flex-direction: column; gap: 36px; flex: 1; }
  .photo { flex: none; height: 560px; background: center/cover no-repeat; position: relative; }
  .credit { position: absolute; right: 16px; bottom: 12px; font-size: 20px; color: #fff; text-shadow: 0 1px 4px #000; }
  .top { display: flex; justify-content: space-between; align-items: center; font-size: 26px; color: #a09e97; }
  .cat { text-transform: uppercase; letter-spacing: .08em; font-weight: 700; color: #7fb0e0; }
  .main { margin: auto 0; display: flex; flex-direction: column; gap: 40px; }
  h1 { font-size: 76px; line-height: 1.12; font-weight: 800; letter-spacing: -.01em; }
  .photo + .pad h1 { font-size: 56px; }
  p { font-size: 40px; line-height: 1.42; color: #d6d4cd; }
  .photo + .pad p { font-size: 31px; }
  .foot { margin-top: auto; display: flex; justify-content: space-between; align-items: flex-end; gap: 24px;
    font-size: 24px; color: #a09e97; border-top: 2px solid #34332f; padding-top: 28px; }
  .tag { color: #e0a64a; font-style: italic; font-weight: 600; white-space: nowrap; }
  .cover { justify-content: center; }
  .cover h1 { font-size: 112px; }
  .cover .cat { font-size: 30px; }
  .cover p { font-size: 40px; color: #a09e97; }
  .swipe { font-size: 34px; color: #7fb0e0; font-weight: 700; }`;

const page = (inner) => `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${inner}</body></html>`;

const cover = page(`<div class="pad cover">
  <div class="cat">News cards</div>
  <h1>${esc(coverTitle)}</h1>
  <p>${cards.length} key facts, each with its source.</p>
  <div class="swipe">Swipe →</div></div>`);

const slide = (c, i) => {
  const ph = photo(c);
  return page(`${ph ? `<div class="photo" style="background-image:url('${esc(ph.url)}')">${ph.credit ? `<span class="credit">${esc(ph.credit)}</span>` : ''}</div>` : ''}
  <div class="pad">
    <div class="top"><span class="cat">${esc(c.category)}</span><span>${i + 2}/${total}</span></div>
    <div class="main"><h1>${esc(c.headline)}</h1>
    <p>${esc(c.body)}</p></div>
    <div class="foot"><span>Source: ${esc(c.source?.name)} · ${esc(c.date)}</span>${c.confidence === 'reported' ? '<span class="tag">Reported</span>' : ''}</div>
  </div>`);
};

const browser = await chromium.launch();
const tab = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
const slides = [cover, ...cards.map(slide)];
for (const [i, html] of slides.entries()) {
  await tab.setContent(html, { waitUntil: 'networkidle' });
  const name = `${String(i + 1).padStart(2, '0')}-${i ? cards[i - 1].id : 'cover'}.png`;
  await tab.screenshot({ path: resolve(outDir, name) });
  // Warn if text overflows the slide.
  if (await tab.evaluate(() => document.body.scrollHeight > 1350)) console.warn(`overflow: ${name}`);
  console.log(name);
}
await browser.close();
