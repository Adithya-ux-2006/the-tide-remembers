// Generate simple gradient placeholder images as SVGs converted to webp-compatible format
// For simplicity, we'll create small colored SVGs that work as placeholders

const fs = require('fs');
const path = require('path');

const photosDir = path.join(__dirname, '..', 'public', 'photos');

const colors = [
  ['#E8B4A0', '#C96F6F'],
  ['#C9A46A', '#E8B4A0'],
  ['#C96F6F', '#C9A46A'],
  ['#F1E7D6', '#C96F6F'],
  ['#E8B4A0', '#C9A46A'],
  ['#C9A46A', '#F1E7D6'],
  ['#C96F6F', '#F1E7D6'],
  ['#F1E7D6', '#E8B4A0'],
  ['#C9A46A', '#C96F6F'],
  ['#E8B4A0', '#F1E7D6'],
  ['#C96F6F', '#C9A46A'],
  ['#F1E7D6', '#C9A46A'],
];

for (let i = 1; i <= 12; i++) {
  const num = String(i).padStart(2, '0');
  const [c1, c2] = colors[i - 1];
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${c1};stop-opacity:1" />
      <stop offset="100%" style="stop-color:${c2};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="600" fill="url(#g)" />
  <text x="400" y="300" text-anchor="middle" dominant-baseline="middle" font-family="serif" font-size="48" fill="rgba(255,255,255,0.3)">${num}</text>
</svg>`;
  
  fs.writeFileSync(path.join(photosDir, `placeholder-${num}.svg`), svg);
}

console.log('Generated 12 placeholder SVG images');
