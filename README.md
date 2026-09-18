# Our Story — A 3-Year Anniversary Digital Diary

A private, cinematic, book-like website celebrating three beautiful years together.

## Quick Start

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the diary.

## How to Add Your Photos

1. Drop your photos into `photos-raw/` (create the folder if it doesn't exist)
2. Run the optimization script:
   ```bash
   node scripts/optimize-images.mjs
   ```
   This resizes images to max 1600px wide and converts them to WebP in `public/photos/`
3. If you don't have `sharp-cli` or ImageMagick, manually resize and place WebP files in `public/photos/`

## How to Edit Content

### Edit your names and dates
Open `content/config.json` and update:
```json
{
  "partnerName": "Your Partner's Name",
  "myName": "Your Name",
  "startDate": "2023-09-18",
  "anniversaryDate": "2026-09-18",
  "passcode": "",
  "finalLetter": "Your love letter here..."
}
```

### Edit diary entries
Open `content/entries.json` and add/modify entries. Each entry needs:
```json
{
  "id": "unique-id",
  "date": "2024-01-15",
  "title": "Entry Title",
  "body": "Paragraph one.\n\nParagraph two.",
  "images": ["/photos/your-photo.webp"],
  "layout": "left",
  "mood": "✨",
  "caption": "Optional caption"
}
```

**Layouts available:**
- `"left"` — Photo on the left, text on the right
- `"right"` — Photo on the right, text on the left
- `"full"` — Full-bleed image with text overlay
- `"collage"` — Multiple images in overlapping arrangement

## Adding Music

Place an MP3 file at `public/audio/song.mp3`. The music toggle will automatically appear (off by default, user must click to play).

## Deploy to Vercel

This project is configured for static export. Simply connect your repo to Vercel and deploy:

```bash
npm run build
```

The `out/` directory contains the static site.

## Tech Stack

- Next.js 14+ (App Router)
- TypeScript (strict)
- Tailwind CSS v4
- Framer Motion (animations)
- Lenis (smooth scrolling)
- Canvas Confetti (final page celebration)
- Howler.js (optional music)
