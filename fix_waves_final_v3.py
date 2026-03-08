
import os
import re

path = r'c:\Users\dark1\.gemini\antigravity\scratch\HaloWarsCastingTool\casting_html\score.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Completely rewrite drawing logic with correct clipping
clipping_logic = """      // CREATE CLIPPING PATH
      waveCtx.beginPath();
      const tanSkew = Math.tan(-20 * Math.PI / 180); 
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

      // DRAW WAVES"""

# Find the loop entry and DRAW WAVES comment
# Current code looks like:
# document.querySelectorAll('.block').forEach(block => { ... vars ... waves.forEach((w) => {
# I will replace from the start of the block query to the start of waves loop.

pattern = r'document\.querySelectorAll\(\'\.block\'\)\.forEach\(block => \{.*?waves\.forEach\(\(w\) => \{'
replacement = clipping_logic + "\n      waves.forEach((w) => {"
content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Ensure waveTime++ is present
if 'waveTime++;' not in content:
    content = content.replace('waveCtx.restore();', 'waveCtx.restore();\n      waveTime++;')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed clipping logic successfully.")
