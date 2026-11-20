"""Draw the one-page front page for Friday 20 November 2026.

Every pixel is painted with Pillow primitives from the facts listed in
STORIES below. No photos, no downloads, no network, no clock reads, so
running this script twice yields the same PNG byte for byte.

Layout (1024 x 1024): masthead, red standfirst, statistics strip, three
hero cards, four smaller cards, a "Friday by the hours" timeline, a
numbered world map with the day's briefs, a date-check box and a footer.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # outer margin
CW = W - 2 * M              # content width

PAPER = (247, 241, 228)
INK = (28, 28, 30)
FAINT = (96, 96, 92)
BRICK = (158, 48, 38)
BRICK_SOFT = (226, 196, 188)
NAVY = (18, 42, 74)
NAVY_SOFT = (36, 68, 108)
TEAL = (24, 104, 96)
GOLD = (176, 128, 32)
GOLD_SOFT = (238, 214, 150)
SKY = (148, 184, 208)
SKY_SOFT = (214, 230, 238)
LAND = (216, 202, 158)
LAND_LINE = (150, 132, 88)
SEA = (222, 232, 236)
CARD = (255, 253, 247)
RULE = (120, 110, 96)

DJV = "/usr/share/fonts/truetype/dejavu/"
NOTO = "/usr/share/fonts/truetype/noto/"


def face(path, size):
    """Load a face; fall back to Pillow's built-in bitmap face."""
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def serif_b(size):
    return face(DJV + "DejaVuSerif-Bold.ttf", size)


def serif(size):
    return face(NOTO + "NotoSerif-Regular.ttf", size)


def serif_i(size):
    return face(NOTO + "NotoSerif-Italic.ttf", size)


def sans(size):
    return face(DJV + "DejaVuSans.ttf", size)


def sans_b(size):
    return face(DJV + "DejaVuSans-Bold.ttf", size)


def wrap(d, text, font, width):
    """Greedy word wrap using the font's real metrics."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, fill=INK, leading=None, max_lines=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = font.size + 4
    lines = wrap(d, text, font, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, fill=RULE, width=1):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def kicker(d, x, y, num, place, topic, color=BRICK):
    """Numbered kicker line, e.g. '1 · ODISHA · STORM'."""
    f = sans_b(11)
    d.text((x, y), "%d · %s · %s" % (num, place, topic), font=f, fill=color)
    return y + 15


def headline(d, x, y, text, font, width, fill=INK, max_lines=3):
    lines = wrap(d, text, font, width)[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += font.size + 3
    return y


def card_frame(d, x, y, w, h, fill=CARD):
    d.rounded_rectangle([x, y, x + w, y + h], radius=4,
                        fill=fill, outline=RULE, width=1)


# ---------------------------------------------------------------- pictures

def pic_cyclone(d, x, y, w, h):
    """Spiral storm over a coastline."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_SOFT)
    # sea bands
    for i in range(4):
        yy = y + h - 14 - i * 9
        d.line([(x + 6, yy), (x + w - 6, yy)], fill=SKY, width=3)
    # land strip on the right
    d.polygon([(x + w - 52, y + h), (x + w - 30, y + 18),
               (x + w - 12, y + 44), (x + w, y + 30),
               (x + w, y + h)], fill=(196, 178, 128))
    # spiral: shrinking arcs around the eye
    cx, cy = x + w // 2 - 18, y + h // 2 - 8
    for r in range(52, 8, -9):
        a0 = (52 - r) * 7
        d.arc([cx - r, cy - r, cx + r, cy + r],
              start=a0, end=a0 + 250, fill=NAVY, width=5)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=PAPER,
              outline=NAVY, width=2)
    d.text((x + 8, y + 6), "90-100 km/h", font=sans_b(11), fill=NAVY)
    d.text((x + 8, y + 22), "gusts 110", font=sans(10), fill=NAVY)


