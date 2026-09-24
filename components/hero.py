"""Landing hero — the full-screen cinematic title card."""

from __future__ import annotations

from html import escape

from components.svg import PLAY_SVG, PLUS_SVG

# left%, top%, size px, duration s, drift px, opacity
_PARTICLES = [
    (7, 74, 3, 15, -18, 0.5),
    (15, 58, 2, 19, 12, 0.35),
    (23, 80, 4, 16, -10, 0.4),
    (34, 64, 2, 21, 15, 0.3),
    (46, 78, 3, 14, -13, 0.45),
    (57, 57, 2, 20, 11, 0.3),
    (66, 75, 3, 17, -16, 0.4),
    (75, 54, 2, 22, 13, 0.3),
    (84, 71, 4, 16, -12, 0.4),
    (92, 61, 2, 18, 10, 0.35),
]


def _stem(path: str) -> str:
    return path.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()


def render_hero(site: dict) -> str:
    title = escape(site["title_lines"][0])
    title2 = escape(site["title_lines"][1])
    kicker = escape(site["kicker"])
    subtitle = escape(site["subtitle"])
    play_label = escape(site["play_label"])
    explore_label = escape(site["explore_label"])
    brand = escape(site["brand"])

    meta = '<i aria-hidden="true"></i>'.join(
        f"<span>{escape(m)}</span>" for m in site["meta"]
    )

    particles = "\n".join(
        f'<span class="particle" aria-hidden="true" style="left:{x}%;top:{y}%;'
        f'width:{s}px;height:{s}px;animation-duration:{d}s;animation-delay:-{d * 0.6:.1f}s;'
        f'--dx:{dx}px;--o:{o}"></span>'
        for x, y, s, d, dx, o in _PARTICLES
    )

    return f"""
<section class="hero" id="hero" aria-label="{brand} — opening title">
  <div class="hero-media" aria-hidden="true">
    <div class="hero-img" style="background-image:var(--img-{_stem(site['hero_image'])})"></div>
  </div>
  <div class="hero-scrim" aria-hidden="true"></div>
  {particles}
  <div class="hero-content">
    <div class="kicker">{kicker}</div>
    <h1 class="hero-title">
      <span class="l"><b>{title}</b></span>
      <span class="l"><b><em>{title2}</em></b></span>
    </h1>
    <p class="hero-sub">{subtitle}</p>
    <div class="hero-meta">{meta}</div>
    <div class="hero-actions">
      <button class="btn btn-play" type="button" data-play-story>
        {PLAY_SVG}<span>{play_label}</span>
      </button>
      <button class="btn btn-ghost" type="button" data-goto="diary">
        {PLUS_SVG}<span>{explore_label}</span>
      </button>
    </div>
  </div>
  <div class="scroll-cue" aria-hidden="true"><span>SCROLL</span><i></i></div>
</section>
"""
