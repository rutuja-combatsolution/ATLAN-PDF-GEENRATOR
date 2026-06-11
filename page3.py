# page3.py — Page 3 content: cross-section design image + spec annotation text.

import os

from reportlab.lib.colors import black
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase.pdfmetrics import stringWidth

PW, PH   = landscape(A3)
IM       = 10 * mm
IX0      = IM;   IX1 = PW - IM;   IW  = IX1 - IX0
IY0      = IM;   IY1 = PH - IM
TBAR_H   = 6 * mm
TB_H     = 45 * mm
TBAR_BOT = IY0 + TB_H
TBAR_TOP = TBAR_BOT + TBAR_H

FN  = "Helvetica"
FB  = "Helvetica-Bold"
PAD = 1.0 * mm


# ─────────────────────────────────────────────────────────────────────────────
# Word-wrap helper: breaks `text` into lines that fit within `max_w` at the
# given font/size. Returns a list of strings.
# ─────────────────────────────────────────────────────────────────────────────
def _wrap(text, font, size, max_w):
    words  = text.split()
    lines  = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        if stringWidth(test, font, size) <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [text]


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – DESIGN IMAGE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_page3_image(c, image_path=""):

    w = IW * 0.95
    h = (IY1 - TBAR_TOP) * 0.60

    x = IX0 + (IW - w) / 2
    y = IY1 - h - 5 * mm

    if os.path.isfile(image_path):
        c.drawImage(
            image_path,
            x, y,
            width=w, height=h,
            preserveAspectRatio=True,
            mask='auto'
        )


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3 – ANNOTATION TEXT
# ═══════════════════════════════════════════════════════════════════════════════

def draw_page3_annotations(c):
    DRAW_BOT = TBAR_TOP
    DRAW_H   = IY1 - DRAW_BOT

    LEFT_X  = IX0 + 7 * mm
    RIGHT_X = IX0 + IW * 0.55

    # Column widths — used for word-wrapping
    COL_W_LEFT  = (IX0 + IW * 0.55) - LEFT_X  - 4 * mm   # up to right col start
    COL_W_RIGHT = IX1 - RIGHT_X - 4 * mm                  # up to right border

    TEXT_START_Y = DRAW_BOT + DRAW_H * 0.30
    TEXT_BOT     = DRAW_BOT + 2 * mm

    # FIX: header 9pt (12pt was too large — overran column), body 8pt
    FS_HDR   = 9.0
    FS_BODY  = 8.0
    LEAD     = FS_BODY * 1.30    # body line leading
    HDR_LEAD = FS_HDR  * 1.50   # gap consumed after header baseline
    SEC_GAP  = 5.0               # extra gap between sections

    # Each body item is now ONE complete sentence — _wrap() handles line breaks
    left_sections = [
        ("FINAL BACKFILL", [
            "Depth: 500mm minimum",
            "Compaction: To 95% MDD minimum - Compact in 100mm layers",
            "Material Shape: Angular",
            "Size: Not larger than 20mm diameter",
            "Consistency: Free of lumps, debris and sharp objects that could puncture the geotextile",
            "Applicability: Stone, road-base or compacted granular material (non-cohesive) is acceptable if it meets these requirements. In NO case shall clays/cohesive soils be used. Ensure that any site specifications are considered for pavement make-up",
        ]),
        ("INITIAL BACKFILL", [
            "Depth: 100mm",
            "Compaction: 300kg Walk Behind Reversible Compactor",
            "Material Shape: Sand or crushed rock",
            "Size: Not larger than 20mm diameter",
            "Consistency: Free of lumps, debris and sharp objects that could puncture the geotextile",
            "Applicability: Clean washed Sand with no clay or foreign particles. In NO case shall clays/cohesive soils be used",
        ]),
    ]

    right_sections = [
        ("SIDES BACKFILL", [
            "Width: 500-600mm (each side) or as required onsite",
            "Compaction: To 95% MDD minimum - Compact in layers",
            "Material Shape: Angular",
            "Size: Not larger than 20mm diameter",
            "Consistency: Free of lumps, debris and sharp objects that could puncture the geotextile",
            "Applicability: Stone or sand is acceptable if it meets these requirements. In NO case shall clays/cohesive soils be used",
        ]),
        ("BASE / BEDDING", [
            "Depth: 50mm-100mm",
            "Compaction: To 95% MDD minimum",
            "Material Shape: Angular",
            "Size: Not larger than 20mm diameter",
            "Consistency: Free of lumps, debris and sharp objects that could puncture the geotextile",
            "Applicability: Stone or sand is acceptable if it meets these requirements. In NO case shall clays/cohesive soils be used",
        ]),
        ("SUBGRADE", [
            "Compaction: To 100kPa",
        ]),
    ]

    def render_column(col_x, sections, col_w):
        cur_y = TEXT_START_Y
        for hdr, lines in sections:
            if cur_y < TEXT_BOT:
                break

            # Section header — bold, no wrap needed (short)
            c.setFont(FB, FS_HDR)
            c.setFillColor(black)
            c.drawString(col_x, cur_y, hdr)
            cur_y -= HDR_LEAD

            # Body lines — wrap each entry to column width
            c.setFont(FN, FS_BODY)
            for entry in lines:
                wrapped = _wrap(entry, FN, FS_BODY, col_w)
                for wline in wrapped:
                    if cur_y < TEXT_BOT:
                        break
                    c.drawString(col_x, cur_y, wline)
                    cur_y -= LEAD
                if cur_y < TEXT_BOT:
                    break

            cur_y -= SEC_GAP   # extra space between sections

    render_column(LEFT_X,  left_sections,  COL_W_LEFT)
    render_column(RIGHT_X, right_sections, COL_W_RIGHT)
