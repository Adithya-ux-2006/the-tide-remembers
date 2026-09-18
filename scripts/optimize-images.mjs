import { readdirSync, existsSync, mkdirSync } from "fs";
import { join, extname } from "path";
import { execSync } from "child_process";

const PHOTOS_RAW = join(process.cwd(), "photos-raw");
const PHOTOS_OUT = join(process.cwd(), "public", "photos");
const MAX_WIDTH = 1600;
const THUMB_WIDTH = 640;
const QUALITY = 80;

function optimizeImages() {
  if (!existsSync(PHOTOS_RAW)) {
    console.log("photos-raw/ not found. Create it, add your photos, then re-run.");
    return;
  }

  if (!existsSync(PHOTOS_OUT)) mkdirSync(PHOTOS_OUT, { recursive: true });

  const files = readdirSync(PHOTOS_RAW).filter((f) => {
    const ext = extname(f).toLowerCase();
    return [".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic"].includes(ext);
  });

  if (files.length === 0) { console.log("No images in photos-raw/"); return; }

  console.log(`Processing ${files.length} images...`);

  for (const file of files) {
    const inputPath = join(PHOTOS_RAW, file);
    const baseName = file.replace(extname(file), "");
    const outputPath = join(PHOTOS_OUT, `${baseName}.webp`);
    const thumbPath = join(PHOTOS_OUT, `${baseName}-thumb.webp`);

    try {
      // Full size
      execSync(
        `npx sharp-cli --input "${inputPath}" --output "${outputPath}" resize ${MAX_WIDTH} --webp quality ${QUALITY}`,
        { stdio: "pipe" }
      );
      // Thumbnail
      execSync(
        `npx sharp-cli --input "${inputPath}" --output "${thumbPath}" resize ${THUMB_WIDTH} --webp quality ${QUALITY}`,
        { stdio: "pipe" }
      );
      console.log(`✓ ${file} → ${baseName}.webp + ${baseName}-thumb.webp`);
    } catch {
      console.log(`✗ ${file} — install sharp-cli or ImageMagick`);
    }
  }

  console.log("\nDone! Photos in public/photos/");
}

optimizeImages();
