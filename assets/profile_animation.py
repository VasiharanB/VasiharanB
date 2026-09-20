from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os

WIDTH, HEIGHT = 960, 300
FRAMES = 18

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

TITLE = ImageFont.truetype(FONT_SERIF, 44)
SUBTITLE = ImageFont.truetype(FONT_BOLD, 14)
MONO = ImageFont.truetype(FONT_MONO, 12)

def center_x(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return (WIDTH - (box[2] - box[0])) // 2

frames = []

for frame in range(FRAMES):
    t = frame / FRAMES

    image = Image.new("RGB", (WIDTH, HEIGHT), (7, 7, 8))
    draw = ImageDraw.Draw(image)

    # Calm charcoal gradient.
    for y in range(HEIGHT):
        q = y / HEIGHT
        draw.line(
            (0, y, WIDTH, y),
            fill=(8 + int(9*q), 8 + int(7*q), 9 + int(4*q)),
        )

    # Soft ambient gold glow. The only strong motion in the banner.
    ambient = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ambient_draw = ImageDraw.Draw(ambient)

    glow_x = int(-160 + (WIDTH + 320) * t)
    glow_y = int(170 + 18 * math.sin(math.tau * t))

    ambient_draw.ellipse(
        (glow_x - 190, glow_y - 95, glow_x + 190, glow_y + 95),
        fill=(229, 178, 72, 34),
    )
    ambient_draw.ellipse(
        (WIDTH - glow_x - 120, 45, WIDTH - glow_x + 120, 285),
        fill=(245, 210, 126, 14),
    )
    ambient = ambient.filter(ImageFilter.GaussianBlur(55))
    image = Image.alpha_composite(image.convert("RGBA"), ambient)

    draw = ImageDraw.Draw(image)

    # Minimal frame accents.
    draw.rounded_rectangle(
        (2, 2, WIDTH - 3, HEIGHT - 3),
        radius=18,
        outline=(181, 141, 53, 120),
        width=1,
    )
    draw.line((24, 34, 60, 34), fill=(224, 182, 82, 220), width=2)
    draw.line((24, 34, 24, 64), fill=(224, 182, 82, 220), width=2)
    draw.line((WIDTH - 60, 34, WIDTH - 24, 34), fill=(224, 182, 82, 220), width=2)
    draw.line((WIDTH - 24, 34, WIDTH - 24, 64), fill=(224, 182, 82, 220), width=2)

    # Status pill.
    pill_left, pill_top, pill_right, pill_bottom = 344, 28, 616, 56
    draw.rounded_rectangle(
        (pill_left, pill_top, pill_right, pill_bottom),
        radius=14,
        fill=(15, 12, 8, 245),
        outline=(196, 153, 61, 155),
        width=1,
    )
    draw.ellipse((360, 38, 368, 46), fill=(247, 211, 118, 255))
    draw.text(
        (380, 34),
        "BUILDING REAL-WORLD SOFTWARE",
        font=SUBTITLE,
        fill=(239, 215, 146, 255),
    )

    # Name.
    title = "VASIHARAN B"
    title_x = center_x(draw, title, TITLE)
    draw.text(
        (title_x + 1, 95),
        title,
        font=TITLE,
        fill=(69, 48, 15, 165),
    )
    draw.text(
        (title_x, 93),
        title,
        font=TITLE,
        fill=(245, 218, 151, 255),
    )

    # Very subtle title sheen.
    sheen_x = int(title_x - 120 + (TITLE.size * 3 + 120) * t)
    sheen = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen)
    sheen_draw.rectangle(
        (sheen_x, 92, sheen_x + 45, 143),
        fill=(255, 246, 190, 32),
    )
    sheen = sheen.filter(ImageFilter.GaussianBlur(10))
    image = Image.alpha_composite(image, sheen)
    draw = ImageDraw.Draw(image)

    subtitle = "ELECTRONICS & COMMUNICATION ENGINEERING  •  FULL-STACK  •  AI & SYSTEMS"
    draw.text(
        (center_x(draw, subtitle, SUBTITLE), 151),
        subtitle,
        font=SUBTITLE,
        fill=(211, 207, 196, 248),
    )

    # Clean divider.
    divider_y = 190
    draw.line((284, divider_y, 456, divider_y), fill=(161, 123, 42, 145), width=1)
    draw.line((504, divider_y, 676, divider_y), fill=(161, 123, 42, 145), width=1)
    draw.rounded_rectangle(
        (477, divider_y - 3, 483, divider_y + 3),
        radius=2,
        fill=(242, 211, 128, 245),
    )

    draw.text(
        (center_x(draw, "CODE  •  SYSTEMS  •  AI  •  SHIP", MONO), 216),
        "CODE  •  SYSTEMS  •  AI  •  SHIP",
        font=MONO,
        fill=(148, 142, 131, 235),
    )

    tagline = "TURNING PRACTICAL PROBLEMS INTO WORKING SOFTWARE"
    draw.text(
        (center_x(draw, tagline, SUBTITLE), 247),
        tagline,
        font=SUBTITLE,
        fill=(219, 213, 201, 235),
    )

    frames.append(image.convert("P", palette=Image.Palette.ADAPTIVE, colors=96))

output = "assets/hero.gif"
os.makedirs(os.path.dirname(output), exist_ok=True)

frames[0].save(
    output,
    save_all=True,
    append_images=frames[1:],
    duration=120,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Generated {output} ({os.path.getsize(output)} bytes)")
