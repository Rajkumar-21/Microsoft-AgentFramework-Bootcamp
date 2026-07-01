/* =============================================================================
   Agent Framework Bootcamp — site shell (plain JS, no build)
   Injects navbar + sidebar + right TOC, handles theme, drawer, copy, mermaid.
   ============================================================================= */

/* ---- Navigation manifest (single source of truth) ------------------------- */
const NAV = [
  {
    label: 'Get Started',
    items: [
      { id: 'introduction', title: 'Introduction' },
      { id: 'setup-and-configuration', title: 'Setup & Configuration' },
      { id: 'hello-agent', title: 'Hello Agent' },
      { id: 'providers-deep-dive', title: 'Providers Deep Dive' },
    ],
  },
  {
    label: 'Core Foundations',
    items: [
      { id: 'function-tools', title: 'Function Tools' },
      { id: 'conversation-threads', title: 'Conversation Threads' },
      { id: 'streaming-responses', title: 'Streaming Responses' },
    ],
  },
  {
    label: 'Tools & Workflows',
    items: [
      { id: 'structured-outputs', title: 'Structured Outputs' },
      { id: 'hosted-tools', title: 'Hosted Tools' },
      { id: 'mcp-tools', title: 'MCP Tools' },
      { id: 'middleware-system', title: 'Middleware' },
      { id: 'workflows-sequential', title: 'Sequential Workflows' },
      { id: 'workflows-handoff', title: 'Handoff Workflows' },
      { id: 'workflows-concurrent', title: 'Concurrent Workflows' },
    ],
  },
  {
    label: 'Multi-Agent & Production',
    items: [
      { id: 'agent-as-tool', title: 'Agent as Tool' },
      { id: 'supervisor-agent', title: 'Supervisor Agent' },
      { id: 'sub-workflows', title: 'Sub-Workflows' },
      { id: 'human-in-the-loop', title: 'Human in the Loop' },
      { id: 'memory-persistence', title: 'Memory & Persistence' },
      { id: 'observability', title: 'Observability' },
      { id: 'declarative-agents', title: 'Declarative Agents' },
      { id: 'agent-to-agent', title: 'Agent-to-Agent (A2A)' },
      { id: 'deployment', title: 'Deployment' },
      { id: 'capstone-project', title: 'Capstone Project' },
    ],
  },
  {
    label: 'Real-World Projects',
    items: [
      { id: 'agent-registry', title: 'Agent Registry & Marketplace' },
      { id: 'project-ops-copilot', title: 'Ops Copilot' },
      { id: 'project-commerce-concierge', title: 'Commerce Concierge' },
    ],
  },
  {
    label: 'Architecture',
    items: [{ id: 'patterns-overview', title: 'Patterns Overview' }],
  },
];

/* flat ordered list for prev/next + search */
const FLAT = NAV.flatMap((s) => s.items.map((i) => ({ ...i, section: s.label })));

/* ---- helpers -------------------------------------------------------------- */
const $ = (sel, root = document) => root.querySelector(sel);
const currentId = () => {
  const f = location.pathname.split('/').pop() || 'index.html';
  return f.replace(/\.html$/, '') || 'index';
};

/* ---- theme (no-FOUC bootstrap runs inline in <head>) ---------------------- */
function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t);
  try { localStorage.setItem('af-theme', t); } catch (e) {}
  const btn = $('#themeToggle');
  if (btn) btn.textContent = t === 'dark' ? '☀️' : '🌙';
}
function toggleTheme() {
  const cur = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
  applyTheme(cur === 'dark' ? 'light' : 'dark');
}

/* ---- navbar --------------------------------------------------------------- */
function buildNavbar() {
  const el = $('#navbar');
  if (!el) return;
  const t = document.documentElement.getAttribute('data-theme') === 'dark' ? '☀️' : '🌙';
  el.className = 'nav';
  el.innerHTML = `
    <button class="icon-btn nav__menu" id="menuToggle" aria-label="Open menu">☰</button>
    <a class="nav__brand" href="index.html">
      <span class="nav__logo">AF</span>
      <span class="nav__title"><strong>Agent Framework</strong><span>Bootcamp</span></span>
    </a>
    <div class="nav__spacer"></div>
    <label class="nav__search">
      <span aria-hidden="true">🔎</span>
      <input id="searchInput" type="search" placeholder="Search lessons…" autocomplete="off" />
    </label>
    <nav class="nav__links">
      <a class="nav__link" href="introduction.html">Lessons</a>
      <a class="nav__link" href="https://github.com/Rajkumar-21/Microsoft-AgentFramework-Bootcamp" target="_blank" rel="noopener">GitHub ↗</a>
    </nav>
    <button class="icon-btn" id="themeToggle" aria-label="Toggle theme">${t}</button>
    <div class="search-pop" id="searchPop"></div>`;
  $('#themeToggle').addEventListener('click', toggleTheme);
  $('#menuToggle').addEventListener('click', () => toggleDrawer(true));
  wireSearch();
}

