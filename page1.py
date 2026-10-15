# page1.py - Sheet 1: general arrangement.
#
# Right-hand column, top to bottom: tank storage capacity, parts list, site level
# confirmation, notes, approval stamp. The blocks are scaled up to fill the full column
# height and spaced evenly, so no empty band is left under the tables.
#
# Plan and front elevation are drawn at ONE scale in the area left of that column - the
# scale shrinks until every dimension and callout fits, so a long tank can never run into
# the column. Spare height is shared evenly above the plan, between plan and elevation, and
# below the elevation.

from reportlab.lib import colors
from reportlab.lib.colors import black
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

from Internal.plan_view import draw_plan_view, plan_margins, FN, FB
from Internal.elevation_view import draw_elevation_view, left_need

PW, PH = landscape(A3)
IM = 10 * mm
IX0, IX1 = IM, PW - IM
IY0, IY1 = IM, PH - IM
TB_TOP = IY0 + 45 * mm                      # top of the title block
TBAR_TOP = TB_TOP + 6 * mm                  # top of the tolerance bar

NOTES = ["NOTES:",
         "1. THE EXCAVATION MUST HAVE A MINIMUM OF",
         "    500mm CLEARANCE AROUND THE ENTIRETY OF THE TANK OR",
         "    AS REQUIRED ON-SITE.",
         "2. ACCESS MANHOLES Ø375 ROUND LIDS - CLASS 'D' (BY ATLAN)",
         "    Ø300 PVC RISERS (BY OTHERS)."]

RIGHT_W = 276                       # width of the right-hand column
RIGHT_X = IX1 - 8 - RIGHT_W         # its left edge
LIMIT = RIGHT_X - 8                 # plan + elevation, labels included, stay left of this
ELEV_RIGHT_NEED = 52                # 500 dimension, right pipe stub + arrow

ELEV_BASE = 46          # room under the elevation tank: base RL label + title
ELEV_ABOVE = 72         # room above top of storage: callouts, 500 extension

COL_TOP = IY1 - 10                  # column spans from here ...
COL_BOTTOM = TB_TOP + 5             # ... down to the stamp's bottom edge
KMAX = 1.4                          # largest enlargement of the column blocks
GAP_MIN = 14


# ----------------------------------------------------------------------------------
# COLUMN BLOCKS  (k = enlargement factor, 1.0 = compact)
# ----------------------------------------------------------------------------------

def _notes_fs():
    return min(9.5, (RIGHT_W - 4) / max(stringWidth(t, FN, 1) for t in NOTES))


def _notes_h(k):
    fs = _notes_fs()
    return fs + (len(NOTES) - 1) * fs * 1.28 * k + 3


def _notes(c, x, top, k):
    fs = _notes_fs()
    lead = fs * 1.28 * k
    c.setFillColor(black)
    for i, t in enumerate(NOTES):
        c.setFont(FB if i == 0 else FN, fs)
        c.drawString(x + 2, top - fs - i * lead, t)


def _capacity_h(k):
    return 19 * k


def _capacity_box(c, x, top, text, k):
    """Boxed heading across the column width; text shrinks to fit."""
    h = _capacity_h(k)
    fs = min(13.0 * min(k, 1.2), (RIGHT_W - 8) / stringWidth(text, FN, 1))
    c.setStrokeColor(black)
    c.setLineWidth(0.8)
    c.rect(x, top - h, RIGHT_W, h, stroke=1, fill=0)
    c.setFont(FN, fs)
    c.setFillColor(black)
    c.drawCentredString(x + RIGHT_W / 2, top - h / 2 - fs * 0.35, text)


def _parts_h(n, k):
    return (16 + 13 + max(n, 1) * 12.5) * k


