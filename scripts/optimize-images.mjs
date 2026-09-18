import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join, extname } from "path";
import { execSync } from "child_process";

const PHOTOS_RAW = join(process.cwd(), "photos-raw");
const PHOTOS_OUT = join(process.cwd(), "public", "photos");
const MAX_WIDTH = 1600;
const QUALITY = 80;

function optimizeImages() {
  if (!existsSync(PHOTOS_RAW)) {
    console.log("photos-raw/ directory not found. Create it and add your photos there.");
    console.log("Then run: node scripts/optimize-images.mjs");
    return;
  }

  if (!existsSync(PHOTOS_OUT)) {
    mkdirSync(PHOTOS_OUT, { recursive: true });
  }

  const files = readdirSync(PHOTOS_RAW).filter((f) => {
    const ext = extname(f).toLowerCase();
    return [".jpg", ".jpeg", ".png", ".webp", ".avif", ".heic"].includes(ext);
  });

  if (files.length === 0) {
    console.log("No image files found in photos-raw/");
    return;
  }

  console.log(`Found ${files.length} images to optimize...`);

  for (const file of files) {
    const inputPath = join(PHOTOS_RAW, file);
    const outputFile = file.replace(extname(file), ".webp");
    const outputPath = join(PHOTOS_OUT, outputFile);

    try {
      execSync(
        `npx sharp-cli --input "${inputPath}" --output "${outputPath}" resize ${MAX_WIDTH} --webp quality ${QUALITY}`,
        { stdio: "pipe" }
      );
      console.log(`✓ ${file} → ${outputFile}`);
    } catch {
      console.log(`✗ Failed to process ${file} - trying with convert...`);
      try {
        execSync(
          `convert "${inputPath}" -resize ${MAX_WIDTH}x -quality ${QUALITY} "${outputPath}"`,
          { stdio: "pipe" }
        );
        console.log(`✓ ${file} → ${outputFile} (via ImageMagick)`);
      } catch {
        console.log(`✗ Could not process ${file}. Install sharp-cli or ImageMagick.`);
      }
    }
  }

  console.log("\nDone! Your optimized photos are in public/photos/");
}

optimizeImages();
