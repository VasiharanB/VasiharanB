from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import os
import random

WIDTH, HEIGHT = 960, 300
FRAMES = 24
random.seed(20260920)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

TITLE = ImageFont.truetype(FONT_BOLD, 44)
SUBTITLE = ImageFont.truetype(FONT_BOLD, 14)
MONO = ImageFont.truetype(FONT_MONO, 12)

particles = [
    (random.randrange(WIDTH), random.randrange(HEIGHT),
     random.uniform(0.5, 1.3), random.uniform(0, math.tau))
    for _ in range(110)
]

frames = []

for frame in range(FRAMES):
    image = Image.new("RGB", (WIDTH, HEIGHT), (4, 4, 5))

    # Deep cinematic gradient.
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        r = 4 + int(11 * y / HEIGHT)
        g = 4 + int(8 * y / HEIGHT)
        b = 3 + int(5 * y / HEIGHT)
        draw.line((0, y, WIDTH, y), fill=(r, g, b))

    # Moving golden light bloom.
    bloom = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    bloom_draw = ImageDraw.Draw(bloom)
    sweep_x = -160 + ((frame * 58) % (WIDTH + 360))
    bloom_draw.ellipse(
        (sweep_x - 140, 25, sweep_x + 140, HEIGHT - 20),
        fill=(232, 182, 70, 42),
    )
    bloom_draw.ellipse(
        (WIDTH - sweep_x - 180, 55, WIDTH - sweep_x + 100, HEIGHT + 80),
        fill=(255, 224, 120, 18),
    )
    bloom = bloom.filter(ImageFilter.GaussianBlur(34))
    image = Image.alpha_composite(image.convert("RGBA"), bloom)

    draw = ImageDraw.Draw(image)

    # Tech grid.
    for x in range(0, WIDTH, 36):
        draw.line((x, 0, x, HEIGHT), fill=(220, 170, 60, 10), width=1)
    for y in range(0, HEIGHT, 36):
        draw.line((0, y, WIDTH, y), fill=(220, 170, 60, 8), width=1)

    # Glitter field.
    for x, y, size, phase in particles:
        xx = (x + frame * 7) % WIDTH
        yy = y + 2 * math.sin(frame / 3 + phase)
        intensity = int(45 + 150 * (0.5 + 0.5 * math.sin(frame * 0.65 + phase)))
        radius = max(1, int(size))
        draw.ellipse(
            (xx - radius, yy - radius, xx + radius, yy + radius),
            fill=(248, 213, 113, intensity),
        )
        if intensity > 150:
            draw.line((xx - 3, yy, xx + 3, yy), fill=(255, 242, 170, intensity), width=1)
            draw.line((xx, yy - 3, xx, yy + 3), fill=(255, 242, 170, intensity), width=1)

    # Rotating orbital HUD.
    cx, cy = 805, 92
    angle = frame * math.tau / 18
    draw.ellipse(
        (cx - 92, cy - 38, cx + 92, cy + 38),
        outline=(226, 179, 67, 120),
        width=1,
    )
    px = cx + 92 * math.cos(angle)
    py = cy + 38 * math.sin(angle)
    draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=(255, 236, 150, 240))

    # Frame corners.
    draw.rounded_rectangle(
        (2, 2, WIDTH - 3, HEIGHT - 3),
        radius=18,
        outline=(220, 172, 58, 145),
        width=1,
    )
    draw.line((24, 34, 60, 34), fill=(236, 193, 91, 220), width=3)
    draw.line((24, 34, 24, 64), fill=(236, 193, 91, 220), width=3)
    draw.line((WIDTH - 60, 34, WIDTH - 24, 34), fill=(236, 193, 91, 220), width=3)
    draw.line((WIDTH - 24, 34, WIDTH - 24, 64), fill=(236, 193, 91, 220), width=3)

    # Status pill.
    draw.rounded_rectangle(
        (343, 28, 617, 56),
        radius=14,
        fill=(20, 14, 6),
        outline=(215, 165, 52, 180),
        width=1,
    )
    pulse = 4 + 2 * math.sin(frame * math.pi / 5)
    draw.ellipse(
        (360 - pulse, 42 - pulse, 360 + pulse, 42 + pulse),
        fill=(246, 209, 111, 235),
    )
    draw.text(
        (375, 34),
        "BUILDING REAL-WORLD SOFTWARE",
        font=SUBTITLE,
        fill=(242, 216, 130, 255),
    )

    # Cinematic title with moving shimmer.
    title = "VASIHARAN B"
    bbox = draw.textbbox((0, 0), title, font=TITLE)
    title_width = bbox[2] - bbox[0]
    title_x = (WIDTH - title_width) // 2
    title_y = 92

    draw.text(
        (title_x + 2, title_y + 2),
        title,
        font=TITLE,
        fill=(75, 45, 9, 170),
    )
    draw.text(
        (title_x, title_y),
        title,
        font=TITLE,
        fill=(245, 216, 137, 255),
    )

    shimmer_x = title_x - 60 + ((frame * 38) % (title_width + 160))
    shine = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    shine_draw = ImageDraw.Draw(shine)
    shine_draw.rectangle(
        (shimmer_x, title_y - 4, shimmer_x + 70, title_y + 52),
        fill=(255, 246, 186, 120),
    )
    shine = shine.filter(ImageFilter.GaussianBlur(8))
    image = Image.alpha_composite(image, shine)
    draw = ImageDraw.Draw(image)
    draw.text(
        (title_x, title_y),
        title,
        font=TITLE,
        fill=(255, 233, 165, 220),
    )

    subtitle = "ELECTRONICS & COMMUNICATION ENGINEERING  •  FULL-STACK  •  AI & SYSTEMS"
    sb = draw.textbbox((0, 0), subtitle, font=SUBTITLE)
    draw.text(
        ((WIDTH - (sb[2] - sb[0])) / 2, 148),
        subtitle,
        font=SUBTITLE,
        fill=(221, 214, 199, 255),
    )

    draw.line((258, 188, 458, 188), fill=(224, 173, 59, 210), width=1)
    draw.line((502, 188, 702, 188), fill=(224, 173, 59, 210), width=1)
    draw.polygon(
        [(480, 182), (486, 188), (480, 194), (474, 188)],
        fill=(255, 235, 150, 255),
    )

    draw.text(
        (340, 216),
        "CODE  •  SYSTEMS  •  AI  •  SHIP",
        font=MONO,
        fill=(160, 150, 135, 255),
    )
    draw.text(
        (274, 246),
        "TURNING PRACTICAL PROBLEMS INTO WORKING SOFTWARE",
        font=SUBTITLE,
        fill=(226, 218, 202, 235),
    )

    frames.append(image.convert("P"))

output = "assets/hero.gif"
os.makedirs(os.path.dirname(output), exist_ok=True)
frames[0].save(
    output,
    save_all=True,
    append_images=frames[1:],
    duration=95,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Generated {output} ({os.path.getsize(output)} bytes)")
