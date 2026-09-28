"""Content configuration for “The Tide Remembers”.

Everything a writer/editor needs to change lives here:

* SITE          – landing page copy (title, buttons, metadata, closing lines)
* SEED_ENTRIES  – the six original chapters, in the same schema as user memories

The live diary lives in ``data/memories.json`` (see :mod:`data.store`); on
first run it is seeded from ``SEED_ENTRIES``.

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
    "meta": ["2026", "3 YEARS", "6 MOMENTS", "BEACH", "SEA", "WILDLIFE"],
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
    "anniv_kicker": "HAPPY 3 YEAR ANNIVERSARY TO US",
    "anniv_line": "I know it was hard, but we made it, Buttercup. I love you.",
    "footer_meta": "A CINEMATIC DIGITAL DIARY · SIX MOMENTS · 2026",
    "end_kicker": "END OF VOLUME ONE",
    "end_title": "Until the Next Wave",
    "end_body": "Six moments, remembered in order. The shoreline keeps the rest.",
}

# ---------------------------------------------------------------------------
# Count words – “Six moments…”, “SIX MOMENTS” — identical to the original copy
# for six entries, sensible beyond that.
# ---------------------------------------------------------------------------

_COUNT_WORDS = {
    0: "No",
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
    15: "Fifteen",
    16: "Sixteen",
    17: "Seventeen",
    18: "Eighteen",
    19: "Nineteen",
    20: "Twenty",
    21: "Twenty-One",
    22: "Twenty-Two",
    23: "Twenty-Three",
    24: "Twenty-Four",
    25: "Twenty-Five",
    26: "Twenty-Six",
    27: "Twenty-Seven",
    28: "Twenty-Eight",
    29: "Twenty-Nine",
    30: "Thirty",
}


def count_word(n: int) -> str:
    """“Six” / “Seven” — the spelled-out number used in the copy."""
    return _COUNT_WORDS.get(n, str(n))


def build_site(entries: list[dict]) -> dict:
    """Copy ``SITE`` with every “six moments” reference made dynamic.

    With exactly six entries the output is byte-identical to the original
    static copy.
    """
    site = dict(SITE)
    n = len(entries)
    w = count_word(n)
    site["count"] = n
    site["count_word"] = w
    site["subtitle"] = f"{w} moments. One shoreline. A memory carried by the sea."
    site["meta"] = [
        SITE["meta"][0],
        SITE["meta"][1],
        f"{n} MOMENTS",
        *SITE["meta"][3:],
    ]
    site["intro_heading"] = f"{w} moments,\none shoreline."
    site["intro_body"] = (
        f"No grand plot. {w} frames from one stretch of coast — the light "
        "that stayed, the water that moved, and the small traveller who "
        "crossed our path somewhere in between."
    )
    site["footer_meta"] = f"A CINEMATIC DIGITAL DIARY · {w.upper()} MOMENTS · 2026"
    site["end_body"] = f"{w} moments, remembered in order. The shoreline keeps the rest."
    if n == 0:
        site["subtitle"] = "No moments yet. One shoreline — waiting to be written."
        site["intro_body"] = (
            "No grand plot yet. Only one stretch of coast, waiting for the "
            "first frame of a new diary."
        )
        site["end_body"] = "Nothing remembered yet. The shoreline keeps the rest."
    return site


# ---------------------------------------------------------------------------
# Moods offered in the add / edit form (chips)
# ---------------------------------------------------------------------------

MOODS: list[str] = [
    "calm",
    "joyful",
    "nostalgic",
    "tender",
    "grateful",
    "adventurous",
    "reflective",
]

# Layouts new memories cycle through — ``feature`` is skipped because it owns
# the tortoise quote (rendering it twice would duplicate the quote block).
USER_LAYOUTS: list[str] = ["full", "split", "overlap", "aside", "finale"]

# ---------------------------------------------------------------------------
# The six original chapters
#
#   chapter  – stored as an int, rendered as “CHAPTER xx”
#   memory   – the caption shown under the photo (story = optional long text)
#   layout   – full | split | overlap | feature | aside | finale
#              (each layout gives every photo its own cinematic treatment)
# ---------------------------------------------------------------------------

SEED_ENTRIES: list[dict] = [
    {
        "id": "tide-01",
        "chapter": 1,
        "title": "Where the Water Begins",
        "image": "assets/photo1.jpg",
        "date": "2026-09-01",
        "location": "",
        "memory": (
            "The day opened slowly — salt on the skin, light on the water, "
            "and nowhere else we needed to be."
        ),
        "story": "",
        "mood": "",
        "tags": ["beach", "morning"],
        "layout": "full",
        "origin": "seed",
    },
    {
        "id": "tide-02",
        "chapter": 2,
        "title": "Salt in the Air",
        "image": "assets/photo2.jpg",
        "date": "2026-09-04",
        "location": "",
        "memory": (
            "Wind, warm light, and the first real breath of the season. "
            "We walked until the noise turned into weather."
        ),
        "story": "",
        "mood": "",
        "tags": ["wind", "walk"],
        "layout": "split",
        "origin": "seed",
    },
    {
        "id": "tide-03",
        "chapter": 3,
        "title": "A Quiet Shore",
        "image": "assets/photo3.jpg",
        "date": "2026-09-07",
        "location": "",
        "memory": (
            "Low tide and long pauses — the kind of quiet that only feels "
            "full when someone is sitting beside you."
        ),
        "story": "",
        "mood": "",
        "tags": ["lowtide", "quiet"],
        "layout": "overlap",
        "origin": "seed",
    },
    {
        "id": "tide-04",
        "chapter": 4,
        "title": "The Little Traveller",
        "image": "assets/photo4.jpg",
        "date": "2026-09-10",
        "location": "",
        "memory": (
            "We found it near the water’s edge: small, armoured, "
            "entirely unbothered by the size of the ocean."
        ),
        "story": "",
        "mood": "",
        "tags": ["tortoise", "wildlife"],
        "layout": "feature",
        "origin": "seed",
    },
    {
        "id": "tide-05",
        "chapter": 5,
        "title": "Between Tide & Sand",
        "image": "assets/photo5.jpg",
        "date": "2026-09-12",
        "location": "",
        "memory": (
            "Footprints filled as fast as we made them. We stopped trying "
            "to keep them, and kept walking anyway."
        ),
        "story": "",
        "mood": "",
        "tags": ["footprints", "evening"],
        "layout": "aside",
        "origin": "seed",
    },
    {
        "id": "tide-06",
        "chapter": 6,
        "title": "Until the Next Wave",
        "image": "assets/photo6.jpg",
        "date": "2026-09-14",
        "location": "",
        "memory": (
            "We left the shore the way you close a good book — slowly, "
            "already missing the last page."
        ),
        "story": "",
        "mood": "",
        "tags": ["goodbye", "sea"],
        "layout": "finale",
        "origin": "seed",
    },
]

# Backwards-compatible alias (previews, older imports).
DIARY_ENTRIES: list[dict] = SEED_ENTRIES


def _data_uri(path: Path) -> str:
    """Read an image file and return an inline data URI."""
    suffix = path.suffix.lower()
    mime = "image/webp" if suffix == ".webp" else "image/jpeg"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


_MISSING_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 9'>"
    "<rect width='16' height='9' fill='#0a1c2f'/>"
    "<path d='M0 6.5 Q4 5 8 6.5 T16 6.5 V9 H0Z' fill='#123047'/>"
    "</svg>"
)


@st.cache_data(show_spinner=False)
def _load_images(base_dir: str, paths: tuple[str, ...]) -> dict[str, str]:
    base = Path(base_dir)
    images: dict[str, str] = {}
    for rel in paths:
        file = base / rel
        if file.exists():
            images[rel] = _data_uri(file)
        else:  # graceful fallback so a missing photo never breaks the page
            images[rel] = "data:image/svg+xml," + quote(_MISSING_SVG)
    return images


def load_images(base_dir: str, entries: list[dict] | None = None) -> dict[str, str]:
    """Map every photo path (relative, e.g. assets/photo1.jpg) to a data URI.

    Cached by the exact set of paths, so newly uploaded photos always
    invalidate the cache while unchanged diaries stay fast.
    """
    source = entries if entries is not None else DIARY_ENTRIES
    paths = {str(e.get("image") or "") for e in source if e.get("image")}
    paths.add(SITE["hero_image"])
    return _load_images(base_dir, tuple(sorted(paths)))
