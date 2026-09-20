from pathlib import Path
import math
import os
import re
import tempfile

import cairosvg
from PIL import Image

WIDTH, HEIGHT = 1200, 340
FRAME_COUNT = 28
FRAME_DELAY_MS = 500

SVG_PATH = Path("assets/header.svg")
OUTPUT = Path("assets/hero.gif")
TMP = Path(tempfile.mkdtemp(prefix="header-gif-"))

source = SVG_PATH.read_text(encoding="utf-8")

# Turn the real animated SVG into rasterized video frames.
# The artwork/layout comes directly from assets/header.svg; only the
# SVG animation states are baked into individual frames.
base = re.sub(r'<animate(?:Transform)?\b[^>]*/>', '', source)


def bake_frame(t: float) -> str:
    s = base

    # Animated gold-gradient sweep: 8-second cycle.
    p8 = (t % 8.0) / 8.0
    x1 = -100 + 200 * p8
    x2 = 0 + 200 * p8
    s = re.sub(
        r'(<linearGradient id="gold"[^>]*\bx1=")[^"]*(")',
        rf'\g<1>{x1:.3f}%\g<2>',
        s,
        count=1,
    )
    s = re.sub(
        r'(<linearGradient id="gold"[^>]*\bx1="[^"]*"[^>]*\bx2=")[^"]*(")',
        rf'\g<1>{x2:.3f}%\g<2>',
        s,
        count=1,
    )

    # Moving scan line: 6-second cycle.
    p6 = (t % 6.0) / 6.0
    scan_x = -160 + 1360 * p6
    s = re.sub(
        r'(<rect x=")[^"]+(" y="0" width="160" height="340" fill="#F4CF6A")',
        rf'\g<1>{scan_x:.3f}\g<2>',
        s,
        count=1,
    )

    # Orbiting rings: preserve the original 10s and 14s motion.
    angle1 = 360 * ((t % 10.0) / 10.0)
    angle2 = -360 * ((t % 14.0) / 14.0)
    ellipses = list(re.finditer(r'<ellipse rx="92" ry="38"[^>]*>', s))
    replacements = [
        f'<ellipse transform="rotate({angle1:.3f})" rx="92" ry="38" fill="none" stroke="#E6B64B" stroke-width="1.2">',
        f'<ellipse transform="rotate({angle2:.3f})" rx="92" ry="38" fill="none" stroke="#C9901F" stroke-width="0.8" opacity="0.7">',
    ]
    for match, replacement in zip(reversed(ellipses[:2]), reversed(replacements)):
        s = s[:match.start()] + replacement + s[match.end():]

    # 2-second pulsing center orb and live badge.
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * ((t % 2.0) / 2.0) - math.pi / 2)
    orb_r = 6 + 3 * pulse
    orb_opacity = 0.6 + 0.4 * pulse
    s = re.sub(
        r'(<circle cx="0" cy="0" r=")[^"]+(" fill="#FFF0A6")',
        rf'\g<1>{orb_r:.3f}\g<2>',
        s,
        count=1,
    )
    s = re.sub(
        r'(<circle cx="0" cy="0" r="[^"]+" fill="#FFF0A6" filter="#[^"]*"?)',
        lambda m: m.group(1),
        s,
        count=0,
    )
    s = re.sub(
        r'(<circle cx="0" cy="0" r="[^"]+" fill="#FFF0A6"[^>]*)>',
        rf'\1 opacity="{orb_opacity:.3f}">',
        s,
        count=1,
    )

    badge_r = 4 + 2 * pulse
    s = re.sub(
        r'(<g transform="translate\(455 34\)">\s*<rect[^>]+>\s*<circle cx="20" cy="15" r=")[^"]+(" fill="#E4B74B")',
        rf'\g<1>{badge_r:.3f}\g<2>',
        s,
        count=1,
    )

    # Center diamond rotation: 6-second cycle.
    diamond_angle = 360 * p6
    s = re.sub(
        r'(<polygon points="600,-6 606,0 600,6 594,0"[^>]*)(>)',
        rf'\1 transform="rotate({diamond_angle:.3f} 600 0)"\2',
        s,
        count=1,
    )

    return s


frames = []

for index in range(FRAME_COUNT):
    t = index * (FRAME_DELAY_MS / 1000.0)
    svg_frame = bake_frame(t)
    png_path = TMP / f"frame-{index:03d}.png"

    cairosvg.svg2png(
        bytestring=svg_frame.encode("utf-8"),
        write_to=str(png_path),
        output_width=WIDTH,
        output_height=HEIGHT,
    )

    frame = Image.open(png_path).convert("RGB")
    frame = frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=96)
    frames.append(frame)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
frames[0].save(
    OUTPUT,
    save_all=True,
    append_images=frames[1:],
    duration=FRAME_DELAY_MS,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Generated {OUTPUT} ({os.path.getsize(OUTPUT)} bytes)")
