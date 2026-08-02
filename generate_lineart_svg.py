#!/usr/bin/env python3
"""
generate_lineart_svg.py
Converts avatar photo into crisp floating line-art braille (no solid background block).
"""
import sys
sys.path.insert(0, "d:/Readme File/Shubhankarmaity/lib")

from PIL import Image, ImageOps, ImageFilter

DOT_BITS = {
    (0, 0): 0x01, (1, 0): 0x02, (2, 0): 0x04, (3, 0): 0x40,
    (0, 1): 0x08, (1, 1): 0x10, (2, 1): 0x20, (3, 1): 0x80,
}

def image_to_lineart_braille(img, cols=65):
    img = img.convert("L")
    
    # Crop character
    crop_w = int(img.height * 1.0)
    portrait = img.crop((0, 0, crop_w, img.height))
    
    # Resize
    px_w = cols * 2
    aspect = portrait.height / portrait.width
    px_h = int(px_w * aspect / 2.0)
    px_h -= px_h % 4
    portrait = portrait.resize((px_w, px_h))

    # Edge detection to extract clean outlines without background box
    edges = portrait.filter(ImageFilter.FIND_EDGES)
    edges = ImageOps.autocontrast(edges)
    
    pixels = edges.load()
    rows_out = []
    threshold = 90
    
    for by in range(0, px_h, 4):
        line_chars = []
        for bx in range(0, px_w, 2):
            code = 0
            for dy in range(4):
                for dx in range(2):
                    x, y = bx + dx, by + dy
                    val = pixels[x, y] if x < px_w and y < px_h else 0
                    if val > threshold:  # edge pixel!
                        code |= DOT_BITS[(dy, dx)]
            line_chars.append(chr(0x2800 + code))
        rows_out.append("".join(line_chars))
    return rows_out

def rows_to_svg(rows, dot_color="#7dd3fc", bg="none", font_size=10, line_height=11):
    width = max(len(r) for r in rows) * (font_size * 0.6) + 20
    height = len(rows) * line_height + 20

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(width)} {int(height)}" width="{int(width)}" height="{int(height)}">',
        f'<rect width="100%" height="100%" fill="{bg}"/>',
        "<style>",
        "text { font-family: 'Courier New', monospace; white-space: pre; }",
        ".row { opacity: 0; animation: reveal 0.6s ease forwards; }",
        "@keyframes reveal { to { opacity: 1; } }",
        "</style>",
    ]

    for i, row in enumerate(rows):
        y = 15 + i * line_height
        delay = round(i * 0.03, 3)
        escaped = row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_lines.append(
            f'<text class="row" x="10" y="{y}" font-size="{font_size}" fill="{dot_color}" style="animation-delay:{delay}s">{escaped}</text>'
        )

    svg_lines.append("</svg>")
    return "\n".join(svg_lines)

def main():
    img = Image.open("assets/myphoto.png")
    rows = image_to_lineart_braille(img, cols=65)
    
    dark_svg = rows_to_svg(rows, dot_color="#58a6ff", bg="none")
    light_svg = rows_to_svg(rows, dot_color="#0969da", bg="none")

    with open("dark_lineart.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("light_lineart.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)
    print("Wrote dark_lineart.svg and light_lineart.svg")

if __name__ == "__main__":
    main()