def pic_globe(d, x, y, w, h):
    """Globe with a thermometer beside it."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 222))
    cx, cy, r = x + w // 2 - 26, y + h // 2 + 4, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(88, 158, 120),
              outline=NAVY, width=2)
    # rough continents
    d.ellipse([cx - 30, cy - 26, cx - 2, cy + 2], fill=(222, 196, 110))
    d.ellipse([cx + 2, cy - 12, cx + 30, cy + 26], fill=(222, 196, 110))
    d.ellipse([cx - 12, cy + 14, cx + 12, cy + 34], fill=(222, 196, 110))
    # thermometer
    tx = x + w - 46
    d.rounded_rectangle([tx, y + 12, tx + 12, y + h - 26], radius=6,
                        fill=(255, 255, 255), outline=BRICK, width=2)
    d.rectangle([tx + 3, y + h - 52, tx + 9, y + h - 30], fill=BRICK)
    d.ellipse([tx - 5, y + h - 34, tx + 17, y + h - 12], fill=BRICK)
    d.text((x + 8, y + 6), "FINAL DAY", font=sans_b(11), fill=NAVY)


def pic_cricket(d, x, y, w, h):
    """Bat, ball and stumps on a green strip."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 178))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 158, 84))
    # stumps
    sx = x + w - 58
    for i in range(3):
        d.rectangle([sx + i * 10, y + h - 62, sx + i * 10 + 6, y + h - 26],
                    fill=(232, 196, 110), outline=(120, 84, 32))
    d.rectangle([sx - 2, y + h - 66, sx + 28, y + h - 62],
                fill=(232, 196, 110))
    # bat, leaning
    d.polygon([(x + 34, y + h - 26), (x + 52, y + h - 26),
               (x + 78, y + 34), (x + 62, y + 26)], fill=(222, 188, 110),
              outline=(120, 84, 32))
    d.rectangle([x + 66, y + 12, x + 76, y + 34], fill=(120, 84, 32))
    # red ball
    d.ellipse([x + w - 108, y + 26, x + w - 88, y + 46], fill=BRICK)
    d.text((x + 8, y + 6), "NZ 315/6", font=sans_b(11), fill=NAVY)
    d.text((x + 8, y + 22), "Phillips 118", font=sans(10), fill=NAVY)


def pic_fort(d, x, y, w, h):
    """Arched gateway of an old fort (Purana Quila)."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 220, 180))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(176, 148, 100))
    # wall with battlements
    d.rectangle([x + 12, y + 20, x + w - 12, y + h - 10],
                fill=(196, 120, 72))
    for bx in range(x + 12, x + w - 12, 18):
        d.rectangle([bx, y + 14, bx + 12, y + 20], fill=(196, 120, 72))
    # arched gate
    gx, gw = x + w // 2 - 24, 48
    d.pieslice([gx, y + h - 36, gx + gw, y + h - 8], 180, 360,
               fill=(70, 42, 28))
    d.rectangle([gx, y + h - 22, gx + gw, y + h - 10], fill=(70, 42, 28))
    # flag on the left tower, date top right
    d.line([(x + 18, y + 2), (x + 18, y + 14)], fill=INK, width=2)
    d.polygon([(x + 18, y + 2), (x + 32, y + 6), (x + 18, y + 10)],
              fill=(214, 120, 40))
    d.text((x + w - 56, y + 3), "20-22 NOV", font=sans_b(9),
           fill=(90, 60, 30))


def pic_flood(d, x, y, w, h):
    """Flooded street: house, water, rain."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 206, 214))
    # rain, left half only so the label stays clear
    for i in range(5):
        rx = x + 8 + i * 18
        d.line([(rx, y + 4), (rx - 4, y + 16)], fill=(110, 130, 150),
               width=2)
    # house
    hx = x + w // 2 - 36
    d.polygon([(hx - 5, y + 21), (hx + 36, y + 6), (hx + 77, y + 21)],
              fill=BRICK)
    d.rectangle([hx, y + 20, hx + 72, y + 40], fill=(222, 196, 150),
                outline=INK, width=1)
    d.rectangle([hx + 30, y + 28, hx + 42, y + 40], fill=(90, 60, 40))
    # water
    for yy in (y + h - 12, y + h - 5):
        d.arc([x + 8, yy - 6, x + w - 8, yy + 6], 0, 180,
              fill=NAVY, width=3)
    d.text((x + w - 52, y + 3), "18.3 FT", font=sans_b(10), fill=NAVY)


