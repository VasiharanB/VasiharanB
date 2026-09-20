from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

WIDTH, HEIGHT = 1200, 350
FRAMES = 10

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE = ImageFont.truetype(SERIF, 56)
SUBTITLE = ImageFont.truetype(SANS, 16)
TAGLINE = ImageFont.truetype(SANS, 15)

def center_x(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return (WIDTH - (box[2] - box[0])) // 2

frames = []

for i in range(FRAMES):
    t = i / FRAMES
    image = Image.new("RGB", (WIDTH, HEIGHT), (7, 7, 8))
    draw = ImageDraw.Draw(image)

    # Quiet charcoal gradient.
    for y in range(HEIGHT):
        q = y / HEIGHT
        value = int(8 + 7 * q)
        draw.line((0, y, WIDTH, y), fill=(value, value, value + 1))

    image = image.convert("RGBA")

    # Barely visible warm ambient glow.
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * t)
    alpha = int(10 + 9 * pulse)
    gd.ellipse((WIDTH // 2 - 260, 45, WIDTH // 2 + 260, 320),
               fill=(224, 178, 82, alpha))
    glow = glow.filter(ImageFilter.GaussianBlur(85))
    image = Image.alpha_composite(image, glow)

    draw = ImageDraw.Draw(image)

    # Minimal framing rule — no boxes, grids, badges, or HUD elements.
    draw.line((120, 292, 1080, 292), fill=(148, 109, 40, 75), width=1)

    title = "VASIHARAN B"
    tx = center_x(draw, title, TITLE)
    draw.text((tx, 100), title, font=TITLE, fill=(239, 215, 166, 255))

    subtitle = "ELECTRONICS & COMMUNICATION ENGINEERING   •   FULL-STACK   •   AI & SYSTEMS"
    sx = center_x(draw, subtitle, SUBTITLE)
    draw.text((sx, 174), subtitle, font=SUBTITLE, fill=(205, 202, 195, 235))

    # Small, centered gold rule.
    draw.line((470, 213, 730, 213), fill=(177, 130, 45, 155), width=1)
    draw.ellipse((597, 209, 603, 215), fill=(242, 207, 119, 220))

    tagline = "TURNING PRACTICAL PROBLEMS INTO WORKING SOFTWARE"
    gx = center_x(draw, tagline, TAGLINE)
    draw.text((gx, 244), tagline, font=TAGLINE, fill=(185, 181, 173, 220))

    frames.append(
        image.convert("P", palette=Image.Palette.ADAPTIVE, colors=64)
    )

output = "assets/hero.gif"
os.makedirs(os.path.dirname(output), exist_ok=True)

frames[0].save(
    output,
    save_all=True,
    append_images=frames[1:],
    duration=190,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Generated {output} ({os.path.getsize(output)} bytes)")
