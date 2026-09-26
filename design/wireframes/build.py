"""Generate editable SVG wireframes for Figma import.

Run: python3 design/wireframes/build.py
Outputs one SVG per screen plus all-screens.svg (drag into Figma).
Uses Finance Tracker DS v0.1 tokens: 440 frame, 36 margins, 368 / 177 widths.
"""
from pathlib import Path

OUT = Path(__file__).parent

# ---- Tokens (Finance Tracker DS v0.1) -------------------------------------
BG = "#FFFFFF"
SURFACE = "#EEF0F2"
BORDER = "#DDE1E5"
MUTED = "#6B737B"
TEXT = "#0A0A0A"
INV = "#000000"
INV_TEXT = "#F5F6F7"
INV_MUTED = "#8A9199"
ACCENT = "#E9B99A"
GAIN = "#5E9E7A"
LOSS = "#E46247"
VIOLET = "#8C7FD6"
LILAC = "#B9A7F0"
BLUE = "#6F86C9"
TRACK = "#E3E6EA"
SUN = "#F2AE7B"
DUSK4 = "#6E7C88"

W, H = 440, 956
M = 36            # side margin
CW = 368          # full-width component
HW = 177          # half-width component
GUT = 14

DISPLAY = "Inter"
MONO = "Space Mono"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def t(x, y, s, size=15, fill=TEXT, weight=400, family=DISPLAY, anchor="start",
      ls=None, name=None):
    extra = f' letter-spacing="{ls}"' if ls is not None else ""
    nid = f' id="{esc(name)}"' if name else ""
    return (f'<text{nid} x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')


def label(x, y, s, fill=MUTED, anchor="start", size=11):
    return t(x, y, s.upper(), size=size, fill=fill, family=MONO, anchor=anchor, ls=0.8)


def num(x, y, s, size=40, fill=TEXT, anchor="start", weight=400):
    return t(x, y, s, size=size, fill=fill, family=MONO, anchor=anchor, weight=weight)


