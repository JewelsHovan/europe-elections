// Usage: node phoneshot.mjs <url> <out.png> [height]
// Real mobile emulation (390px, DPR 2, touch) via the Chrome DevTools Protocol.
import { spawn } from "node:child_process";
import { writeFileSync, rmSync } from "node:fs";

const [url, out, h = "2400"] = process.argv.slice(2);
const port = 9333 + Math.floor(Math.random() * 500);
rmSync(`/tmp/chp-cdp-${port}`, { recursive: true, force: true });
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", [
  "--headless=new", `--remote-debugging-port=${port}`, `--user-data-dir=/tmp/chp-cdp-${port}`,
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
let id = 0; const pending = new Map();
ws.addEventListener("message", (e) => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise((r) => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
await send("Emulation.setDeviceMetricsOverride", { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
await send("Emulation.setTouchEmulationEnabled", { enabled: true });
await send("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1" });
await send("Page.enable");
await send("Page.navigate", { url });
await sleep(5000);
const m = await send("Runtime.evaluate", { expression: process.env.EXPR || "JSON.stringify({w: document.documentElement.clientWidth, sw: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})", returnByValue: true });
console.log("metrics", m.result.result.value);
const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true, clip: { x: 0, y: 0, width: 390, height: +h, scale: 1 } });
writeFileSync(out, Buffer.from(shot.result.data, "base64"));
console.log("wrote", out);
ws.close(); chrome.kill();
process.exit(0);
