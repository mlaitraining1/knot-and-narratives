"""
Generates original, abstract placeholder imagery for The Knot & Narratives.
These are NOT photographs of people/events — they are generative gradient +
bokeh compositions in the brand palette, meant to stand in for the
photographer's real portfolio work until he uploads it. Fully original,
license-free, self-hosted (no external hotlinking / no reliability risk).
"""
import random
from PIL import Image, ImageDraw, ImageFilter

random.seed(7)

PALETTE = {
    "gold":   [(217, 154, 52), (184, 127, 35), (247, 214, 148), (255, 236, 196)],
    "ink":    [(27, 46, 40), (46, 69, 61), (13, 22, 19), (61, 92, 79)],
    "rose":   [(193, 118, 111), (231, 196, 190), (107, 52, 46), (219, 158, 150)],
    "dusk":   [(27, 46, 40), (193, 118, 111), (217, 154, 52), (46, 69, 61)],
    "ivory":  [(251, 246, 236), (243, 234, 216), (217, 154, 52), (231, 196, 190)],
}

def make_image(w, h, mood="dusk", bokeh=14, grain=10, streaks=0, vignette=True, seed=None):
    if seed is not None:
        random.seed(seed)
    colors = PALETTE[mood]
    base = Image.new("RGB", (w, h), colors[0])

    # Diagonal gradient underlay
    grad = Image.new("RGB", (w, h))
    top = random.choice(colors)
    bottom = random.choice([c for c in colors if c != top])
    for y in range(h):
        t = y / h
        row = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        for x in range(0, w, 4):
            grad.paste(row, (x, y, min(x + 4, w), y + 1))
    base = Image.blend(base, grad, 0.9)

    draw_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(draw_layer)

    # Bokeh circles (soft blurred light discs — classic golden-hour wedding-photo look)
    for _ in range(bokeh):
        r = random.randint(int(min(w, h) * 0.03), int(min(w, h) * 0.16))
        cx = random.randint(-r, w + r)
        cy = random.randint(-r, h + r)
        c = random.choice(colors)
        alpha = random.randint(28, 90)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(c[0], c[1], c[2], alpha))

    # Motion streaks (implies choreography / movement)
    for _ in range(streaks):
        y0 = random.randint(0, h)
        length = random.randint(int(w * 0.3), int(w * 0.8))
        x0 = random.randint(0, w - length)
        thickness = random.randint(2, 6)
        c = random.choice(colors)
        draw.line([(x0, y0), (x0 + length, y0 - random.randint(20, 90))],
                   fill=(c[0], c[1], c[2], random.randint(20, 45)), width=thickness)

    draw_layer = draw_layer.filter(ImageFilter.GaussianBlur(radius=min(w, h) * 0.02))
    base = Image.alpha_composite(base.convert("RGBA"), draw_layer).convert("RGB")

    # Fine grain (film-like texture)
    if grain:
        noise = Image.effect_noise((w, h), grain).convert("L")
        noise_rgb = Image.merge("RGB", (noise, noise, noise))
        base = Image.blend(base, noise_rgb, 0.035)

    # Vignette
    if vignette:
        vig = Image.new("L", (w, h), 0)
        vd = ImageDraw.Draw(vig)
        vd.ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
        vig = vig.filter(ImageFilter.GaussianBlur(radius=min(w, h) * 0.18))
        dark = Image.new("RGB", (w, h), (10, 16, 14))
        base = Image.composite(base, dark, vig)

    base = base.filter(ImageFilter.GaussianBlur(radius=0.4))
    return base

OUT = "/home/claude/site/images/gallery"
import os
os.makedirs(OUT, exist_ok=True)

