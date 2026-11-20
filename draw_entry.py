#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page, from scratch.

One 1024x1024 PNG, deterministic: same input -> same bytes every run.
No network, no external assets; every glyph and shape is drawn here.
Layout: masthead, one lead story, four cards in two rows, one wide
strip, and a three-item footer. News verified 20 Nov 2026 from
Reuters, CNN, ANI/PTI, IMD and Sensor Tower estimates.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
CARD = (255, 253, 246)
INK = (22, 22, 22)
GREY = (74, 74, 74)
NAVY = (20, 36, 62)
RED = (176, 42, 42)
RULE = (201, 194, 174)
ORANGE = (214, 110, 30)
TEAL = (18, 110, 105)

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF_REG = FONT_DIR + "LiberationSerif-Regular.ttf"
SANS = FONT_DIR + "LiberationSans-Regular.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped text; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def card(draw, box, bar_color):
    """A white story card with a coloured left bar and hairline border."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=RULE, width=1)
    draw.rectangle([x0, y0, x0 + 6, y1], fill=bar_color)


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_B, 16)
    draw.text((x, y), text, font=f, fill=color)
    return y + 22


# ---------------------------------------------------------------- icons
def icon_clock(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY, width=4)
    for ang in (0, 90, 180, 270):
        a = math.radians(ang)
        x1 = cx + int(0.78 * r * math.sin(a))
        y1 = cy - int(0.78 * r * math.cos(a))
        x2 = cx + int(0.92 * r * math.sin(a))
        y2 = cy - int(0.92 * r * math.cos(a))
        draw.line([x1, y1, x2, y2], fill=NAVY, width=3)
    draw.line([cx, cy, cx, cy - int(0.55 * r)], fill=RED, width=4)
    draw.line([cx, cy, cx + int(0.45 * r), cy + int(0.25 * r)], fill=INK, width=4)
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_flame_city(draw, x, y, s):
    # grey skyline
    for i, h in enumerate((34, 52, 28, 44, 38)):
        bx = x + i * (s // 5)
        draw.rectangle([bx, y + s - h, bx + s // 6, y + s], fill=(120, 120, 120))
    # flame
    fx, fy = x + s // 2, y + s // 2
    draw.polygon([(fx - 16, fy + 18), (fx - 20, fy - 6), (fx - 8, fy + 2),
                  (fx, fy - 22), (fx + 10, fy - 2), (fx + 18, fy - 10),
                  (fx + 16, fy + 18)], fill=ORANGE)
    draw.polygon([(fx - 8, fy + 16), (fx - 4, fy - 2), (fx + 2, fy + 6),
                  (fx + 8, fy - 6), (fx + 8, fy + 16)], fill=(232, 178, 40))


def icon_chart(draw, x, y, s):
    # three falling red candles
    tops = (0.15, 0.30, 0.48)
    for i, t in enumerate(tops):
        bx = x + 8 + i * (s // 3)
        top = y + int(s * t)
        bot = y + int(s * (t + 0.30))
        draw.line([bx + 8, y + int(s * (t - 0.06)), bx + 8, bot + 6],
                  fill=RED, width=2)
        draw.rectangle([bx, top, bx + 16, bot], fill=RED)
    draw.line([x + 4, y + 6, x + s - 6, y + s - 8], fill=INK, width=3)
    draw.polygon([(x + s - 6, y + s - 8), (x + s - 20, y + s - 10),
                  (x + s - 8, y + s - 22)], fill=INK)


def icon_sunset_palm(draw, x, y, s):
    draw.ellipse([x + 8, y + 4, x + s - 8, y + s - 8], fill=(232, 120, 40))
    draw.rectangle([x, y + int(s * 0.62), x + s, y + int(s * 0.66)],
                   fill=(232, 120, 40))
    # palm trunk + fronds
    tx = x + int(s * 0.68)
    draw.line([tx, y + s, tx - 6, y + int(s * 0.42)], fill=(60, 48, 30), width=5)
    for dx, dy in ((-26, -14), (-14, -22), (0, -24), (14, -20), (24, -10)):
        draw.line([tx - 6, y + int(s * 0.42), tx - 6 + dx, y + int(s * 0.42) + dy],
                  fill=(46, 110, 52), width=4)


def icon_cyclone(draw, x, y, s):
    cx, cy = x + s // 2, y + int(s * 0.42)
    for r, start, end in ((34, 20, 300), (24, 120, 40), (14, 220, 140)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, end,
                 fill=TEAL, width=5)
    for dx in (-18, 0, 18):
        draw.ellipse([cx + dx - 3, y + s - 16, cx + dx + 3, y + s - 6],
                     fill=(70, 130, 180))


def icon_tanker(draw, x, y, s):
    # sea
    draw.line([x, y + int(s * 0.78), x + s, y + int(s * 0.78)],
              fill=(70, 130, 180), width=3)
    draw.line([x + 6, y + int(s * 0.88), x + s - 6, y + int(s * 0.88)],
              fill=(70, 130, 180), width=2)
    # hull + deck
    draw.polygon([(x + 4, y + int(s * 0.55)), (x + s - 4, y + int(s * 0.55)),
                  (x + s - 14, y + int(s * 0.78)), (x + 14, y + int(s * 0.78))],
                 fill=(52, 52, 52))
    draw.rectangle([x + int(s * 0.55), y + int(s * 0.34), x + int(s * 0.72),
                    y + int(s * 0.55)], fill=(90, 90, 90))
    # flame on deck
    fx = x + int(s * 0.28)
    draw.polygon([(fx - 10, y + int(s * 0.55)), (fx - 12, y + int(s * 0.30)),
                  (fx - 3, y + int(s * 0.42)), (fx + 2, y + int(s * 0.22)),
                  (fx + 8, y + int(s * 0.40)), (fx + 12, y + int(s * 0.30)),
                  (fx + 10, y + int(s * 0.55))], fill=ORANGE)


# ---------------------------------------------------------------- page
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # masthead
    d.rectangle([14, 14, W - 15, 106], fill=NAVY)
    d.text((30, 26), "THE DAILY GLOBE", font=font(SERIF, 52), fill=(248, 244, 232))
    d.text((W - 30, 34), "FRIDAY", font=font(SANS_B, 26),
           fill=(232, 178, 40), anchor="ra")
    d.text((W - 30, 66), "20 NOVEMBER 2026", font=font(SANS_B, 26),
           fill=(248, 244, 232), anchor="ra")
    d.line([14, 112, W - 15, 112], fill=RED, width=4)

    # ---- lead: Trump / Iran
    card(d, (14, 122, W - 15, 300), RED)
    y = kicker(d, 34, 136, "DIPLOMACY  ·  WASHINGTON")
    d.text((34, y), "TRUMP: NO RUSH ON IRAN", font=font(SERIF, 46), fill=INK)
    y += 56
    text_block(d, 34, y,
               "The president says he is in no rush to decide on Iran — any new "
               "strikes wait until 2027. “We’ve got time,” he says, as Israel "
               "warns it may act alone.",
               font(SANS, 19), GREY, 640, 25)
    icon_clock(d, 900, 212, 52)

    # ---- row 2: Kyiv | Markets
    card(d, (14, 312, 502, 516), NAVY)
    y = kicker(d, 34, 326, "WAR  ·  KYIV")
    d.text((34, y), "MISSILES RAIN\nON KYIV", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 34, y,
               "Russia launches a mass missile attack overnight. Fires burn "
               "in several districts; debris hits a home in Obolonskyi.",
               font(SANS, 17), GREY, 330, 23)
    icon_flame_city(d, 400, 420, 84)

    card(d, (522, 312, W - 15, 516), TEAL)
    y = kicker(d, 542, 326, "MARKETS  ·  NEW YORK")
    d.text((542, y), "DOW SINKS 1,101", font=font(SERIF, 33), fill=INK)
    y += 46
    text_block(d, 542, y,
               "Wall Street’s worst day in months: Dow −2.2%, below 50,000; "
               "S&P −2.0%; Nasdaq −2.3%. Anthropic’s record $81.3bn IPO "
               "debuts — shares +17%.",
               font(SANS, 17), GREY, 330, 23)
    icon_chart(d, 908, 420, 84)

    # ---- row 3: GTA VI | Cyclone Akvan
    card(d, (14, 528, 502, 732), ORANGE)
    y = kicker(d, 34, 542, "CULTURE  ·  GAMES")
    d.text((34, y), "GTA VI: $2.36\nBILLION", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 34, y,
               "First-day sales estimated at 24.6m copies — the biggest "
               "entertainment launch ever. Critics give it 99 on Metacritic.",
               font(SANS, 17), GREY, 330, 23)
    icon_sunset_palm(d, 400, 636, 84)

    card(d, (522, 528, W - 15, 732), TEAL)
    y = kicker(d, 542, 542, "WEATHER  ·  INDIA")
    d.text((542, y), "CYCLONE AKVAN\nNEARS INDIA", font=font(SERIF, 33), fill=INK)
    y += 82
    text_block(d, 542, y,
               "About 300,000 people evacuated in Odisha. Landfall near "
               "Gopalpur today, winds up to 100 km/h; 423 rescue teams out.",
               font(SANS, 17), GREY, 330, 23)
    icon_cyclone(d, 908, 636, 84)

    # ---- strip: Hormuz tanker
    card(d, (14, 744, W - 15, 866), NAVY)
    y = kicker(d, 34, 758, "ENERGY  ·  THE GULF")
    d.text((34, y), "TANKER BURNS NEAR HORMUZ", font=font(SERIF, 32), fill=INK)
    y += 44
    text_block(d, 34, y,
               "A tanker catches fire after hitting a mine east of the Strait of "
               "Hormuz. Houthi rebels claim strikes on four targets in Saudi Arabia.",
               font(SANS, 18), GREY, 700, 24)
    icon_tanker(d, 900, 772, 80)

    # ---- footer: three short items
    d.line([14, 884, W - 15, 884], fill=RULE, width=2)
    foot = [
        ("SPACE", "Voyager 1 reaches one light-day from Earth, NASA confirms."),
        ("TRADE", "South Korea’s exports top $1 trillion for the first time."),
        ("EUROPE", "Genoa airport halts flights for four hours after drones are seen."),
    ]
    fx = 30
    for tag, txt in foot:
        d.text((fx, 898), tag, font=font(SANS_B, 15), fill=RED)
        text_block(d, fx, 920, txt, font(SANS, 15), GREY, 300, 20)
        fx += 332
    d.line([14, 982, W - 15, 982], fill=RULE, width=1)
    d.text((W // 2, 990), "THE DAILY GLOBE  ·  FRIDAY 20 NOVEMBER 2026  ·  "
           "Sources: Reuters, CNN, ANI / PTI, IMD, Sensor Tower estimates",
           font=font(SANS, 13), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    build().save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")
