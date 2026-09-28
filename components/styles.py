"""All styling for the cinematic diary.

``STREAMLIT_CSS`` hides the default Streamlit chrome so the app reads as a
standalone website. ``get_styles()`` returns the full stylesheet injected
into the embedded page document.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# CSS injected into the Streamlit host page — hides every default widget
# ---------------------------------------------------------------------------

STREAMLIT_CSS = """
<style>
  html, body, [data-testid="stAppViewContainer"], .stApp {
    background: #04070c !important;
    height: 100%;
  }
  #MainMenu, footer, header,
  [data-testid="stHeader"],
  [data-testid="stToolbar"],
  [data-testid="stDecoration"],
  [data-testid="stSidebar"],
  [data-testid="stSidebarNav"],
  [data-testid="stStatusWidget"] {
    display: none !important;
  }
  .stApp { overflow: hidden !important; }
  .block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
  }
  [data-testid="stVerticalBlock"],
  [data-testid="stVerticalBlockBorderWrapper"] {
    gap: 0 !important;
    padding: 0 !important;
    border: none !important;
  }
  iframe[data-testid="stIFrame"],
  iframe[data-testid="stCustomComponentV1"] {
    display: block;
    width: 100% !important;
    height: 100dvh !important;
    border: none !important;
  }
</style>
"""

_IMAGE_VARS_TEMPLATE = "\n".join(
    "  --img-{stem}: url(\"{uri}\");" for stem in []  # placeholder, replaced below
)


def _image_vars(images: dict[str, str]) -> str:
    """Build :root custom properties — each photo is embedded exactly once."""
    lines = []
    for path in sorted(images):
        stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()
        lines.append(f'  --img-{stem}: url("{images[path]}");')
    return "\n".join(lines)


def get_styles(images: dict[str, str]) -> str:
    """Return the complete stylesheet for the embedded page."""
    css = _CSS.replace("__IMAGE_VARS__", _image_vars(images))
    return css


_CSS = r"""
/* =====================================================================
   THE TIDE REMEMBERS — cinematic digital diary
   ===================================================================== */

:root {
  --bg0: #04070c;
  --bg1: #07111c;
  --bg2: #0b1a2a;
  --ink: #eef3f8;
  --muted: #94a9bd;
  --line: rgba(238, 243, 248, 0.12);
  --aqua: #5cc7d6;
  --gold: #d6b478;
  --serif: "Playfair Display", Georgia, "Times New Roman", serif;
  --sans: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif;
  --pad: clamp(1.4rem, 5vw, 6rem);
  --ease-out: cubic-bezier(0.19, 1, 0.22, 1);
  --ease-soft: cubic-bezier(0.22, 1, 0.36, 1);
__IMAGE_VARS__
}

* { margin: 0; padding: 0; box-sizing: border-box; }

[hidden] { display: none !important; }

html {
  scroll-behavior: smooth;
  background: var(--bg0);
}

html, body { height: 100%; }

