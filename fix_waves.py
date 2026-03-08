
import os

path = r'c:\Users\dark1\.gemini\antigravity\scratch\HaloWarsCastingTool\casting_html\score.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Redefine waves for better transparency/clarity
waves_code = """    const waves = [
      { y: 0.5, length: 0.005, amplitude: 40, speed: 0.006, opacity: 0.5 },
      { y: 0.5, length: 0.009, amplitude: 30, speed: -0.005, opacity: 0.4 },
      { y: 0.5, length: 0.003, amplitude: 50, speed: 0.004, opacity: 0.5 },
      { y: 0.5, length: 0.007, amplitude: 20, speed: 0.008, opacity: 0.6 },
      { y: 0.5, length: 0.004, amplitude: 35, speed: -0.003, opacity: 0.4 }
    ];"""

import re
content = re.sub(r'const waves = \[.*?\];', waves_code, content, flags=re.DOTALL)

# 2. Fix clipping logic in drawWaves
clipping_logic = """      // CREATE CLIPPING PATH
      waveCtx.beginPath();
      document.querySelectorAll('.block').forEach(block => {
        const w = block.offsetWidth;
        const h = block.offsetHeight;
        const canvasLeft = parseFloat(waveCanvas.style.left) || 0;
        
        // offsetLeft is relative to #scoreboard.
        const x = block.offsetLeft - canvasLeft;
        
        // Match the / lean (skewX -20deg). bottom moves +h*tan(20)
        const tanSkew = Math.tan(20 * Math.PI / 180);
        const skewShift = h * tanSkew;
        const halfShift = skewShift / 2;

        if (w <= 0) return;

        // Origin 50% 50%: top is shifted left, bottom shifted right
        waveCtx.moveTo(x - halfShift, 0);
        waveCtx.lineTo(x + w - halfShift, 0);
        waveCtx.lineTo(x + w + halfShift, h);
        waveCtx.lineTo(x + halfShift, h);
        waveCtx.closePath();
      });
      waveCtx.clip();"""

# Replace the old loop
content = re.sub(r'// CREATE CLIPPING PATH.*?waveCtx\.clip\(\);', clipping_logic, content, flags=re.DOTALL)

# 3. Final touch: remove shadow blur and adjust width
content = content.replace('waveCtx.lineWidth = 15; // Slightly thinner', 'waveCtx.lineWidth = 12;')
content = content.replace('waveCtx.shadowBlur = 0; // Remove shadow to prevent border bleed', 'waveCtx.shadowBlur = 0;')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied final fixes via script.")
