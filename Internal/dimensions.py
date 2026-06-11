from math import atan2, cos, sin


# =====================================================
# ARROW
# =====================================================

def draw_arrow(c, x1, y1, x2, y2, size=4):

    c.line(x1, y1, x2, y2)

    angle = atan2(y2 - y1, x2 - x1)

    a1 = angle + 2.7
    a2 = angle - 2.7

    c.line(
        x2,
        y2,
        x2 + size * cos(a1),
        y2 + size * sin(a1)
    )

    c.line(
        x2,
        y2,
        x2 + size * cos(a2),
        y2 + size * sin(a2)
    )


# =====================================================
# HORIZONTAL DIMENSION
# =====================================================
def draw_dimension_horizontal(
    c,
    x1,
    x2,
    y,
    text,
    ext_start=None
):

    # extension lines
    if ext_start is not None:

        c.line(x1, ext_start, x1, y)
        c.line(x2, ext_start, x2, y)

    # dimension line
    c.line(x1, y, x2, y)

    draw_arrow(c, x1, y, x2, y)
    draw_arrow(c, x2, y, x1, y)

    c.setFont("Helvetica", 7)

    c.drawCentredString(
        (x1 + x2) / 2,
        y + 5,
        str(text)
    )


# =====================================================
# VERTICAL DIMENSION
# =====================================================
def draw_dimension_vertical(
    c,
    x,
    y1,
    y2,
    text,
    ext_start=None,
    ext_end=None
):

    # extension lines from tank border
    if ext_start is not None:
        c.line(ext_start, y1, x, y1)

    if ext_end is not None:
        c.line(ext_end, y2, x, y2)

    # dimension line
    c.line(x, y1, x, y2)

    # arrows
    draw_arrow(c, x, y1, x, y2)
    draw_arrow(c, x, y2, x, y1)

    # text
    c.saveState()

    text_y = (y1 + y2) / 2

    c.translate(x - 12, text_y)
    c.rotate(90)

    c.setFont("Helvetica", 7)

    c.drawCentredString(
        0,
        0,
        str(text)
    )

    c.restoreState()