body {
  font-family: var(--sans);
  color: var(--ink);
  background:
    radial-gradient(130% 90% at 50% -15%, #0b2138 0%, rgba(11, 33, 56, 0) 55%),
    linear-gradient(180deg, #04070c 0%, #07111c 30%, #050d16 62%, #04070c 100%);
  background-attachment: fixed;
  overflow-x: hidden;
  min-height: 100%;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

button { font: inherit; color: inherit; background: none; border: 0; cursor: pointer; }
a { color: inherit; text-decoration: none; }
img { display: block; max-width: 100%; }

::selection { background: rgba(92, 199, 214, 0.35); color: #fff; }

::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: #05090f; }
::-webkit-scrollbar-thumb { background: #1b3247; border-radius: 9px; }
::-webkit-scrollbar-thumb:hover { background: #2a4b66; }

:focus-visible { outline: 2px solid var(--aqua); outline-offset: 3px; }

/* ---------------------------------------------------------------------
   Atmosphere — grain, ocean glow, vignette, opening veil
   --------------------------------------------------------------------- */

.grain {
  position: fixed;
  inset: -60%;
  width: 220%;
  height: 220%;
  pointer-events: none;
  z-index: 500;
  opacity: 0.055;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.72' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  animation: grain 1.1s steps(6) infinite;
}

@keyframes grain {
  0%   { transform: translate(0, 0); }
  20%  { transform: translate(-3%, 2%); }
  40%  { transform: translate(2%, -3%); }
  60%  { transform: translate(-2%, -2%); }
  80%  { transform: translate(3%, 3%); }
  100% { transform: translate(0, 0); }
}

.glow {
  position: fixed;
  border-radius: 50%;
  filter: blur(90px);
  pointer-events: none;
  z-index: 0;
}
.glow-a {
  width: 55vmax; height: 55vmax;
  top: -18vmax; left: -14vmax;
  background: radial-gradient(circle, rgba(19, 84, 118, 0.5), rgba(19, 84, 118, 0) 65%);
  opacity: 0.55;
  animation: drift-a 28s ease-in-out infinite alternate;
}
.glow-b {
  width: 48vmax; height: 48vmax;
  bottom: -16vmax; right: -12vmax;
  background: radial-gradient(circle, rgba(14, 96, 110, 0.42), rgba(14, 96, 110, 0) 65%);
  opacity: 0.5;
  animation: drift-b 34s ease-in-out infinite alternate;
}

@keyframes drift-a {
  from { transform: translate3d(0, 0, 0) scale(1); }
  to   { transform: translate3d(6vmax, 5vmax, 0) scale(1.12); }
}
@keyframes drift-b {
  from { transform: translate3d(0, 0, 0) scale(1.08); }
  to   { transform: translate3d(-5vmax, -4vmax, 0) scale(1); }
}

.vignette {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 480;
  background: radial-gradient(ellipse at 50% 50%, rgba(0, 0, 0, 0) 52%, rgba(0, 0, 0, 0.5) 100%);
}

.veil {
  position: fixed;
  inset: 0;
  z-index: 600;
  background: var(--bg0);
  pointer-events: none;
  animation: veil 1.4s var(--ease-soft) 0.15s forwards;
}
@keyframes veil { to { opacity: 0; visibility: hidden; } }

/* ---------------------------------------------------------------------
   Scroll progress hairline
   --------------------------------------------------------------------- */

.progress-line {
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 2px;
  z-index: 130;
  background: rgba(238, 243, 248, 0.06);
}
.progress-line i {
  display: block;
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--aqua), var(--gold));
  transition: width 0.12s linear;
}

/* ---------------------------------------------------------------------
   Top bar
   --------------------------------------------------------------------- */

.topbar {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 120;
  display: flex;
  align-items: center;
  gap: clamp(0.75rem, 2vw, 2rem);
  padding: 0.95rem var(--pad);
  background: linear-gradient(180deg, rgba(4, 7, 12, 0.82), rgba(4, 7, 12, 0));
  backdrop-filter: blur(2px);
  transition: background 0.5s ease, backdrop-filter 0.5s ease;
}
.topbar.scrolled {
  background: rgba(5, 9, 15, 0.78);
  backdrop-filter: blur(14px) saturate(1.2);
  border-bottom: 1px solid rgba(238, 243, 248, 0.07);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  flex-shrink: 0;
}
.brand svg { width: 22px; height: 14px; color: var(--aqua); opacity: 0.9; }
.brand span {
  font-family: var(--serif);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.24em;
  white-space: nowrap;
}

.topnav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: clamp(0.15rem, 1vw, 0.6rem);
  flex: 1;
}
.tn {
  position: relative;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.18em;
  color: rgba(238, 243, 248, 0.42);
  padding: 0.45rem 0.5rem;
  transition: color 0.35s ease;
}
.tn::after {
  content: "";
  position: absolute;
  left: 50%; bottom: 0.15rem;
  width: 0; height: 1px;
  background: var(--aqua);
  transform: translateX(-50%);
  transition: width 0.35s var(--ease-soft);
}
.tn:hover { color: var(--ink); }
.tn.active { color: var(--ink); }
.tn.active::after { width: 60%; }

.mini-play {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: rgba(238, 243, 248, 0.75);
  border: 1px solid rgba(238, 243, 248, 0.22);
  padding: 0.5rem 0.95rem;
  border-radius: 2px;
  transition: border-color 0.35s ease, color 0.35s ease, background 0.35s ease;
}
.mini-play svg { width: 9px; height: 10px; fill: currentColor; }
.mini-play:hover {
  color: #06121c;
  background: var(--ink);
  border-color: var(--ink);
}

.mini-add {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.22em;
  color: rgba(92, 199, 214, 0.92);
  border: 1px solid rgba(92, 199, 214, 0.42);
  padding: 0.5rem 0.95rem;
  border-radius: 2px;
  transition: border-color 0.35s ease, color 0.35s ease, background 0.35s ease;
}
.mini-add svg { width: 10px; height: 10px; }
.mini-add:hover {
  color: #04121a;
  background: var(--aqua);
  border-color: var(--aqua);
}

/* ---------------------------------------------------------------------
   Right-hand chapter rail
   --------------------------------------------------------------------- */

.rail {
  position: fixed;
  right: clamp(0.8rem, 1.6vw, 1.6rem);
  top: 50%;
  transform: translateY(-50%);
  z-index: 115;
  display: flex;
  flex-direction: column;
  gap: 1.05rem;
}
.rail-item {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.55rem;
  color: rgba(238, 243, 248, 0.34);
  transition: color 0.35s ease;
}
.rail-num {
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  opacity: 0;
  transform: translateX(6px);
  transition: opacity 0.35s ease, transform 0.35s var(--ease-soft);
}
.rail-line {
  display: block;
  width: 18px; height: 1px;
  background: currentColor;
  transition: width 0.4s var(--ease-soft);
}
.rail-tortoise {
  width: 17px; height: 11px;
  opacity: 0.55;
  transition: opacity 0.35s ease;
}
.rail-item:hover,
.rail-item.active { color: var(--aqua); }
.rail-item:hover .rail-num,
.rail-item.active .rail-num { opacity: 1; transform: translateX(0); }
.rail-item.active .rail-line { width: 30px; }
.rail-item.active .rail-tortoise { opacity: 1; }

/* ---------------------------------------------------------------------
   Hero
   --------------------------------------------------------------------- */

.hero {
  position: relative;
  min-height: 100vh;
  min-height: 100svh;
  display: flex;
  align-items: flex-end;
  overflow: hidden;
  isolation: isolate;
}

.hero-media { position: absolute; inset: 0; z-index: -2; overflow: hidden; }
.hero-img {
  position: absolute;
  inset: -4%;
  background-size: cover;
  background-position: center 38%;
  animation: kenburns 26s ease-in-out infinite alternate;
  will-change: transform;
}
@keyframes kenburns {
  from { transform: scale(1.02); }
  to   { transform: scale(1.13); }
}

.hero-scrim {
  position: absolute;
  inset: 0;
  z-index: -1;
  background:
    linear-gradient(100deg, rgba(4, 7, 12, 0.94) 0%, rgba(4, 7, 12, 0.72) 34%, rgba(4, 7, 12, 0.18) 64%, rgba(4, 7, 12, 0.42) 100%),
    linear-gradient(180deg, rgba(4, 7, 12, 0.7) 0%, rgba(4, 7, 12, 0) 26%, rgba(4, 7, 12, 0) 55%, rgba(4, 7, 12, 0.92) 100%);
}

.hero-content {
  position: relative;
  width: min(860px, 100%);
  padding: clamp(6.5rem, 14vh, 9rem) var(--pad) clamp(4.5rem, 11vh, 7rem);
}

.kicker {
  display: inline-flex;
  align-items: center;
  gap: 0.85rem;
  font-size: 0.66rem;
  font-weight: 600;
  letter-spacing: 0.38em;
  color: var(--aqua);
  margin-bottom: clamp(1.1rem, 2.5vh, 1.7rem);
  opacity: 0;
  animation: fade-up 1s var(--ease-soft) 0.45s forwards;
}
.kicker::before {
  content: "";
  width: 2.6rem; height: 1px;
  background: linear-gradient(90deg, var(--aqua), transparent);
}

.hero-title {
  font-family: var(--serif);
  font-weight: 600;
  font-size: clamp(2.7rem, 7.4vw, 6.4rem);
  line-height: 0.98;
  letter-spacing: 0.01em;
  text-wrap: balance;
}
.hero-title .l { display: block; overflow: hidden; padding-bottom: 0.06em; }
.hero-title .l > b {
  display: block;
  font-weight: 600;
  transform: translateY(112%);
  animation: hero-line 1.25s var(--ease-out) forwards;
}
.hero-title .l:nth-child(1) > b { animation-delay: 0.55s; }
.hero-title .l:nth-child(2) > b { animation-delay: 0.7s; }
.hero-title .l em {
  font-style: italic;
  color: transparent;
  background: linear-gradient(105deg, #f3f8fc 20%, #b9d9e4 55%, #d6b478 95%);
  -webkit-background-clip: text;
  background-clip: text;
}

@keyframes hero-line { to { transform: translateY(0); } }
@keyframes fade-up {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

.hero-sub {
  margin-top: clamp(1.1rem, 2.6vh, 1.7rem);
  max-width: 34rem;
  font-size: clamp(0.95rem, 1.35vw, 1.13rem);
  font-weight: 300;
  line-height: 1.7;
  color: var(--muted);
  opacity: 0;
  animation: fade-up 1s var(--ease-soft) 0.95s forwards;
}

.hero-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.55rem 0.95rem;
  margin-top: clamp(1.2rem, 3vh, 1.9rem);
  opacity: 0;
  animation: fade-up 1s var(--ease-soft) 1.15s forwards;
}
.hero-meta span {
  font-size: 0.63rem;
  font-weight: 600;
  letter-spacing: 0.26em;
  color: rgba(238, 243, 248, 0.6);
}
.hero-meta i {
  width: 3px; height: 3px;
  border-radius: 50%;
  background: rgba(238, 243, 248, 0.3);
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.85rem;
  margin-top: clamp(1.6rem, 4vh, 2.4rem);
  opacity: 0;
  animation: fade-up 1s var(--ease-soft) 1.35s forwards;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  padding: 1rem 1.9rem;
  border-radius: 2px;
  transition: transform 0.4s var(--ease-soft), box-shadow 0.4s ease,
              background 0.4s ease, border-color 0.4s ease, color 0.4s ease;
}
.btn svg { flex-shrink: 0; }
.btn-play {
  background: linear-gradient(135deg, #f6f9fc, #dce7f0);
  color: #06121c;
  box-shadow: 0 10px 34px rgba(0, 0, 0, 0.45);
}
.btn-play svg { width: 11px; height: 12px; fill: currentColor; }
.btn-play:hover {
  transform: translateY(-2px);
  box-shadow: 0 16px 44px rgba(92, 199, 214, 0.28);
}
.btn-ghost {
  border: 1px solid rgba(238, 243, 248, 0.3);
  color: var(--ink);
  background: rgba(238, 243, 248, 0.03);
  backdrop-filter: blur(6px);
}
.btn-ghost svg { width: 11px; height: 11px; stroke: currentColor; stroke-width: 2.2; }
.btn-ghost:hover {
  transform: translateY(-2px);
  border-color: var(--aqua);
  background: rgba(92, 199, 214, 0.1);
}

.scroll-cue {
  position: absolute;
  right: var(--pad);
  bottom: clamp(2.2rem, 6vh, 3.4rem);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.7rem;
  opacity: 0;
  animation: fade-up 1s var(--ease-soft) 1.8s forwards;
}
.scroll-cue span {
  font-size: 0.58rem;
  font-weight: 600;
  letter-spacing: 0.34em;
  color: rgba(238, 243, 248, 0.5);
  writing-mode: vertical-rl;
}
.scroll-cue i {
  width: 1px; height: 52px;
  background: linear-gradient(180deg, rgba(92, 199, 214, 0.9), transparent);
  overflow: hidden;
  position: relative;
}
.scroll-cue i::after {
  content: "";
  position: absolute;
  left: 0; top: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(180deg, transparent, #fff);
  animation: cue 2.2s ease-in-out infinite;
}
@keyframes cue { 0% { top: -100%; } 60%, 100% { top: 100%; } }

.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(190, 226, 236, 0.85);
  pointer-events: none;
  z-index: 1;
  animation: float-up linear infinite;
}
@keyframes float-up {
  0%   { transform: translateY(0) translateX(0); opacity: 0; }
  12%  { opacity: var(--o, 0.4); }
  100% { transform: translateY(-46vh) translateX(var(--dx, 12px)); opacity: 0; }
}

/* ---------------------------------------------------------------------
   Section intro (the diary timeline)
   --------------------------------------------------------------------- */

.section-intro {
  position: relative;
  padding: clamp(5rem, 13vh, 9rem) var(--pad) clamp(3rem, 8vh, 5.5rem);
  scroll-margin-top: 70px;
}
.si-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: clamp(2rem, 5vw, 5rem);
  align-items: end;
  max-width: 1400px;
  margin: 0 auto;
}
.si-heading {
  font-family: var(--serif);
  font-size: clamp(2.1rem, 4.6vw, 3.9rem);
  font-weight: 500;
  line-height: 1.08;
  margin-top: 1.1rem;
  white-space: pre-line;
}
.si-body {
  color: var(--muted);
  font-weight: 300;
  font-size: clamp(0.92rem, 1.15vw, 1.02rem);
  line-height: 1.85;
  max-width: 46ch;
}

.si-timeline {
  display: flex;
  gap: clamp(0.6rem, 1.6vw, 1.4rem);
  margin-top: clamp(1.6rem, 4vh, 2.6rem);
  border-top: 1px solid var(--line);
  padding-top: 1.1rem;
}
.si-tick {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  align-items: flex-start;
  color: rgba(238, 243, 248, 0.4);
  transition: color 0.35s ease;
}
.si-tick i {
  display: block;
  width: clamp(22px, 4vw, 46px);
  height: 2px;
  background: currentColor;
  opacity: 0.55;
  transition: opacity 0.35s ease, background 0.35s ease;
}
.si-tick span {
  font-size: 0.6rem;
  font-weight: 600;
  letter-spacing: 0.18em;
}
.si-tick:hover { color: var(--ink); }
.si-tick.on { color: var(--aqua); }
.si-tick.on i { opacity: 1; box-shadow: 0 0 12px rgba(92, 199, 214, 0.7); }

/* ---------------------------------------------------------------------
   Diary index — search, moods, the chronological list
   --------------------------------------------------------------------- */

.di-index {
  position: relative;
  max-width: 1400px;
  margin: clamp(2.6rem, 7vh, 4.5rem) auto 0;
  padding: clamp(1.3rem, 3vw, 2.1rem);
  border: 1px solid var(--line);
  border-radius: 4px;
  background: linear-gradient(180deg, rgba(11, 26, 42, 0.7), rgba(7, 17, 28, 0.45));
  backdrop-filter: blur(8px);
}
.di-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.di-search {
  flex: 1;
  min-width: 220px;
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.72rem 0.95rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  background: rgba(4, 7, 12, 0.55);
  transition: border-color 0.35s ease;
}
.di-search:focus-within { border-color: rgba(92, 199, 214, 0.55); }
.di-search svg { width: 14px; height: 14px; flex-shrink: 0; color: var(--muted); }
.di-search input {
  flex: 1;
  min-width: 0;
  background: none;
  border: 0;
  outline: none;
  color: var(--ink);
  font: inherit;
  font-size: 0.88rem;
}
.di-search input::placeholder { color: rgba(148, 169, 189, 0.6); }
.di-search input::-webkit-search-cancel-button { filter: invert(0.6); }
.di-count {
  font-size: 0.6rem;
  font-weight: 600;
  letter-spacing: 0.26em;
  color: var(--muted);
}
.di-count b { color: var(--aqua); font-weight: 700; }

.di-chips { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1.1rem; }
.di-chip {
  font-size: 0.56rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: rgba(238, 243, 248, 0.55);
  border: 1px solid var(--line);
  padding: 0.44rem 0.82rem;
  border-radius: 999px;
  transition: color 0.3s ease, border-color 0.3s ease, background 0.3s ease;
}
.di-chip:hover { color: var(--ink); border-color: rgba(238, 243, 248, 0.32); }
.di-chip.is-on { color: #04121a; background: var(--aqua); border-color: var(--aqua); }

.di-list { margin-top: 1.3rem; }
.di-year {
  padding: 1.3rem 0 0.45rem;
  border-bottom: 1px solid var(--line);
  font-size: 0.6rem;
  font-weight: 700;
  letter-spacing: 0.36em;
  color: var(--gold);
}
.di-list > .di-year:first-child { padding-top: 0; }
.di-month {
  padding: 1.05rem 0 0.35rem;
  font-size: 0.55rem;
  font-weight: 600;
  letter-spacing: 0.3em;
  color: rgba(148, 169, 189, 0.72);
}
.di-row {
  display: grid;
  grid-template-columns: 2.6rem minmax(0, 1fr) auto auto;
  align-items: center;
  gap: clamp(0.6rem, 1.6vw, 1.3rem);
  padding: 0.85rem 0.5rem;
  border-bottom: 1px solid rgba(238, 243, 248, 0.06);
  cursor: pointer;
  transition: background 0.3s ease, transform 0.4s var(--ease-soft);
}
.di-row:hover { background: rgba(92, 199, 214, 0.07); transform: translateX(5px); }
.di-row:focus-visible { outline: 1px solid var(--aqua); outline-offset: -1px; }
.di-num {
  font-family: var(--serif);
  font-size: 0.98rem;
  font-weight: 600;
  color: var(--aqua);
  opacity: 0.85;
}
.di-main { display: flex; flex-direction: column; gap: 0.3rem; min-width: 0; }
.di-title {
  font-family: var(--serif);
  font-size: clamp(1.02rem, 1.6vw, 1.24rem);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.di-sub {
  font-size: 0.58rem;
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.di-tags { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 0.4rem; }
.di-tag {
  font-style: normal;
  font-size: 0.52rem;
  font-weight: 600;
  letter-spacing: 0.16em;
  color: rgba(214, 180, 120, 0.88);
  border: 1px solid rgba(214, 180, 120, 0.3);
  padding: 0.26rem 0.52rem;
  border-radius: 999px;
}
.di-acts { display: flex; gap: 0.45rem; }
.di-act {
  font-size: 0.54rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: rgba(238, 243, 248, 0.55);
  border: 1px solid var(--line);
  padding: 0.42rem 0.72rem;
  border-radius: 2px;
  transition: color 0.3s ease, border-color 0.3s ease, background 0.3s ease;
}
.di-act:hover { color: var(--ink); border-color: rgba(238, 243, 248, 0.38); }
.di-act.is-danger:hover {
  color: #ffb3b3;
  border-color: rgba(255, 138, 138, 0.5);
  background: rgba(255, 90, 90, 0.1);
}
.di-empty { padding: clamp(2rem, 6vh, 3.5rem) 1rem; text-align: center; }
.di-empty-title {
  font-family: var(--serif);
  font-size: clamp(1.2rem, 3vw, 1.7rem);
  font-weight: 500;
}
.di-empty-body {
  margin-top: 0.55rem;
  color: var(--muted);
  font-weight: 300;
  font-size: 0.9rem;
}
.di-foot { display: flex; justify-content: center; margin-top: 1.6rem; }
.di-foot .di-add { width: auto; padding: 0.9rem 1.7rem; }
.di-foot .di-add svg { width: 11px; height: 12px; }

/* ---------------------------------------------------------------------
   Chapters — shared
   --------------------------------------------------------------------- */

.chapter {
  position: relative;
  scroll-margin-top: 64px;
}

.ch-label {
  display: inline-flex;
  align-items: center;
  gap: 0.7rem;
  font-size: 0.63rem;
  font-weight: 700;
  letter-spacing: 0.34em;
  color: var(--gold);
}
.ch-label::before {
  content: "";
  width: 1.6rem; height: 1px;
  background: currentColor;
  opacity: 0.7;
}

.ch-title {
  font-family: var(--serif);
  font-size: clamp(1.9rem, 4vw, 3.4rem);
  font-weight: 500;
  line-height: 1.1;
  margin-top: 0.9rem;
  text-wrap: balance;
}

.ch-caption {
  margin-top: 1.1rem;
  color: var(--muted);
  font-weight: 300;
  font-size: clamp(0.9rem, 1.1vw, 1rem);
  line-height: 1.85;
  max-width: 48ch;
}

.ch-num {
  font-family: var(--serif);
  font-weight: 700;
  line-height: 1;
  color: transparent;
  -webkit-text-stroke: 1px rgba(238, 243, 248, 0.14);
  user-select: none;
  pointer-events: none;
}

.ch-rule {
  width: 4.5rem; height: 1px;
  background: linear-gradient(90deg, var(--aqua), transparent);
  margin-top: 1.6rem;
}

.ch-label-sub {
  margin-top: 1.5rem;
  font-size: 0.57rem;
  letter-spacing: 0.3em;
  color: var(--aqua);
}
.ch-label-sub::before { background: var(--aqua); }

.ch-meta {
  margin-top: 0.9rem;
  font-size: 0.64rem;
  font-weight: 600;
  letter-spacing: 0.22em;
  color: rgba(214, 180, 120, 0.92);
}

.ch-story-wrap { max-width: 58ch; }
.ch-story p {
  color: rgba(238, 243, 248, 0.74);
  font-weight: 300;
  font-size: clamp(0.9rem, 1.1vw, 1rem);
  line-height: 1.9;
}
.ch-story p + p { margin-top: 1rem; }

/* Frames — photo presentation + hover */

.frame {
  position: relative;
  overflow: hidden;
  border-radius: 3px;
  background: var(--bg2);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.45);
  isolation: isolate;
}
.frame-bg {
  position: absolute;
  inset: -7%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: blur(30px) brightness(0.42) saturate(1.2);
}
.frame-media {
  position: absolute;
  inset: 0;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  transform: translateY(var(--py, 0px)) scale(var(--sc, 1.001));
  transition: transform 1.1s var(--ease-soft), filter 0.7s ease;
  will-change: transform;
}
.frame::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(4, 7, 12, 0) 48%, rgba(4, 7, 12, 0.55) 100%);
  opacity: 0.9;
  transition: opacity 0.6s ease;
  pointer-events: none;
}
.frame:hover .frame-media {
  --sc: 1.02;
  filter: brightness(1.07) saturate(1.06);
}
.frame:hover { box-shadow: 0 40px 100px rgba(0, 0, 0, 0.62); }
.frame:hover::after { opacity: 0.6; }

.frame-cap {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  z-index: 2;
  display: flex;
  align-items: baseline;
  gap: 0.8rem;
  padding: 1.1rem 1.3rem;
  background: linear-gradient(180deg, rgba(4, 7, 12, 0), rgba(4, 7, 12, 0.82));
  transform: translateY(102%);
  transition: transform 0.55s var(--ease-soft);
}
.frame:hover .frame-cap { transform: translateY(0); }
.fc-num {
  font-family: var(--serif);
  font-size: 0.85rem;
  color: var(--gold);
  letter-spacing: 0.1em;
}
.fc-title {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: rgba(238, 243, 248, 0.85);
}
.fc-tag {
  margin-left: auto;
  font-size: 0.58rem;
  letter-spacing: 0.22em;
  color: rgba(238, 243, 248, 0.45);
}

/* Layout: full-bleed (ch 01) */

.layout-full { padding: clamp(1.5rem, 4vh, 3rem) 0; }
.full-frame {
  position: relative;
  height: clamp(500px, 92vh, 1050px);
  border-radius: 0;
  box-shadow: none;
}
.full-frame .frame-cap { padding-left: var(--pad); padding-bottom: 1.4rem; }
.full-content {
  position: absolute;
  left: var(--pad);
  bottom: clamp(4.5rem, 11vh, 7.5rem);
  z-index: 3;
  max-width: min(640px, 82%);
}
.full-frame .ch-num {
  position: absolute;
  top: clamp(1.5rem, 5vh, 3.5rem);
  right: var(--pad);
  z-index: 2;
  font-size: clamp(5.5rem, 14vw, 12rem);
}

/* Layout: split (ch 02) */

.layout-split { padding: clamp(3rem, 8vh, 6rem) 0; }
.split-grid {
  display: grid;
  grid-template-columns: minmax(0, 43%) minmax(0, 57%);
  align-items: stretch;
  min-height: 84vh;
}
.split-text {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: clamp(2rem, 5vh, 4rem) clamp(1.6rem, 3.4vw, 3.4rem) clamp(2rem, 5vh, 4rem) var(--pad);
}
.split-text .ch-num {
  position: absolute;
  top: -0.15em;
  left: calc(var(--pad) - 0.06em);
  font-size: clamp(7rem, 15vw, 13rem);
  z-index: -1;
}
.split-text .ch-label,
.split-text .ch-title,
.split-text .ch-caption { position: relative; }
.split-frame { min-height: 84vh; border-radius: 3px 0 0 3px; }

/* Layout: overlap (ch 03) */

.layout-overlap { padding: clamp(3.5rem, 9vh, 7rem) 0 clamp(5rem, 12vh, 9rem); }
.overlap-wrap {
  position: relative;
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 var(--pad);
}
.overlap-frame {
  width: min(72%, 980px);
  height: clamp(420px, 72vh, 820px);
}
.glass-card {
  position: absolute;
  right: var(--pad);
  bottom: -2.5rem;
  width: min(430px, 46%);
  padding: clamp(1.5rem, 2.6vw, 2.3rem);
  background: linear-gradient(160deg, rgba(11, 26, 42, 0.86), rgba(5, 10, 17, 0.94));
  border: 1px solid rgba(238, 243, 248, 0.1);
  backdrop-filter: blur(16px) saturate(1.25);
  box-shadow: 0 34px 70px rgba(0, 0, 0, 0.55);
}
.glass-card .ch-title { font-size: clamp(1.5rem, 2.6vw, 2.2rem); }
.glass-card .ch-caption { margin-top: 0.85rem; font-size: 0.9rem; }
.vert-num {
  position: absolute;
  top: 0;
  right: calc(var(--pad) * 0.28);
  writing-mode: vertical-rl;
  font-family: var(--serif);
  font-size: clamp(4rem, 8vw, 7rem);
  font-weight: 700;
  color: transparent;
  -webkit-text-stroke: 1px rgba(238, 243, 248, 0.13);
  user-select: none;
  z-index: -1;
}

/* Layout: feature / tortoise chapter (ch 04) */

.layout-feature {
  padding: clamp(4.5rem, 12vh, 8.5rem) var(--pad);
  text-align: center;
}
.feature-head { max-width: 720px; margin: 0 auto; }
.feature-tortoise {
  width: 54px; height: 34px;
  color: var(--aqua);
  opacity: 0.9;
  margin: 0 auto 1.3rem;
  filter: drop-shadow(0 0 18px rgba(92, 199, 214, 0.45));
}
.feature-head .ch-label { justify-content: center; }
.feature-head .ch-label::after {
  content: "";
  width: 1.6rem; height: 1px;
  background: currentColor;
  opacity: 0.7;
}
.feature-head .ch-caption { margin-left: auto; margin-right: auto; }
.feature-frame {
  position: relative;
  max-width: 1280px;
  height: clamp(380px, 68vh, 780px);
  margin: clamp(2.4rem, 6vh, 4rem) auto 0;
  border: 1px solid rgba(238, 243, 248, 0.09);
}
.quote {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: clamp(2rem, 5vh, 3.2rem);
  padding: 0 var(--pad);
  font-family: var(--serif);
  font-style: italic;
  font-size: clamp(1.15rem, 2vw, 1.6rem);
  font-weight: 400;
  color: rgba(238, 243, 248, 0.88);
}
.quote svg { width: 26px; height: 17px; color: var(--gold); flex-shrink: 0; }

/* Layout: aside (ch 05) */

.layout-aside { padding: clamp(3rem, 8vh, 6rem) 0; }
.aside-grid {
  display: grid;
  grid-template-columns: minmax(0, 57%) minmax(0, 43%);
  align-items: stretch;
  min-height: 84vh;
}
.aside-frame {
  min-height: 84vh;
  border-radius: 0 3px 3px 0;
}
.aside-text {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: clamp(2rem, 6vh, 5rem) var(--pad) clamp(2rem, 6vh, 5rem) clamp(1.6rem, 3.4vw, 3.6rem);
}
.aside-text .ch-num {
  position: absolute;
  top: 0.1em;
  right: var(--pad);
  font-size: clamp(6.5rem, 13vw, 11rem);
}

/* Layout: finale (ch 06) */

.layout-finale { padding: clamp(1.5rem, 4vh, 3rem) 0 0; }
.finale-frame {
  position: relative;
  height: clamp(520px, 96vh, 1100px);
  border-radius: 0;
  box-shadow: none;
}
.finale-frame .frame-media { animation: none; }
.finale-frame::after {
  background:
    radial-gradient(ellipse at 50% 42%, rgba(4, 7, 12, 0.1) 0%, rgba(4, 7, 12, 0.72) 100%),
    linear-gradient(180deg, rgba(4, 7, 12, 0.55) 0%, rgba(4, 7, 12, 0.1) 30%, rgba(4, 7, 12, 0.96) 100%);
  opacity: 1;
}
.finale-content {
  position: absolute;
  inset: 0;
  z-index: 3;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  text-align: center;
  padding: var(--pad) var(--pad) clamp(5rem, 14vh, 9rem);
}
.finale-content .ch-label { justify-content: center; }
.finale-content .ch-title { font-size: clamp(2.2rem, 5.4vw, 4.6rem); }
.finale-content .ch-caption {
  margin-left: auto; margin-right: auto;
  max-width: 44ch;
  color: rgba(238, 243, 248, 0.75);
}
.finale-content .ch-num {
  position: absolute;
  bottom: clamp(1.5rem, 5vh, 3rem);
  right: var(--pad);
  font-size: clamp(5rem, 12vw, 10rem);
}

.closing {
  text-align: center;
  padding: clamp(3.5rem, 9vh, 6.5rem) var(--pad) clamp(2rem, 5vh, 3.5rem);
  max-width: 780px;
  margin: 0 auto;
}
.closing-tortoise { width: 40px; height: 25px; color: var(--aqua); opacity: 0.75; margin: 0 auto 1.4rem; }
.closing-line {
  font-family: var(--serif);
  font-size: clamp(1.25rem, 2.4vw, 1.8rem);
  font-weight: 400;
  font-style: italic;
  line-height: 1.55;
  color: rgba(238, 243, 248, 0.9);
}

/* Anniversary dedication */

.dedication {
  position: relative;
  text-align: center;
  max-width: 920px;
  margin: 0 auto;
  padding: clamp(2.5rem, 7vh, 5rem) var(--pad) clamp(3rem, 8vh, 5.5rem);
}
.dedication::before {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse at 50% 50%, rgba(92, 199, 214, 0.08), transparent 68%);
  pointer-events: none;
}
.ded-kicker {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.9rem;
  font-size: clamp(0.6rem, 1.4vw, 0.68rem);
  font-weight: 700;
  letter-spacing: 0.4em;
  color: var(--gold);
}
.ded-kicker::before,
.ded-kicker::after {
  content: "";
  width: clamp(1.6rem, 5vw, 3rem);
  height: 1px;
}
.ded-kicker::before { background: linear-gradient(90deg, transparent, var(--gold)); }
.ded-kicker::after { background: linear-gradient(90deg, var(--gold), transparent); }
.ded-line {
  position: relative;
  margin-top: clamp(1.2rem, 3vh, 1.8rem);
  font-family: var(--serif);
  font-style: italic;
  font-weight: 500;
  font-size: clamp(1.5rem, 3.4vw, 2.6rem);
  line-height: 1.45;
  color: var(--ink);
  text-wrap: balance;
}

/* Footer */

.site-footer {
  padding: clamp(2rem, 5vh, 3.2rem) var(--pad) clamp(2.4rem, 6vh, 3.6rem);
}
.footer-rule {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(238, 243, 248, 0.16), transparent);
  margin-bottom: clamp(1.6rem, 4vh, 2.4rem);
}
.footer-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem 2rem;
  max-width: 1440px;
  margin: 0 auto;
}
.footer-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  font-family: var(--serif);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.22em;
}
.footer-brand svg { width: 18px; height: 12px; color: var(--aqua); opacity: 0.8; }
.footer-meta {
  font-size: 0.6rem;
  font-weight: 600;
  letter-spacing: 0.26em;
  color: rgba(238, 243, 248, 0.42);
}
.footer-tick {
  font-size: 0.6rem;
  letter-spacing: 0.2em;
  color: rgba(238, 243, 248, 0.35);
  transition: color 0.3s ease;
}
.footer-tick:hover { color: var(--aqua); }

