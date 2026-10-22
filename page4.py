# page4.py — Page 4 content: Bill of Materials (tank components).

from reportlab.lib.colors import black, HexColor
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A3, landscape

# ── Shared geometry (mirrors main.py) ─────────────────────────────────────────
PW, PH   = landscape(A3)
IM       = 10 * mm
IX0      = IM;   IX1 = PW - IM;   IW = IX1 - IX0
IY1      = PH - IM
TBAR_TOP = IM + 45 * mm + 6 * mm

FN, FB = "Helvetica", "Helvetica-Bold"
GREY   = HexColor("#888888")
RULE   = HexColor("#DDDDDD")

# Item | Category | Quantity | Unit
COL_PROPS = [0.45, 0.25, 0.15, 0.15]
HEADERS   = ["Item", "Category", "Quantity", "Unit"]


def draw_page4_components(c, components, project_name=""):
    """components: list of {"item", "category", "quantity", "unit"}."""
    PAD    = 6 * mm
    HEAD_H = 16 * mm
    HDR_H  = 10 * mm

    x0, w = IX0 + 12 * mm, IW - 24 * mm
    top   = IY1 - 12 * mm

    c.setFillColor(black)
    c.setFont(FB, 18)
    c.drawString(x0, top - 18, "Bill of Materials")

    card_top = top - 34
    n        = max(len(components), 1)
    row_h    = min(12 * mm, (card_top - TBAR_TOP - 12 * mm - HEAD_H - HDR_H) / n)
    card_h   = HEAD_H + HDR_H + n * row_h + 4 * mm

    c.setStrokeColor(RULE)
    c.setLineWidth(0.8)
    c.roundRect(x0, card_top - card_h, w, card_h, 4)

    c.setFillColor(black)
    c.setFont(FB, 12)
    c.drawString(x0 + PAD, card_top - 7 * mm, project_name)
    c.setFont(FN, 8)
    c.setFillColor(GREY)
    c.drawString(x0 + PAD, card_top - 12 * mm, f"{len(components)} line items")
    c.line(x0, card_top - HEAD_H, x0 + w, card_top - HEAD_H)

    tx   = x0 + PAD
    tw   = w - 2 * PAD
    cols = [tx]
    for p in COL_PROPS:
        cols.append(cols[-1] + tw * p)

    # Header row (Quantity is right-aligned, like the app's BOM table)
    hdr_top = card_top - HEAD_H
    hdr_y   = hdr_top - HDR_H / 2 - 3
    c.setFillColor(black)
    c.setFont(FB, 9)
    for i, h in enumerate(HEADERS):
        if h == "Quantity":
            c.drawRightString(cols[i + 1] - PAD, hdr_y, h)
        else:
            c.drawString(cols[i] + 2 * mm, hdr_y, h)
    c.setStrokeColor(RULE)
    c.line(tx, hdr_top - HDR_H, tx + tw, hdr_top - HDR_H)

    # Data rows
    c.setFont(FN, 10)
    for r, comp in enumerate(components):
        row_top = hdr_top - HDR_H - r * row_h
        row_bot = row_top - row_h
        mid_y   = row_bot + row_h / 2 - 3.5

        c.setFillColor(black)
        c.setFont(FN, 10)
        c.drawString(cols[0] + 2 * mm, mid_y, str(comp.get("item", "")))
        c.drawString(cols[1] + 2 * mm, mid_y, str(comp.get("category", "")))
        c.drawRightString(cols[3] - PAD, mid_y, str(comp.get("quantity", "")))
        c.drawString(cols[3] + 2 * mm, mid_y, str(comp.get("unit", "")))

        c.setStrokeColor(RULE)
        c.line(tx, row_bot, tx + tw, row_bot)