/* ---- sidebar -------------------------------------------------------------- */
function buildSidebar() {
  const el = $('#sidebar');
  if (!el) return;
  const cur = currentId();
  el.className = 'sidebar';
  el.innerHTML = NAV.map((sec) => `
    <div class="sidebar__section">
      <div class="sidebar__heading"><span class="dot"></span>${sec.label}</div>
      <ul class="sidebar__list">
        ${sec.items.map((i) => `
          <li><a class="sidebar__link ${i.id === cur ? 'is-active' : ''}" href="${i.id}.html">${i.title}</a></li>`).join('')}
      </ul>
    </div>`).join('');
}

/* ---- mobile drawer -------------------------------------------------------- */
function toggleDrawer(open) {
  const sb = $('#sidebar');
  let bd = $('#backdrop');
  if (!bd) {
    bd = document.createElement('div');
    bd.id = 'backdrop';
    bd.className = 'backdrop';
    bd.addEventListener('click', () => toggleDrawer(false));
    document.body.appendChild(bd);
  }
  if (sb) sb.classList.toggle('is-open', open);
  bd.classList.toggle('is-open', open);
}

/* ---- right-hand "On this page" TOC ---------------------------------------- */
function buildToc() {
  const toc = $('#toc');
  const doc = $('#doc');
  if (!toc || !doc) return;
  const heads = [...doc.querySelectorAll('h2, h3')];
  if (!heads.length) { toc.style.display = 'none'; return; }
  heads.forEach((h, idx) => { if (!h.id) h.id = 'h-' + idx + '-' + h.textContent.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); });
  toc.className = 'toc';
  toc.innerHTML = `<div class="toc__title">On this page</div>
    <ul class="toc__list">
      ${heads.map((h) => `<li><a class="${h.tagName === 'H3' ? 'lvl-3' : ''}" href="#${h.id}">${h.textContent}</a></li>`).join('')}
    </ul>`;
  // scroll spy
  const links = [...toc.querySelectorAll('a')];
  const obs = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        links.forEach((l) => l.classList.toggle('is-active', l.getAttribute('href') === '#' + e.target.id));
      }
    });
  }, { rootMargin: '-80px 0px -70% 0px', threshold: 0 });
  heads.forEach((h) => obs.observe(h));
}

/* ---- prev / next pager ---------------------------------------------------- */
function buildPager() {
  const doc = $('#doc');
  if (!doc) return;
  const cur = currentId();
  const idx = FLAT.findIndex((i) => i.id === cur);
  if (idx === -1) return;
  const prev = FLAT[idx - 1];
  const next = FLAT[idx + 1];
  const pager = document.createElement('div');
  pager.className = 'pager';
  pager.innerHTML = `
    ${prev ? `<a class="pager__link" href="${prev.id}.html"><span class="pager__dir">← Previous</span><span class="pager__title">${prev.title}</span></a>` : '<span></span>'}
    ${next ? `<a class="pager__link pager__next" href="${next.id}.html"><span class="pager__dir">Next →</span><span class="pager__title">${next.title}</span></a>` : '<span></span>'}`;
  doc.appendChild(pager);
}

/* ---- copy buttons on code blocks ------------------------------------------ */
function wireCopyButtons() {
  document.querySelectorAll('.code-block').forEach((block) => {
    const btn = block.querySelector('.code-block__copy');
    const code = block.querySelector('code');
    if (!btn || !code) return;
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.innerText);
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 1600);
      } catch (e) { btn.textContent = 'Press Ctrl+C'; }
    });
  });
}