/* ---------------------------------------------------------------------
   Reveal on scroll
   --------------------------------------------------------------------- */

.reveal {
  opacity: 0;
  transform: translateY(30px);
  filter: blur(7px);
  transition:
    opacity 1.05s var(--ease-soft),
    transform 1.05s var(--ease-soft),
    filter 1.05s var(--ease-soft);
  transition-delay: var(--d, 0s);
  will-change: opacity, transform;
}
.reveal.in {
  opacity: 1;
  transform: translateY(0);
  filter: blur(0);
}

/* ---------------------------------------------------------------------
   Story mode (full-screen cinematic player)
   --------------------------------------------------------------------- */

.story {
  position: fixed;
  inset: 0;
  z-index: 400;
  background: #030609;
  opacity: 0;
  visibility: hidden;
  transform: scale(1.02);
  transition: opacity 0.7s var(--ease-soft), transform 0.7s var(--ease-soft), visibility 0.7s;
}
.story.open {
  opacity: 1;
  visibility: visible;
  transform: scale(1);
}

.story-slides { position: absolute; inset: 0; overflow: hidden; }
.story-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 1s ease;
  transform: scale(1.035);
}
.story-slide.active { opacity: 1; transform: scale(1); transition: opacity 1s ease, transform 6.5s linear; }
.story-bg {
  position: absolute;
  inset: -6%;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  filter: blur(34px) brightness(0.4) saturate(1.2);
}
.story-img {
  position: absolute;
  inset: 0;
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
}
.story-slide.active .story-img { animation: story-zoom 7.5s ease-out forwards; }
@keyframes story-zoom {
  from { transform: scale(1.0); }
  to   { transform: scale(1.09); }
}

