import os

# Localized Names (English)
leaders_banished = ["Atriox", "Decimus", "Voridus", "Pavium", "Colony", "YapYap The Destroyer", "The Arbiter", "Shipmaster"]
leaders_unsc = ["Captain Cutter", "Isabel", "Professor Anders", "Sergeant Forge", "Serina", "Kinsano", "Sergeant Johnson", "Commander Jerome"]

all_leaders = leaders_banished + leaders_unsc

out_dir = os.path.join("casting_html", "leaders")
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
else:
    # Cleanup old SVGs
    for f in os.listdir(out_dir):
        if f.endswith(".svg"):
            os.remove(os.path.join(out_dir, f))

print(f"Generating assets in {out_dir}")

for l in all_leaders:
    is_banished = l in leaders_banished
    # Colors: Dark Red for Banished, Dark Blue for UNSC
    bg_color = "#8B0000" if is_banished else "#00008B"
    text_color = "#FFFFFF"
    
    # Simple SVG placeholder
    svg_content = f'''<svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad_{l}" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
          <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
        </linearGradient>
      </defs>
      <rect width="100%" height="100%" fill="url(#grad_{l})" rx="15" ry="15"/>
      <circle cx="64" cy="50" r="35" stroke="{text_color}" stroke-width="2" fill="none" opacity="0.7"/>
      <text x="50%" y="54%" font-family="Arial, sans-serif" font-weight="bold" font-size="28" fill="{text_color}" text-anchor="middle" dy=".3em">{l[:3].upper()}</text>
      <text x="50%" y="88%" font-family="Arial, sans-serif" font-size="14" fill="{text_color}" text-anchor="middle">{l}</text>
    </svg>'''
    
    filename = f"{l.replace(' ', '_')}.svg"
    filepath = os.path.join(out_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(svg_content)
    print(f"Created {filename}")

print("Done.")
