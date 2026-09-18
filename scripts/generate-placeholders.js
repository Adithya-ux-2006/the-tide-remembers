const fs = require('fs');
const path = require('path');

const photosDir = path.join(__dirname, '..', 'public', 'photos');

const gradients = [
  ['#E5384A', '#1a1a2e'], ['#F5C16C', '#2d1f3d'], ['#E5384A', '#0f3460'],
  ['#1a1a2e', '#E5384A'], ['#F5C16C', '#16213e'], ['#e94560', '#1a1a2e'],
  ['#0f3460', '#F5C16C'], ['#533483', '#E5384A'], ['#1a1a2e', '#F5C16C'],
  ['#e94560', '#0f3460'], ['#F5C16C', '#533483'], ['#E5384A', '#16213e'],
  ['#1a1a2e', '#e94560'], ['#0f3460', '#E5384A'], ['#533483', '#F5C16C'],
  ['#16213e', '#E5384A'], ['#F5C16C', '#1a1a2e'], ['#E5384A', '#533483'],
];

for (let i = 1; i <= 18; i++) {
  const num = String(i).padStart(2, '0');
  const [c1, c2] = gradients[i - 1];
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">
  <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:${c1};stop-opacity:1"/>
    <stop offset="100%" style="stop-color:${c2};stop-opacity:1"/>
  </linearGradient></defs>
  <rect width="640" height="360" fill="url(#g)"/>
  <text x="320" y="180" text-anchor="middle" dominant-baseline="middle" font-family="sans-serif" font-size="36" fill="rgba(255,255,255,0.15)">${num}</text>
</svg>`;
  fs.writeFileSync(path.join(photosDir, `ep${num}.svg`), svg);
}

// Backdrop images (wider)
for (let i = 1; i <= 6; i++) {
  const num = String(i).padStart(2, '0');
  const [c1, c2] = gradients[i - 1];
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">
  <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" style="stop-color:${c1};stop-opacity:1"/>
    <stop offset="100%" style="stop-color:${c2};stop-opacity:1"/>
  </linearGradient></defs>
  <rect width="1280" height="720" fill="url(#g)"/>
  <text x="640" y="360" text-anchor="middle" dominant-baseline="middle" font-family="sans-serif" font-size="48" fill="rgba(255,255,255,0.1)">BACKDROP ${num}</text>
</svg>`;
  fs.writeFileSync(path.join(photosDir, `backdrop${num}.svg`), svg);
}

console.log('Generated 18 episode thumbnails + 6 backdrops');