.story-fade {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    linear-gradient(180deg, rgba(3, 6, 9, 0.78) 0%, rgba(3, 6, 9, 0) 24%, rgba(3, 6, 9, 0) 40%, rgba(3, 6, 9, 0.88) 88%),
    radial-gradient(ellipse at 50% 55%, rgba(3, 6, 9, 0) 40%, rgba(3, 6, 9, 0.5) 100%);
}

.story-ui { position: absolute; inset: 0; display: flex; flex-direction: column; }

.story-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: clamp(1.1rem, 3vh, 1.8rem) var(--pad) 0;
}
.story-brand {
  display: inline-flex;
  align-items: center;
  gap: 0.6rem;
  font-family: var(--serif);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.26em;
  color: rgba(238, 243, 248, 0.8);
}
.story-brand svg { width: 20px; height: 13px; color: var(--aqua); }
.story-close {
  width: 42px; height: 42px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(238, 243, 248, 0.25);
  border-radius: 50%;
  color: var(--ink);
  transition: border-color 0.35s ease, background 0.35s ease, transform 0.35s ease;
}
.story-close svg { width: 13px; height: 13px; stroke: currentColor; stroke-width: 2; }
.story-close:hover { border-color: var(--aqua); background: rgba(92, 199, 214, 0.12); transform: rotate(90deg); }

