# US+ — Our 3-Year Anniversary Streaming Diary

A dark, cinematic streaming-app-style website that presents our 3 years together as a show catalog.

## Quick Start

```bash
npm install
npm run dev
```

Visit **http://localhost:3000** to see the app flow:
1. **Intro** — Animated US+ wordmark with glow effect (2.5s, skippable, plays once per session)
2. **Profile Select** — "Who's watching?" screen with emoji profile tiles
3. **Browse** — Hero billboard, horizontal carousels, cards with hover preview
4. **Watch** — Full-screen story mode with crossfading images and cinematic subtitles
5. **Credits** — Rolling credits with the final letter and "Renewed for Season 4"

## How to Add Episodes

1. Add your photos to `photos-raw/` (create if needed)
2. Run `node scripts/optimize-images.mjs` to generate WebP thumbnails and full-size images
3. Edit `content/entries.json` — each entry needs:
   ```json
   {
     "id": "s1e01-how-we-met",
     "season": 1,
     "episode": 1,
     "date": "2023-09-18",
     "title": "How We Met",
     "synopsis": "1-2 line card description",
     "story": "Paragraph one.\n\nParagraph two.\n\nParagraph three.",
     "thumb": "/photos/your-thumb.webp",
     "images": ["/photos/img1.webp", "/photos/img2.webp"],
     "backdrop": "/photos/backdrop.webp",
     "tags": ["Firsts", "Favorites"],
     "runtime": "1 evening that lasted forever",
     "featured": true,
     "top10": false
   }
   ```

## How to Add Rows

Edit `content/rows.json`:
```json
{ "id": "my-row", "title": "My Custom Row", "type": "custom", "entryIds": ["s1e01-how-we-met"] }
```

Row types: `season`, `tag`, `top10`, `continue`, `custom`

## Configuration

Edit `content/config.json`:
```json
{
  "appName": "US+",
  "myName": "Your Name",
  "partnerName": "Partner's Name",
  "startDate": "2023-09-18",
  "anniversaryDate": "2026-09-18",
  "passcode": "",
  "finalLetter": ["Paragraph 1", "Paragraph 2"]
}
```

Set `passcode` to a non-empty string to enable the gate screen.

## Adding Music

Place an MP3 at `public/audio/song.mp3`. The music toggle appears automatically.

## Deploy to Vercel

```bash
npm run build
```

Push to Vercel — the project uses static export (`output: "export"`).

## Tech Stack

- Next.js 16+ (App Router) with static export
- TypeScript (strict), Tailwind CSS v4
- Framer Motion (all animation, layoutId transitions)
- Embla Carousel (horizontal rows with drag/swipe)
- Lenis (smooth page scrolling)
- Howler.js (optional music)
- Canvas Confetti (credits celebration)
