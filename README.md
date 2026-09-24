# THE TIDE REMEMBERS

**A little story about the sea, the shore, and the ones we found along the way.**

A premium, Netflix-inspired *cinematic digital diary* built with Streamlit. Six personal
photographs are presented as six chapters of one continuous shoreline story — full-screen
hero, chapter navigation, scroll choreography, and a full-screen “Play Story” documentary
mode.

> **A CINEMATIC DIGITAL DIARY**
> 2026 · 6 MOMENTS · BEACH · SEA · WILDLIFE

---

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501**.

---

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub
2. Open [Streamlit Community Cloud](https://share.streamlit.io)
3. Select the repository
4. Select `app.py` as the main file path
5. Deploy

No environment variables or secrets are required — the six photos are embedded from
`assets/` using relative paths resolved at runtime.

---

## Project Structure

```text
the-tide-remembers/
│
├── app.py                  # entry point — assembles the page, hides Streamlit chrome
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   ├── photo1.jpg          # chapter 01 (also the hero still)
│   ├── photo2.jpg
│   ├── photo3.jpg
│   ├── photo4.jpg          # the little traveller — tortoise chapter
│   ├── photo5.jpg
│   └── photo6.jpg
│
├── components/
│   ├── hero.py             # full-screen landing hero
│   ├── chapters.py         # nav, timeline, six chapter layouts, footer
│   ├── story.py            # full-screen “Play Story” player markup
│   ├── scripts.py          # scroll choreography + story player (vanilla JS)
│   ├── styles.py           # all CSS + Streamlit chrome-hiding styles
│   └── svg.py              # tortoise motif + player icons
│
├── data/
│   └── diary.py            # ← ALL content lives here
│
└── .streamlit/
    └── config.toml         # dark theme defaults
```

---

## Editing Content (photos, titles, captions)

Everything editable lives in **`data/diary.py`** — the frontend never needs to change.

### Replace a photo

1. Drop the new file into `assets/` (e.g. `assets/photo1.jpg`)
2. Keep the same filename, **or** update the `image` key of that chapter:

```python
{
    "chapter": "01",
    "title": "Where the Water Begins",
    "image": "assets/photo1.jpg",     # ← your photo
    "caption": "The day opened slowly…",
    "layout": "full",
}
```

### Edit the landing copy

```python
SITE = {
    "kicker": "A CINEMATIC DIGITAL DIARY",
    "title_lines": ["THE TIDE", "REMEMBERS"],
    "subtitle": "Six moments. One shoreline. A memory carried by the sea.",
    "hero_image": "assets/photo1.jpg",
    "meta": ["2026", "6 MOMENTS", "BEACH", "SEA", "WILDLIFE"],
    ...
}
```

### Chapter layouts

Each entry’s `layout` key controls how the photo is staged (all six are different
on purpose, so no two chapters feel repeated):

| layout     | feel                                        |
| ---------- | ------------------------------------------- |
| `full`     | edge-to-edge cinematic still                |
| `split`    | editorial text column + bleeding image      |
| `overlap`  | large still + overlapping glass caption     |
| `feature`  | the tortoise chapter — centered, quoted     |
| `aside`    | mirrored split with offset typography       |
| `finale`   | full-screen closing frame                   |

---

## Experience

- **▶ PLAY STORY** — opens a full-screen documentary player: slow Ken Burns zoom,
  crossfades, lower-third titles, segmented progress bars, keyboard controls
  (`←` `→` `space` `esc`), and an end card.
- **＋ EXPLORE MEMORIES** — glides to the full diary timeline.
- **Chapter navigation** — top bar numbers, right-hand rail, and timeline ticks all
  track the active chapter and are clickable.
- **Tortoise motif** — silhouette in the brand mark, a dedicated marker on chapter 04
  in the rail, and the line *“Some journeys are meant to be slow.”*

---

## Design Notes

- **Typography** — Playfair Display (display) + Inter (UI/body)
- **Palette** — deep ocean blacks/blues, aqua accent, sand-gold chapter numerals
- **Atmosphere** — animated film grain, drifting ocean glows, vignette, scroll progress
- **Performance** — no heavy JS libraries; photos are optimized (~800 KB total) and
  inlined once as CSS custom properties
- **Accessibility** — semantic landmarks, focus styles, `prefers-reduced-motion`
  support, labelled interactive controls
- **Responsive** — cinematic on desktop/laptop/tablet; stacks into a clean vertical
  story on mobile with no horizontal overflow

---

## Git

```bash
git init
git add .
git commit -m "Create cinematic beach digital diary"
```

Push to a new remote:

```bash
git remote add origin https://github.com/<your-user>/the-tide-remembers.git
git branch -M main
git push -u origin main
```