.story-bars {
  display: flex;
  gap: 6px;
  padding: clamp(1rem, 3vh, 1.7rem) var(--pad) 0;
}
.sbar {
  flex: 1;
  height: 2px;
  background: rgba(238, 243, 248, 0.18);
  overflow: hidden;
  border-radius: 2px;
}
.sbar-fill {
  display: block;
  height: 100%;
  width: 0%;
  background: linear-gradient(90deg, var(--aqua), #eaf7fa);
}
.sbar.done .sbar-fill { width: 100%; background: rgba(238, 243, 248, 0.75); }

.story-center {
  margin-top: auto;
  padding: 0 var(--pad) clamp(7.5rem, 20vh, 11rem);
  max-width: 860px;
}
.story-chap {
  font-size: 0.64rem;
  font-weight: 700;
  letter-spacing: 0.38em;
  color: var(--gold);
}
.story-title {
  font-family: var(--serif);
  font-size: clamp(2rem, 5.4vw, 4.2rem);
  font-weight: 500;
  line-height: 1.06;
  margin-top: 0.7rem;
}
.story-text {
  margin-top: 1rem;
  max-width: 52ch;
  font-weight: 300;
  font-size: clamp(0.92rem, 1.3vw, 1.1rem);
  line-height: 1.8;
  color: rgba(238, 243, 248, 0.78);
}

.story-center.anim .story-chap { animation: story-rise 0.75s var(--ease-out) 0.15s both; }
.story-center.anim .story-title { animation: story-rise 0.85s var(--ease-out) 0.3s both; }
.story-center.anim .story-text  { animation: story-rise 0.9s var(--ease-out) 0.5s both; }
@keyframes story-rise {
  from { opacity: 0; transform: translateY(26px); filter: blur(6px); }
  to   { opacity: 1; transform: translateY(0); filter: blur(0); }
}

.story-bottom {
  position: absolute;
  left: 0; right: 0; bottom: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 0 var(--pad) clamp(1.3rem, 4vh, 2.2rem);
}
.story-controls { display: flex; align-items: center; gap: 0.7rem; }
.sctrl {
  width: 46px; height: 46px;
  display: grid;
  place-items: center;
  border: 1px solid rgba(238, 243, 248, 0.28);
  border-radius: 50%;
  color: var(--ink);
  background: rgba(4, 7, 12, 0.4);
  backdrop-filter: blur(8px);
  transition: border-color 0.3s ease, background 0.3s ease, transform 0.3s ease;
}
.sctrl svg { width: 13px; height: 13px; fill: currentColor; }
.sctrl:hover { border-color: var(--aqua); background: rgba(92, 199, 214, 0.16); transform: scale(1.06); }
.sctrl.main { width: 54px; height: 54px; background: rgba(238, 243, 248, 0.94); color: #06121c; border: none; }
.sctrl.main svg { width: 15px; height: 15px; }
.sctrl.main:hover { background: #fff; }

.story-count {
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 0.26em;
  color: rgba(238, 243, 248, 0.6);
}
.story-count b { color: var(--ink); font-weight: 700; }

.story-center,
.story-bottom { transition: opacity 0.6s ease; }
.story.ended .story-center,
.story.ended .story-bottom { opacity: 0; pointer-events: none; }

/* End card */

.story-end {
  position: absolute;
  inset: 0;
  z-index: 5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: var(--pad);
  background: radial-gradient(ellipse at 50% 60%, rgba(9, 24, 38, 0.94), rgba(3, 6, 9, 0.985));
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.9s ease, visibility 0.9s;
}
.story-end.show { opacity: 1; visibility: visible; }
.se-tortoise { width: 64px; height: 40px; color: var(--aqua); margin-bottom: 1.6rem; filter: drop-shadow(0 0 22px rgba(92, 199, 214, 0.5)); }
.se-kicker {
  font-size: 0.64rem;
  font-weight: 700;
  letter-spacing: 0.4em;
  color: var(--gold);
}
.se-title {
  font-family: var(--serif);
  font-size: clamp(2.2rem, 6vw, 4.6rem);
  font-weight: 500;
  margin-top: 0.9rem;
}
.se-body {
  margin-top: 1.1rem;
  max-width: 40ch;
  font-weight: 300;
  line-height: 1.8;
  color: var(--muted);
}
.se-actions { display: flex; flex-wrap: wrap; gap: 0.85rem; justify-content: center; margin-top: 2.2rem; }
.se-quote {
  margin-top: 2.6rem;
  font-family: var(--serif);
  font-style: italic;
  font-size: 1.02rem;
  color: rgba(238, 243, 248, 0.55);
}
.se-ded {
  margin-top: 1.5rem;
  max-width: 46ch;
  font-family: var(--serif);
  font-style: italic;
  font-size: clamp(1.02rem, 1.7vw, 1.3rem);
  line-height: 1.65;
  color: var(--gold);
  text-wrap: balance;
}

/* ---------------------------------------------------------------------
   Memory dialog + toast
   --------------------------------------------------------------------- */

.mm {
  position: fixed;
  inset: 0;
  z-index: 400;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: clamp(0.7rem, 3vh, 2.5rem);
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.4s ease, visibility 0.4s;
}
.mm.open { opacity: 1; visibility: visible; }
.mm-veil {
  position: absolute;
  inset: 0;
  background: rgba(3, 6, 10, 0.84);
  backdrop-filter: blur(9px);
}
.mm-card {
  position: relative;
  width: min(740px, 100%);
  max-height: 100%;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(238, 243, 248, 0.14);
  border-radius: 5px;
  background: linear-gradient(180deg, rgba(11, 26, 42, 0.985), rgba(5, 11, 18, 0.995));
  box-shadow: 0 44px 110px rgba(0, 0, 0, 0.72);
  transform: translateY(20px) scale(0.985);
  transition: transform 0.5s var(--ease-out);
}
.mm.open .mm-card { transform: none; }

.mm-del-card {
  width: min(520px, 100%);
  padding: clamp(1.7rem, 4vw, 2.5rem);
  text-align: center;
}
.mm-del-card .mm-kicker { justify-content: center; color: #ff9a9a; }
.mm-del-card .mm-heading { font-size: clamp(1.35rem, 3vw, 1.8rem); }
.mm-del-body {
  margin-top: 0.9rem;
  color: var(--muted);
  font-weight: 300;
  font-size: 0.9rem;
  line-height: 1.75;
}

.mm-head { position: relative; padding: clamp(1.5rem, 3vw, 2.1rem) clamp(1.4rem, 3vw, 2.2rem) 0; }
.mm-kicker { font-size: 0.57rem; font-weight: 700; letter-spacing: 0.34em; color: var(--gold); }
.mm-heading {
  font-family: var(--serif);
  font-weight: 500;
  font-size: clamp(1.5rem, 3.4vw, 2.1rem);
  line-height: 1.15;
  margin-top: 0.5rem;
}
.mm-x {
  position: absolute;
  top: clamp(1.1rem, 3vw, 1.7rem);
  right: clamp(1.1rem, 3vw, 1.7rem);
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 50%;
  color: var(--muted);
  transition: color 0.3s ease, border-color 0.3s ease, transform 0.45s var(--ease-soft);
}
.mm-x svg { width: 12px; height: 12px; stroke: currentColor; stroke-width: 1.6; }
.mm-x:hover { color: var(--ink); border-color: rgba(238, 243, 248, 0.42); transform: rotate(90deg); }

.mm-scroll { overflow-y: auto; padding: 1.5rem clamp(1.4rem, 3vw, 2.2rem) 0.4rem; }
.mm-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.05rem 1.15rem; }
.mm-wide { grid-column: 1 / -1; }
.mm-f { display: flex; flex-direction: column; gap: 0.45rem; min-width: 0; }
.mm-f > span {
  font-size: 0.54rem;
  font-weight: 700;
  letter-spacing: 0.26em;
  color: rgba(148, 169, 189, 0.95);
}
.mm-f > span i { font-style: normal; letter-spacing: 0.12em; opacity: 0.6; }
.mm-f input,
.mm-f textarea {
  width: 100%;
  background: rgba(4, 7, 12, 0.55);
  border: 1px solid var(--line);
  border-radius: 3px;
  color: var(--ink);
  font: inherit;
  font-size: 0.92rem;
  padding: 0.72rem 0.85rem;
  outline: none;
  resize: vertical;
  transition: border-color 0.3s ease, background 0.3s ease;
}
.mm-f input:focus,
.mm-f textarea:focus {
  border-color: rgba(92, 199, 214, 0.62);
  background: rgba(6, 14, 24, 0.82);
}
.mm-f textarea { line-height: 1.7; font-weight: 300; }
.mm-f input[type="date"] { color-scheme: dark; }
.mm-f input::placeholder,
.mm-f textarea::placeholder { color: rgba(148, 169, 189, 0.45); }

.mm-moods { display: flex; flex-wrap: wrap; gap: 0.45rem; }
.mm-mood {
  font-size: 0.54rem;
  font-weight: 700;
  letter-spacing: 0.18em;
  color: rgba(238, 243, 248, 0.55);
  border: 1px solid var(--line);
  padding: 0.44rem 0.74rem;
  border-radius: 999px;
  transition: color 0.3s ease, border-color 0.3s ease, background 0.3s ease;
}
.mm-mood:hover { color: var(--ink); border-color: rgba(238, 243, 248, 0.35); }
.mm-mood.is-on { color: #04121a; background: var(--gold); border-color: var(--gold); }

.mm-pick {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  font-size: 0.62rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: var(--aqua);
  border: 1px dashed rgba(92, 199, 214, 0.48);
  padding: 1.15rem 1.35rem;
  border-radius: 3px;
  transition: background 0.3s ease, border-color 0.3s ease;
}
.mm-pick svg { width: 12px; height: 12px; }
.mm-pick:hover { background: rgba(92, 199, 214, 0.1); border-color: var(--aqua); }

.mm-prev { display: flex; gap: 1rem; align-items: center; }
.mm-prev-img {
  width: 176px;
  height: 110px;
  flex-shrink: 0;
  background-color: var(--bg2);
  background-size: cover;
  background-position: center;
  border: 1px solid var(--line);
  border-radius: 3px;
}
.mm-prev-side { display: flex; flex-direction: column; gap: 0.6rem; align-items: flex-start; }
.mm-prev-meta { font-size: 0.55rem; font-weight: 700; letter-spacing: 0.24em; color: var(--aqua); }
.mm-prev-x {
  font-size: 0.55rem;
  font-weight: 700;
  letter-spacing: 0.2em;
  color: rgba(255, 154, 154, 0.95);
  border: 1px solid rgba(255, 138, 138, 0.35);
  padding: 0.44rem 0.78rem;
  border-radius: 2px;
  transition: background 0.3s ease, border-color 0.3s ease;
}
.mm-prev-x:hover { background: rgba(255, 90, 90, 0.14); border-color: rgba(255, 138, 138, 0.7); }

.mm-error {
  margin-top: 1.05rem;
  padding: 0.72rem 0.95rem;
  border: 1px solid rgba(255, 138, 138, 0.34);
  border-radius: 3px;
  background: rgba(255, 90, 90, 0.1);
  color: #ffb3b3;
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.03em;
}

.mm-foot {
  display: flex;
  justify-content: flex-end;
  gap: 0.8rem;
  padding: clamp(1.3rem, 3vw, 1.8rem) clamp(1.4rem, 3vw, 2.2rem);
}
.mm-foot .btn { width: auto; padding: 0.88rem 1.55rem; font-size: 0.66rem; }
.mm-foot .btn:disabled,
.btn-danger:disabled { opacity: 0.55; cursor: progress; transform: none; }
.btn-danger {
  border: 1px solid rgba(255, 138, 138, 0.5);
  background: rgba(255, 90, 90, 0.16);
  color: #ffc4c4;
}
.btn-danger:hover {
  border-color: rgba(255, 138, 138, 0.85);
  background: rgba(255, 90, 90, 0.3);
  color: #fff;
}

.tide-toast {
  position: fixed;
  left: 50%;
  bottom: clamp(1.2rem, 4vh, 2.6rem);
  z-index: 500;
  max-width: min(540px, calc(100% - 2rem));
  padding: 0.88rem 1.35rem;
  border: 1px solid rgba(92, 199, 214, 0.5);
  border-radius: 3px;
  background: rgba(9, 24, 38, 0.97);
  box-shadow: 0 26px 64px rgba(0, 0, 0, 0.62);
  color: var(--ink);
  font-size: 0.72rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-align: center;
  opacity: 0;
  visibility: hidden;
  transform: translate(-50%, 26px);
  transition: opacity 0.4s ease, visibility 0.4s, transform 0.5s var(--ease-out);
}
.tide-toast.show { opacity: 1; visibility: visible; transform: translate(-50%, 0); }
.tide-toast.is-error { border-color: rgba(255, 138, 138, 0.55); color: #ffc4c4; }

/* ---------------------------------------------------------------------
   Responsive
   --------------------------------------------------------------------- */

@media (max-width: 1100px) {
  .rail { display: none; }
}

@media (max-width: 900px) {
  .si-grid { grid-template-columns: 1fr; align-items: start; }
  .split-grid,
  .aside-grid { grid-template-columns: 1fr; min-height: 0; }
  .split-text,
  .aside-text { padding: clamp(2.4rem, 6vh, 3.5rem) var(--pad); }
  .split-text .ch-num { position: static; font-size: clamp(4.5rem, 18vw, 7rem); margin-bottom: -0.28em; }
  .aside-text { order: 2; justify-content: flex-start; }
  .aside-frame { order: 1; min-height: clamp(400px, 72vh, 640px); border-radius: 0; }
  .aside-text .ch-num { position: static; font-size: clamp(4.5rem, 18vw, 7rem); margin-bottom: -0.28em; }
  .split-frame { min-height: clamp(400px, 70vh, 620px); border-radius: 0; }
  .overlap-frame { width: 100%; height: clamp(380px, 62vh, 560px); }
  .glass-card {
    position: relative;
    right: auto; bottom: auto;
    width: calc(100% - 1.4rem);
    margin: -3.5rem auto 0;
  }
  .vert-num { display: none; }
  .hero { align-items: flex-end; }
  .hero-content { padding-bottom: clamp(5.5rem, 14vh, 7rem); }
  .scroll-cue { display: none; }
  .full-content { max-width: 88%; bottom: clamp(3.5rem, 9vh, 5rem); }
  .frame-cap { transform: translateY(0); background: linear-gradient(180deg, rgba(4, 7, 12, 0), rgba(4, 7, 12, 0.78)); }
  .fc-tag { display: none; }
  .di-row { grid-template-columns: 2.3rem minmax(0, 1fr) auto; }
  .di-tags { display: none; }
  .mm-grid { grid-template-columns: 1fr; }
  .mm-prev-img { width: 132px; height: 88px; }
}

@media (max-width: 640px) {
  .brand span { display: none; }
  .topbar { padding: 0.75rem clamp(0.9rem, 4vw, 1.4rem); gap: 0.5rem; }
  .tn { font-size: 0.62rem; padding: 0.4rem 0.34rem; letter-spacing: 0.12em; }
  .mini-play { padding: 0.45rem 0.7rem; font-size: 0.6rem; }
  .mini-play span { display: none; }
  .mini-add { padding: 0.45rem 0.7rem; font-size: 0.6rem; }
  .mini-add span { display: none; }
  .di-head { flex-direction: column; align-items: stretch; }
  .di-search { min-width: 0; }
  .di-row {
    grid-template-columns: 2.1rem minmax(0, 1fr);
    row-gap: 0.55rem;
    padding: 0.9rem 0.3rem;
  }
  .di-acts { grid-column: 2; justify-self: start; }
  .di-foot .di-add { width: 100%; }
  .mm { padding: 0; align-items: stretch; }
  .mm-card {
    width: 100%;
    max-height: 100dvh;
    border-radius: 0;
    border: none;
    box-shadow: none;
  }
  .mm-del-card { padding: clamp(1.6rem, 7vw, 2.2rem); }
  .mm-foot .btn { flex: 1; padding: 0.95rem 1rem; }
  .mm-prev { flex-direction: column; align-items: stretch; }
  .mm-prev-img { width: 100%; height: clamp(150px, 34vw, 210px); }
  .hero-meta span { font-size: 0.56rem; letter-spacing: 0.2em; }
  .btn { width: 100%; padding: 0.95rem 1.4rem; }
  .hero-actions { flex-direction: column; align-items: stretch; }
  .si-timeline { flex-wrap: wrap; row-gap: 0.9rem; }
  .full-frame, .finale-frame { height: clamp(460px, 88vh, 760px); }
  .full-content { left: clamp(1.1rem, 5vw, 1.6rem); right: clamp(1.1rem, 5vw, 1.6rem); max-width: none; }
  .full-frame .ch-num { right: clamp(1.1rem, 5vw, 1.6rem); }
  .story-center { padding-bottom: clamp(8.5rem, 24vh, 12rem); }
  .story-bottom { flex-direction: row; }
  .footer-row { flex-direction: column; align-items: flex-start; gap: 0.7rem; }
  .ded-kicker { font-size: 0.56rem; letter-spacing: 0.2em; gap: 0.6rem; }
  .ded-kicker::before,
  .ded-kicker::after { width: 1.1rem; }
  .ded-line { font-size: clamp(1.3rem, 5.6vw, 1.7rem); }
}

/* ---------------------------------------------------------------------
   Reduced motion
   --------------------------------------------------------------------- */

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .reveal { opacity: 1; transform: none; filter: none; }
  .veil { display: none; }
}
"""
