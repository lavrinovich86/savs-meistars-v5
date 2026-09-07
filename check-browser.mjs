// Pārbauda lapu īstā pārlūkā: izkārtojuma pārpilde, slāņu slēdži, izvēlne
// un forma. Slāņu slēdži ir šīs versijas galvenā interaktīvā daļa, tāpēc
// tos pārbauda gan kā aria stāvokli, gan kā reālu SVG grupu redzamību.
//
// Priekšnosacījums: Chromium ar --remote-debugging-port=9333 un lapa,
// kas pieejama pārbaudāmajā URL (noklusējums — lokāls serveris).
//
//   python3 -m http.server 8751 --bind 127.0.0.1 --directory .
//   chromium --headless --remote-debugging-port=9333 http://127.0.0.1:8751/
//   node check-browser.mjs

import { writeFile } from 'node:fs/promises';

const PAGE = process.env.PAGE_URL || 'http://127.0.0.1:8751/';
const PORT = process.env.CDP_PORT || 9333;

const tabs = await (await fetch(`http://localhost:${PORT}/json`)).json();
const tab = tabs.find(t => t.url.startsWith(PAGE))
  || await (await fetch(`http://localhost:${PORT}/json/new?${PAGE}`, { method: 'PUT' })).json();

const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));

let sequence = 0;
const pending = new Map();
ws.addEventListener('message', event => {
  const data = JSON.parse(event.data);
  if (data.id) { pending.get(data.id)?.(data); pending.delete(data.id); }
});
const call = (method, params = {}) => new Promise((resolve, reject) => {
  const id = ++sequence;
  pending.set(id, data => data.error ? reject(data.error) : resolve(data.result));
  ws.send(JSON.stringify({ id, method, params }));
});
const evaluate = async expr =>
  (await call('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true })).result.value;

await call('Page.enable');
await call('Page.navigate', { url: PAGE });
await new Promise(r => setTimeout(r, 900));
await evaluate('document.fonts.ready.then(()=>true)');

const results = [];

// --- izkārtojums dažādos platumos ---
for (const width of [1440, 1024, 768, 390, 320]) {
  await call('Emulation.setDeviceMetricsOverride',
    { width, height: 1000, deviceScaleFactor: 1, mobile: width < 760 });
  results.push(await evaluate(`({
    width: ${width},
    overflow: document.documentElement.scrollWidth > innerWidth,
    images: [...document.images].every(i => i.complete && i.naturalWidth > 0),
    brokenAnchors: [...document.querySelectorAll('a[href^="#"]')]
      .filter(a => a.hash && !document.querySelector(a.hash)).length
  })`));
}

await call('Emulation.setDeviceMetricsOverride',
  { width: 1440, height: 1050, deviceScaleFactor: 1, mobile: false });

// --- slāņi: sākuma stāvoklis ---
results.push(await evaluate(`(() => {
  const svg = document.getElementById('dwg-roof');
  const groups = [...svg.querySelectorAll('[data-layer]')];
  return {
    check: 'layers-default',
    buttonsPressed: [...document.querySelectorAll('.layer[data-target="dwg-roof"]')]
      .every(b => b.getAttribute('aria-pressed') === 'true'),
    noDataOff: !svg.hasAttribute('data-off'),
    allVisible: groups.every(g => getComputedStyle(g).display !== 'none'),
    groupCount: groups.length
  };
})()`));

// --- slāņi: viena izslēgšana un atgriešana ---
results.push(await evaluate(`(() => {
  const svg = document.getElementById('dwg-roof');
  const btn = document.querySelector('.layer[data-target="dwg-roof"][data-layer="pv"]');
  const pv = svg.querySelector('[data-layer="pv"]');
  const arh = svg.querySelector('[data-layer="arh"]');
  btn.click();
  const off = {
    pressed: btn.getAttribute('aria-pressed'),
    dataOff: svg.getAttribute('data-off'),
    pvHidden: getComputedStyle(pv).display === 'none',
    arhStillVisible: getComputedStyle(arh).display !== 'none'
  };
  btn.click();
  const back = {
    pressed: btn.getAttribute('aria-pressed'),
    dataOff: svg.getAttribute('data-off'),
    pvVisible: getComputedStyle(pv).display !== 'none'
  };
  return { check: 'layer-toggle', off, back };
})()`));

// --- slāņi: uzklājami, nevis pārslēdzami skati ---
results.push(await evaluate(`(() => {
  const svg = document.getElementById('dwg-roof');
  const pick = l => document.querySelector('.layer[data-target="dwg-roof"][data-layer="' + l + '"]');
  const grp = l => svg.querySelector('[data-layer="' + l + '"]');
  pick('pv').click();
  pick('elt').click();
  const both = {
    dataOff: svg.getAttribute('data-off'),
    pvHidden: getComputedStyle(grp('pv')).display === 'none',
    eltHidden: getComputedStyle(grp('elt')).display === 'none',
    othersVisible: ['arh', 'jumt', 'izm'].every(l => getComputedStyle(grp(l)).display !== 'none')
  };
  pick('pv').click();
  const one = {
    dataOff: svg.getAttribute('data-off'),
    pvBack: getComputedStyle(grp('pv')).display !== 'none',
    eltStillHidden: getComputedStyle(grp('elt')).display === 'none'
  };
  pick('elt').click();
  return { check: 'layers-additive', both, one, cleared: !svg.hasAttribute('data-off') };
})()`));

// --- pārējie rasējumi ---
results.push(await evaluate(`(() => {
  const out = {};
  for (const id of ['dwg-elev', 'dwg-el']) {
    const svg = document.getElementById(id);
    const btn = document.querySelector('.layer[data-target="' + id + '"]');
    const layer = btn.dataset.layer;
    const g = svg.querySelector('[data-layer="' + layer + '"]');
    btn.click();
    out[id] = { layer, hidden: getComputedStyle(g).display === 'none' };
    btn.click();
    out[id].restored = getComputedStyle(g).display !== 'none';
  }
  return { check: 'other-drawings', ...out };
})()`));

// --- izvēlne un forma ---
await call('Emulation.setDeviceMetricsOverride',
  { width: 390, height: 900, deviceScaleFactor: 1, mobile: true });
results.push(await evaluate(`(() => {
  const burger = document.getElementById('burger');
  burger.click();
  const opened = burger.getAttribute('aria-expanded') === 'true';
  document.querySelector('#nav a').click();
  const closed = burger.getAttribute('aria-expanded') === 'false';
  document.querySelector('[data-service="elektro"]').click();
  const selected = document.getElementById('f-service').value === 'elektro';
  document.getElementById('form').requestSubmit();
  const shown = !document.getElementById('e-name').hidden;
  const marked = document.getElementById('f-name').getAttribute('aria-invalid') === 'true';
  document.getElementById('f-name').value = 'Pārbaude';
  document.getElementById('f-name').dispatchEvent(new Event('input', { bubbles: true }));
  const cleared = document.getElementById('e-name').hidden;
  return { check: 'menu-and-form', menuOpens: opened, menuCloses: closed,
           serviceSelects: selected, emptyShowsError: shown, ariaInvalid: marked,
           errorClears: cleared };
})()`));

console.log(JSON.stringify(results, null, 2));
await writeFile(new URL('browser-checks.json', import.meta.url), JSON.stringify(results, null, 2));
ws.close();

const layers = results.find(r => r.check === 'layer-toggle');
const additive = results.find(r => r.check === 'layers-additive');
const other = results.find(r => r.check === 'other-drawings');
const dflt = results.find(r => r.check === 'layers-default');
const form = results.find(r => r.check === 'menu-and-form');

const failed = results.some(r => r.overflow || r.images === false || r.brokenAnchors > 0)
  || !dflt.buttonsPressed || !dflt.noDataOff || !dflt.allVisible || dflt.groupCount !== 5
  || layers.off.pressed !== 'false' || !layers.off.pvHidden || !layers.off.arhStillVisible
  || layers.back.pressed !== 'true' || !layers.back.pvVisible
  || !additive.both.pvHidden || !additive.both.eltHidden || !additive.both.othersVisible
  || !additive.one.pvBack || !additive.one.eltStillHidden || !additive.cleared
  || !other['dwg-elev'].hidden || !other['dwg-elev'].restored
  || !other['dwg-el'].hidden || !other['dwg-el'].restored
  || !form.menuOpens || !form.menuCloses || !form.serviceSelects
  || !form.emptyShowsError || !form.ariaInvalid || !form.errorClears;

if (failed) process.exitCode = 1;
console.log(failed ? 'PĀRBAUDE NEIZDEVĀS' : 'Visas pārbaudes izturētas');
