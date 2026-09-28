"""Chapter presentation — navigation, timeline, and the photo layouts."""

from __future__ import annotations

import re
from html import escape

from components.svg import PLAY_SVG, PLUS_SVG, TORTOISE_SVG
from data.diary import MOODS
from data.store import chronological

# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

_MONTHS = (
    "JANUARY",
    "FEBRUARY",
    "MARCH",
    "APRIL",
    "MAY",
    "JUNE",
    "JULY",
    "AUGUST",
    "SEPTEMBER",
    "OCTOBER",
    "NOVEMBER",
    "DECEMBER",
)
_MONTHS_SHORT = tuple(m[:3] for m in _MONTHS)


def _n(value) -> str:
    """Chapter numbers always render as two digits: 1 → “01”, “7” → “07”."""
    try:
        return f"{int(str(value).strip()):02d}"
    except (TypeError, ValueError):
        return str(value)


def fmt_date(iso: str, short: bool = False) -> str:
    """“2026-09-24” → “24 SEPTEMBER 2026” (or “24 SEP 2026”)."""
    iso = (iso or "").strip()
    if len(iso) >= 10:
        try:
            y, m, d = int(iso[0:4]), int(iso[5:7]), int(iso[8:10])
            if 1 <= m <= 12:
                month = _MONTHS_SHORT[m - 1] if short else _MONTHS[m - 1]
                return f"{d:02d} {month} {y}"
        except ValueError:
            pass
    return iso


def _is_user(entry: dict) -> bool:
    """True for memories the visitor wrote (the six originals are “seed”)."""
    return str(entry.get("origin") or "user") != "seed"


def _has_meta(entry: dict) -> bool:
    """The entry carries personal detail beyond the original caption."""
    return _is_user(entry) or bool(
        entry.get("location") or entry.get("mood") or entry.get("story")
    )


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


