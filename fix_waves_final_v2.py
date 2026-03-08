
import os
import re

path = r'c:\Users\dark1\.gemini\antigravity\scratch\HaloWarsCastingTool\casting_html\score.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Completely redefine drawWaves to be 100% sure
new_draw_waves = """    function drawWaves() {
      if (!waveWidth || !waveHeight) {
        requestAnimationFrame(drawWaves);
        return;
      }
      // Clean state reset
      waveCtx.setTransform(1, 0, 0, 1, 0, 0);
      waveCtx.clearRect(0, 0, waveWidth, waveHeight);

      const p1Color = getComputedStyle(document.body).getPropertyValue('--p1-color') || '#cc2222';
      const p2Color = getComputedStyle(document.body).getPropertyValue('--p2-color') || '#2244cc';

      const gradient = waveCtx.createLinearGradient(0, 0, waveWidth, 0);
      gradient.addColorStop(0, p1Color);
      gradient.addColorStop(0.35, p1Color);
      gradient.addColorStop(0.48, 'rgba(255, 255, 255, 0.4)'); // Brighter center
      gradient.addColorStop(0.52, 'rgba(255, 255, 255, 0.4)');
      gradient.addColorStop(0.65, p2Color);
      gradient.addColorStop(1, p2Color);

      waveCtx.lineWidth = 12;
      waveCtx.shadowBlur = 0;

      const tanSkew = Math.tan(-20 * Math.PI / 180); // Match CSS skewX(-20deg)

      waveCtx.save();
      waveCtx.filter = "blur(3px)"; // Internal blur only, no bleed

      // CREATE CLIPPING PATH
      waveCtx.beginPath();
      document.querySelectorAll('.block').forEach(block => {
        const w = block.offsetWidth;
        const h = block.offsetHeight;
        const canvasLeft = parseFloat(waveCanvas.style.left) || 0;
        const x = block.offsetLeft - canvasLeft;
        
        const shiftX = h * tanSkew;
        const halfS = shiftX / 2;

        if (w <= 0) return;

        // Path following the exact skewed box geometry (\\ lean)
        waveCtx.moveTo(x - halfS, 0);
        waveCtx.lineTo(x + w - halfS, 0);
        waveCtx.lineTo(x + w + halfS, h);
        waveCtx.lineTo(x + halfS, h);
        waveCtx.closePath();
      });
      waveCtx.clip();

      // DRAW WAVES
      waves.forEach((w) => {
        waveCtx.beginPath();
        waveCtx.strokeStyle = gradient;
        waveCtx.globalAlpha = w.opacity;

        const startX = -400;
        const endX = waveWidth + 400;
        for (let x = startX; x < endX; x += 10) {
          const time = waveTime * w.speed;
          const y = (waveHeight * 0.5) +
            Math.sin(x * w.length + time) * (w.amplitude) +
            Math.sin(x * 0.01 + time * 0.5) * (w.amplitude * 0.3);

          const shiftedX = x + (y * tanSkew);

          if (x === startX) waveCtx.moveTo(shiftedX, y);
          else waveCtx.lineTo(shiftedX, y);
        }
        waveCtx.stroke();
      });

      waveCtx.restore();
      waveTime++;
      requestAnimationFrame(drawWaves);
    }"""

# Use regex to replace the entire function body
pattern = r'function drawWaves\(\) \{.*?\}\n    // Initialize wave canvas'
replacement = new_draw_waves + "\n    // Initialize wave canvas"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Rewrote drawWaves function successfully.")