def _parts_list(c, x, top, rows, k):
    w = RIGHT_W
    props = [0.10, 0.63, 0.10, 0.17]
    ws = [w * p for p in props]
    xs = [x]
    for cw in ws[:-1]:
        xs.append(xs[-1] + cw)
    title_h, hdr_h, row_h = 16 * k, 13 * k, 12.5 * k
    # text size: bigger with k, but the longest description must fit its column
    fs = 8.0 * min(k, 1.15)
    longest = max((stringWidth(r[1], FN, 1) for r in rows), default=0)
    if longest:
        fs = min(fs, (ws[1] - 6) / longest)
    fs_hdr = min(8.0 * min(k, 1.15), fs + 0.5)
    h = _parts_h(len(rows), k)
    bot = top - h

    c.setStrokeColor(black)
    c.setFillColor(black)
    c.setLineWidth(1.2)
    c.rect(x, bot, w, h, stroke=1, fill=0)
    c.setLineWidth(0.5)
    c.line(x, top - title_h, x + w, top - title_h)
    c.line(x, top - title_h - hdr_h, x + w, top - title_h - hdr_h)
    for i in range(1, len(rows)):
        yy = top - title_h - hdr_h - i * row_h
        c.line(x, yy, x + w, yy)
    for cx in xs[1:]:
        c.line(cx, bot, cx, top - title_h)

    c.setFont(FN, fs_hdr)
    c.drawCentredString(x + w / 2, top - title_h / 2 - fs_hdr * 0.35, "PARTS LIST")
    for hdr, cx, cw in zip(["ITEM", "DESCRIPTION", "QTY", "REMARKS"], xs, ws):
        c.drawCentredString(cx + cw / 2, top - title_h - hdr_h / 2 - fs_hdr * 0.35, hdr)
    c.setFont(FN, fs)
    for i, (item, desc, qty, rem) in enumerate(rows):
        base = top - title_h - hdr_h - (i + 0.5) * row_h - fs * 0.35
        c.drawCentredString(xs[0] + ws[0] / 2, base, item)
        c.drawString(xs[1] + 3, base, desc)
        c.drawCentredString(xs[2] + ws[2] / 2, base, qty)
        if rem:
            c.drawString(xs[3] + 3, base, rem)


def _site_h(k):
    return (22 + 7 * 15) * k


def _site_level(c, x, top, k):
    w = RIGHT_W
    title_h, row_h = 22 * k, 15 * k
    h = _site_h(k)
    bot = top - h
    c.setStrokeColor(black)
    c.setFillColor(black)
    c.setLineWidth(1.4)
    c.rect(x, bot, w, h, stroke=1, fill=0)
    c.setLineWidth(0.5)
    t_bot = top - title_h
    c.line(x, t_bot, x + w, t_bot)
    for i in range(1, 7):
        c.line(x, t_bot - i * row_h, x + w, t_bot - i * row_h)
    div = x + w * 0.75
    foot_div = x + w * 0.30
    c.line(div, t_bot, div, t_bot - 4 * row_h)
    c.line(foot_div, bot, foot_div, t_bot - 4 * row_h)

    fs_t = 11 * min(k, 1.2)
    c.setFont(FB, fs_t)
    c.drawCentredString(x + w / 2, top - title_h / 2 - fs_t * 0.35, "Site Level Confirmation")

    rows = [("Finished Surface Level (FSL)", "RL:", "l"), ("Access Cover Thickness", "mm", "r"),
            ("Inlet Invert Level", "RL:", "l"), ("Outlet Invert Level", "RL:", "l")]
    fs = min(8.5 * min(k, 1.15),
             (div - x - 8) / max(stringWidth(r[0], FN, 1) for r in rows))
    c.setFont(FN, fs)
    for i, (lbl, val, al) in enumerate(rows):
        yy = t_bot - (i + 0.5) * row_h - fs * 0.35
        c.drawRightString(div - 3, yy, lbl)
        if al == "l":
            c.drawString(div + 3, yy, val)
        else:
            c.drawRightString(x + w - 3, yy, val)
    for i, lbl in enumerate(["Company:", "Name:", "Date:"]):
        c.drawString(x + 3, t_bot - (4 + i + 0.5) * row_h - fs * 0.35, lbl)


def _stamp_h(k):
    return 32 * min(k, 1.25)


def _stamp(c, x, y, w, k):
    h = _stamp_h(k)
    fs = 15 * min(k, 1.25)
    red = colors.Color(0.85, 0.1, 0.1)
    c.saveState()                                # keeps the outline text mode from leaking
    c.setStrokeColor(red)
    c.setLineWidth(2)
    c.roundRect(x, y, w, h, 7, stroke=1, fill=0)
    t = c.beginText()
    t.setFont(FB, fs)
    t.setTextRenderMode(1)                       # outline letters
    c.setLineWidth(0.8)
    txt = "ISSUE FOR APPROVAL"
    t.setTextOrigin(x + (w - stringWidth(txt, FB, fs)) / 2, y + h - fs - 3)
    t.textOut(txt)
    c.drawText(t)
    c.restoreState()

    c.saveState()
    c.setFillColor(red)
    c.setFont(FB, 7.5 * min(k, 1.25))
    c.drawCentredString(x + w / 2, y + 6, "NOT FOR CONSTRUCTION")
    c.restoreState()