def r(x, y, w, h, fill=BG, rx=0, stroke=None, sw=1, dash=None, opacity=None, name=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    nid = f' id="{esc(name)}"' if name else ""
    return f'<rect{nid} x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}{d}{o}/>'


def c(cx, cy, rad, fill=TEXT, stroke=None, sw=1, opacity=None):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="{fill}"{s}{o}/>'


def line(x1, y1, x2, y2, stroke=BORDER, sw=1, dash=None, cap="round"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')


def path(d, stroke="none", fill="none", sw=2, dash=None, opacity=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{opacity}"' if opacity is not None else ""
    return (f'<path d="{d}" stroke="{stroke}" fill="{fill}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"{ds}{o}/>')


def g(name, *children):
    return f'<g id="{esc(name)}">' + "".join(children) + "</g>"


def poly(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def smooth(pts):
    """Catmull-Rom to cubic bezier for a soft line."""
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(len(pts) - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[i + 2] if i + 2 < len(pts) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


# ---- Shared chrome ----------------------------------------------------------
def status_bar(dark=False):
    f = INV_TEXT if dark else TEXT
    return g("Status bar", t(M, 34, "9:41", 15, f, 600), r(W - M - 26, 24, 26, 12, "none", 3, f, 1.2))


def tab_bar(active):
    tabs = ["Wealth", "Spend", "Habits", "Ask AI"]
    parts = [r(0, H - 84, W, 84, BG), line(0, H - 84, W, H - 84, BORDER)]
    step = CW / 4
    for i, name in enumerate(tabs):
        cx = M + step * i + step / 2
        on = name == active
        col = TEXT if on else MUTED
        parts.append(r(cx - 11, H - 70, 22, 22, "none" if not on else TEXT, 7,
                       None if on else col, 1.5))
        parts.append(t(cx, H - 32, name, 11, col, 600 if on else 400, anchor="middle"))
    return g("Tab bar", *parts)


def card(name, x, y, w, h, *children, fill=BG, rx=36):
    return g(name, r(x, y, w, h, fill, rx, name=f"{name} / bg"), *children)


def pill_button(x, y, w, s, dark=True, h=52):
    fill, col = (INV, INV_TEXT) if dark else (BG, TEXT)
    stroke = None if dark else BORDER
    return g(f"Button / {s}", r(x, y, w, h, fill, h / 2, stroke),
             t(x + w / 2, y + h / 2 + 5, s, 15, col, 600, anchor="middle"))


def segmented(x, y, w, opts, active):
    h = 36
    parts = [r(x, y, w, h, SURFACE, 18)]
    seg = w / len(opts)
    for i, o in enumerate(opts):
        sx = x + seg * i
        if o == active:
            parts.append(r(sx + 3, y + 3, seg - 6, h - 6, INV, 15))
        parts.append(t(sx + seg / 2, y + 23, o, 12, INV_TEXT if o == active else MUTED,
                       family=MONO, anchor="middle"))
    return g("Segmented / horizon", *parts)


def frame(name, body, bg=SURFACE, extra_defs=""):
    return (f'<g id="{esc(name)}">'
            f'{r(0, 0, W, H, bg, 0, name=name + " / background")}{body}</g>'), extra_defs


# ---- Screen 1: Onboarding · savings range ----------------------------------
def s_onboarding():
    b = [status_bar()]
    b.append(g("Top", path("M44 82 L36 90 L44 98", TEXT, sw=2),
               label(W - M, 95, "Step 2 of 4", anchor="end")))
    # progress
    b.append(g("Progress", *[r(M + i * (CW / 4), 112, CW / 4 - 6, 4,
                               TEXT if i < 2 else BORDER, 2) for i in range(4)]))
    b.append(g("Heading",
               t(M, 176, "How much do you want", 28, TEXT, 400, ls=-0.5),
               t(M, 210, "to save each month?", 28, TEXT, 400, ls=-0.5),
               t(M, 246, "Set a range. Your plan is built around the", 15, MUTED),
               t(M, 268, "minimum — the stretch is a bonus.", 15, MUTED)))

    # Range card
    y0 = 300
    tx0, tx1 = M + 24, M + CW - 24
    hmin, hmax = tx0 + (tx1 - tx0) * 0.30, tx0 + (tx1 - tx0) * 0.55
    rc = [label(M + 24, y0 + 40, "Minimum"), num(M + 24, y0 + 78, "₹15,000", 28),
          label(M + CW - 24, y0 + 40, "Stretch", anchor="end"),
          num(M + CW - 24, y0 + 78, "₹25,000", 28, anchor="end"),
          r(tx0, y0 + 122, tx1 - tx0, 6, TRACK, 3),
          r(hmin, y0 + 122, hmax - hmin, 6, INV, 3),
          c(hmin, y0 + 125, 13, BG, INV, 2), c(hmax, y0 + 125, 13, BG, INV, 2),
          t(tx0, y0 + 164, "₹0", 12, MUTED, family=MONO),
          t(tx1, y0 + 164, "₹50,000", 12, MUTED, family=MONO, anchor="end"),
          r(M + 24, y0 + 186, CW - 48, 44, SURFACE, 14),
          t(M + 40, y0 + 213, "18–29% of your take-home", 13, TEXT),
          t(M + CW - 40, y0 + 213, "Healthy", 13, GAIN, 600, anchor="end")]
    b.append(card("Card / Savings range", M, y0, CW, 250, *rc))

    # Breakdown card
    y1 = 570
    rows = [("Take-home pay", "₹85,000", TEXT), ("Fixed costs", "− ₹32,000", MUTED),
            ("Savings minimum", "− ₹15,000", MUTED)]
    bc = [label(M + 24, y1 + 36, "What's left to spend")]
    for i, (a, v, col) in enumerate(rows):
        yy = y1 + 72 + i * 36
        bc += [t(M + 24, yy, a, 15, TEXT), t(M + CW - 24, yy, v, 15, col, family=MONO, anchor="end")]
    bc += [line(M + 24, y1 + 170, M + CW - 24, y1 + 170, BORDER),
           t(M + 24, y1 + 202, "Spendable / month", 15, TEXT, 600),
           num(M + CW - 24, y1 + 204, "₹38,000", 22, anchor="end")]
    b.append(card("Card / Spendable breakdown", M, y1, CW, 226, *bc))

    b.append(pill_button(M, H - 96, CW, "Continue"))
    return frame("01 Onboarding · Savings range", "".join(b))


# ---- Screen 2: Wealth home ---------------------------------------------------
def s_wealth():
    b = [status_bar()]
    b.append(g("Header",
               label(M, 88, "Net worth · today"),
               num(M, 136, "₹12,50,096", 40),
               t(M, 164, "+ ₹42,300 this month", 13, GAIN, family=MONO),
               r(W - M - 40, 64, 40, 40, BG, 20),
               t(W - M - 20, 90, "₹", 16, TEXT, 600, anchor="middle")))
    b.append(segmented(M, 186, CW, ["3M", "1Y", "5Y", "10Y"], "5Y"))

    # Forecast chart card
    cy, ch = 238, 330
    x0, x1 = M + 20, M + CW - 20
    top, bot = cy + 90, cy + 262
    n = 6
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]

    def ys(vals):
        return [bot - (bot - top) * v for v in vals]
    base = list(zip(xs, ys([0.10, 0.20, 0.30, 0.40, 0.50, 0.60])))
    cur = list(zip(xs, ys([0.10, 0.24, 0.30, 0.46, 0.60, 0.72])))
    pot = list(zip(xs, ys([0.10, 0.28, 0.44, 0.62, 0.80, 1.00])))
    hi = list(zip(xs, ys([0.10, 0.32, 0.46, 0.66, 0.86, 1.06])))
    lo = list(zip(xs, ys([0.10, 0.18, 0.16, 0.28, 0.36, 0.42])))
    band = poly(hi) + " L" + " L".join(f"{x:.1f} {y:.1f}" for x, y in reversed(lo)) + " Z"
    floor_y = ys([0.14])[0]
    scrub_x = xs[3]
    cc = [label(M + 20, cy + 34, "Forecast · 5 years"),
          t(M + 20, cy + 62, "In today's rupees", 13, MUTED),
          r(M + CW - 20 - 96, cy + 20, 96, 30, SURFACE, 15),
          t(M + CW - 20 - 48, cy + 40, "Scenarios ▾", 12, TEXT, anchor="middle")]
    for i in range(4):
        yy = top + (bot - top) * i / 3
        cc.append(line(x0, yy, x1, yy, TRACK, 1, "2 4"))
    cc += [path(band, fill=LILAC, opacity=0.25),
           line(x0, floor_y, x1, floor_y, LOSS, 1, "4 4"),
           t(x1, floor_y - 6, "Floor", 10, LOSS, family=MONO, anchor="end"),
           path(smooth(base), DUSK4, sw=2, dash="5 5"),
           path(smooth(pot), VIOLET, sw=2.5),
           path(smooth(cur), TEXT, sw=2.5),
           line(scrub_x, top - 8, scrub_x, bot, TEXT, 1),
           c(scrub_x, cur[3][1], 6, BG, TEXT, 2)]
    # tooltip (inverse)
    tx, ty = scrub_x - 128, top - 4
    cc.append(g("Tooltip / scrub",
                r(tx, ty, 116, 64, INV, 14),
                label(tx + 12, ty + 20, "Sep 2029 · age 31", INV_MUTED, size=9),
                num(tx + 12, ty + 44, "₹31.4L", 18, INV_TEXT),
                t(tx + 12, ty + 58, "2 goals reached", 10, INV_MUTED)))
    for i, yr in enumerate(["26", "27", "28", "29", "30", "31"]):
        cc.append(t(xs[i], bot + 22, f"'{yr}", 11, MUTED, family=MONO, anchor="middle"))
    # legend
    ly = cy + ch - 26
    leg = [("Current", TEXT, None), ("Good habits", VIOLET, None), ("Baseline", DUSK4, "4 3")]
    lx = M + 20
    for name, col, dash in leg:
        cc += [line(lx, ly - 4, lx + 18, ly - 4, col, 2.5, dash), t(lx + 24, ly, name, 12, MUTED)]
        lx += 24 + len(name) * 7 + 22
    b.append(card("Card / Forecast", M, cy, CW, ch, *cc))

    # Goal timeline strip
    gy = 584
    gt = [label(M + 20, gy + 30, "Goals on your timeline"),
          t(M + CW - 20, gy + 30, "+ Add", 13, TEXT, 600, anchor="end"),
          line(x0, gy + 74, x1, gy + 74, TRACK, 3)]
    goals = [(xs[0] + 30, "Goa trip", SUN, "circle"), (xs[2] - 10, "Car", LOSS, "square"),
             (xs[3] + 12, "House", GAIN, "diamond"), (xs[5] - 16, "Venture", BLUE, "circle")]
    for gx, name, col, shape in goals:
        if shape == "circle":
            gt.append(c(gx, gy + 74, 8, col))
        elif shape == "square":
            gt.append(r(gx - 7, gy + 67, 14, 14, col, 3))
        else:
            gt.append(path(f"M{gx} {gy+64} L{gx+10} {gy+74} L{gx} {gy+84} L{gx-10} {gy+74} Z", fill=col))
        gt.append(t(gx, gy + 104, name, 12, TEXT, anchor="middle"))
    gt.append(t(M + 20, gy + 130, "Drag a goal to see how it moves your curve", 12, MUTED))
    b.append(card("Card / Goal timeline", M, gy, CW, 148, *gt, rx=24))

    # Half cards
    hy = 746
    b.append(card("Card / Habits gap", M, hy, HW, 112,
                  label(M + 16, hy + 28, "Good habits add", size=10),
                  num(M + 16, hy + 64, "₹38L", 26, VIOLET),
                  t(M + 16, hy + 90, "by 2031", 12, MUTED), rx=24))
    ax = M + HW + GUT
    b.append(card("Card / Ask AI", ax, hy, HW, 112,
                  label(ax + 16, hy + 28, "Ask AI", INV_MUTED, size=10),
                  t(ax + 16, hy + 60, "“What if I buy the", 13, INV_TEXT),
                  t(ax + 16, hy + 78, "car in 2027?”", 13, INV_TEXT),
                  t(ax + HW - 16, hy + 98, "→", 16, INV_TEXT, anchor="end"),
                  fill=INV, rx=24))
    b.append(tab_bar("Wealth"))
    return frame("02 Wealth · Home", "".join(b))


# ---- Screen 3: Spend home ----------------------------------------------------
def s_spend():
    b = [status_bar()]
    b.append(g("Header", label(M, 88, "September · day 26 of 30"),
               t(M, 124, "Spend", 28, TEXT, 400, ls=-0.5)))

    # Budget gauge card (sun)
    gy = 148
    gcx, gcy, gr = W / 2, gy + 168, 118
    import math

    def arc(frac):
        a0, a1 = math.pi, math.pi * (1 - frac)
        x0_, y0_ = gcx + gr * math.cos(a0), gcy - gr * math.sin(a0)
        x1_, y1_ = gcx + gr * math.cos(a1), gcy - gr * math.sin(a1)
        return f"M{x0_:.1f} {y0_:.1f} A{gr} {gr} 0 0 1 {x1_:.1f} {y1_:.1f}"
    frac = 0.56
    sx, sy = gcx + gr * math.cos(math.pi * (1 - frac)), gcy - gr * math.sin(math.pi * (1 - frac))
    gc = [label(M + 24, gy + 34, "Monthly budget"),
          path(arc(1.0), TRACK, sw=10), path(arc(frac), TEXT, sw=10),
          c(sx, sy, 12, SUN), line(M + 24, gcy, M + CW - 24, gcy, BORDER, 1, "3 4"),
          num(gcx, gcy - 34, "₹21,400", 30, anchor="middle"),
          t(gcx, gcy - 8, "of ₹38,000 spent", 13, MUTED, anchor="middle"),
          t(M + 24, gcy + 30, "Savings ₹18,000 ✓", 12, GAIN, family=MONO),
          t(M + CW - 24, gcy + 30, "4 days left", 12, MUTED, family=MONO, anchor="end")]
    b.append(card("Card / Budget gauge", M, gy, CW, 232, *gc))

    # You can spend more (ghost fill)
    ry = 394
    bars_x0 = M + 24
    bw, bgap = 30, 14
    budget_h = 96
    base_y = ry + 208
    vals = [0.55, 0.40, 0.62, 0.35]
    weeks = ["W1", "W2", "W3", "W4"]
    rc = [label(M + 24, ry + 32, "Room to spend", fill=TEXT),
          t(M + 24, ry + 58, "₹8,200 of guilt-free money", 15, TEXT, 600),
          t(M + 24, ry + 78, "You've hit your savings. Enjoy some of it.", 13, MUTED),
          line(bars_x0 - 4, base_y - budget_h, bars_x0 + 4 * (bw + bgap), base_y - budget_h, MUTED, 1, "3 3")]
    for i, v in enumerate(vals):
        bx = bars_x0 + i * (bw + bgap)
        h_ = budget_h * v
        rc += [r(bx, base_y - budget_h, bw, budget_h - h_, "none", 10, ACCENT, 1.5, "3 3"),
               r(bx, base_y - h_, bw, h_, INV, 10),
               t(bx + bw / 2, base_y + 18, weeks[i], 11, MUTED, family=MONO, anchor="middle")]
    ex = bars_x0 + 4 * (bw + bgap) + 8
    rc += [r(ex, ry + 126, CW - (ex - M) - 24, 30, BG, 15, ACCENT, 1.5, "3 3"),
           t(ex + 12, ry + 146, "Unused room", 11, TEXT),
           r(ex, ry + 164, CW - (ex - M) - 24, 30, INV, 15),
           t(ex + 12, ry + 184, "Spent", 11, INV_TEXT)]
    b.append(card("Card / Room to spend", M, ry, CW, 242, *rc))

    # Rebalance (donut + sliders)
    ey = 648
    dcx, dcy, dr = M + 70, ey + 124, 46
    import math as m2
    cats = [("Rent", 0.40, INV, True), ("Food", 0.22, VIOLET, False),
            ("Travel", 0.14, BLUE, False), ("Fun", 0.24, ACCENT, False)]
    circ = 2 * m2.pi * dr
    off = 0
    ec = [label(M + 24, ey + 32, "Rebalance categories"),
          t(M + CW - 24, ey + 32, "Total stays ₹38,000", 11, MUTED, family=MONO, anchor="end")]
    for name, frac_, col, _ in cats:
        seg = circ * frac_
        ec.append(f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="none" stroke="{col}" stroke-width="16" '
                  f'stroke-dasharray="{seg - 2:.1f} {circ - seg + 2:.1f}" stroke-dashoffset="{-off:.1f}" '
                  f'transform="rotate(-90 {dcx} {dcy})"/>')
        off += seg
    sx0 = M + 150
    sx1 = M + CW - 24
    for i, (name, frac_, col, locked) in enumerate(cats):
        yy = ey + 70 + i * 34
        ec.append(t(sx0, yy, name + (" 🔒" if locked else ""), 12, TEXT))
        ec.append(r(sx0 + 64, yy - 5, sx1 - sx0 - 64, 4, TRACK, 2))
        kx = sx0 + 64 + (sx1 - sx0 - 64) * (frac_ / 0.45)
        ec.append(r(sx0 + 64, yy - 5, kx - sx0 - 64, 4, col, 2))
        if not locked:
            ec.append(c(kx, yy - 3, 8, BG, col, 2))
    b.append(card("Card / Rebalance", M, ey, CW, 212, *ec, rx=24))
    b.append(tab_bar("Spend"))
    return frame("03 Spend · Home", "".join(b))


# ---- Screen 4: Subscriptions -------------------------------------------------
def s_subs():
    b = [status_bar()]
    b.append(g("Header", path("M44 82 L36 90 L44 98", TEXT, sw=2),
               label(M, 138, "Subscriptions · monthly"),
               num(M, 184, "₹4,860", 40),
               t(M, 212, "11 active · ₹58,320 a year", 13, MUTED, family=MONO)))
    # insight card (inverse)
    iy = 240
    b.append(card("Card / Insight", M, iy, CW, 150,
                  label(M + 24, iy + 34, "Insight", INV_MUTED),
                  t(M + 24, iy + 66, "No Spotify use in 3 months", 17, INV_TEXT, 600),
                  t(M + 24, iy + 90, "Cancelling saves ₹1,428 a year.", 13, INV_MUTED),
                  r(M + 24, iy + 106, 110, 32, INV_TEXT, 16),
                  t(M + 79, iy + 127, "Cancel", 13, INV, 600, anchor="middle"),
                  r(M + 144, iy + 106, 90, 32, "none", 16, INV_MUTED, 1),
                  t(M + 189, iy + 127, "Keep", 13, INV_TEXT, anchor="middle"),
                  fill=INV, rx=24))

    groups = [("Entertainment", "₹1,247", [("Netflix", "₹649", "Used 2 days ago", False),
                                              ("Spotify", "₹119", "Not used · 3 mo", True),
                                              ("Hotstar", "₹479", "Used last week", False)]),
              ("AI tools", "₹3,413", [("Claude", "₹1,700", "Used today", False),
                                         ("ChatGPT", "₹1,713", "Overlaps with Claude", True)]),
              ("Work tools", "₹200", [("Figma", "Paid by work", "Reimbursable", False)])]
    y = 402
    for gname, total, items in groups:
        h_ = 44 + len(items) * 48
        parts = [label(M + 20, y + 28, gname), t(M + CW - 20, y + 28, total, 12, MUTED, family=MONO, anchor="end")]
        for i, (nm, price, meta, flag) in enumerate(items):
            yy = y + 44 + i * 48
            if i:
                parts.append(line(M + 20, yy, M + CW - 20, yy, SURFACE))
            parts += [r(M + 20, yy + 6, 36, 36, SURFACE, 10),
                      t(M + 38, yy + 29, nm[0], 14, TEXT, 600, anchor="middle"),
                      t(M + 68, yy + 22, nm, 15, TEXT),
                      t(M + 68, yy + 38, meta, 11, LOSS if flag else MUTED, family=MONO),
                      t(M + CW - 20, yy + 29, price, 14, TEXT, family=MONO, anchor="end")]
        b.append(card(f"Card / {gname}", M, y, CW, h_, *parts, rx=24))
        y += h_ + 12
    b.append(tab_bar("Spend"))
    return frame("04 Spend · Subscriptions", "".join(b))


# ---- Screen 5: Breathe-in ----------------------------------------------------
def s_breathe():
    defs = ('<linearGradient id="night" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#030507"/><stop offset="0.35" stop-color="#0B1520"/>'
            '<stop offset="0.7" stop-color="#16283A"/><stop offset="1" stop-color="#243A4E"/>'
            '</linearGradient>')
    b = ['<rect x="0" y="0" width="440" height="956" fill="url(#night)"/>', status_bar(dark=True)]
    cx, cy = W / 2, 380
    b.append(g("Breath circle",
               c(cx, cy, 150, "#E8ECF2", opacity=0.05),
               c(cx, cy, 112, "#E8ECF2", opacity=0.08),
               c(cx, cy, 76, "#E8ECF2", opacity=0.9),
               t(cx, cy + 6, "Breathe in", 17, INV, 600, anchor="middle"),
               t(cx, cy + 190, "4 · 4 · 6", 12, INV_MUTED, family=MONO, anchor="middle")))
    b.append(g("Message",
               t(cx, 640, "You've checked 7 times today.", 22, INV_TEXT, 300, anchor="middle"),
               t(cx, 676, "Your 10-year plan hasn't changed", 15, INV_MUTED, anchor="middle"),
               t(cx, 698, "since this morning.", 15, INV_MUTED, anchor="middle")))
    b.append(g("Actions",
               r(M, H - 158, CW, 52, INV_TEXT, 26),
               t(W / 2, H - 127, "Back to my day", 15, INV, 600, anchor="middle"),
               t(W / 2, H - 72, "Show me the numbers anyway", 13, INV_MUTED, anchor="middle")))
    return frame("05 Wealth · Breathe in", "".join(b), bg="#030507", extra_defs=defs)


SCREENS = [("01-onboarding-savings-range", s_onboarding), ("02-wealth-home", s_wealth),
           ("03-spend-home", s_spend), ("04-subscriptions", s_subs), ("05-breathe-in", s_breathe)]


def wrap(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}</defs>{body}</svg>\n')


def main():
    gap = 80
    all_body, all_defs = [], []
    for i, (slug, fn) in enumerate(SCREENS):
        body, defs = fn()
        (OUT / f"{slug}.svg").write_text(wrap(W, H, body, defs), encoding="utf-8")
        all_body.append(f'<g transform="translate({i * (W + gap)} 0)">{body}</g>')
        all_defs.append(defs)
    total_w = len(SCREENS) * W + (len(SCREENS) - 1) * gap
    (OUT / "all-screens.svg").write_text(wrap(total_w, H, "".join(all_body), "".join(all_defs)),
                                         encoding="utf-8")
    print("wrote", len(SCREENS) + 1, "files to", OUT)


if __name__ == "__main__":
    main()
