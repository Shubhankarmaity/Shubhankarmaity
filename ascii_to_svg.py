#!/usr/bin/env python3
"""
ascii_to_svg.py
Converts a photo into a terminal-style animated braille-art SVG,
for use in a GitHub profile README (matches the "neofetch card" look).

Usage:
    python ascii_to_svg.py --input photo.jpg --cols 60 --out-dir .

Produces:
    dark.svg   (bright dots, for GitHub dark mode)
    light.svg  (dark dots, for GitHub light mode)

In your README.md, embed both like this so GitHub swaps automatically:

    <img src="dark.svg#gh-dark-mode-only" width="380" />
    <img src="light.svg#gh-light-mode-only" width="380" />
"""

import argparse
from PIL import Image, ImageOps

# Unicode braille cell = 2 cols x 4 rows of dots.
# Bit weights per dot position (row, col):
DOT_BITS = {
    (0, 0): 0x01, (1, 0): 0x02, (2, 0): 0x04, (3, 0): 0x40,
    (0, 1): 0x08, (1, 1): 0x10, (2, 1): 0x20, (3, 1): 0x80,
}


def image_to_braille_rows(path, cols=60, threshold=140, invert=False):
    """Convert an image to a list of braille-art text rows."""
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img)

    # Each braille cell covers a 2x4 pixel block, and terminal cells are
    # taller than wide, so we correct the aspect ratio (~2.0x) for pixels.
    px_w = cols * 2
    aspect = img.height / img.width
    px_h = int(px_w * aspect / 2.0) * 4 // 4 or 4
    px_h -= px_h % 4
    if px_h < 4:
        px_h = 4
    img = img.resize((px_w, px_h))

    pixels = img.load()
    rows_out = []
    for by in range(0, px_h, 4):
        line_chars = []
        for bx in range(0, px_w, 2):
            code = 0
            for dy in range(4):
                for dx in range(2):
                    x, y = bx + dx, by + dy
                    val = pixels[x, y] if x < px_w and y < px_h else 255
                    is_dark = val < threshold
                    if invert:
                        is_dark = not is_dark
                    if is_dark:
                        code |= DOT_BITS[(dy, dx)]
            line_chars.append(chr(0x2800 + code))
        rows_out.append("".join(line_chars))
    return rows_out


def rows_to_svg(rows, dot_color="#7dd3fc", bg="none", font_size=10, line_height=11):
    width = max(len(r) for r in rows) * (font_size * 0.6) + 20
    height = len(rows) * line_height + 20

    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {int(width)} {int(height)}" '
        f'width="{int(width)}" height="{int(height)}">',
        f'<rect width="100%" height="100%" fill="{bg}"/>',
        "<style>",
        "text { font-family: 'Courier New', monospace; white-space: pre; }",
        ".row { opacity: 0; animation: reveal 0.6s ease forwards; }",
        "@keyframes reveal { to { opacity: 1; } }",
        "</style>",
    ]

    for i, row in enumerate(rows):
        y = 15 + i * line_height
        delay = round(i * 0.035, 3)
        escaped = (
            row.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        svg_lines.append(
            f'<text class="row" x="10" y="{y}" font-size="{font_size}" '
            f'fill="{dot_color}" style="animation-delay:{delay}s">{escaped}</text>'
        )

    svg_lines.append("</svg>")
    return "\n".join(svg_lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to your photo")
    ap.add_argument("--cols", type=int, default=60, help="Braille columns (width)")
    ap.add_argument("--out-dir", default=".", help="Output directory")
    ap.add_argument("--threshold", type=int, default=140)
    args = ap.parse_args()

    rows = image_to_braille_rows(args.input, cols=args.cols, threshold=args.threshold)

    dark_svg = rows_to_svg(rows, dot_color="#7dd3fc", bg="none")
    light_svg = rows_to_svg(rows, dot_color="#1e3a8a", bg="none")

    with open(f"{args.out_dir}/dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(f"{args.out_dir}/light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)

    print(f"Wrote {args.out_dir}/dark.svg and {args.out_dir}/light.svg ({len(rows)} rows)")


if __name__ == "__main__":
    main()
