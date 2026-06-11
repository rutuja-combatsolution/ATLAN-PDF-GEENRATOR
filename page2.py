"""
page2.py

Page 2 content: full-bleed isometric image filling the entire drawing area
(above the tolerance bar, inside the inner border).
Falls back to a visible placeholder box if the image file is not found.
"""

from reportlab.lib.colors import black, HexColor
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A3, landscape

import os

# ── Shared geometry (mirrors main.py) ─────────────────────────────────────────
PW, PH   = landscape(A3)
IM       = 10 * mm
IX0      = IM;   IX1 = PW - IM;   IW  = IX1 - IX0
IY0      = IM;   IY1 = PH - IM
TBAR_H   = 6 * mm
TB_H     = 45 * mm
TBAR_BOT = IY0 + TB_H
TBAR_TOP = TBAR_BOT + TBAR_H


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2 – ISOMETRIC IMAGE
# ═══════════════════════════════════════════════════════════════════════════════

def draw_page2_image(c, image_path):
    """
    Draw the isometric image on page 2, filling the full drawing area
    (between the inner border top and the tolerance bar top, edge-to-edge).
    Shows a placeholder grey box if the file is not found.
    """
    draw_x = IX0
    draw_y = TBAR_TOP
    draw_w = IW
    draw_h = IY1 - TBAR_TOP

    if os.path.isfile(image_path):
        c.drawImage(
            image_path,
            draw_x, draw_y,
            width=draw_w, height=draw_h,
            preserveAspectRatio=True,
            anchor="c",
            mask="auto",
        )
    else:
        # Placeholder
        c.setStrokeColor(black)
        c.setLineWidth(1)
        c.rect(draw_x, draw_y, draw_w, draw_h, stroke=1, fill=0)
        c.setFont("Helvetica", 14)
        c.setFillColor(HexColor("#AAAAAA"))
        c.drawCentredString(
            draw_x + draw_w / 2,
            draw_y + draw_h / 2,
            f"Image not found: {image_path}"
        )
        c.setFillColor(black)