def render_topbar(site: dict, entries: list[dict]) -> str:
    brand = escape(site["brand"])
    nav = "".join(
        f'<button class="tn" type="button" data-goto="{i}" '
        f'aria-label="Chapter {i:02d}">{i:02d}</button>'
        for i in range(1, len(entries) + 1)
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
  <button class="mini-add" type="button" data-add-memory aria-label="Add memory">
    {PLUS_SVG}<span>ADD MEMORY</span>
  </button>
</header>
"""


def render_rail(entries: list[dict]) -> str:
    """Vertical chapter rail — the feature chapter is marked with the tortoise."""
    items = []
    for i, entry in enumerate(entries, start=1):
        marker = (
            f'<span class="rail-tortoise" aria-hidden="true">{TORTOISE_SVG}</span>'
            if entry["layout"] == "feature"
            else '<span class="rail-line" aria-hidden="true"></span>'
        )
        num = _n(entry["chapter"])
        items.append(
            f'<button class="rail-item" type="button" data-goto="{i}" '
            f'aria-label="Chapter {num}: {escape(entry["title"])}">'
            f'<span class="rail-num">{num}</span>{marker}</button>'
        )
    return f'<nav class="rail" aria-label="Story progress">{"".join(items)}</nav>'


# ---------------------------------------------------------------------------
# Diary index — search, mood chips, chronological timeline list
# ---------------------------------------------------------------------------

_SEARCH_SVG = (
    '<svg viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg" fill="none" '
    'stroke="currentColor" stroke-width="1.6" aria-hidden="true">'
    '<circle cx="6" cy="6" r="4.4"/><path d="M9.4 9.4 13 13"/></svg>'
)


def _search_blob(entry: dict, pos: int) -> str:
    parts = [
        _n(entry.get("chapter") or pos),
        str(entry.get("title") or ""),
        str(entry.get("memory") or ""),
        str(entry.get("caption") or ""),
        str(entry.get("story") or ""),
        str(entry.get("location") or ""),
        str(entry.get("mood") or ""),
        " ".join(str(t) for t in entry.get("tags") or []),
        str(entry.get("date") or ""),
        fmt_date(entry.get("date") or ""),
        fmt_date(entry.get("date") or "", short=True),
    ]
    return escape(" ".join(p for p in parts if p).lower())


def _mood_chips(entries: list[dict]) -> str:
    present: list[str] = []
    for mood in MOODS:
        if any(
            (e.get("mood") or "").lower() == mood for e in entries
        ):
            present.append(mood)
    for e in entries:
        mood = (e.get("mood") or "").lower()
        if mood and mood not in present:
            present.append(mood)
    chips = ['<button type="button" class="di-chip is-on" data-mood="">ALL</button>']
    chips += [
        f'<button type="button" class="di-chip" data-mood="{escape(m)}">'
        f"{escape(m.upper())}</button>"
        for m in present
    ]
    return "".join(chips)


def _timeline_rows(entries: list[dict]) -> str:
    positions = {e["id"]: i for i, e in enumerate(entries, start=1)}
    out: list[str] = []
    year = month = None
    for entry in chronological(entries):
        date = (entry.get("date") or "").strip()
        row_year, row_month = "", ""
        if len(date) >= 7:
            row_year, row_month = date[:4], date[5:7]
        else:
            row_year = "UNDATED"
        if row_year != year:
            year, month = row_year, None
            out.append(f'<div class="di-year">{escape(year)}</div>')
        if row_month and row_month != month:
            month = row_month
            try:
                label = _MONTHS[int(row_month) - 1]
            except (ValueError, IndexError):
                label = escape(row_month)
            out.append(f'<div class="di-month">{label}</div>')

        pos = positions.get(entry["id"], 1)
        mood = (entry.get("mood") or "").strip()
        tags = "".join(
            f'<i class="di-tag">{escape(str(t))}</i>'
            for t in (entry.get("tags") or [])[:4]
        )
        sub_parts = [fmt_date(date, short=True)]
        if entry.get("location"):
            sub_parts.append(escape(str(entry["location"]).strip()))
        if mood:
            sub_parts.append(escape(mood.upper()))
        out.append(
            f'<div class="di-row" role="link" tabindex="0" data-goto="{pos}" '
            f'data-id="{escape(entry["id"])}" data-mood="{escape(mood.lower())}" '
            f'data-search="{_search_blob(entry, pos)}">'
            f'<span class="di-num">{_n(entry.get("chapter") or pos)}</span>'
            f'<span class="di-main">'
            f'<span class="di-title">{escape(entry["title"])}</span>'
            f'<span class="di-sub">{" · ".join(sub_parts)}</span></span>'
            f'<span class="di-tags">{tags}</span>'
            f'<span class="di-acts">'
            f'<button type="button" class="di-act" data-edit="{escape(entry["id"])}">'
            f"EDIT</button>"
            f'<button type="button" class="di-act is-danger" '
            f'data-del="{escape(entry["id"])}">DELETE</button>'
            f"</span></div>"
        )
    return "".join(out)


def render_index(entries: list[dict]) -> str:
    """Search box, mood chips, chronological list of every memory, add button."""
    count = len(entries)
    return f"""
<div class="di-index reveal" style="--d:.18s">
  <div class="di-head">
    <label class="di-search" for="diarySearch">
      {_SEARCH_SVG}
      <input type="search" id="diarySearch" placeholder="Search memories"
             autocomplete="off" spellcheck="false" aria-label="Search memories">
    </label>
    <div class="di-count"><b id="diaryCount">{count}</b> MEMORIES</div>
  </div>
  <div class="di-chips" role="group" aria-label="Filter by mood">{_mood_chips(entries)}</div>
  <div class="di-list" id="diaryList">{_timeline_rows(entries)}</div>
  <div class="di-empty" id="diaryEmpty" hidden>
    <div class="di-empty-title">NO MEMORIES HERE YET</div>
    <p class="di-empty-body">Maybe the next one is waiting to be written.</p>
  </div>
  <div class="di-foot">
    <button type="button" class="btn btn-play di-add" data-add-memory>
      {PLUS_SVG}ADD MEMORY
    </button>
  </div>
</div>
"""


def render_intro(site: dict, entries: list[dict]) -> str:
    label = escape(site["intro_label"])
    heading = escape(site["intro_heading"])
    body = escape(site["intro_body"])
    ticks = "".join(
        f'<button class="si-tick" type="button" data-goto="{i}" '
        f'aria-label="Go to chapter {_n(e["chapter"])}">'
        f'<i aria-hidden="true"></i><span>{_n(e["chapter"])}</span></button>'
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
  {render_index(entries)}
</section>
"""


def render_dedication(site: dict) -> str:
    """The anniversary dedication — the final word before the footer."""
    kicker = escape(site["anniv_kicker"])
    line = escape(site["anniv_line"])
    return f"""
<section class="dedication reveal" aria-label="Anniversary dedication">
  <div class="ded-kicker">{kicker}</div>
  <p class="ded-line">{line}</p>
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
    img = f"var(--img-{_stem(entry['image'])})"
    num = _n(entry["chapter"])
    return (
        f'<div class="frame-bg" aria-hidden="true" style="background-image:{img}"></div>'
        f'<div class="frame-media" role="img" aria-label="Chapter {num}: '
        f'{title}" style="background-image:{img}"></div>'
    )


def _cap(entry: dict) -> str:
    num = _n(entry["chapter"])
    return (
        f'<figcaption class="frame-cap">'
        f'<span class="fc-num">{num}</span>'
        f'<span class="fc-title">{escape(entry["title"])}</span>'
        f'<span class="fc-tag">CHAPTER {num}</span></figcaption>'
    )


def _label(entry: dict) -> str:
    return f'<div class="ch-label">CHAPTER {_n(entry["chapter"])}</div>'


def _title(entry: dict, tid: str) -> str:
    return f'<h2 class="ch-title" id="{tid}">{escape(entry["title"])}</h2>'


def _meta(entry: dict) -> str:
    """Date · location line — only for memories carrying personal detail."""
    if not _has_meta(entry):
        return ""
    parts = [fmt_date(entry.get("date") or "")]
    if entry.get("location"):
        parts.append(str(entry["location"]).strip())
    parts = [escape(p) for p in parts if p]
    if not parts:
        return ""
    return f'<div class="ch-meta">{" · ".join(parts)}</div>'


def _caption(entry: dict) -> str:
    text = str(entry.get("caption") or entry.get("memory") or "")
    label = ""
    if _has_meta(entry):
        label = '<div class="ch-label ch-label-sub">THE MEMORY</div>'
    return f'{label}<p class="ch-caption">{escape(text)}</p>'


def _story(entry: dict) -> str:
    """The long “THE STORY” block — only when the memory has story text."""
    text = str(entry.get("story") or "").strip()
    if not text:
        return ""
    paragraphs = "".join(
        "<p>" + escape(chunk).replace("\n", "<br>") + "</p>"
        for chunk in re.split(r"\n\s*\n", text)
    )
    return (
        '<div class="ch-story-wrap reveal">'
        '<div class="ch-label ch-label-sub">THE STORY</div>'
        f'<div class="ch-story">{paragraphs}</div></div>'
    )


# ---------------------------------------------------------------------------
# The six layouts
# ---------------------------------------------------------------------------


def _layout_full(entry: dict, i: int) -> str:
    tid = f"ch-{i}-title"
    return f"""
<section class="chapter layout-full" id="chapter-{i}" data-chapter="{i}" aria-labelledby="{tid}">
  <div class="frame full-frame reveal" data-parallax>
    {_media(entry)}
    <div class="ch-num" aria-hidden="true">{_n(entry["chapter"])}</div>
    <div class="full-content">
      {_label(entry)}{_title(entry, tid)}{_meta(entry)}{_caption(entry)}{_story(entry)}
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
      <div class="ch-num" aria-hidden="true">{_n(entry["chapter"])}</div>
      {_label(entry)}{_title(entry, tid)}{_meta(entry)}{_caption(entry)}{_story(entry)}
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
    <div class="vert-num" aria-hidden="true">{_n(entry["chapter"])}</div>
    <figure class="frame overlap-frame reveal" data-parallax>
      {_media(entry)}{_cap(entry)}
    </figure>
    <div class="glass-card reveal" style="--d:.16s">
      {_label(entry)}{_title(entry, tid)}{_meta(entry)}{_caption(entry)}{_story(entry)}
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
    {_label(entry)}{_title(entry, tid)}{_meta(entry)}{_caption(entry)}{_story(entry)}
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
      <div class="ch-num" aria-hidden="true">{_n(entry["chapter"])}</div>
      {_label(entry)}{_title(entry, tid)}{_meta(entry)}{_caption(entry)}{_story(entry)}
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
    <div class="ch-num" aria-hidden="true">{_n(entry["chapter"])}</div>
    <div class="finale-content">
      {_label(entry)}{_title(entry, tid)}{_meta(entry)}{_caption(entry)}{_story(entry)}
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
    """Timeline intro + index + every chapter + closing line."""
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
