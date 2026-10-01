(() => {
const DATA = JSON.parse(document.getElementById("elec-data").textContent);
const GEO = JSON.parse(document.getElementById("geo-data").textContent);
const DEPS = DATA.deps;
const byCode = Object.fromEntries(DEPS.map((d) => [d.c, d]));
const lg = (p) => Math.log(p / (1 - p));
const ex = (x) => 1 / (1 + Math.exp(-x));
const SVGNS = "http://www.w3.org/2000/svg";

const SCEN = {
  phil: { opp: "Philippe", def: 56, note: "Le Pen vs Édouard Philippe" },
  mel: { opp: "Mélenchon", def: 68, note: "Le Pen vs Jean-Luc Mélenchon" },
};
const state = { layer: "proj", scen: "phil", nat: { phil: SCEN.phil.def, mel: SCEN.mel.def }, sel: null };

// Le Pen share of the runoff vote in a department, for the current scenario and national share
function proj(d, scen = state.scen, nat = state.nat[scen]) {
  if (scen === "phil") return 100 * ex(lg(nat / 100) + d.lean);
  return 100 - 100 * ex(lg((100 - nat) / 100) + d.leanL);
}
const RATINGS = [
  { min: 60, key: "safe-rn", label: "Safe RN (60+)" },
  { min: 55, key: "likely-rn", label: "Likely RN (55–60)" },
  { min: 52, key: "lean-rn", label: "Lean RN (52–55)" },
  { min: 48, key: "toss", label: "Toss-up (48–52)" },
  { min: 45, key: "lean-opp", label: "Lean OPP (45–48)" },
  { min: 40, key: "likely-opp", label: "Likely OPP (40–45)" },
  { min: -1, key: "safe-opp", label: "Safe OPP (under 40)" },
];
const OPPCOL = {
  phil: { "lean-opp": "#efc77a", "likely-opp": "#d98f2b", "safe-opp": "#9a5a0c" },
  mel: { "lean-opp": "#f1a39b", "likely-opp": "#d24b3f", "safe-opp": "#8f2018" },
  mac: { "lean-opp": "#efc77a", "likely-opp": "#d98f2b", "safe-opp": "#9a5a0c" },
};
const RNCOL = { "safe-rn": "#1c2868", "likely-rn": "#3d4fa1", "lean-rn": "#8d9bd6", toss: "#b8b1a2" };
const rating = (v) => RATINGS.find((r) => v >= r.min);
const ratingColor = (key, side) => RNCOL[key] || OPPCOL[side][key];
const ratingLabel = (r, opp) => r.label.replace("OPP", opp);

const BLOC = { fr: ["RN + allies", "#2b3a8c"], left: ["Left (NFP)", "#d0453a"], cen: ["Macron camp", "#e0a12f"], right: ["LR + right", "#4c9fd6"] };

const bins = (stops, colors) => (v) => { for (let i = 0; i < stops.length; i++) if (v < stops[i]) return colors[i]; return colors[colors.length - 1]; };

const LAYERS = {
  proj: {
    name: "Projected runoff",
    value: (d) => proj(d),
    color: (d) => ratingColor(rating(proj(d)).key, state.scen),
    legend: () => RATINGS.map((r) => [ratingColor(r.key, state.scen), ratingLabel(r, SCEN[state.scen].opp)]),
    fmt: (d) => `Le Pen ${proj(d).toFixed(1)}%`,
  },
  flip: {
    name: "Flip point",
    value: (d) => d.flip,
    color: (d) => bins([45, 50, 53, 56, 60], ["#1c2868", "#5a6bbd", "#8e5fc0", "#c3a2e3", "#e3b25a", "#9a5a0c"])(d.flip),
    legend: () => [["#1c2868", "RN carries it even while losing nationally (under 45)"], ["#5a6bbd", "45–50"], ["#8e5fc0", "50–53: battleground"], ["#c3a2e3", "53–56: battleground"], ["#e3b25a", "56–60: falls only in a landslide"], ["#9a5a0c", "Firewall (60+)"]],
    fmt: (d) => `flips when Le Pen wins ${d.flip.toFixed(1)}% nationally`,
  },
  lp22: {
    name: "2022 runoff",
    value: (d) => d.lp22,
    color: (d) => ratingColor(rating(d.lp22).key, "mac"),
    legend: () => RATINGS.map((r) => [ratingColor(r.key, "mac"), ratingLabel(r, "Macron").replace("RN", "Le Pen")]),
    fmt: (d) => `Le Pen ${d.lp22.toFixed(1)}%`,
  },
  lead24: {
    name: "2024 leading bloc",
    value: (d) => d.l24[d.lead24],
    color: (d) => BLOC[d.lead24][1],
    opacity: (d) => Math.min(1, 0.35 + (d.l24[d.lead24] - 25) / 25 * 0.65),
    legend: () => Object.values(BLOC).map(([n, c]) => [c, n]).concat([["none", "Paler = smaller lead share"]]),
    fmt: (d) => `${BLOC[d.lead24][0]} ${d.l24[d.lead24].toFixed(1)}%`,
  },
  shift: {
    name: "Far-right shift 2022→24",
    value: (d) => d.shift,
    color: (d) => d.c.startsWith("97") ? "#6b6b6b" : bins([-2, 0, 2, 4, 6], ["#2f8f83", "#9fd3c9", "#c9cde8", "#8d9bd6", "#5466b5", "#1c2868"])(d.shift),
    legend: () => [["#2f8f83", "Fell more than 2 pts"], ["#9fd3c9", "Fell 0–2"], ["#c9cde8", "Rose 0–2"], ["#8d9bd6", "Rose 2–4"], ["#5466b5", "Rose 4–6"], ["#1c2868", "Rose 6+"], ["#6b6b6b", "Not comparable (overseas)"]],
    fmt: (d) => d.c.startsWith("97") ? "n/a overseas" : `${d.shift > 0 ? "+" : ""}${d.shift.toFixed(1)} pts`,
  },
  eu24: {
    name: "2024 European: Bardella",
    value: (d) => d.eu24.bardella,
    color: (d) => bins([20, 30, 35, 40, 45], ["#dfe3f5", "#b3bde8", "#8d9bd6", "#5a6bbd", "#3d4fa1", "#1c2868"])(d.eu24.bardella),
    legend: () => [["#dfe3f5", "Under 20%"], ["#b3bde8", "20–30"], ["#8d9bd6", "30–35"], ["#5a6bbd", "35–40"], ["#3d4fa1", "40–45"], ["#1c2868", "45+"]],
    fmt: (d) => `Bardella list ${d.eu24.bardella.toFixed(1)}%`,
  },
};

// ---- build the map
for (const el of document.querySelectorAll(".static-only")) el.remove();
document.documentElement.classList.add("js");
const svg = document.getElementById("map");
svg.setAttribute("viewBox", `0 0 ${GEO.w} ${GEO.h}`);
const gDeps = document.createElementNS(SVGNS, "g");
const gReg = document.createElementNS(SVGNS, "g");
const gCity = document.createElementNS(SVGNS, "g");
svg.append(gDeps, gReg, gCity);
const shapes = {};
for (const [code, d] of Object.entries(GEO.paths)) {
  const p = document.createElementNS(SVGNS, "path");
  p.setAttribute("d", d);
  p.setAttribute("class", "dep");
  p.dataset.c = code;
  gDeps.append(p);
  shapes[code] = [p];
}
// magnified Île-de-France inset in the empty Atlantic corner
const IDF = ["75", "77", "78", "91", "92", "93", "94", "95"];
const gInset = document.createElementNS(SVGNS, "g");
svg.append(gInset);
const idfBox = (() => {
  const tmp = document.createElementNS(SVGNS, "g");
  for (const c of IDF) tmp.append(shapes[c][0].cloneNode());
  gInset.append(tmp);
  const b = tmp.getBBox(); tmp.remove(); return b;
})();
{
  const k = 1.45, ox = 10, oy = 26;
  const frame = document.createElementNS(SVGNS, "rect");
  frame.setAttribute("x", ox - 4); frame.setAttribute("y", oy - 18);
  frame.setAttribute("width", idfBox.width * k + 8); frame.setAttribute("height", idfBox.height * k + 22);
  frame.setAttribute("class", "inset-frame");
  const lab = document.createElementNS(SVGNS, "text");
  lab.setAttribute("x", ox); lab.setAttribute("y", oy - 6); lab.setAttribute("class", "city-label");
  lab.textContent = "Île-de-France";
  const g = document.createElementNS(SVGNS, "g");
  g.setAttribute("transform", `translate(${ox - idfBox.x * k} ${oy - idfBox.y * k}) scale(${k})`);
  for (const c of IDF) {
    const p = shapes[c][0].cloneNode();
    p.setAttribute("vector-effect", "non-scaling-stroke");
    g.append(p); shapes[c].push(p);
  }
  gInset.append(frame, lab, g);
}
for (const d of Object.values(GEO.regions)) {
  const p = document.createElementNS(SVGNS, "path");
  p.setAttribute("d", d);
  p.setAttribute("class", "reg");
  gReg.append(p);
}
for (const [name, [x, y]] of Object.entries(GEO.cities)) {
  const c = document.createElementNS(SVGNS, "circle");
  c.setAttribute("cx", x); c.setAttribute("cy", y); c.setAttribute("r", 2.2); c.setAttribute("class", "city");
  const t = document.createElementNS(SVGNS, "text");
  const east = ["Strasbourg", "Nice"].includes(name);
  t.setAttribute("x", east ? x - 4 : x + 4); t.setAttribute("y", y + 3.5); t.setAttribute("class", "city-label");
  if (east) t.setAttribute("text-anchor", "end");
  t.textContent = name;
  if (["Toulon", "Le Havre", "Montpellier", "Perpignan"].includes(name)) { c.classList.add("minor"); t.classList.add("minor"); }
  gCity.append(c, t);
}
// overseas tiles
const dom = document.getElementById("dom");
const DOMS = ["971", "972", "973", "974", "976"];
dom.setAttribute("viewBox", `0 0 ${GEO.w} 46`);
DOMS.forEach((code, i) => {
  const x = 10 + i * 110;
  const r = document.createElementNS(SVGNS, "rect");
  r.setAttribute("x", x); r.setAttribute("y", 4); r.setAttribute("width", 26); r.setAttribute("height", 26); r.setAttribute("rx", 3);
  r.setAttribute("class", "dep"); r.dataset.c = code;
  const t = document.createElementNS(SVGNS, "text");
  t.setAttribute("x", x + 32); t.setAttribute("y", 21); t.setAttribute("class", "city-label");
  t.textContent = byCode[code].n;
  dom.append(r, t);
  shapes[code] = [r];
});

// ---- controls
const layerBox = document.getElementById("layers");
for (const [key, L] of Object.entries(LAYERS)) {
  const b = document.createElement("button");
  b.type = "button"; b.textContent = L.name; b.dataset.layer = key;
  b.addEventListener("click", () => { state.layer = key; render(); });
  layerBox.append(b);
}
const scenBox = document.getElementById("scen");
const slider = document.getElementById("nat");
const natOut = document.getElementById("nat-out");
scenBox.addEventListener("change", (e) => { state.scen = e.target.value; slider.value = state.nat[state.scen]; render(); });
slider.addEventListener("input", () => { state.nat[state.scen] = +slider.value; render(); });
for (const b of document.querySelectorAll("[data-preset]")) {
  b.addEventListener("click", () => {
    const [scen, v] = b.dataset.preset.split(":");
    state.scen = scen; state.nat[scen] = +v; state.layer = "proj";
    document.querySelector(`#scen input[value=${scen}]`).checked = true;
    slider.value = v; render();
  });
}
const pick = document.getElementById("pick");
for (const d of [...DEPS].sort((a, b) => a.n.localeCompare(b.n, "fr"))) {
  const o = document.createElement("option"); o.value = d.c; o.textContent = `${d.n} (${d.c})`; pick.append(o);
}
pick.addEventListener("change", () => select(pick.value || null));

// ---- hover tooltip and selection
const tip = document.getElementById("tip");
function onMove(e) {
  if (e.pointerType && e.pointerType !== "mouse") return;
  const c = e.target.dataset && e.target.dataset.c;
  if (!c) { tip.hidden = true; return; }
  const d = byCode[c];
  tip.hidden = false;
  tip.textContent = `${d.n}: ${LAYERS[state.layer].fmt(d)}`;
  const box = document.getElementById("mapwrap").getBoundingClientRect();
  tip.style.left = Math.min(e.clientX - box.left + 12, box.width - 200) + "px";
  tip.style.top = e.clientY - box.top + 12 + "px";
}
for (const el of [svg, dom]) {
  el.addEventListener("pointermove", onMove);
  el.addEventListener("mouseleave", () => (tip.hidden = true));
  el.addEventListener("click", (e) => { const c = e.target.dataset && e.target.dataset.c; if (c) select(c === state.sel ? null : c); if (c && matchMedia("(max-width: 980px)").matches) document.getElementById("panel").scrollIntoView({ behavior: "smooth", block: "nearest" }); });
}
function select(c) {
  state.sel = c; pick.value = c || "";
  for (const [code, els] of Object.entries(shapes)) for (const el of els) el.classList.toggle("sel", code === c);
  if (c) for (const el of shapes[c]) el.parentNode.append(el);
  renderPanel();
}

// ---- rendering
const pct = (v) => v.toFixed(1) + "%";
function bar(label, v, color, max = 60) {
  return `<div class="pb"><span>${label}</span><span class="pt"><span style="width:${Math.min(100, v / max * 100)}%;background:${color}"></span></span><span class="num">${pct(v)}</span></div>`;
}
function renderPanel() {
  const el = document.getElementById("panel");
  const d = byCode[state.sel];
  if (!d) {
    el.innerHTML = `<p class="muted">Tap a department (or pick one from the list above) for its full record. On a computer, hover to see its value.</p>` + summaryHTML();
    return;
  }
  const s = SCEN[state.scen];
  const v = proj(d), r = rating(v);
  const lead = Object.entries(d.l24).sort((a, b) => b[1] - a[1]);
  el.innerHTML = `
  <h3>${d.n} <span class="muted">(${d.c})</span></h3>
  <p class="muted small">${d.r} · ${(d.ins / 1000).toFixed(0)}k registered voters</p>
  <div class="kv"><span>Projected runoff, ${s.note} at ${state.nat[state.scen]}% nationally</span><strong><span class="sw" style="background:${ratingColor(r.key, state.scen)}"></span>Le Pen ${pct(v)}</strong><span class="muted">${ratingLabel(r, s.opp)}</span></div>
  <div class="kv"><span>Flip point vs Philippe-type opponent</span><strong>${pct(d.flip)}</strong><span class="muted">national Le Pen share at which this department tips to her</span></div>
  <h4>2022 presidential</h4>
  ${bar("Le Pen R1", d.p1.lepen, "#2b3a8c")}${bar("Macron R1", d.p1.macron, "#e0a12f")}${bar("Mélenchon R1", d.p1.melenchon, "#d0453a")}${bar("Zemmour R1", d.p1.zemmour, "#5b4636")}${bar("Le Pen runoff", d.lp22, "#2b3a8c", 100)}
  <h4>2024 legislative, first round (turnout ${pct(d.turn24)})</h4>
  ${lead.map(([k, val]) => bar(BLOC[k][0], val, BLOC[k][1])).join("")}
  <h4>2024 European election</h4>
  ${bar("Bardella (RN)", d.eu24.bardella, "#2b3a8c")}${bar("Glucksmann (PS-PP)", d.eu24.glucksmann, "#e46a9a")}${bar("Hayer (Macron)", d.eu24.hayer, "#e0a12f")}${bar("Aubry (LFI)", d.eu24.aubry, "#d0453a")}${bar("Bellamy (LR)", d.eu24.bellamy, "#4c9fd6")}${bar("Maréchal (Reconquête)", d.eu24.marechal, "#5b4636")}
  ${d.c.startsWith("97") ? `<p class="muted small">Overseas: the RN stood in few 2024 legislative races here, so the projection uses the 2022 runoff alone. The 2022 Le Pen vote overseas was largely an anti-Macron vote and may not carry over.</p>` : ""}
  <p><button type="button" id="clear">Clear selection</button></p>`;
  document.getElementById("clear").addEventListener("click", () => select(null));
}
function summaryHTML() {
  const counts = {}; let ins = {};
  for (const d of DEPS) { const k = rating(proj(d)).key; counts[k] = (counts[k] || 0) + 1; ins[k] = (ins[k] || 0) + d.ins; }
  const s = SCEN[state.scen];
  const rows = RATINGS.map((r) => `<tr><td><span class="sw" style="background:${ratingColor(r.key, state.scen)}"></span>${ratingLabel(r, s.opp)}</td><td class="num">${counts[r.key] || 0}</td><td class="num">${((ins[r.key] || 0) / 1e6).toFixed(1)}M</td></tr>`).join("");
  return `<h4>${s.note}, Le Pen at ${state.nat[state.scen]}% nationally</h4><div class="table-wrap"><table class="compact"><thead><tr><th>Rating</th><th class="num">Depts</th><th class="num">Voters</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
function renderRegions() {
  const groups = {};
  for (const d of DEPS) (groups[d.r] ||= []).push(d);
  const s = SCEN[state.scen];
  const rows = Object.entries(groups).map(([name, ds]) => {
    const ins = ds.reduce((a, d) => a + d.ins, 0);
    const w = (f) => ds.reduce((a, d) => a + d.ins * f(d), 0) / ins;
    const p = w(proj), p22 = w((d) => d.lp22), fr = w((d) => d.l24.fr);
    const tight = ds.filter((d) => { const v = proj(d); return v >= 45 && v < 55; }).map((d) => d.n);
    return { name, ins, p, p22, fr, tight };
  }).sort((a, b) => b.p - a.p);
  document.getElementById("regions-body").innerHTML = rows.map((r) => {
    const rt = rating(r.p);
    return `<tr><td>${r.name}</td><td class="num">${(r.ins / 1e6).toFixed(1)}M</td><td class="num">${pct(r.p22)}</td><td class="num">${pct(r.fr)}</td><td class="num"><strong>${pct(r.p)}</strong></td><td><span class="sw" style="background:${ratingColor(rt.key, state.scen)}"></span>${ratingLabel(rt, s.opp).replace(/ \(.*\)/, "")}</td><td class="small">${r.tight.join(", ") || "<span class='muted'>none</span>"}</td></tr>`;
  }).join("");
  document.getElementById("regions-scen").textContent = `${s.note}, Le Pen at ${state.nat[state.scen]}% nationally`;
}
function render() {
  const L = LAYERS[state.layer];
  for (const d of DEPS) for (const el of shapes[d.c] || []) {
    el.style.fill = L.color(d);
    el.style.fillOpacity = L.opacity ? L.opacity(d) : 1;
  }
  for (const b of layerBox.children) b.setAttribute("aria-pressed", b.dataset.layer === state.layer);
  const isProj = state.layer === "proj";
  document.getElementById("scenario-controls").classList.toggle("dim", !isProj);
  natOut.textContent = `${state.nat[state.scen]}%`;
  document.getElementById("legend").innerHTML = L.legend().map(([c, t]) => `<span><span class="sw" style="${c === "none" ? "border:1px dashed var(--muted)" : `background:${c}`}"></span>${t}</span>`).join("");
  document.getElementById("layer-desc").textContent = document.getElementById("desc-" + state.layer).textContent;
  renderPanel();
  renderRegions();
}
render();
})();
