import sharp from 'sharp';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const PHOTOS_RAW = path.join(__dirname, '..', 'photos-raw');
const PHOTOS_OUT = path.join(__dirname, '..', 'public', 'photos');
const MAX_WIDTH = 1600;
const THUMB_WIDTH = 640;
const QUALITY = 80;

async function optimizeImages() {
  if (!fs.existsSync(PHOTOS_RAW)) {
    console.log('photos-raw/ not found. Create it, add your photos, then re-run.');
    return;
  }

  if (!fs.existsSync(PHOTOS_OUT)) fs.mkdirSync(PHOTOS_OUT, { recursive: true });

  const files = fs.readdirSync(PHOTOS_RAW).filter(f => {
    const ext = path.extname(f).toLowerCase();
    return ['.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic'].includes(ext);
  });

  if (files.length === 0) { console.log('No images in photos-raw/'); return; }

  console.log(`Processing ${files.length} images...`);

  for (const file of files) {
    const inputPath = path.join(PHOTOS_RAW, file);
    const baseName = file.replace(path.extname(file), '');

    try {
      const metadata = await sharp(inputPath).metadata();
      const resizeWidth = Math.min(metadata.width || MAX_WIDTH, MAX_WIDTH);

      await sharp(inputPath)
        .resize(resizeWidth)
        .webp({ quality: QUALITY })
        .toFile(path.join(PHOTOS_OUT, `${baseName}.webp`));

      await sharp(inputPath)
        .resize(THUMB_WIDTH)
        .webp({ quality: QUALITY })
        .toFile(path.join(PHOTOS_OUT, `${baseName}-thumb.webp`));

      console.log(`✓ ${file} → ${baseName}.webp + ${baseName}-thumb.webp`);
    } catch (err) {
      console.log(`✗ ${file} — ${err.message}`);
    }
  }

  console.log('\nDone! Photos in public/photos/');
}

optimizeImages();