def pic_game(d, x, y, w, h):
    """Game controller with a big VI."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 32, 64))
    d.text((x + 8, y + 12), "VI", font=serif_b(26),
           fill=(255, 255, 255))
    # controller body on the right
    d.rounded_rectangle([x + 64, y + 10, x + w - 8, y + h - 8],
                        radius=14, fill=(88, 72, 140))
    d.ellipse([x + 74, y + 18, x + 92, y + 36], fill=(30, 24, 52))
    d.ellipse([x + w - 40, y + 18, x + w - 22, y + 36], fill=(30, 24, 52))
    for bx, by, col in ((x + w - 62, y + 22, GOLD),
                        (x + w - 48, y + 34, (120, 200, 120)),
                        (x + w - 76, y + 34, (120, 170, 220))):
        d.ellipse([bx, by, bx + 9, by + 9], fill=col)


def pic_bars(d, x, y, w, h):
    """Two bars: the draft cut from 144 paragraphs to 80."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.text((x + 8, y + 2), "144 -> 80", font=sans_b(11), fill=NAVY)
    bx = x + 14
    d.text((bx, y + 14), "first draft", font=sans(9), fill=FAINT)
    d.rectangle([bx, y + 25, bx + w - 28, y + 33], fill=NAVY)
    d.text((bx, y + 35), "slimmed draft", font=sans(9), fill=FAINT)
    d.rectangle([bx, y + 46, bx + int((w - 28) * 80 / 144), y + 52],
                fill=BRICK)


# ------------------------------------------------------------------- map