/* ---- search --------------------------------------------------------------- */
function wireSearch() {
  const input = $('#searchInput');
  const pop = $('#searchPop');
  if (!input || !pop) return;
  const render = (q) => {
    const term = q.trim().toLowerCase();
    if (!term) { pop.classList.remove('is-open'); return; }
    const hits = FLAT.filter((i) => i.title.toLowerCase().includes(term) || i.section.toLowerCase().includes(term));
    pop.innerHTML = hits.length
      ? hits.map((i) => `<a href="${i.id}.html"><div>${i.title}</div><div class="sect">${i.section}</div></a>`).join('')
      : '<div class="empty">No lessons found.</div>';
    pop.classList.add('is-open');
  };
  input.addEventListener('input', (e) => render(e.target.value));
  input.addEventListener('focus', (e) => render(e.target.value));
  document.addEventListener('click', (e) => { if (!pop.contains(e.target) && e.target !== input) pop.classList.remove('is-open'); });
}

/* ---- mermaid + highlight -------------------------------------------------- */
function initLibs() {
  if (window.mermaid) {
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    window.mermaid.initialize({
      startOnLoad: false,
      theme: dark ? 'dark' : 'default',
      themeVariables: { primaryColor: '#6366f1', primaryBorderColor: '#4f46e5', fontFamily: 'Inter, sans-serif' },
      flowchart: { curve: 'basis' },
    });
    try {
      const p = window.mermaid.run({ querySelector: '.mermaid' });
      if (p && typeof p.then === 'function') p.then(wireDiagramZoom).catch(() => {});
    } catch (e) {}
    // fallback in case run resolved synchronously or threw
    setTimeout(wireDiagramZoom, 700);
  }
  if (window.hljs) {
    document.querySelectorAll('pre code').forEach((el) => { try { window.hljs.highlightElement(el); } catch (e) {} });
  }
}

/* ---- diagram zoom + download (lightbox) ----------------------------------- */
const _slug = (s) => (s || 'diagram').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') || 'diagram';

function _triggerDownload(url, filename) {
  const a = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => { try { URL.revokeObjectURL(url); } catch (e) {} }, 4000);
}

function _svgString(svg) {
  const clone = svg.cloneNode(true);
  clone.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
  clone.removeAttribute('style');
  return new XMLSerializer().serializeToString(clone);
}

function downloadSvg(svg, name) {
  const blob = new Blob([_svgString(svg)], { type: 'image/svg+xml;charset=utf-8' });
  _triggerDownload(URL.createObjectURL(blob), _slug(name) + '.svg');
}

function downloadPng(svg, name) {
  const str = _svgString(svg);
  const rect = svg.getBoundingClientRect();
  const vb = svg.viewBox && svg.viewBox.baseVal;
  const w = Math.ceil((vb && vb.width) || rect.width || 800);
  const h = Math.ceil((vb && vb.height) || rect.height || 600);
  const scale = 2;
  const img = new Image();
  img.onload = () => {
    const canvas = document.createElement('canvas');
    canvas.width = w * scale; canvas.height = h * scale;
    const ctx = canvas.getContext('2d');
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    ctx.fillStyle = dark ? '#0f1424' : '#ffffff';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.scale(scale, scale);
    ctx.drawImage(img, 0, 0, w, h);
    canvas.toBlob((blob) => { if (blob) _triggerDownload(URL.createObjectURL(blob), _slug(name) + '.png'); });
  };
  img.onerror = () => downloadSvg(svg, name); // graceful fallback
  img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(str)));
}

