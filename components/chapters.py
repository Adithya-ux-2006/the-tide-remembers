"""Chapter presentation — navigation, timeline, and the six photo layouts."""

from __future__ import annotations

from html import escape

from components.svg import PLAY_SVG, TORTOISE_SVG

# ---------------------------------------------------------------------------
# Page furniture
# ---------------------------------------------------------------------------


def render_atmosphere() -> str:
    """Fixed background layers: grain, ocean glows, vignette, opening veil."""
    return (
        '<div class="veil" aria-hidden="true"></div>'
        '<div class="glow glow-a" aria-hidden="true"></div>'
        '<div class="glow glow-b" aria-hidden="true"></div>'
        '<div class="grain" aria-hidden="true"></div>'
        '<div class="vignette" aria-hidden="true"></div>'
        '<div class="progress-line" aria-hidden="true"><i id="progressFill"></i></div>'
    )


def render_topbar(site: dict) -> str:
    brand = escape(site["brand"])
    nav = "".join(
        f'<button class="tn" type="button" data-goto="{i}" '
        f'aria-label="Chapter {i:02d}">{i:02d}</button>'
        for i in range(1, 7)
    )
    return f"""
<header class="topbar" id="topbar">
  <a class="brand" href="#hero" data-goto="hero" aria-label="{brand} — back to top">
    {TORTOISE_SVG}<span>{brand}</span>
  </a>
  <nav class="topnav" aria-label="Chapter navigation">{nav}</nav>
  <button class="mini-play" type="button" data-play-story aria-label="Play story">
    {PLAY_SVG}<span>PLAY</span>
  </button>
</header>
"""


def render_rail(entries: list[dict]) -> str:
    """Vertical chapter rail — chapter 04 is marked with the tortoise."""
    items = []
    for i, entry in enumerate(entries, start=1):
        marker = (
            f'<span class="rail-tortoise" aria-hidden="true">{TORTOISE_SVG}</span>'
            if entry["layout"] == "feature"
            else '<span class="rail-line" aria-hidden="true"></span>'
        )
        items.append(
            f'<button class="rail-item" type="button" data-goto="{i}" '
            f'aria-label="Chapter {entry["chapter"]}: {escape(entry["title"])}">'
            f'<span class="rail-num">{entry["chapter"]}</span>{marker}</button>'
        )
    return f'<nav class="rail" aria-label="Story progress">{"".join(items)}</nav>'


def render_intro(site: dict, entries: list[dict]) -> str:
    label = escape(site["intro_label"])
    heading = escape(site["intro_heading"])
    body = escape(site["intro_body"])
    ticks = "".join(
        f'<button class="si-tick" type="button" data-goto="{i}" '
        f'aria-label="Go to chapter {e["chapter"]}">'
        f'<i aria-hidden="true"></i><span>{e["chapter"]}</span></button>'
        for i, e in enumerate(entries, start=1)
    )
    return f"""
<section class="section-intro" id="diary" aria-label="{label}">
  <div class="si-grid">
    <div class="si-left reveal">
      <div class="ch-label">{label}</div>
      <h2 class="si-heading">{heading}</h2>
    </div>
    <div class="si-right reveal" style="--d:.14s">
      <p class="si-body">{body}</p>
      <div class="si-timeline" role="group" aria-label="Timeline of chapters">{ticks}</div>
    </div>
  </div>
</section>
"""


def render_footer(site: dict) -> str:
    meta = escape(site["footer_meta"])
    brand = escape(site["brand"])
    return f"""
<footer class="site-footer">
  <div class="footer-rule" aria-hidden="true"></div>
  <div class="footer-row">
    <span class="footer-brand">{TORTOISE_SVG}{brand}</span>
    <button class="footer-tick" type="button" data-goto="hero">BACK TO TOP</button>
    <span class="footer-meta">{meta}</span>
  </div>
</footer>
"""


# ---------------------------------------------------------------------------
# Shared chapter pieces
# ---------------------------------------------------------------------------


def _stem(path: str) -> str:
    return path.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()


def _media(entry: dict) -> str:
    title = escape(entry["title"])
    return (
        f'<div class="frame-media" role="img" aria-label="Chapter {entry["chapter"]}: '
        f'{title}" style="background-image:var(--img-{_stem(entry["image"])})"></div>'
    )


def _cap(entry: dict) -> str:
    return (
        f'<figcaption class="frame-cap">'
        f'<span class="fc-num">{entry["chapter"]}</span>'
        f'<span class="fc-title">{escape(entry["title"])}</span>'
        f'<span class="fc-tag">CHAPTER {entry["chapter"]}</span></figcaption>'
    )


