 # page1.py — Page 1 content: Parts List + Site Level Confirmation tables.

from reportlab.lib.colors import black
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

from Internal.plan_view import draw_plan_view
from Internal.elevation_view import draw_elevation_view

# ── Shared constants (re-imported to keep page modules self-consistent) ───────
# These mirror the values in main.py; import from main if preferred.
from reportlab.lib.pagesizes import A3, landscape
PW, PH    = landscape(A3)
IM        = 10 * mm
IX0       = IM;   IX1 = PW - IM;   IW  = IX1 - IX0
IY0       = IM;   IY1 = PH - IM
TBAR_H    = 6 * mm
TB_H      = 45 * mm
TBAR_BOT  = IY0 + TB_H
TBAR_TOP  = TBAR_BOT + TBAR_H

CLW = 0.5
FN  = "Helvetica"
FB  = "Helvetica-Bold"
PAD = 1.0 * mm


def clip_text(text, font, size, max_width):
    while len(text) > 1 and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text

def draw_page1_diagrams(c, drawing_data):

    draw_plan_view(
        c,
        drawing_data,
        x=140,
        y=450
    )


    draw_elevation_view(
        c,
        drawing_data,
        x=140,
        y=300
    )
    
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1 TABLES
# ═══════════════════════════════════════════════════════════════════════════════

def draw_page1_tables(c, parts_list=None):
    """Draw the Parts List and Site Level Confirmation tables on page 1."""
    if parts_list is None:
        parts_list = []

    # ── Region geometry ───────────────────────────────────────────────────────
    BDR_X1     = IM
    BDR_X2     = PW - IM
    COL_W_GRID = (BDR_X2 - BDR_X1) / 6

    REGION_L = BDR_X1 + 4 * COL_W_GRID
    REGION_R = IX1
    REGION_W = REGION_R - REGION_L

    REGION_BOT = TBAR_TOP
    REGION_TOP = IY1

    OUTER_PAD = 5 * mm
    TABLE_GAP = 8 * mm
    TBL_W     = REGION_W - 2 * OUTER_PAD
    TBL_X     = REGION_L + OUTER_PAD

    TITLE_H = 8 * mm
    HDR_H   = 7 * mm
    ROW_H   = 6 * mm

    FS_TITLE = 9
    FS_HDR   = 9
    FS_DATA  = 9

    _draw_parts_list(c, TBL_X, TBL_W, REGION_TOP, OUTER_PAD,
                     TITLE_H, HDR_H, ROW_H, FS_TITLE, FS_HDR, FS_DATA,
                     parts_list)

    # p1_bot is needed to position Table 2 below Table 1
    p1_h   = TITLE_H + HDR_H + len(parts_list) * ROW_H
    p1_top = REGION_TOP - OUTER_PAD
    p1_bot = p1_top - p1_h

    _draw_site_level_confirmation(c, TBL_X, TBL_W, p1_bot, TABLE_GAP,
                                  TITLE_H, ROW_H, FS_TITLE, FS_DATA)


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 1 – PARTS LIST
# ─────────────────────────────────────────────────────────────────────────────

def _draw_parts_list(c, TBL_X, TBL_W, REGION_TOP, OUTER_PAD,
                     TITLE_H, HDR_H, ROW_H, FS_TITLE, FS_HDR, FS_DATA,
                     parts_data=None):
    if parts_data is None:
        parts_data = []

    ROW_H = 5*mm
    p1_props  = [0.09, 0.50, 0.10, 0.31]
    p1_widths = [TBL_W * p for p in p1_props]
    p1_xs     = [TBL_X]
    for w in p1_widths[:-1]:
        p1_xs.append(p1_xs[-1] + w)

    p1_h    = TITLE_H + HDR_H + len(parts_data) * ROW_H
    p1_top  = REGION_TOP - OUTER_PAD
    p1_bot  = p1_top - p1_h
    title_bot = p1_top  - TITLE_H
    hdr_bot   = title_bot - HDR_H

    # Outer border (no fill)
    c.setStrokeColor(black)
    c.setLineWidth(1.5)
    c.rect(TBL_X, p1_bot, TBL_W, p1_h, stroke=1, fill=0)

    # Horizontal dividers
    c.setLineWidth(CLW)
    c.line(TBL_X, title_bot, TBL_X + TBL_W, title_bot)
    c.line(TBL_X, hdr_bot,   TBL_X + TBL_W, hdr_bot)
    for ri in range(1, len(parts_data)):
        ry = hdr_bot - ri * ROW_H
        c.setLineWidth(0.4)
        c.line(TBL_X, ry, TBL_X + TBL_W, ry)

    # Vertical column dividers (header row + data rows; NOT through title)
    for ci in range(1, len(p1_xs)):
        c.setLineWidth(CLW)
        c.line(p1_xs[ci], hdr_bot,  p1_xs[ci], title_bot)
        c.setLineWidth(0.4)
        c.line(p1_xs[ci], p1_bot,   p1_xs[ci], hdr_bot)

    # Title (bold, centred, no fill)
    c.setFillColor(black)
    c.setFont(FN, FS_TITLE)
    c.drawCentredString(TBL_X + TBL_W / 2,
                        title_bot + (TITLE_H - FS_TITLE) / 2,
                        "PARTS LIST")

    # Column headers (bold)
    c.setFont(FN, FS_HDR)
    for hdr, cx, cw in zip(["ITEM", "DESCRIPTION", "QTY", "REMARKS"],
                             p1_xs, p1_widths):
        c.drawCentredString(cx + cw / 2,
                            hdr_bot + (HDR_H - FS_HDR) / 2,
                            hdr)

    # Data rows
    c.setFont(FN, FS_DATA)
    for ri, (item, desc, qty, rem) in enumerate(parts_data):
        row_bot = hdr_bot - (ri + 1) * ROW_H
        mid_y   = row_bot + (ROW_H - FS_DATA) / 2
        c.drawCentredString(p1_xs[0] + p1_widths[0] / 2, mid_y, item)
        c.drawString(p1_xs[1] + PAD, mid_y,
                     clip_text(desc, FN, FS_DATA, p1_widths[1] - 2 * PAD))
        c.drawCentredString(p1_xs[2] + p1_widths[2] / 2, mid_y, qty)
        if rem:
            c.drawString(p1_xs[3] + PAD, mid_y,
                         clip_text(rem, FN, FS_DATA, p1_widths[3] - 2 * PAD))