let _lb = null;
function _ensureLightbox() {
  if (_lb) return _lb;
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.innerHTML = `
    <div class="lightbox__bar">
      <span class="lightbox__title" id="lbTitle"></span>
      <div class="lightbox__actions">
        <button class="dg-btn" data-act="zoomout" title="Zoom out">−</button>
        <button class="dg-btn" data-act="zoomin" title="Zoom in">+</button>
        <button class="dg-btn" data-act="reset" title="Reset view">Reset</button>
        <button class="dg-btn" data-act="png" title="Download PNG">⬇ PNG</button>
        <button class="dg-btn" data-act="svg" title="Download SVG">⬇ SVG</button>
        <button class="dg-btn" data-act="close" title="Close (Esc)" aria-label="Close">✕</button>
      </div>
    </div>
    <div class="lightbox__stage" id="lbStage"><div class="lightbox__canvas" id="lbCanvas"></div></div>
    <div class="lightbox__hint">Scroll to zoom · drag to pan · Esc to close</div>`;
  document.body.appendChild(lb);
  _lb = lb;

  const state = { scale: 1, x: 0, y: 0, dragging: false, sx: 0, sy: 0, svg: null, title: '' };
  lb._state = state;
  const canvas = lb.querySelector('#lbCanvas');
  const stage = lb.querySelector('#lbStage');
  const apply = () => { canvas.style.transform = `translate(${state.x}px, ${state.y}px) scale(${state.scale})`; };
  lb._apply = apply;
  const zoom = (factor) => { state.scale = Math.min(Math.max(state.scale * factor, 0.2), 8); apply(); };

  lb.querySelector('[data-act="zoomin"]').addEventListener('click', () => zoom(1.25));
  lb.querySelector('[data-act="zoomout"]').addEventListener('click', () => zoom(1 / 1.25));
  lb.querySelector('[data-act="reset"]').addEventListener('click', () => { state.scale = 1; state.x = 0; state.y = 0; apply(); });
  lb.querySelector('[data-act="close"]').addEventListener('click', closeLightbox);
  lb.querySelector('[data-act="png"]').addEventListener('click', () => { if (state.svg) downloadPng(state.svg, state.title); });
  lb.querySelector('[data-act="svg"]').addEventListener('click', () => { if (state.svg) downloadSvg(state.svg, state.title); });

  stage.addEventListener('wheel', (e) => { e.preventDefault(); zoom(e.deltaY < 0 ? 1.12 : 1 / 1.12); }, { passive: false });
  stage.addEventListener('mousedown', (e) => { state.dragging = true; state.sx = e.clientX - state.x; state.sy = e.clientY - state.y; stage.classList.add('is-grabbing'); });
  window.addEventListener('mousemove', (e) => { if (!state.dragging) return; state.x = e.clientX - state.sx; state.y = e.clientY - state.sy; apply(); });
  window.addEventListener('mouseup', () => { state.dragging = false; stage.classList.remove('is-grabbing'); });
  lb.addEventListener('click', (e) => { if (e.target === lb || e.target === stage) closeLightbox(); });
  document.addEventListener('keydown', (e) => {
    if (!_lb || !_lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') closeLightbox();
    else if (e.key === '+' || e.key === '=') zoom(1.25);
    else if (e.key === '-') zoom(1 / 1.25);
    else if (e.key === '0') { state.scale = 1; state.x = 0; state.y = 0; apply(); }
  });
  return lb;
}

function openLightbox(svg, title) {
  const lb = _ensureLightbox();
  const st = lb._state;
  st.svg = svg; st.title = title; st.scale = 1; st.x = 0; st.y = 0;
  lb.querySelector('#lbTitle').textContent = title;
  const canvas = lb.querySelector('#lbCanvas');
  canvas.innerHTML = '';
  canvas.appendChild(svg.cloneNode(true));
  lb._apply();
  lb.classList.add('is-open');
  document.body.classList.add('no-scroll');
}

function closeLightbox() {
  if (!_lb) return;
  _lb.classList.remove('is-open');
  document.body.classList.remove('no-scroll');
}

function wireDiagramZoom() {
  document.querySelectorAll('.diagram').forEach((dg) => {
    const body = dg.querySelector('.diagram__body');
    const svg = body && body.querySelector('svg');
    if (!body || !svg || dg.dataset.zoomWired) return;
    dg.dataset.zoomWired = '1';

    const title = (dg.querySelector('.diagram__title') || {}).textContent || 'diagram';
    const tools = document.createElement('div');
    tools.className = 'diagram__tools';
    tools.innerHTML = `
      <button class="dg-btn" data-act="open" title="Open fullscreen">⤢ Expand</button>
      <button class="dg-btn" data-act="png" title="Download PNG">⬇ PNG</button>
      <button class="dg-btn" data-act="svg" title="Download SVG">⬇ SVG</button>`;
    dg.appendChild(tools);

    tools.querySelector('[data-act="open"]').addEventListener('click', (e) => { e.stopPropagation(); openLightbox(svg, title); });
    tools.querySelector('[data-act="png"]').addEventListener('click', (e) => { e.stopPropagation(); downloadPng(svg, title); });
    tools.querySelector('[data-act="svg"]').addEventListener('click', (e) => { e.stopPropagation(); downloadSvg(svg, title); });
    body.addEventListener('click', () => openLightbox(svg, title));
  });
}

/* ---- boot ----------------------------------------------------------------- */
document.addEventListener('DOMContentLoaded', () => {
  buildNavbar();
  buildSidebar();
  buildToc();
  buildPager();
  wireCopyButtons();
  initLibs();
});
