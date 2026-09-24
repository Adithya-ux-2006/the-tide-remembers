"""Full-screen story mode — a cinematic player for the six chapters."""

from __future__ import annotations

from html import escape

from components.svg import (
    CLOSE_SVG,
    NEXT_SVG,
    PAUSE_SVG,
    PREV_SVG,
    TORTOISE_SVG,
)


def _stem(path: str) -> str:
    return path.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()


def render_story(site: dict, entries: list[dict]) -> str:
    brand = escape(site["brand"])

    slides = "".join(
        f'<div class="story-slide" data-i="{i - 1}">'
        f'<div class="story-img" role="img" aria-label="Chapter {e["chapter"]}: '
        f'{escape(e["title"])}" '
        f'style="background-image:var(--img-{_stem(e["image"])})"></div></div>'
        for i, e in enumerate(entries, start=1)
    )

    bars = "".join('<span class="sbar"><i class="sbar-fill"></i></span>' for _ in entries)

    first = entries[0]
    count = f"{len(entries):02d}"

    return f"""
<div class="story" id="story" role="dialog" aria-modal="true" aria-label="Story mode" aria-hidden="true">
  <div class="story-slides" aria-hidden="true">{slides}</div>
  <div class="story-fade" aria-hidden="true"></div>
  <div class="story-ui">
    <div class="story-top">
      <div class="story-brand">{TORTOISE_SVG}<span>{brand}</span></div>
      <button class="story-close" type="button" data-story-close aria-label="Close story mode">{CLOSE_SVG}</button>
    </div>
    <div class="story-bars" aria-hidden="true">{bars}</div>
    <div class="story-center" id="storyCenter">
      <div class="story-chap" id="storyChap">CHAPTER {first["chapter"]}</div>
      <h2 class="story-title" id="storyTitle">{escape(first["title"])}</h2>
      <p class="story-text" id="storyText">{escape(first["caption"])}</p>
    </div>
    <div class="story-bottom">
      <div class="story-controls">
        <button class="sctrl" type="button" data-s-prev aria-label="Previous chapter">{PREV_SVG}</button>
        <button class="sctrl main" type="button" data-s-toggle aria-label="Pause">{PAUSE_SVG}</button>
        <button class="sctrl" type="button" data-s-next aria-label="Next chapter">{NEXT_SVG}</button>
      </div>
      <div class="story-count"><b id="storyIndex">{first["chapter"]}</b> / {count}</div>
    </div>
  </div>
  <div class="story-end" id="storyEnd" aria-hidden="true">
    <div class="se-tortoise" aria-hidden="true">{TORTOISE_SVG}</div>
    <div class="se-kicker">{escape(site["end_kicker"])}</div>
    <div class="se-title">{escape(site["end_title"])}</div>
    <p class="se-body">{escape(site["end_body"])}</p>
    <div class="se-actions">
      <button class="btn btn-play" type="button" data-s-replay>REPLAY</button>
      <button class="btn btn-ghost" type="button" data-s-explore>{escape(site["explore_label"])}</button>
    </div>
    <div class="se-quote">“{escape(site["tortoise_quote"])}”</div>
  </div>
</div>
"""
