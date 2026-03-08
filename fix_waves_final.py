
import os
import re

path = r'c:\Users\dark1\.gemini\antigravity\scratch\HaloWarsCastingTool\casting_html\score.html'

with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Correct tanSkew to match skewX(-20deg) -> negative
content = content.replace('const tanSkew = Math.tan(20 * Math.PI / 180); // POSITIVE skew for right-leaning /', 
                          'const tanSkew = Math.tan(-20 * Math.PI / 180); // Correct for skewX(-20deg)')
# There's another one inside the loop in some previous version or my last rewrite
content = content.replace('const tanSkew = Math.tan(20 * Math.PI / 180);', 
                          'const tanSkew = Math.tan(-20 * Math.PI / 180);')

# 2. Update the clipping polygon math for negative skew (\ lean)
# Current: 
# waveCtx.moveTo(x - halfShift, 0); 
# waveCtx.lineTo(x + w - halfShift, 0);
# waveCtx.lineTo(x + w + halfShift, h);
# waveCtx.lineTo(x + halfShift, h);
# With negative tanSkew, halfShift will be negative.
# Let's write it explicitly for clarity:
clipping_logic = """      // CREATE CLIPPING PATH
      waveCtx.beginPath();
      document.querySelectorAll('.block').forEach(block => {
        const w = block.offsetWidth;
        const h = block.offsetHeight;
        const canvasLeft = parseFloat(waveCanvas.style.left) || 0;
        const x = block.offsetLeft - canvasLeft;
        
        // Match skewX(-20deg).
        const angleRad = -20 * Math.PI / 180;
        const tanS = Math.tan(angleRad);
        const shiftX = h * tanS;
        const halfS = shiftX / 2;

        if (w <= 0) return;

        // With negative skew, top is at x - halfShift (which is x + positive_value because halfS is negative)
        // Wait, tan(-20) is -0.36. halfS = (h * -0.36)/2 = -0.18h.
        // Top shift = -halfS = +0.18h (Moves Right). Correct for \
        // Bottom shift = +halfS = -0.18h (Moves Left). Correct for \
        waveCtx.moveTo(x - halfS, 0);
        waveCtx.lineTo(x + w - halfS, 0);
        waveCtx.lineTo(x + w + halfS, h);
        waveCtx.lineTo(x + halfS, h);
        waveCtx.closePath();
      });
      waveCtx.clip();"""

content = re.sub(r'// CREATE CLIPPING PATH.*?waveCtx\.clip\(\);', clipping_logic, content, flags=re.DOTALL)

# 3. Remove CSS blur to prevent bleeding
content = content.replace('filter: blur(3px);', 'filter: none;')
content = content.replace('/* Softer, ambient look */', '/* Blur removed to prevent edge bleed */')

# 4. Add internal blur to waves (optional but nice)
content = content.replace('waveCtx.save();', 'waveCtx.save();\n      waveCtx.filter = "blur(3px)";')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied skew correction and removed bleed.")
