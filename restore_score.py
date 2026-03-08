
import os
import re

path = r'c:\Users\dark1\.gemini\antigravity\scratch\HaloWarsCastingTool\casting_html\score.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Defined a clean drawWaves function
clean_draw_waves = """    function drawWaves() {
      if (!waveWidth || !waveHeight) {
        requestAnimationFrame(drawWaves);
        return;
      }
      
      waveCtx.setTransform(1, 0, 0, 1, 0, 0);
      waveCtx.clearRect(0, 0, waveWidth, waveHeight);
      waveTime += 1;

      const p1Block = document.getElementById('p1-block');
      const p2Block = document.getElementById('p2-block');
      if (!p1Block || !p2Block) {
        requestAnimationFrame(drawWaves);
        return;
      }

      const p1Color = getComputedStyle(p1Block).getPropertyValue('--team-color').trim() || '#ff0000';
      const p2Color = getComputedStyle(p2Block).getPropertyValue('--team-color').trim() || '#0000ff';

      const gradient = waveCtx.createLinearGradient(0, 0, waveWidth, 0);
      gradient.addColorStop(0, p1Color);
      gradient.addColorStop(0.35, p1Color);
      gradient.addColorStop(0.48, 'rgba(255, 255, 255, 0.4)');
      gradient.addColorStop(0.52, 'rgba(255, 255, 255, 0.4)');
      gradient.addColorStop(0.65, p2Color);
      gradient.addColorStop(1, p2Color);

      const tanSkew = Math.tan(-20 * Math.PI / 180); 
      
      waveCtx.save();
      waveCtx.filter = "blur(3px)";

      // CLIPPING
      waveCtx.beginPath();
      document.querySelectorAll('.block').forEach(block => {
        const w = block.offsetWidth;
        const h = block.offsetHeight;
        const canvasLeft = parseFloat(waveCanvas.style.left) || 0;
        const x = block.offsetLeft - canvasLeft;
        
        const shiftX = h * tanSkew;
        const halfS = shiftX / 2;

        if (w <= 0) return;

        waveCtx.moveTo(x - halfS, 0);
        waveCtx.lineTo(x + w - halfS, 0);
        waveCtx.lineTo(x + w + halfS, h);
        waveCtx.lineTo(x + halfS, h);
        waveCtx.closePath();
      });
      waveCtx.clip();

      // DRAW
      waves.forEach((w) => {
        waveCtx.beginPath();
        waveCtx.strokeStyle = gradient;
        waveCtx.globalAlpha = w.opacity;
        waveCtx.lineWidth = 12;

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
      requestAnimationFrame(drawWaves);
    }"""

# Replace the entire drawWaves function block
# The original starts at 'function drawWaves() {' and ends before '// Initial calls'
pattern = r'function drawWaves\(\) \{.*?\}\s+// Initial calls'
replacement = clean_draw_waves + "\n\n    // Initial calls"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Scoreboard syntax and logic restored.")