jobs = [
    # (filename, w, h, mood, bokeh, streaks, seed)
    ("hero-home.jpg", 1920, 1200, "dusk", 26, 6, 1),
    ("hero-portfolio.jpg", 1920, 900, "gold", 22, 4, 2),
    ("hero-stories.jpg", 1920, 900, "rose", 20, 2, 3),
    ("hero-about.jpg", 1920, 900, "ink", 18, 3, 4),
    ("hero-services.jpg", 1920, 900, "dusk", 20, 8, 5),
    ("hero-pricing.jpg", 1920, 900, "gold", 16, 2, 6),
    ("hero-contact.jpg", 1920, 900, "ink", 18, 2, 7),
    ("hero-gallery.jpg", 1920, 900, "rose", 18, 2, 8),
    ("og-cover.jpg", 1200, 630, "dusk", 20, 4, 9),

    ("portfolio-01.jpg", 900, 1200, "gold", 16, 5, 11),
    ("portfolio-02.jpg", 900, 700, "rose", 14, 2, 12),
    ("portfolio-03.jpg", 900, 1100, "ink", 16, 6, 13),
    ("portfolio-04.jpg", 900, 900, "dusk", 15, 3, 14),
    ("portfolio-05.jpg", 900, 1300, "gold", 18, 7, 15),
    ("portfolio-06.jpg", 900, 700, "ivory", 12, 2, 16),
    ("portfolio-07.jpg", 900, 1150, "rose", 15, 4, 17),
    ("portfolio-08.jpg", 900, 900, "ink", 14, 5, 18),
    ("portfolio-09.jpg", 900, 1250, "gold", 17, 6, 19),
    ("portfolio-10.jpg", 900, 700, "dusk", 13, 2, 20),
    ("portfolio-11.jpg", 900, 1100, "rose", 15, 3, 21),
    ("portfolio-12.jpg", 900, 950, "ivory", 12, 2, 22),
    ("portfolio-13.jpg", 900, 1200, "ink", 16, 8, 23),
    ("portfolio-14.jpg", 900, 750, "gold", 14, 4, 24),
    ("portfolio-15.jpg", 900, 1150, "dusk", 15, 5, 25),

    ("story-01-feature.jpg", 1000, 1200, "gold", 16, 3, 31),
    ("story-02-feature.jpg", 1000, 1200, "rose", 15, 2, 32),
    ("story-01.jpg", 900, 700, "dusk", 13, 2, 33),
    ("story-02.jpg", 900, 700, "gold", 12, 1, 34),
    ("story-03.jpg", 900, 700, "ink", 13, 3, 35),
    ("story-04.jpg", 900, 700, "rose", 12, 2, 36),
    ("story-05.jpg", 900, 700, "ivory", 11, 1, 37),
    ("story-06.jpg", 900, 700, "gold", 13, 2, 38),

    ("about-portrait.jpg", 1000, 1250, "ink", 14, 2, 41),
    ("about-founder-1.jpg", 800, 1000, "gold", 12, 1, 42),
    ("about-founder-2.jpg", 800, 1000, "rose", 12, 1, 43),
    ("about-studio-1.jpg", 1000, 750, "dusk", 14, 3, 44),
    ("about-studio-2.jpg", 1000, 750, "ivory", 12, 1, 45),

    ("service-photo.jpg", 900, 1100, "gold", 15, 4, 51),
    ("service-choreo.jpg", 900, 1100, "dusk", 16, 9, 52),
    ("service-films.jpg", 900, 1100, "ink", 14, 6, 53),

    ("gallery-sample-01.jpg", 900, 1100, "gold", 14, 2, 61),
    ("gallery-sample-02.jpg", 900, 800, "rose", 12, 1, 62),
    ("gallery-sample-03.jpg", 900, 1050, "ink", 13, 2, 63),
    ("gallery-sample-04.jpg", 900, 900, "dusk", 12, 3, 64),
    ("gallery-sample-05.jpg", 900, 1100, "ivory", 11, 1, 65),
    ("gallery-sample-06.jpg", 900, 750, "gold", 12, 2, 66),

    ("insta-01.jpg", 520, 360, "gold", 8, 2, 71),
    ("insta-02.jpg", 520, 360, "rose", 8, 1, 72),
    ("insta-03.jpg", 520, 360, "ink", 8, 2, 73),
    ("insta-04.jpg", 520, 360, "dusk", 8, 3, 74),
    ("insta-05.jpg", 520, 360, "ivory", 7, 1, 75),
    ("insta-06.jpg", 520, 360, "gold", 8, 2, 76),
    ("insta-07.jpg", 520, 360, "rose", 8, 1, 77),
    ("insta-08.jpg", 520, 360, "ink", 8, 2, 78),
]

for name, w, h, mood, bokeh, streaks, seed in jobs:
    img = make_image(w, h, mood=mood, bokeh=bokeh, streaks=streaks, seed=seed)
    img.save(f"{OUT}/{name}", quality=82, optimize=True)

print(f"Generated {len(jobs)} images in {OUT}")
