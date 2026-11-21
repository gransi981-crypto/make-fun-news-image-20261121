#!/usr/bin/env python3
"""Draw the front page for Saturday 21 November 2026.

One-page newspaper, 1024x1024 PNG. Deterministic: fixed layout, fixed
text, no randomness, no timestamps. Run: python3 render.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (163, 29, 29)
NAVY = (20, 38, 77)
GREY = (110, 105, 95)
GOLD = (176, 132, 40)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    """Greedy word wrap by measured width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, max_w, leading, color=INK):
    """Draw wrapped paragraph; returns y just below the last line."""
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def rule(d, x, y, w, color=INK, width=2):
    d.line([(x, y), (x + w, y)], fill=color, width=width)


def draw_scene(d, x, y, w, h):
    """Stylised night skyline under a barrage: dark sky, searchlights,
    falling missile trails, city blocks. Pure vector shapes."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(0.06, 0.12), (0.22, 0.06), (0.38, 0.16), (0.55, 0.08),
                   (0.71, 0.14), (0.86, 0.07), (0.94, 0.2), (0.31, 0.22),
                   (0.63, 0.24), (0.12, 0.28)]:
        d.ellipse([x + w * sx - 2, y + h * sy - 2, x + w * sx + 2, y + h * sy + 2],
                  fill=(240, 235, 220))
    for bx, tx in [(0.18, 0.42), (0.62, 0.38), (0.84, 0.60)]:
        d.polygon([(x + w * bx, y + h), (x + w * tx, y + 8),
                   (x + w * tx + 26, y + 8)], fill=(70, 95, 140))
    for mx, my, mdx in [(0.30, 0.30, 0.10), (0.55, 0.18, -0.08), (0.78, 0.34, 0.12)]:
        hx, hy = x + w * mx, y + h * my
        d.line([(hx - w * mdx, hy - 34), (hx, hy)], fill=(255, 190, 90), width=3)
        d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=(255, 220, 130))
    base = y + h
    blocks = [(0.00, 0.62), (0.14, 0.48), (0.28, 0.70), (0.44, 0.55),
              (0.58, 0.74), (0.72, 0.50), (0.86, 0.66)]
    for bx, bh in blocks:
        bw = w * 0.14
        d.rectangle([x + w * bx, base - h * bh, x + w * bx + bw, base],
                    fill=(10, 18, 38))
        for wy in range(3):
            for wx in range(2):
                wxp = x + w * bx + 8 + wx * 22
                wyp = base - h * bh + 10 + wy * 18
                if (wx + wy) % 2 == 0:
                    d.rectangle([wxp, wyp, wxp + 8, wyp + 10], fill=(255, 205, 110))


def draw_chart(d, x, y, w, h):
    """Falling market line on a light panel."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=GREY, width=1)
    pts = [(0.05, 0.22), (0.18, 0.30), (0.30, 0.26), (0.44, 0.48),
           (0.58, 0.44), (0.72, 0.66), (0.86, 0.62), (0.97, 0.82)]
    xy = [(x + w * px, y + h * py) for px, py in pts]
    d.line(xy, fill=RED, width=3)
    for px, py in xy:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.text((x + 8, y + 6), "S&P 500", font=font(SANS_B, 15), fill=GREY)
    d.text((x + w - 58, y + 6), "-3.7%", font=font(SANS_B, 17), fill=RED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    CW = W - 2 * M

    # ---- Masthead ----
    d.rectangle([0, 0, W, 104], fill=NAVY)
    f_mast = font(SERIF_B, 78)
    t = "THE WORLD"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 8), t, font=f_mast,
           fill=(247, 243, 234))
    f_date = font(SANS_B, 24)
    d.text((M, 118), "SATURDAY 21 NOVEMBER 2026", font=f_date, fill=INK)
    tag = "ONE DAY · ONE PAGE"
    d.text((W - M - d.textlength(tag, font=f_date), 118), tag, font=f_date,
           fill=RED)
    rule(d, M, 150, CW, INK, 3)

    # ---- Lead story (left, x36-632) ----
    lx, ly, lw = M, 166, 596
    f_kick = font(SANS_B, 19)
    d.text((lx, ly), "WAR IN EUROPE", font=f_kick, fill=RED)
    y = ly + 28
    y = para(d, lx, y, "Russia's biggest barrage hits Kyiv — and Poland",
             font(SERIF_B, 43), lw, 50)
    y += 6
    draw_scene(d, lx, y, lw, 148)
    y += 148 + 10
    y = para(d, lx, y,
             "More than 400 drones and 110 missiles struck Ukraine overnight — "
             "the biggest attack of the year. Eight were killed in Kyiv. Russian "
             "missiles also came down in Poland, and Warsaw called it a deliberate "
             "provocation.",
             font(SERIF, 20), lw, 27)
    y += 4
    y = para(d, lx, y,
             "Zelensky called Putin a “killer” after Trump called him “my friend”.",
             font(SERIF_B, 20), lw, 27)
    assert y <= 630, f"lead overflow: {y}"

    # ---- Right column (x668-988) ----
    rx, rw = 668, W - M - 668
    d.text((rx, ly), "MARKETS", font=f_kick, fill=RED)
    y2 = ly + 28
    y2 = para(d, rx, y2, "S&P 500 falls into correction",
              font(SERIF_B, 30), rw, 36)
    y2 += 4
    draw_chart(d, rx, y2, rw, 96)
    y2 += 96 + 10
    y2 = para(d, rx, y2,
              "The Nasdaq erases all of its 2026 gains. Anthropic slides again; "
              "Nvidia faces an SEC probe.",
              font(SERIF, 19), rw, 26)
    y2 += 14
    rule(d, rx, y2, rw, GREY, 1)
    y2 += 12
    d.text((rx, y2), "BY THE NUMBERS", font=f_kick, fill=RED)
    y2 += 28
    for big, small in [("-3.7%", "S&P 500 in one day"),
                       ("400+", "drones fired at Ukraine"),
                       ("100,000", "youth mobility places")]:
        d.text((rx, y2), big, font=font(SERIF_B, 24), fill=RED)
        d.text((rx + 118, y2 + 4), small, font=font(SERIF, 17), fill=INK)
        y2 += 30
    assert y2 <= 630, f"right column overflow: {y2}"

    # ---- Second row: three stories ----
    y3 = 636
    rule(d, M, y3, CW, INK, 2)
    y3 += 12
    col_w = (CW - 2 * 20) // 3
    stories = [
        ("DIPLOMACY", "UK and EU sign post-Brexit deals",
         "Three deals on food, carbon and youth mobility."),
        ("DISASTER", "Peru shaken by 6.8 quake",
         "A 6.8 quake strikes Junín; tremors felt in Lima, 320 km away."),
        ("JUSTICE", "Court: Myanmar guilty of genocide",
         "Guilty of genocide against the Rohingya, the court rules."),
    ]
    for i, (kick, head, body) in enumerate(stories):
        sx = M + i * (col_w + 20)
        d.text((sx, y3), kick, font=f_kick, fill=RED)
        yy = para(d, sx, y3 + 28, head, font(SERIF_B, 23), col_w, 28)
        yy += 4
        yy = para(d, sx, yy, body, font(SERIF, 17), col_w, 22)
        assert yy <= 790, f"story {i} overflow: {yy}"

    # ---- Briefs grid ----
    y6 = 792
    rule(d, M, y6, CW, INK, 2)
    y6 += 10
    d.text((M, y6), "THE DAY IN BRIEF", font=f_kick, fill=RED)
    y6 += 30
    briefs = [
        ("CLIMATE", "COP31 talks in Antalya run past their deadline over fossil fuels."),
        ("CYBER", "FBI crime database hacked as US outages continue."),
        ("GAMES", "GTA VI sets a $3.8bn first-day sales record."),
        ("HEALTH", "Cancer pill makes tumours undetectable in 1 in 12 patients."),
        ("GULF", "Houthi missiles at Riyadh intercepted for a third night."),
        ("BRAZIL", "Bolsonaro hospitalised with an intestinal obstruction."),
    ]
    bw = (CW - 2 * 20) // 3
    for i, (k, txt) in enumerate(briefs):
        col, row = i % 3, i // 3
        bx = M + col * (bw + 20)
        by = y6 + row * 56
        d.text((bx, by), k, font=font(SANS_B, 16), fill=RED)
        end = para(d, bx, by + 20, txt, font(SERIF, 16), bw, 20)
        assert end <= 948, f"brief {i} overflow: {end}"

    # ---- Ticker ----
    ty = 950
    d.rectangle([0, ty, W, ty + 40], fill=NAVY)
    tick = ("GEN Z PROTESTS IN 25 COUNTRIES   ·   BITCOIN TOWARD $62,000   ·   "
            "INDIA LOGS RECORD FOREIGN INFLOWS")
    size = 19
    while size > 10:
        f_tick = font(SANS_B, size)
        if d.textlength(tick, font=f_tick) <= 960:
            break
        size -= 1
    tw = d.textlength(tick, font=f_tick)
    d.text(((W - tw) / 2, ty + (40 - size) / 2 - 2), tick, font=f_tick,
           fill=(247, 243, 234))

    # ---- Footer ----
    f_foot = font(SANS, 14)
    foot = "THE WORLD — a one-page summary of Saturday 21 November 2026 · Sources: BBC, FT, Guardian, Al Jazeera, Reuters"
    d.text((M, 998), foot, font=f_foot, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
