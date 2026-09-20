from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

WIDTH, HEIGHT = 1200, 350
FRAMES = 12

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TITLE = ImageFont.truetype(SERIF, 58)
SUBTITLE = ImageFont.truetype(SANS, 17)
TAGLINE = ImageFont.truetype(SANS, 16)

def center_x(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return (WIDTH - (box[2] - box[0])) // 2

frames = []

for i in range(FRAMES):
    t = i / FRAMES
    image = Image.new("RGB", (WIDTH, HEIGHT), (8, 8, 9))

    # Soft charcoal vertical gradient.
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        q = y / HEIGHT
        r = 8 + int(6 * q)
        g = 8 + int(5 * q)
        b = 9 + int(4 * q)
        draw.line((0, y, WIDTH, y), fill=(r, g, b))

    image = image.convert("RGBA")

    # Gentle ambient glow; deliberately slow and restrained.
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx = int(-160 + (WIDTH + 320) * t)
    gd.ellipse((cx - 180, 120, cx + 180, 480), fill=(220, 170, 65, 18))
    glow = glow.filter(ImageFilter.GaussianBlur(75))
    image = Image.alpha_composite(image, glow)

    draw = ImageDraw.Draw(image)

    # Minimal gold arc.
    bbox = (-180, 45, WIDTH + 180, 470)
    draw.arc(bbox, start=198, end=342, fill=(194, 146, 48, 155), width=1)

    # Moving highlight on the arc.
    hx = int(95 + (WIDTH - 190) * t)
    highlight = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    hd = ImageDraw.Draw(highlight)
    hd.ellipse((hx - 32, 165, hx + 32, 225), fill=(255, 214, 118, 55))
    highlight = highlight.filter(ImageFilter.GaussianBlur(18))
    image = Image.alpha_composite(image, highlight)

    draw = ImageDraw.Draw(image)

    title = "VASIHARAN B"
    tx = center_x(draw, title, TITLE)
    draw.text((tx, 108), title, font=TITLE, fill=(236, 207, 143, 255))

    subtitle = "ELECTRONICS & COMMUNICATION ENGINEERING   •   FULL-STACK   •   AI & SYSTEMS"
    draw.text((center_x(draw, subtitle, SUBTITLE), 181), subtitle, font=SUBTITLE, fill=(209, 205, 197, 235))

    # Fine divider with a soft center glint.
    y = 222
    draw.line((355, y, 845, y), fill=(159, 118, 42, 150), width=1)
    draw.ellipse((596, y - 2, 604, y + 6), fill=(242, 207, 119, 220))

    tagline = "TURNING PRACTICAL PROBLEMS INTO WORKING SOFTWARE"
    draw.text((center_x(draw, tagline, TAGLINE), 261), tagline, font=TAGLINE, fill=(190, 185, 176, 225))

    # Slight vignette for a calmer cinematic finish.
    vignette = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vignette)
    vd.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0, 22))
    vignette = vignette.filter(ImageFilter.GaussianBlur(30))
    image = Image.alpha_composite(image, vignette)

    frames.append(image.convert("P", palette=Image.Palette.ADAPTIVE, colors=64))

output = "assets/hero.gif"
os.makedirs(os.path.dirname(output), exist_ok=True)

frames[0].save(
    output,
    save_all=True,
    append_images=frames[1:],
    duration=170,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Generated {output} ({os.path.getsize(output)} bytes)")