def _draw_column(c, d):
    """Draw the right-hand column, scaled to span COL_TOP .. COL_BOTTOM."""
    n = len(d["parts_list"])
    avail = COL_TOP - COL_BOTTOM - 4 * GAP_MIN
    # heights are linear in k apart from the fixed part of the notes block
    fs = _notes_fs()
    fixed = fs + 3
    per_k = 19 + (len(NOTES) - 1) * fs * 1.28 + (29 + 12.5 * max(n, 1)) + (22 + 105) + 32
    k = max(1.0, min(KMAX, (avail - fixed) / per_k))
    gap = (COL_TOP - COL_BOTTOM - (_capacity_h(k) + _notes_h(k) + _parts_h(n, k)
                                   + _site_h(k) + _stamp_h(k))) / 4
    gap = min(gap, 60)

    y = COL_TOP
    _capacity_box(c, RIGHT_X, y, f"TANK STORAGE CAPACITY: {d['tank_storage']:g}m3", k)
    y -= _capacity_h(k) + gap
    _parts_list(c, RIGHT_X, y, d["parts_list"], k)
    y -= _parts_h(n, k) + gap
    _site_level(c, RIGHT_X, y, k)
    y -= _site_h(k) + gap
    _notes(c, RIGHT_X, y, k)                    # plain text goes after the three tables
    # stamp keeps the bottom of the column, just above the title block
    sw = min(RIGHT_W, 232)
    _stamp(c, RIGHT_X + (RIGHT_W - sw) / 2, COL_BOTTOM, sw, k)


# ----------------------------------------------------------------------------------
# SCALE / LAYOUT
# ----------------------------------------------------------------------------------

def _x_extent(d, s, l, r):
    """(offset of module left from region left, total width) for scale s."""
    ex = max(525 * s, 12)
    off = max(l + ex, left_need(d))             # plan margin, or the elevation's dimension columns
    return off, off + d["length"] * s + ex + r


def _scale(d, left, top, bottom):
    """Largest common plan/elevation scale (pt per mm) that fits left of the column."""
    l, r, t, b = plan_margins(d)
    s = (LIMIT - left) / (d["length"] + 2 * 525)
    for _ in range(4):                          # width depends on s through the red offset
        off, _w = _x_extent(d, s, l, r)
        ex = max(525 * s, 12)
        s = min((LIMIT - left - off - ex - r) / d["length"],
                (LIMIT - left - off - ELEV_RIGHT_NEED) / d["length"])
    avail = top - bottom - t - b
    s_fixed = (avail - ELEV_BASE - ELEV_ABOVE) / (d["exc_width"] + d["stack_h"])
    s_cover = (avail - ELEV_BASE - 44) / (d["exc_width"] + d["stack_h"] + d["cover"])
    return min(s, s_fixed, s_cover)


def draw_page1(c, d):
    bottom = TBAR_TOP + 6
    left = IX0 + 6
    top = IY1 - 6                                         # whole left area is free for the drawings
    s = _scale(d, left, top, bottom)

    _draw_column(c, d)

    # --- plan + elevation, one scale; spare height shared in three equal gaps -------------
    l, r, t, b = plan_margins(d)
    ex = max(525 * s, 12)
    plan_h = t + d["width"] * s + 2 * ex + b
    elev_h = ELEV_BASE + d["stack_h"] * s + max(ELEV_ABOVE, d["cover"] * s + 44)
    gap3 = max((top - bottom) - plan_h - elev_h, 0) / 3   # above plan / between / below elevation
    off, _w = _x_extent(d, s, l, r)
    mx = left + off                                      # module left edge
    my = top - gap3 - t - ex - d["width"] * s            # module bottom edge
    ey = bottom + gap3 + ELEV_BASE                       # elevation base
    elev_top = ey + d["stack_h"] * s + max(ELEV_ABOVE, d["cover"] * s + 44)
    draw_plan_view(c, d, mx, my, s, floor_y=elev_top + 2)
    draw_elevation_view(c, d, mx, ey, s, view="front", annotate=True)
