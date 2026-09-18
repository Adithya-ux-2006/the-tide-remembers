import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PHOTOS_RAW = path.join(__dirname, '..', 'photos-raw');

const files = fs.readdirSync(PHOTOS_RAW).filter(f => {
  const ext = path.extname(f).toLowerCase();
  return ['.jpg', '.jpeg', '.png', '.webp', '.avif', '.heic'].includes(ext);
});

console.log('Photo file details:\n');

const photos = files.map(file => {
  const filePath = path.join(PHOTOS_RAW, file);
  const stat = fs.statSync(filePath);
  const baseName = file.replace(path.extname(file), '');

  // Try to extract date from filename
  let dateSource = 'file modified';
  let date = stat.mtime;

  // IMG_20260731_233050_877 pattern
  const imgMatch = file.match(/IMG_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})/);
  if (imgMatch) {
    date = new Date(`${imgMatch[1]}-${imgMatch[2]}-${imgMatch[3]}T${imgMatch[4]}:${imgMatch[5]}:${imgMatch[6]}`);
    dateSource = 'filename (IMG_)';
  }

  // Screenshot_20260801_002901 pattern
  const ssMatch = file.match(/Screenshot_(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})/);
  if (ssMatch) {
    date = new Date(`${ssMatch[1]}-${ssMatch[2]}-${ssMatch[3]}T${ssMatch[4]}:${ssMatch[5]}:${ssMatch[6]}`);
    dateSource = 'filename (Screenshot)';
  }

  return { file, baseName, date, dateSource, birthtime: stat.birthtime, mtime: stat.mtime };
});

// Sort by date
photos.sort((a, b) => a.date.getTime() - b.date.getTime());

photos.forEach((p, i) => {
  console.log(`${i + 1}. ${p.file}`);
  console.log(`   Date: ${p.date.toISOString()} (${p.dateSource})`);
  console.log(`   Created: ${p.birthtime.toISOString()}`);
  console.log(`   Modified: ${p.mtime.toISOString()}\n`);
});