# ─────────────────────────────────────────────────────────────────────────────
# TABLE 2 – SITE LEVEL CONFIRMATION
# ─────────────────────────────────────────────────────────────────────────────

def _draw_site_level_confirmation(c, TBL_X, TBL_W, p1_bot, TABLE_GAP,
                                  TITLE_H, ROW_H, FS_TITLE, FS_DATA):
    """
    Layout:
      - Title row: full width, centred bold
      - 4 data rows with a vertical divider at 75% from left
      - 3 footer rows (Company / Name / Date) with a divider at 30% from left
    """

    S2_X        = TBL_X + 30*mm 
    S2_W        = TBL_W -30 *mm
    S2_DIV      = S2_X + S2_W * 0.75   # data-rows divider (label | value)
    S2_FOOT_DIV = S2_X + S2_W * 0.30   # footer divider (label | blank)
    

    s2_data_rows = 4
    s2_foot_rows = 3

    S2_ROW_H = 6 * mm   # reduce table height

    s2_h= TITLE_H + (s2_data_rows + s2_foot_rows) * S2_ROW_H
    s2_top = p1_bot - TABLE_GAP
    s2_bot = s2_top - s2_h

    s2_title_bot = s2_top - TITLE_H

    # Outer border
    c.setStrokeColor(black)
    c.setLineWidth(1.5)
    
    c.rect(S2_X, s2_bot, S2_W, s2_h, stroke=1, fill=0)

    # Horizontal line below title
    c.setLineWidth(CLW)
    c.line(S2_X, s2_title_bot, S2_X + S2_W, s2_title_bot)

    # Horizontal lines between every body row
    c.setLineWidth(0.4)
    for ri in range(1, s2_data_rows + s2_foot_rows):
        ry = s2_title_bot - ri * ROW_H
        c.line(S2_X, ry, S2_X + S2_W, ry)

    # Vertical divider for data rows (4) at 75%
    s2_data_bot = s2_title_bot - s2_data_rows * ROW_H
    c.setLineWidth(0.4)
    c.line(S2_DIV, s2_data_bot, S2_DIV, s2_title_bot)

    # Vertical divider for footer rows (3) at 30%
    c.line(S2_FOOT_DIV, s2_bot, S2_FOOT_DIV, s2_data_bot)

    # Title
    c.setFillColor(black)
    c.setFont(FB,12)
    c.drawCentredString(S2_X + S2_W / 2,
                        s2_title_bot + (TITLE_H - FS_TITLE) / 2,
                        "Site Level Confirmation")

    # Data rows
    s2_data = [
        ("Finished Surface Level (FSL)", "R", "RL:", "L"),
        ("Access Cover Thickness",       "R", "mm",  "R"),
        ("Inlet Invert Level",           "R", "RL:", "L"),
        ("Outlet Invert Level",          "R", "RL:", "L"),
    ]
    label_w = S2_DIV - S2_X
    val_w   = S2_W   - label_w

    c.setFont(FN, FS_DATA)
    for ri, (label, la, val, va) in enumerate(s2_data):
        row_bot = s2_title_bot - (ri + 1) * ROW_H
        mid_y   = row_bot + (ROW_H - FS_DATA) / 2

        if la == "L":
           c.drawString(S2_X + PAD + 10*mm, mid_y,
                    clip_text(label, FN, FS_DATA, label_w - 2 * PAD))
        else:
            lw = stringWidth(label, FN, FS_DATA)
            c.drawString(S2_DIV - PAD - lw, mid_y,
                         clip_text(label, FN, FS_DATA, label_w - 2 * PAD))

        if va == "L":
            c.drawString(S2_DIV + PAD, mid_y,
                         clip_text(val, FN, FS_DATA, val_w - 2 * PAD))
        else:
            vw = stringWidth(val, FN, FS_DATA)
            c.drawString(S2_X + S2_W - PAD - vw, mid_y,
                         clip_text(val, FN, FS_DATA, val_w - 2 * PAD))

    # Footer rows
    foot_label_w = S2_FOOT_DIV - S2_X
    c.setFont(FN, FS_DATA)
    for ri, label in enumerate(["Company:", "Name:", "Date:"]):
        row_bot = s2_title_bot - (s2_data_rows + ri + 1) * ROW_H
        mid_y   = row_bot + (ROW_H - FS_DATA) / 2
        c.drawString(S2_X + PAD, mid_y,
                     clip_text(label, FB, FS_DATA, foot_label_w - 2 * PAD))

    c.setFillColor(black)