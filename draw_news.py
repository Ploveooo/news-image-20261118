#!/usr/bin/env python3
"""Draw entry.png: a one-page news front page summing up the world news of
Wednesday 18 November 2026.

Six verified stories (see SOURCES.md), one per card, each with a flat
pictogram, a kicker, a headline and one short summary line. The date is in
the masthead and the footer so the day the image sums up is unmistakable.

Output: 1024x1024 PNG, well under 1 MiB. Run: python3 draw_news.py
Requires Pillow (build-time only; the entry program main.py is stdlib-only
and just copies the finished entry.png).
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 231)      # warm newsprint
INK = (27, 42, 65)           # dark navy text
NAVY = (22, 35, 63)          # masthead band
RED = (193, 39, 45)          # masthead rule
GOLD = (232, 184, 75)        # masthead small caps
CARD = (255, 255, 255)
CARD_EDGE = (201, 194, 178)
SUMMARY = (70, 83, 106)      # grey-navy body text
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    for path in (os.path.join(FONT_DIR, name),
                 "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_SERIF = font("DejaVuSerif-Bold.ttf", 56)
F_KICKER = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 27)
F_BODY = font("DejaVuSans.ttf", 19)
F_FOOT = font("DejaVuSans.ttf", 18)
F_TOP = font("DejaVuSans-Bold.ttf", 24)


def wrap(text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_tracked(drw, cx, y, text, fnt, fill, tracking=6):
    """Draw centred text with extra letter spacing."""
    widths = [fnt.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        drw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking


# ---------------------------------------------------------------- pictograms
# Each draws a simple white flat pictogram centred on (cx, cy), ~110px wide.

def pic_tanker(drw, cx, cy):
    # hull
    drw.polygon([(cx - 52, cy + 8), (cx + 52, cy + 8), (cx + 40, cy + 36),
                 (cx - 40, cy + 36)], fill=WHITE)
    # containers + funnel
    drw.rectangle([cx - 44, cy - 14, cx - 18, cy + 8], fill=WHITE)
    drw.rectangle([cx - 12, cy - 14, cx + 12, cy + 8], fill=WHITE)
    drw.rectangle([cx + 20, cy - 30, cx + 34, cy + 8], fill=WHITE)
    # waves
    for dy in (48, 58):
        drw.arc([cx - 52, cy + dy - 8, cx - 18, cy + dy + 8], 0, 180, fill=WHITE, width=4)
        drw.arc([cx - 12, cy + dy - 8, cx + 22, cy + dy + 8], 0, 180, fill=WHITE, width=4)
        drw.arc([cx + 28, cy + dy - 8, cx + 56, cy + dy + 8], 0, 180, fill=WHITE, width=4)


def pic_bridge(drw, cx, cy):
    # deck
    drw.rectangle([cx - 56, cy + 18, cx + 56, cy + 26], fill=WHITE)
    # towers
    drw.rectangle([cx - 48, cy - 42, cx - 38, cy + 18], fill=WHITE)
    drw.rectangle([cx + 38, cy - 42, cx + 48, cy + 18], fill=WHITE)
    # main cable
    drw.arc([cx - 48, cy - 66, cx + 48, cy + 18], 0, 180, fill=WHITE, width=4)
    # suspenders
    for sx in (-28, 0, 28):
        drw.line([sx + cx, cy - 18, sx + cx, cy + 18], fill=WHITE, width=3)
    # water
    for dy in (40, 50):
        drw.line([cx - 56, cy + dy, cx + 56, cy + dy], fill=WHITE, width=3)


def pic_flags(drw, cx, cy):
    for i, px in enumerate((cx - 42, cx, cx + 42)):
        drw.line([px, cy - 46, px, cy + 44], fill=WHITE, width=4)
        top = cy - 46 + i * 4
        drw.polygon([(px, top), (px + 34, top + 8), (px, top + 18)], fill=WHITE)


def pic_virus(drw, cx, cy):
    import math
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        x2, y2 = cx + 46 * math.cos(a), cy + 46 * math.sin(a)
        drw.line([x1, y1, x2, y2], fill=WHITE, width=5)
        drw.ellipse([x2 - 7, y2 - 7, x2 + 7, y2 + 7], fill=WHITE)
    drw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=WHITE)


def pic_tent(drw, cx, cy):
    # tent
    drw.polygon([(cx - 52, cy + 36), (cx, cy - 34), (cx + 52, cy + 36)], fill=WHITE)
    # door cut out in the card's accent colour is faked by drawing the
    # tent in two halves around a dark slit
    drw.polygon([(cx - 12, cy + 36), (cx, cy + 2), (cx + 12, cy + 36)],
                fill=(70, 83, 106))
    # snowflake above
    sx, sy = cx + 34, cy - 42
    for dx, dy in ((0, -10), (0, 10), (-9, -5), (9, 5), (-9, 5), (9, -5)):
        drw.line([sx, sy, sx + dx, sy + dy], fill=WHITE, width=3)
    # ground
    drw.line([cx - 56, cy + 44, cx + 56, cy + 44], fill=WHITE, width=4)


def pic_globe(drw, cx, cy):
    # planet: outer ring, latitude chords, one meridian arc
    drw.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], outline=WHITE, width=6)
    drw.line([cx - 44, cy - 16, cx + 44, cy - 16], fill=WHITE, width=4)
    drw.line([cx - 48, cy + 16, cx + 48, cy + 16], fill=WHITE, width=4)
    drw.arc([cx - 22, cy - 48, cx + 22, cy + 48], 270, 90, fill=WHITE, width=4)
    drw.arc([cx - 22, cy - 48, cx + 22, cy + 48], 90, 270, fill=WHITE, width=4)


STORIES = [
    dict(kicker="MIDDLE EAST", accent=(179, 64, 42), pic=pic_tanker,
         head="U.S. sinks five Iranian tankers; Iran hits back",
         body="Tehran hit ships near Hormuz and a U.S. base in Jordan."),
    dict(kicker="UKRAINE", accent=(46, 94, 140), pic=pic_bridge,
         head="Crimea bridge hit for a second night",
         body="Kyiv struck the Kerch bridge again; Russia hit two Ukrainian bridges as talks near."),
    dict(kicker="DIPLOMACY", accent=(31, 110, 107), pic=pic_flags,
         head="Trump heads to China for Xi\u2013Putin summit",
         body="Trilateral meeting in Beijing; China calls the gathering \u201cgroundbreaking\u201d."),
    dict(kicker="HEALTH", accent=(106, 76, 147), pic=pic_virus,
         head="U.S. loses measles-free status",
         body="More than 5,400 cases this year \u2014 the worst outbreak in over three decades."),
    dict(kicker="GAZA", accent=(140, 107, 31), pic=pic_tent,
         head="U.N. warns of cold deaths in Gaza",
         body="1.7 million still displaced as winter sets in; four nations urge Israel to let aid in."),
    dict(kicker="CLIMATE", accent=(46, 125, 50), pic=pic_globe,
         head="COP31 talks enter decisive phase",
         body="Antalya negotiators work through a draft of 144 disputed items; talks end Friday."),
]


def draw_card(drw, x, y, w, h, story):
    drw.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_EDGE, width=2)
    # pictogram band on the left
    band_w = 150
    drw.rectangle([x + 2, y + 2, x + band_w, y + h - 2], fill=story["accent"])
    story["pic"](drw, x + band_w // 2 + 1, y + h // 2)
    # text zone
    tx = x + band_w + 18
    tw = w - band_w - 36
    cy = y + 16
    drw.text((tx, cy), story["kicker"], font=F_KICKER, fill=story["accent"])
    cy += 30
    for line in wrap(story["head"], F_HEAD, tw)[:3]:
        drw.text((tx, cy), line, font=F_HEAD, fill=INK)
        cy += 34
    cy += 4
    for line in wrap(story["body"], F_BODY, tw)[:3]:
        drw.text((tx, cy), line, font=F_BODY, fill=SUMMARY)
        cy += 25


def main():
    img = Image.new("RGB", (W, H), PAPER)
    drw = ImageDraw.Draw(img)

    # ---- masthead ----
    drw.rectangle([0, 0, W, 148], fill=NAVY)
    draw_tracked(drw, W // 2, 22, "THE WORLD IN ONE IMAGE", F_TOP, GOLD, tracking=8)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    # fit the date inside the page: shrink the serif until it fits
    size = 56
    while size > 30:
        fnt = font("DejaVuSerif-Bold.ttf", size)
        if fnt.getlength(date) <= W - 48:
            break
        size -= 2
    dw = fnt.getlength(date)
    drw.text(((W - dw) / 2, 56), date, font=fnt, fill=WHITE)
    drw.rectangle([0, 142, W, 148], fill=RED)

    # ---- story grid: 2 cols x 3 rows ----
    gx, gy = 16, 164
    cw, chh, gap = 488, 252, 16
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        draw_card(drw, gx + col * (cw + gap), gy + row * (chh + gap),
                  cw, chh, story)

    # ---- footer ----
    fy = gy + 3 * chh + 2 * gap  # 952
    drw.line([16, fy + 8, W - 16, fy + 8], fill=CARD_EDGE, width=2)
    foot = "Reported on 18 November 2026  ·  Sources: NDTV · Qatar Tribune · UN News · Dawn · AP / AFP"
    fw = F_FOOT.getlength(foot)
    drw.text(((W - fw) / 2, fy + 22), foot, font=F_FOOT, fill=SUMMARY)

    img.save(OUT, "PNG")
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
