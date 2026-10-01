// Make a 1200x630 link-preview image (og:image) for a country page.
// Usage: node src/preview.mjs <page-url> <map-selector> <title> <subtitle> <out.png>
// Captures the page's map element at desktop width, then lays it out beside the title.
import { spawn } from "node:child_process";
import { writeFileSync, rmSync } from "node:fs";

const [url, selector, title, subtitle, out] = process.argv.slice(2);
const port = 9400 + Math.floor(Math.random() * 400);
const dir = `/tmp/chp-preview-${port}`;
rmSync(dir, { recursive: true, force: true });
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", [
  "--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=${dir}`,
  "--no-first-run", "--disable-gpu", "--hide-scrollbars", "about:blank",
], { stdio: "ignore" });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let target;
for (let i = 0; i < 50 && !target; i++) {
  await sleep(200);
  try { target = (await (await fetch(`http://127.0.0.1:${port}/json`)).json()).find((t) => t.type === "page"); } catch {}
}
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r));
let id = 0;
const pending = new Map();
ws.addEventListener("message", (e) => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async (expression) => (await send("Runtime.evaluate", { expression, returnByValue: true })).result.result.value;

await send("Page.enable");
await send("Emulation.setDeviceMetricsOverride", { width: 1300, height: 1000, deviceScaleFactor: 2, mobile: false });
await send("Page.navigate", { url });
await sleep(4000);
const box = JSON.parse(await evaluate(`(() => { const e = document.querySelector(${JSON.stringify(selector)}); e.scrollIntoView(); const r = e.getBoundingClientRect(); return JSON.stringify({ x: r.x + scrollX, y: r.y + scrollY, w: r.width, h: r.height }); })()`));
const map = (await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { x: box.x, y: box.y, width: box.w, height: box.h, scale: 1 } })).result.data;

const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;");
const card = `<!doctype html><meta charset="utf-8"><style>
body { margin: 0; width: 1200px; height: 630px; background: #121418; color: #e6e8eb; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; display: flex; overflow: hidden; }
.t { flex: 0 0 470px; padding: 64px 0 56px 64px; display: flex; flex-direction: column; }
h1 { font-size: 58px; line-height: 1.08; margin: 0 0 22px; font-weight: 700; letter-spacing: -0.02em; }
p { font-size: 25px; line-height: 1.4; color: #c4c9d0; margin: 0; }
.u { margin-top: auto; font-size: 20px; color: #8fb0ff; }
.m { flex: 1; display: flex; align-items: center; justify-content: center; padding: 24px; }
.m img { max-width: 100%; max-height: 582px; border-radius: 10px; }
</style><div class="t"><h1>${esc(title)}</h1><p>${esc(subtitle)}</p><div class="u">julienhovan.com/europe-elections</div></div><div class="m"><img src="data:image/png;base64,${map}"></div>`;
await send("Emulation.setDeviceMetricsOverride", { width: 1200, height: 630, deviceScaleFactor: 1, mobile: false });
await send("Page.navigate", { url: "data:text/html;base64," + Buffer.from(card).toString("base64") });
await sleep(1500);
const shot = (await send("Page.captureScreenshot", { format: "png", clip: { x: 0, y: 0, width: 1200, height: 630, scale: 1 } })).result.data;
writeFileSync(out, Buffer.from(shot, "base64"));
console.log("wrote", out);
ws.close();
chrome.kill();
process.exit(0);