def _label(entry: dict) -> str:
    return f'<div class="ch-label">CHAPTER {entry["chapter"]}</div>'


def _title(entry: dict, tid: str) -> str:
    return f'<h2 class="ch-title" id="{tid}">{escape(entry["title"])}</h2>'


def _caption(entry: dict) -> str:
    return f'<p class="ch-caption">{escape(entry["caption"])}</p>'


# ---------------------------------------------------------------------------
# The six layouts
# ---------------------------------------------------------------------------


def _layout_full(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-full" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="frame full-frame reveal" data-parallax>
    {_media(entry)}
    <div class="ch-num" aria-hidden="true">{entry["chapter"]}</div>
    <div class="full-content">
      {_label(entry)}{_title(entry, tid)}{_caption(entry)}
    </div>
    {_cap(entry)}
  </div>
</section>
"""


def _layout_split(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-split" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="split-grid">
    <div class="split-text reveal">
      <div class="ch-num" aria-hidden="true">{entry["chapter"]}</div>
      {_label(entry)}{_title(entry, tid)}{_caption(entry)}
      <div class="ch-rule" aria-hidden="true"></div>
    </div>
    <figure class="frame split-frame reveal" style="--d:.12s" data-parallax>
      {_media(entry)}{_cap(entry)}
    </figure>
  </div>
</section>
"""


def _layout_overlap(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-overlap" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="overlap-wrap">
    <div class="vert-num" aria-hidden="true">{entry["chapter"]}</div>
    <figure class="frame overlap-frame reveal" data-parallax>
      {_media(entry)}{_cap(entry)}
    </figure>
    <div class="glass-card reveal" style="--d:.16s">
      {_label(entry)}{_title(entry, tid)}{_caption(entry)}
    </div>
  </div>
</section>
"""


def _layout_feature(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-feature" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="feature-head reveal">
    <div class="feature-tortoise" aria-hidden="true">{TORTOISE_SVG}</div>
    {_label(entry)}{_title(entry, tid)}{_caption(entry)}
  </div>
  <figure class="frame feature-frame reveal" style="--d:.12s" data-parallax>
    {_media(entry)}{_cap(entry)}
  </figure>
</section>
"""


def _layout_aside(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-aside" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="aside-grid">
    <figure class="frame aside-frame reveal" data-parallax>
      {_media(entry)}{_cap(entry)}
    </figure>
    <div class="aside-text reveal" style="--d:.12s">
      <div class="ch-num" aria-hidden="true">{entry["chapter"]}</div>
      {_label(entry)}{_title(entry, tid)}{_caption(entry)}
      <div class="ch-rule" aria-hidden="true"></div>
    </div>
  </div>
</section>
"""


def _layout_finale(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-finale" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="frame finale-frame reveal" data-parallax>
    {_media(entry)}
    <div class="ch-num" aria-hidden="true">{entry["chapter"]}</div>
    <div class="finale-content">
      {_label(entry)}{_title(entry, tid)}{_caption(entry)}
    </div>
    {_cap(entry)}
  </div>
</section>
"""


_LAYOUTS = {
    "full": _layout_full,
    "split": _layout_split,
    "overlap": _layout_overlap,
    "feature": _layout_feature,
    "aside": _layout_aside,
    "finale": _layout_finale,
}


def render_chapter(entry: dict, i: int) -> str:
    """Render a single chapter (layout chosen by the entry's ``layout`` key)."""
    layout = _LAYOUTS.get(entry.get("layout", "full"), _layout_full)
    body = layout(entry, i)
    # The tortoise quote sits directly beneath the feature chapter.
    quote = escape(entry.get("_quote") or "")
    if entry.get("layout") == "feature" and quote:
        body += (
            f'\n<div class="quote reveal" id="tortoise-quote">'
            f'{TORTOISE_SVG}<span>“{quote}”</span></div>'
        )
    return body


def render_diary(site: dict, entries: list[dict]) -> str:
    """Timeline intro + the six chapters + closing line."""
    closing = escape(site["closing_line"])
    quote = site["tortoise_quote"]
    chapters = []
    for i, entry in enumerate(entries, start=1):
        entry = {**entry, "_quote": quote if entry.get("layout") == "feature" else ""}
        chapters.append(render_chapter(entry, i))

    closing_html = f"""
<div class="closing reveal">
  <div class="closing-tortoise" aria-hidden="true">{TORTOISE_SVG}</div>
  <p class="closing-line">“{closing}”</p>
</div>
"""
    return render_intro(site, entries) + "".join(chapters) + closing_html
