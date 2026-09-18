import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PHOTOS_RAW = path.join(__dirname, '..', 'photos-raw');

async function getDateFromExif(filePath) {
  try {
    const metadata = await sharp(filePath).metadata();
    // Try to get date from EXIF
    if (metadata.exif) {
      const exifStr = metadata.exif.toString('latin1');
      // Look for DateTimeOriginal (tag 0x9003) or DateTime (tag 0x0132)
      const dateMatch = exifStr.match(/(\d{4}):(\d{2}):(\d{2}) (\d{2}):(\d{2}):(\d{2})/);
      if (dateMatch) {
        return new Date(`${dateMatch[1]}-${dateMatch[2]}-${dateMatch[3]}T${dateMatch[4]}:${dateMatch[5]}:${dateMatch[6]}`);
      }
    }
  } catch {}
  // Fallback: file modification time
  const stat = fs.statSync(filePath);
  return stat.mtime;
}

async function main() {
  const files = fs.readdirSync(PHOTOS_RAW).filter(f => {
    const ext = path.extname(f).toLowerCase();
    return ['.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic'].includes(ext);
  });

  console.log('Analyzing photo dates...\n');

  const photos = [];
  for (const file of files) {
    const filePath = path.join(PHOTOS_RAW, file);
    const date = await getDateFromExif(filePath);
    const baseName = file.replace(path.extname(file), '');
    photos.push({ file, baseName, date, dateStr: date.toISOString().split('T')[0] });
  }

  // Sort by date ascending (oldest first)
  photos.sort((a, b) => a.date.getTime() - b.date.getTime());

  console.log('Photos in chronological order:\n');
  photos.forEach((p, i) => {
    console.log(`  ${i + 1}. ${p.file}`);
    console.log(`     Date: ${p.dateStr}`);
    console.log(`     WebP: /photos/${p.baseName}.webp`);
    console.log(`     Thumb: /photos/${p.baseName}-thumb.webp\n`);
  });

  // Output JSON mapping
  const entries = [
    "S1 E1 — How We Met",
    "S1 E2 — Our First Date",
    "S2 E1 — The Laughs We Shared",
    "S2 E2 — One Year Together",
    "S3 E1 — Adventures Together",
    "S3 E2 — Three Years"
  ];

  console.log('=== MAPPING (oldest photo → earliest entry) ===\n');
  const mapping = entries.map((entry, i) => ({
    entry,
    photo: photos[i] ? photos[i].file : 'N/A',
    thumb: photos[i] ? `/photos/${photos[i].baseName}-thumb.webp` : 'N/A',
    full: photos[i] ? `/photos/${photos[i].baseName}.webp` : 'N/A',
  }));
  console.log(JSON.stringify(mapping, null, 2));
}

main();
