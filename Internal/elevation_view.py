# ==========================================================
# elevation_view.py
# ==========================================================

from reportlab.lib import colors
from reportlab.lib.units import mm

from Internal.plan_view import (
    draw_dimension_horizontal,
    draw_dimension_vertical,
    draw_flow_arrow,
)
 
# ======================================================
# ATLANCUBE SIDE ELEVATION PANEL
# ======================================================

def draw_side_panel(c, x, y, w, h):

    c.saveState()

    mid_y = y + (h / 2)

    # ---------------------------------
    # OUTER PANEL
    # ---------------------------------

    # PANEL BORDER

    c.setLineWidth(3)

    c.rect(
        x,
        y,
        w,
        h,
        stroke=1,
        fill=0
    )

    
    # ---------------------------------
    # 3 CHAMBERS
    # ---------------------------------

    gap = w * 0.18

    bay_w = (
        w - (2 * gap)
    ) / 3

    bay1_x = x
    bay2_x = x + bay_w + gap
    bay3_x = x + (2 * bay_w) + (2 * gap)

     

    # ---------------------------------
    # BOLD ZIG-ZAGS
    # ---------------------------------

    c.setLineWidth(8)

    for bx in [
        bay1_x,
        bay2_x,
        bay3_x
    ]:

        rib_offset = bay_w * 0.15
        neck_width = bay_w * 0.12

        left = bx + rib_offset
        right = bx + bay_w - rib_offset

        center_l = (
            bx
            + (bay_w / 2)
            - neck_width
        )

        center_r = (
            bx
            + (bay_w / 2)
            + neck_width
        )

        # upper zig-zag

        c.line(
            left,
            y + h,
            center_l,
            mid_y
        )

        c.line(
            right,
            y + h,
            center_r,
            mid_y
        )

        # lower zig-zag

        c.line(
            left,
            y,
            center_l,
            mid_y
        )

        c.line(
            right,
            y,
            center_r,
            mid_y
        )

    c.restoreState()
