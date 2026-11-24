#!/usr/bin/env node
/* safe-area.mjs: every visible piece of text (titles, captions) must sit inside the Instagram safe area of a 1080x1920
 * composition: x 60 to 940, y 220 to 1500. Opens the composition in headless Chrome, seeks the GSAP timelines to each
 * sample time and measures the text itself (a Range over its text nodes, not the box around it).
 *
 * `npx hyperframes check` has its own, narrower safe-zone warning (y 288-1248, x 120-888); run it with --safe-zone off
 * and use this script for the real limits (ESTILO.md can change them with the flags below).
 *
 * Usage:
 *   node safe-area.mjs --index videos/<p>/public/index.html [--modo vertical|horizontal] [--step 0.25] [--at 0,1.5,3] [--min-opacity 0.6]
 *                      [--x0 60 --x1 940 --y0 220 --y1 1500] [--tol 1] [--json]
 * Skip an element on purpose (a background texture, a logo watermark) with data-safe-ignore on it or an ancestor.
 * An element counts as seen when its opacity (multiplied up its ancestors) is at least --min-opacity, so a title
 * still sliding in from outside the area is not flagged until it is on screen at full strength.
 * Exit 1 when any text leaves the area.
 */
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

const argv = process.argv.slice(2);
const opt = (name, def) => { const i = argv.indexOf("--" + name); return i < 0 ? def : argv[i + 1]; };
const flag = (name) => argv.includes("--" + name);
const index = opt("index");
if (!index) { console.error("usage: node safe-area.mjs --index <index.html> [--step 0.25] [--at t1,t2]"); process.exit(2); }
// --modo vertical (default): Instagram safe area on 1080x1920. --modo horizontal: 1920x1080, 5% from every edge and the
// bottom 130 px left free for the player controls (progress bar, buttons, YouTube captions).
const modo = opt("modo", "vertical");
const H = modo === "horizontal";
const CW = H ? 1920 : 1080, CH = H ? 1080 : 1920;
const D = H ? { x0: 96, x1: 1824, y0: 54, y1: 950 } : { x0: 60, x1: 940, y0: 220, y1: 1500 };
const box = { x0: +opt("x0", D.x0), x1: +opt("x1", D.x1), y0: +opt("y0", D.y0), y1: +opt("y1", D.y1) };
const tol = +opt("tol", 1), minOpacity = +opt("min-opacity", 0.6), step = +opt("step", 0.25);

const require = createRequire(import.meta.url);
let chromium;
try { ({ chromium } = require("playwright")); } catch { try { ({ chromium } = require("playwright-core")); } catch {
  console.error("playwright not found (it ships with the cloud image; elsewhere: npm i -D playwright)"); process.exit(2); } }

const exe = ["/usr/bin/google-chrome", "/opt/pw-browsers/chromium"].find((p) => { try { return require("node:fs").existsSync(p); } catch { return false; } });
const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"], ...(exe ? { executablePath: exe } : {}) });
const page = await browser.newPage({ viewport: { width: CW, height: CH }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(resolve(index)).href, { waitUntil: "load" });
await page.waitForTimeout(800);

const info = await page.evaluate(() => {
  const root = document.querySelector("[data-composition-id][data-duration]") || document.querySelector("[data-duration]");
  return { duration: root ? parseFloat(root.getAttribute("data-duration")) : 0,
           w: root ? parseFloat(root.getAttribute("data-width") || 0) : 0, h: root ? parseFloat(root.getAttribute("data-height") || 0) : 0 };
});
if (info.w && info.h && (info.w !== CW || info.h !== CH)) {
  console.error(`FAIL the composition is ${info.w}x${info.h}, not ${CW}x${CH} (--modo ${modo})`); await browser.close(); process.exit(1);
}
let times = opt("at") ? opt("at").split(",").map(Number) : [];
if (!times.length) { const d = info.duration || 10; for (let t = 0; t <= d + 1e-6; t += step) times.push(+t.toFixed(3)); }

const seen = new Map();   // "label|side" -> {first,last,n}
let sampled = 0;
for (const t of times) {
  const hits = await page.evaluate(([t, box, tol, minOpacity]) => {
    for (const tl of Object.values(window.__timelines || {})) { try { tl.pause(); tl.seek(t, false); } catch (e) {} }
    const out = [];
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    const byEl = new Map();
    for (let n = walker.nextNode(); n; n = walker.nextNode()) {
      if (!n.textContent.trim()) continue;
      const el = n.parentElement;
      if (!el || ["SCRIPT", "STYLE", "NOSCRIPT", "TITLE"].includes(el.tagName)) continue;
      if (el.closest("[data-safe-ignore]")) continue;
      // outside its own clip window (data-start/data-duration on it or an ancestor) the runtime hides it: skip
      let off = false;
      for (let e = el; e; e = e.parentElement) {
        if (e.hasAttribute && e.hasAttribute("data-start") && e.hasAttribute("data-duration") && !e.hasAttribute("data-composition-id")) {
          const st = parseFloat(e.getAttribute("data-start")), du = parseFloat(e.getAttribute("data-duration"));
          if (t < st - 1e-6 || t >= st + du - 1e-6) { off = true; break; }
        }
      }
      if (off) continue;
      (byEl.get(el) || byEl.set(el, []).get(el)).push(n);
    }
    for (const [el, nodes] of byEl) {
      let op = 1, hidden = false;
      for (let e = el; e && e !== document.documentElement; e = e.parentElement) {
        const cs = getComputedStyle(e);
        if (cs.display === "none" || cs.visibility === "hidden") { hidden = true; break; }
        op *= parseFloat(cs.opacity);
      }
      if (hidden || op < minOpacity) continue;
      let l = 1e9, r = -1e9, tp = 1e9, b = -1e9;
      for (const n of nodes) {
        const rg = document.createRange(); rg.selectNodeContents(n);
        for (const q of rg.getClientRects()) { if (q.width < 1 || q.height < 1) continue; l = Math.min(l, q.left); r = Math.max(r, q.right); tp = Math.min(tp, q.top); b = Math.max(b, q.bottom); }
      }
      if (l > r) continue;
      const sides = [];
      if (l < box.x0 - tol) sides.push("esquerda " + Math.round(l));
      if (r > box.x1 + tol) sides.push("direita " + Math.round(r));
      if (tp < box.y0 - tol) sides.push("topo " + Math.round(tp));
      if (b > box.y1 + tol) sides.push("base " + Math.round(b));
      if (sides.length) out.push({ label: (el.id ? "#" + el.id + " " : "") + JSON.stringify(el.textContent.trim().slice(0, 40)), sides });
    }
    return out;
  }, [t, box, tol, minOpacity]);
  sampled++;
  for (const h of hits) for (const s of h.sides) {
    const k = h.label + "|" + s.split(" ")[0];
    const e = seen.get(k) || { label: h.label, side: s, first: t, last: t, n: 0 };
    e.last = t; e.n++; e.side = s; seen.set(k, e);
  }
}
await browser.close();
const list = [...seen.values()];
if (flag("json")) console.log(JSON.stringify({ box, sampled, violations: list }, null, 1));
else {
  for (const e of list) console.log(`FAIL ${e.label}: passa da área segura (${e.side} px) de ${e.first}s a ${e.last}s`);
  console.log(`${list.length ? "FAIL" : "PASS"}: ${sampled} amostras; área x ${box.x0}-${box.x1}, y ${box.y0}-${box.y1}`);
}
process.exit(list.length ? 1 : 0);