CONTINENTS = {
    "n_america": [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80),
                  (-85, 80), (-75, 73), (-65, 60), (-55, 52), (-60, 45),
                  (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 29),
                  (-97, 26), (-105, 22), (-110, 24), (-117, 33), (-125, 40),
                  (-125, 49), (-135, 58), (-155, 60), (-165, 60)],
    "s_america": [(-80, 10), (-75, 12), (-70, 12), (-62, 10), (-55, 6),
                  (-50, 0), (-45, -5), (-40, -10), (-38, -15), (-40, -22),
                  (-48, -28), (-55, -35), (-65, -40), (-70, -50),
                  (-73, -53), (-70, -45), (-72, -35), (-72, -25),
                  (-78, -15), (-80, -5)],
    "europe": [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (3, 53),
               (8, 57), (10, 59), (18, 56), (21, 55), (24, 59), (28, 60),
               (30, 62), (32, 70), (40, 68), (45, 68), (40, 60), (35, 55),
               (30, 50), (28, 45), (23, 40), (20, 40), (15, 38), (10, 38),
               (3, 42), (-2, 37)],
    "africa": [(-17, 15), (-15, 25), (-10, 30), (-5, 35), (10, 37),
               (20, 32), (30, 31), (35, 28), (38, 22), (42, 15), (48, 11),
               (51, 10), (45, 0), (40, -10), (35, -20), (32, -28),
               (25, -34), (18, -35), (15, -27), (12, -18), (12, -8),
               (8, 4), (-8, 5), (-13, 8), (-17, 12)],
    "asia": [(30, 70), (40, 68), (50, 70), (60, 70), (70, 73), (80, 73),
             (90, 75), (100, 77), (110, 76), (120, 73), (130, 72),
             (140, 72), (150, 70), (160, 69), (170, 66), (178, 65),
             (170, 60), (162, 56), (158, 52), (150, 50), (142, 45),
             (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
             (120, 32), (115, 25), (110, 20), (108, 12), (105, 8),
             (100, 7), (97, 10), (92, 16), (88, 22), (85, 20), (80, 15),
             (77, 8), (75, 12), (72, 20), (66, 25), (60, 25), (57, 27),
             (52, 28), (48, 30), (44, 29), (40, 32), (36, 36), (32, 36),
             (30, 40), (28, 45), (30, 50), (35, 55), (40, 60), (35, 65)],
    "oceania": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -33),
                (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
                (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
                (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
                (126, -14), (122, -17), (118, -20)],
}

# (story number, lon, lat, label, dx, dy) — dx/dy shift the numbered
# circle away from the true spot when two stories sit close together.
MAP_DOTS = [
    (1, 85.5, 20.0, "Odisha", 12, 10),
    (2, 30.7, 36.9, "Antalya", 0, 0),
    (3, 174.8, -41.3, "Wellington", 0, 0),
    (4, 77.2, 28.6, "New Delhi", -12, -10),
    (5, -81.7, 28.5, "Florida", 0, 0),
]


def draw_map(d, x, y, w, h):
    """Simplified world map with numbered story dots."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    for poly in CONTINENTS.values():
        pts = [(x + (lon + 180) / 360 * w,
                y + (90 - lat) / 180 * h) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)
    for num, lon, lat, _label, dx, dy in MAP_DOTS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (cx, cy)], fill=BRICK, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=BRICK)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=BRICK,
                  outline=(255, 255, 255), width=2)
        d.text((cx - 3, cy - 7), str(num), font=sans_b(10),
               fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "Red numbers mark the places in stories 1-5.",
           font=sans(9), fill=FAINT)


# ------------------------------------------------------------------ page

STATS = [
    ("300,000", "people evacuated\nin Odisha"),
    ("423", "rescue teams\ndeployed"),
    ("194", "delegations\nat COP31"),
    ("118", "Phillips' runs\non day two"),
    ("18.3 ft", "St. Johns River\nrecord level"),
    ("80", "paragraphs left\nin COP31 draft"),
]

HEROES = [
    dict(num=1, place="ODISHA", topic="STORM", pic=pic_cyclone,
         head="Akvan comes ashore as 300,000 flee the coast",
         body=("Severe Cyclone Akvan is due ashore near Gopalpur around "
               "noon, winds 90-100 km/h gusting to 110. Odisha has moved "
               "300,000 people to safety and sent out 423 rescue teams."),
         src="The Hindu · IMD"),
    dict(num=2, place="ANTALYA", topic="CLIMATE", pic=pic_globe,
         head="COP31 enters its last day with no deal in sight",
         body=("Negotiators enter the closing day hunting for a final "
               "text, due by midnight. A slimmed draft, cut from 144 "
               "paragraphs to 80, drops fossil fuels and the $120bn "
               "adaptation figure."),
         src="Asia Today · AFP"),
    dict(num=3, place="WELLINGTON", topic="SPORT", pic=pic_cricket,
         head="Phillips' hundred rescues New Zealand - again",
         body=("Glenn Phillips made 118 and Henry Nicholls is 128 not "
               "out as New Zealand passed 300 on day two against India, "
               "after a 216-run stand from 70 for 5."),
         src="NDTV · Times Now"),
]

GRID = [
    dict(num=4, place="NEW DELHI", topic="DIPLOMACY", pic=pic_fort,
         head="Modi opens SCO civilisations forum",
         body=("The prime minister inaugurates the first SCO "
               "Civilisational Dialogue Forum at Purana Quila; "
               "it runs until Sunday."),
         src="Mathrubhumi"),
    dict(num=5, place="FLORIDA", topic="WEATHER", pic=pic_flood,
         head="Florida's floods roll into Friday",
         body=("The St. Johns River holds at a record 18.3 ft near "
               "Cocoa; a high flood risk runs through Friday and "
               "schools stay shut."),
         src="AP · Florida Today"),
    dict(num=6, place="WORLDWIDE", topic="GAMES", pic=pic_game,
         head="GTA VI user scores open at noon",
         body=("A day after launch, Metacritic opens user reviews at "
               "noon Pacific; official sales figures are expected "
               "as early as today."),
         src="Men's Journal"),
    dict(num=7, place="ANTALYA", topic="CLIMATE", pic=pic_bars,
         head="The draft, in numbers",
         body=("144 paragraphs cut to 80. The $120bn adaptation goal "
               "is gone. Electricity to 35% of energy use by 2035 "
               "stays in."),
         src="AFP"),
]

BRIEFS = [
    (8, "ANTALYA", "Australia's Chris Bowen consults delegations "
     "through the night, hunting for consensus. — Asia Today"),
    (9, "ANTALYA", "Closing plenaries began Thursday; finance, "
     "adaptation and a just transition are still unresolved. — Asia Today"),
    (10, "WELLINGTON", "Nicholls unbeaten on 128 at 286 for 6; New "
     "Zealand pass 300 before lunch. — Times Now · NDTV"),
    (11, "NEW DELHI", "The SCO forum runs 20-22 November at Purana "
     "Quila. — Mathrubhumi"),
    (12, "FLORIDA", "Flood watch holds through Saturday evening; more "
     "rain is due overnight into Friday. — Florida Today"),
    (13, "FLORIDA", "Brevard schools stay shut Friday; pupils return "
     "after Thanksgiving. — Florida Today"),
    (14, "WORLDWIDE", "Take-Two has still published no official GTA VI "
     "sales number. — Fox 5"),
    (15, "ODISHA", "Landfall is now expected just east of Gopalpur, "
     "after the forecast shifted north. — The Hindu · IMD"),
    (16, "ANTALYA", "Any final text needs consensus of nearly 200 "
     "countries; recent summits ran a day past deadline. — AFP"),
]

DATE_CHECK = (
    "DATE CHECK \u2713  Not Friday's news, so not on this page: the Shenzhen "
    "summit and its Declaration Towards Peace \u00b7 the ICJ's Myanmar "
    "ruling \u00b7 GTA VI's launch and the $1.84bn estimate \u00b7 "
    "Anthropic's first day of trading \u00b7 Jeffries' nomination \u00b7 "
    "the EU's \u20ac45bn Ukraine loan \u00b7 Florida's record 20th "
    "execution \u00b7 Voyager 1's light-day milestone \u00b7 Kushner's "
    "Berlin remarks \u00b7 Meta's net-zero review \u00b7 Fiona's death "
    "\u2014 all 19 November; Fiji's disaster declaration \u2014 18 November."
)

FOOTER = (
    "Every story on this page happened, or was first reported, on Friday "
    "20 November 2026. Disputed claims are attributed, not stated as fact. "
    "Sources: The Hindu, IMD, Asia Today, AFP, NDTV, Times Now, "
    "Mathrubhumi, AP, Florida Today, Men's Journal, Fox 5."
)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = M, M + CW

    # top bar
    d.text((x0, 12), "THE WORLD IN ONE DAY", font=sans_b(11), fill=BRICK)
    right = "16 STORIES \u00b7 FIVE REGIONS \u00b7 ALL FROM THIS ONE DAY"
    d.text((x1 - d.textlength(right, font=sans_b(11)), 12), right,
           font=sans_b(11), fill=FAINT)
    rule(d, x0, x1, 32, width=2)

    # masthead
    title = "Friday 20 November 2026"
    tf = serif_b(56)
    d.text((x0, 38), title, font=tf, fill=INK)
    stand = ("Akvan hits Odisha \u00b7 COP31's last day in Antalya \u00b7 "
             "Phillips' hundred lifts New Zealand")
    d.text((x0, 102), stand, font=serif_i(19), fill=BRICK)
    rule(d, x0, x1, 128, width=2)

    # statistics strip
    col_w = CW // 6
    y = 136
    for i, (num, label) in enumerate(STATS):
        cx = x0 + i * col_w
        if i:
            d.line([(cx - 6, y), (cx - 6, y + 44)], fill=RULE, width=1)
        d.text((cx, y), num, font=serif_b(27), fill=NAVY)
        for j, ln in enumerate(label.split("\n")):
            d.text((cx, y + 30 + j * 12), ln, font=sans(10), fill=FAINT)
    rule(d, x0, x1, 190, width=2)

    # hero row
    hy, hh = 196, 268
    hw = (CW - 2 * 12) // 3
    for i, s in enumerate(HEROES):
        hx = x0 + i * (hw + 12)
        card_frame(d, hx, hy, hw, hh)
        s["pic"](d, hx + 8, hy + 8, hw - 16, 104)
        yy = kicker(d, hx + 10, hy + 120, s["num"], s["place"], s["topic"])
        yy = headline(d, hx + 10, yy, s["head"], serif_b(20), hw - 20,
                      max_lines=2)
        yy = para(d, hx + 10, yy + 2, s["body"], serif(13), hw - 20,
                  leading=16, max_lines=4)
        d.text((hx + 10, hy + hh - 18), "\u2014 " + s["src"],
               font=sans(10), fill=FAINT)

    # grid row
    gy, gh = 472, 176
    gw = (CW - 3 * 10) // 4
    for i, s in enumerate(GRID):
        gx = x0 + i * (gw + 10)
        card_frame(d, gx, gy, gw, gh)
        s["pic"](d, gx + 7, gy + 7, gw - 14, 54)
        yy = kicker(d, gx + 8, gy + 68, s["num"], s["place"], s["topic"])
        yy = headline(d, gx + 8, yy, s["head"], serif_b(14), gw - 16,
                      max_lines=2)
        yy = para(d, gx + 8, yy + 1, s["body"], serif(11), gw - 16,
                  leading=14, max_lines=3)
        d.text((gx + 8, gy + gh - 16), "\u2014 " + s["src"],
               font=sans(9), fill=FAINT)

    # friday by the hours: one compact strip
    ty = 656
    hours_line = ("FRIDAY BY THE HOURS  \u00b7  03:07 IST  Day two begins "
                  "in Wellington  \u00b7  04:29 IST  Phillips out for 118  "
                  "\u00b7  06:30 GMT  Akvan due ashore near Gopalpur  "
                  "\u00b7  12:00 PT  GTA VI user reviews open  \u00b7  "
                  "MIDNIGHT  COP31 final text due in Antalya")
    para(d, x0, ty, hours_line, sans(11), CW, leading=15, max_lines=2)
    rule(d, x0, x1, 690, width=1)

    # map + briefs
    my = 698
    d.text((x0, my), "WHERE IT HAPPENED", font=sans_b(12), fill=BRICK)
    d.text((x0 + 400, my), "ALSO ON FRIDAY 20 NOVEMBER",
           font=sans_b(12), fill=BRICK)
    draw_map(d, x0, my + 20, 384, 190)
    bx = x0 + 400
    by = my + 20
    for num, place, text in BRIEFS:
        line = "%d  %s \u2014 %s" % (num, place, text)
        by = para(d, bx, by, line, serif(10), x1 - bx, leading=12.5)
        by += 2

    # date check
    dy = 934
    d.rounded_rectangle([x0, dy, x1, dy + 48], radius=4,
                        outline=BRICK, width=2, fill=(252, 244, 238))
    para(d, x0 + 10, dy + 5, DATE_CHECK, sans(10), CW - 20, leading=12.5)

    # footer
    para(d, x0, 988, FOOTER, sans(9.5), CW, fill=FAINT, leading=12)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    build()
    print("wrote entry.png")