def draw_elevation_view(
    c,
    data,
    x=140,
    y=150
):

    # ======================================================
    # SCALE
    # ======================================================

    available_w = 220 * mm
    available_h = 110 * mm

    # ======================================================
    # REAL TANK HEIGHT
    # ======================================================

    real_tank_height = data["height"]

    # ======================================================
    # SCALE
    # ======================================================

    scale_x = (
        available_w
        / data["length"]
    )

    # Use length-based scaling so height grows dynamically
    scale = scale_x

    tank_len = (
        data["length"]
        * scale
    )

    tank_ht = (
        real_tank_height
        * scale
    )

    # ======================================================
    # PANEL GRID
    # ======================================================

    cols = data["length_panels"]
    rows = data["levels"]

    cell_w = tank_len / cols
    cell_h = tank_ht / rows

    # ======================================================
    # TITLE
    # ======================================================

    title = "ELEVATION VIEW"

    c.setFont(
        "Helvetica-Bold",
        20
    )

    text_width = c.stringWidth(
        title,
        "Helvetica-Bold",
        20
    )

    # Center of tank
    title_x = x + (tank_len / 2) - (text_width / 2)
    title_y = y - 70

    c.drawString(
        title_x,
        title_y,
        title
    )

    # Underline

    c.setLineWidth(1.5)

    c.line(
        title_x,
        title_y - 3,
        title_x + text_width,
        title_y - 3
    )

    # ======================================================
    # OUTER BORDER
    # ======================================================

    c.saveState()

    c.setLineWidth(2)

    c.rect(
        x,
        y,
        tank_len,
        tank_ht
    )

    c.restoreState()

    # ======================================================
    # REDRAW PANELS ON TOP
    # ======================================================

    for col in range(cols):

        px = x + (col * cell_w)

        for row in range(rows):

            py = y + (row * cell_h)

            draw_side_panel(
                c,
                px,
                py,
                cell_w,
                cell_h
            )
    # ======================================================
    # HEAVY GRID LINES
    # ======================================================

    c.setStrokeColor(colors.black)
    c.setLineWidth(8)   # increase to 8 if needed

    # Vertical lines
    for col in range(1, cols):
        gx = x + (col * cell_w)

        c.line(
            gx,
            y,
            gx,
            y + tank_ht
        )

    # Horizontal lines
    for row in range(1, rows):
        gy = y + (row * cell_h)

        c.line(
            x,
            gy,
            x + tank_len,
            gy
        )
    # ======================================================
    # GEOFAB WRAP BORDER
    # ======================================================

    INNER_BLUE = 1      # almost on tank wall
    PINK = 7           # small gap
    OUTER_BLUE = 14      # small gap again

    TOP_EXT_PINK = 20
    TOP_EXT_BLUE = 25

    # ------------------------------------------
    # INNER BLUE BORDER (FULL TANK)
    # ------------------------------------------

    c.setStrokeColor(colors.blue)
    c.setLineWidth(3)
    c.setDash(30, 4)

    c.rect(
        x - INNER_BLUE,
        y - INNER_BLUE,
        tank_len + (INNER_BLUE * 2),
        tank_ht + (INNER_BLUE * 2),
        stroke=1,
        fill=0
    )
    c.setDash() 
    # ------------------------------------------
    # PINK BORDER
    # LEFT + BOTTOM + RIGHT ONLY
    # ------------------------------------------

    c.setStrokeColorRGB(1, 0, 1)

    pink_left = x - PINK
    pink_right = x + tank_len + PINK
    pink_bottom = y - PINK
    pink_top = y + tank_ht + TOP_EXT_PINK

    c.line(
        pink_left,
        pink_bottom,
        pink_left,
        pink_top
    )

    c.line(
        pink_left,
        pink_bottom,
        pink_right,
        pink_bottom
    )

    c.line(
        pink_right,
        pink_bottom,
        pink_right,
        pink_top
    )

    # ------------------------------------------
    # OUTER BLUE BORDER
    # LEFT + BOTTOM + RIGHT ONLY
    # ------------------------------------------

    c.setStrokeColor(colors.blue)
    c.setDash(30, 4)

    blue_left = x - OUTER_BLUE
    blue_right = x + tank_len + OUTER_BLUE
    blue_bottom = y - OUTER_BLUE
    blue_top = y + tank_ht + TOP_EXT_BLUE

    c.line(
        blue_left,
        blue_bottom,
        blue_left,
        blue_top
    )

    c.line(
        blue_left,
        blue_bottom,
        blue_right,
        blue_bottom
    )

    c.line(
        blue_right,
        blue_bottom,
        blue_right,
        blue_top
    )

    c.setDash()
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    # ======================================================
    # MANHOLES
    # ======================================================
    
    for mh in data.get("manholes", []):

        panel_x = mh.get(
            "panel_x",
            cols // 2
        )

        mx = (
            x
            + (panel_x * cell_w)
            + (cell_w / 2)
        )

        riser_w = 12
        riser_h = 35

        # Riser
        c.setFillColorRGB(0.60, 0.60, 0.60)
        c.rect(
            mx - (riser_w / 2),
            y + tank_ht,
            riser_w,
            riser_h,
            stroke=1,
            fill=1
        )

        # Lid 
        c.setLineWidth(2)
        c.setFillColorRGB(0.60, 0.60, 0.60)
        c.rect(
            mx - 9,
            y + tank_ht + riser_h,
            18,
            3,
            stroke=1,
            fill=1
        )

        c.setLineWidth(1)

        '''c.drawCentredString(
            mx,
            y + tank_ht + riser_h + 10,
            mh["id"]
        )'''

    
    # ======================================================
    # PIPES
    # ======================================================

    PIPE_EXTENSION = 30

    for pipe in data.get("pipes", []):

        side = pipe["side"].lower()

        # Elevation only shows LEFT and RIGHT wall pipes
        if side not in ["left", "right"]:
            continue

        layer = pipe.get("level", 0)

        pipe_y = (
            y
            + (layer * cell_h)
            + (cell_h / 2)
        )

        pipe_w = max(
            10,
            pipe.get("diameter", 375) / 35
        )

        c.setFillColorRGB(
            0.75,
            0.75,
            0.75
        )

        c.setStrokeColor(colors.black)
        c.setLineWidth(1.5)

        # ==========================================
        # LEFT SIDE PIPE
        # ==========================================

        if side == "left":

            pipe_x = x - PIPE_EXTENSION

            c.rect(
                pipe_x,
                pipe_y - (pipe_w / 2),
                PIPE_EXTENSION,
                pipe_w,
                stroke=1,
                fill=1
            )

            # centerline

            c.setStrokeColorRGB(
                0.60,
                0.60,
                0.60
            )

            c.setDash(3, 2)

            c.line(
                pipe_x,
                pipe_y,
                x,
                pipe_y
            )

            c.setDash()
            c.setStrokeColor(colors.black)

            # flow arrow

            draw_flow_arrow(
                c,
                x,
                pipe_y,
                "WEST",
                pipe.get("type", "INLET"),
                pipe_extension=22
            )

            label_x = pipe_x - 55
            label_y = pipe_y + 10

        # ==========================================
        # RIGHT SIDE PIPE
        # ==========================================

        else:

            pipe_x = x + tank_len

            c.rect(
                pipe_x,
                pipe_y - (pipe_w / 2),
                PIPE_EXTENSION,
                pipe_w,
                stroke=1,
                fill=1
            )

            # centerline

            c.setStrokeColorRGB(
                0.60,
                0.60,
                0.60
            )

            c.setDash(3, 2)

            c.line(
                pipe_x,
                pipe_y,
                pipe_x + PIPE_EXTENSION,
                pipe_y
            )

            c.setDash()
            c.setStrokeColor(colors.black)

            draw_flow_arrow(
                c,
                pipe_x,
                pipe_y,
                "EAST",
                pipe.get("type", "OUTLET"),
                pipe_extension=PIPE_EXTENSION
            )

            label_x = pipe_x + PIPE_EXTENSION + 10
            label_y = pipe_y + 10

        # ==========================================
        # LABEL
        # ==========================================

        c.setFont("Helvetica", 6)

        c.drawString(
            label_x,
            label_y,
            f"{pipe['id']} Ø{pipe['diameter']}"
        )

        c.setFillColor(colors.black)
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
    
    # ======================================================
    # OVERALL LENGTH DIMENSION
    # ======================================================

    draw_dimension_horizontal(
        c,
        x,
        x + tank_len,
        y - 40,
        f"{data['length']:.0f}"
    )

    # ======================================================
    # OVERALL HEIGHT DIMENSION
    # ======================================================

    draw_dimension_vertical(
        c,
        y,
        y + tank_ht,
        x - 50,
        f"{real_tank_height:.0f}"
    )

    # ======================================================
    # LEVEL TEXT
    # ======================================================

    c.setFont(
        "Helvetica",
        7
    )

    c.drawString(
        x + tank_len + 40,
        y + tank_ht,
        f"FSL {data['fsl']:.2f}"
    )

    c.drawString(
        x + tank_len + 40,
        y,
        f"BASE RL {data['base_rl']:.2f}"
    )