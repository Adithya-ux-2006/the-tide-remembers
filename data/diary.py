"""Content configuration for “The Tide Remembers”.

Everything a writer/editor needs to change lives here:

* SITE          – landing page copy (title, buttons, metadata, closing lines)
* DIARY_ENTRIES – the six chapters (chapter number, title, photo, caption, layout)

Replace a photo by dropping a new file into ``assets/`` and pointing the
matching ``image`` key at it. No frontend code needs to be touched.
"""

from __future__ import annotations

import base64
from pathlib import Path
from urllib.parse import quote

import streamlit as st

# ---------------------------------------------------------------------------
# Landing / shared copy
# ---------------------------------------------------------------------------

SITE: dict = {
    "brand": "THE TIDE REMEMBERS",
    "kicker": "A CINEMATIC DIGITAL DIARY",
    "title_lines": ["THE TIDE", "REMEMBERS"],
    "subtitle": "Six moments. One shoreline. A memory carried by the sea.",
    "hero_image": "assets/photo1.jpg",
    "meta": ["2026", "6 MOMENTS", "BEACH", "SEA", "WILDLIFE"],
    "play_label": "PLAY STORY",
    "explore_label": "EXPLORE MEMORIES",
    "intro_label": "THE DIARY",
    "intro_heading": "Six moments,\none shoreline.",
    "intro_body": (
        "No grand plot. Six frames from one stretch of coast — the light "
        "that stayed, the water that moved, and the small traveller who "
        "crossed our path somewhere in between."
    ),
    "tortoise_quote": "Some journeys are meant to be slow.",
    "closing_line": (
        "The tide keeps what we let go — and gives it back, some other summer."
    ),
    "footer_meta": "A CINEMATIC DIGITAL DIARY · SIX MOMENTS · 2026",
    "end_kicker": "END OF VOLUME ONE",
    "end_title": "Until the Next Wave",
    "end_body": "Six moments, remembered in order. The shoreline keeps the rest.",
}

# ---------------------------------------------------------------------------
# The six chapters
#
#   chapter  – shown as “CHAPTER xx”
#   layout   – full | split | overlap | feature | aside | finale
#              (each layout gives every photo its own cinematic treatment)
# ---------------------------------------------------------------------------

DIARY_ENTRIES: list[dict] = [
    {
        "chapter": "01",
        "title": "Where the Water Begins",
        "image": "assets/photo1.jpg",
        "caption": (
            "The day opened slowly — salt on the skin, light on the water, "
            "and nowhere else we needed to be."
        ),
        "layout": "full",
    },
    {
        "chapter": "02",
        "title": "Salt in the Air",
        "image": "assets/photo2.jpg",
        "caption": (
            "Wind, warm light, and the first real breath of the season. "
            "We walked until the noise turned into weather."
        ),
        "layout": "split",
    },
    {
        "chapter": "03",
        "title": "A Quiet Shore",
        "image": "assets/photo3.jpg",
        "caption": (
            "Low tide and long pauses — the kind of quiet that only feels "
            "full when someone is sitting beside you."
        ),
        "layout": "overlap",
    },
    {
        "chapter": "04",
        "title": "The Little Traveller",
        "image": "assets/photo4.jpg",
        "caption": (
            "We found it near the water’s edge: small, armoured, "
            "entirely unbothered by the size of the ocean."
        ),
        "layout": "feature",
    },
    {
        "chapter": "05",
        "title": "Between Tide & Sand",
        "image": "assets/photo5.jpg",
        "caption": (
            "Footprints filled as fast as we made them. We stopped trying "
            "to keep them, and kept walking anyway."
        ),
        "layout": "aside",
    },
    {
        "chapter": "06",
        "title": "Until the Next Wave",
        "image": "assets/photo6.jpg",
        "caption": (
            "We left the shore the way you close a good book — slowly, "
            "already missing the last page."
        ),
        "layout": "finale",
    },
]


def _data_uri(path: Path) -> str:
    """Read an image file and return an inline data URI."""
    suffix = path.suffix.lower()
    mime = "image/webp" if suffix == ".webp" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


@st.cache_data(show_spinner=False)
def load_images(base_dir: str) -> dict[str, str]:
    """Map every configured photo path (relative, e.g. assets/photo1.jpg)
    to an inline data URI so the page works on any host with no path issues.
    """
    base = Path(base_dir)
    paths = {entry["image"] for entry in DIARY_ENTRIES}
    paths.add(SITE["hero_image"])
    images: dict[str, str] = {}
    for rel in sorted(paths):
        file = base / rel
        if file.exists():
            images[rel] = _data_uri(file)
        else:  # graceful fallback so a missing photo never breaks the page
            svg = (
                "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'>"
                "<rect width='16' height='9' fill='#0a1c2f'/>"
                "<path d='M0 6.5 Q4 5 8 6.5 T16 6.5 V9 H0Z' fill='#123047'/>"
                "</svg>"
            )
            images[rel] = "data:image/svg+xml," + quote(svg)
    return images
