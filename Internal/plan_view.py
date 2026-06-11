# ==========================================================
# plan_view.py
# ==========================================================

from reportlab.lib import colors
from reportlab.lib.units import mm 


def draw_flow_arrow(
    c,
    center_x,
    center_y,
    side,
    flow_type,
    pipe_extension=18,
):

    from reportlab.lib import colors

    side = side.upper()
    flow_type = flow_type.upper()

    # -----------------------------------------
    # Support old names
    # -----------------------------------------

    if side == "TOP":
        side = "NORTH"
    elif side == "BOTTOM":
        side = "SOUTH"
    elif side == "LEFT":
        side = "WEST"
    elif side == "RIGHT":
        side = "EAST"

    # -----------------------------------------
    # Style
    # -----------------------------------------

    if flow_type == "INLET":
        c.setStrokeColor(colors.red)
    else:
        c.setStrokeColor(colors.blue)

    c.setLineWidth(1)

    ARROW_GAP  = 8      # gap from pipe
    ARROW_LEN  = 20     # arrow length
    ARROW_HALF = 5     # half height
    SHAFT_EXT  = 6     # shaft extension
    TIP_EXT = 3

    # =====================================================
    # EAST
    # =====================================================

    if side == "EAST":

        y = center_y

        arrow_back_x = (
            center_x
            + pipe_extension
            + ARROW_GAP
        )

        arrow_tip_x = (
            arrow_back_x
            + ARROW_LEN
        )
 
        # center shaft + tail
        
        c.line(
            arrow_back_x - SHAFT_EXT,
            y,
            arrow_tip_x + TIP_EXT,
            y
        )

        # upper edge
        c.line(
            arrow_back_x,
            y + ARROW_HALF,
            arrow_tip_x,
            y
        )

        # lower edge
        c.line(
            arrow_back_x,
            y - ARROW_HALF,
            arrow_tip_x,
            y
        )

        # rear vertical
        c.line(
            arrow_back_x,
            y - ARROW_HALF,
            arrow_back_x,
            y + ARROW_HALF
        )

    # =====================================================
    # WEST
    # =====================================================

    elif side == "WEST":

        y = center_y

        arrow_tip_x = (
            center_x
            - pipe_extension
            - ARROW_GAP
        )
        
        

        arrow_back_x = (
            arrow_tip_x
            - ARROW_LEN
        )

        # center shaft
        c.line(
            arrow_back_x - SHAFT_EXT,
            y,
           arrow_tip_x + TIP_EXT,
            y
        )

        # arrow body
        c.line(
            arrow_back_x,
            y + ARROW_HALF,
            arrow_tip_x,
            y
        )

        c.line(
            arrow_back_x,
            y - ARROW_HALF,
            arrow_tip_x,
            y
        )

        c.line(
            arrow_back_x,
            y - ARROW_HALF,
            arrow_back_x,
            y + ARROW_HALF
        )

    # =====================================================
    # NORTH
    # =====================================================

    elif side == "NORTH":

        x = center_x

        if flow_type == "INLET":

            tip_y = center_y + pipe_extension + ARROW_GAP
            tail_y = tip_y + ARROW_LEN

        else:

            tail_y = center_y + pipe_extension + ARROW_GAP
            tip_y = tail_y + ARROW_LEN

        
        
        c.line(
            x,
            tail_y - SHAFT_EXT,
            x,
            tip_y + TIP_EXT
        )

        c.line(
            x - ARROW_HALF,
            tail_y,
            x,
            tip_y
        )

        c.line(
            x + ARROW_HALF,
            tail_y,
            x,
            tip_y
        )

        c.line(
            x - ARROW_HALF,
            tail_y,
            x + ARROW_HALF,
            tail_y
        )

    # =====================================================
    # SOUTH
    # =====================================================

    elif side == "SOUTH":

        x = center_x

        if flow_type == "INLET":

            tip_y = center_y - pipe_extension - ARROW_GAP
            tail_y = tip_y - ARROW_LEN

        else:

            tail_y = center_y - pipe_extension - ARROW_GAP
            tip_y = tail_y - ARROW_LEN

        c.line(
            x,
            tail_y + SHAFT_EXT,
            x,
            tip_y - TIP_EXT
        )

        c.line(
            x - ARROW_HALF,
            tail_y,
            x,
            tip_y
        )

        c.line(
            x + ARROW_HALF,
            tail_y,
            x,
            tip_y
        )

        c.line(
            x - ARROW_HALF,
            tail_y,
            x + ARROW_HALF,
            tail_y
        )

    # -----------------------------------------
    # Restore defaults
    # -----------------------------------------

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    
    
# ==========================================================
# ATLANCUBE PANEL GRID
# ==========================================================

def draw_panel_grid(
    c,
    x,
    y,
    grid_len,
    grid_wid,
    cols,
    rows
):

    cell_w = grid_len / cols
    cell_h = grid_wid / rows

    c.setStrokeColor(colors.black)

    for row in range(rows):

        for col in range(cols):

            px = x + (col * cell_w)
            py = y + (row * cell_h)

            # =====================================
            # OUTER CUBE
            # =====================================

            c.setLineWidth(1.5)

            c.rect(
                px,
                py,
                cell_w,
                cell_h,
                stroke=1,
                fill=0
            )

            # =====================================
            # 3 x 3 INTERNAL CELL PATTERN
            # =====================================

            gap = min(cell_w, cell_h) * 0.13

            sq_w = (cell_w - (2 * gap)) / 3
            sq_h = (cell_h - (2 * gap)) / 3

            c.setLineWidth(3)

            for r in range(3):
                for cc in range(3):

                    sx = px + (cc * (sq_w + gap))
                    sy = py + (r * (sq_h + gap))

                    corner_radius = min(
                        sq_w,
                        sq_h
                    ) * 0.03

                    c.roundRect(
                        sx,
                        sy,
                        sq_w,
                        sq_h,
                        corner_radius,
                        stroke=1,
                        fill=0
                    )

                    # Center vertical

                    c.line(
                        sx + (sq_w / 2),
                        sy,
                        sx + (sq_w / 2),
                        sy + sq_h
                    )

                    # Center horizontal

                    c.line(
                        sx,
                        sy + (sq_h / 2),
                        sx + sq_w,
                        sy + (sq_h / 2)
                    )

# ==========================================================
# DRAW ROUNDED RECTANGLE
# ==========================================================

def draw_round_rect(c, x, y, w, h, radius):

    c.roundRect(
        x,
        y,
        w,
        h,
        radius,
        stroke=1,
        fill=0
    )


# ==========================================================
# HELPER
# ==========================================================

def get_position_from_offset(
    offset_m,
    tank_length_mm,
    tank_length_drawn
):

    offset_mm = offset_m * 1000

    return (
        offset_mm /
        tank_length_mm
    ) * tank_length_drawn

def draw_filled_arrow(c, tip_x, tip_y, direction, size=6):

    if direction == "LEFT":

        pts = [
                (tip_x, tip_y),
                (tip_x - size, tip_y + size/2),
                (tip_x - size, tip_y - size/2),
            ]

    elif direction == "RIGHT":

        pts = [
            (tip_x, tip_y),
            (tip_x + size, tip_y + size/2),
            (tip_x + size, tip_y - size/2),
        ]

    elif direction == "UP":

        pts = [
                (tip_x, tip_y),
                (tip_x - size/2, tip_y + size),
                (tip_x + size/2, tip_y + size),
            ]

    elif direction == "DOWN":

        pts = [
            (tip_x, tip_y),
            (tip_x - size/2, tip_y - size),
            (tip_x + size/2, tip_y - size),
        ]

    p = c.beginPath()

    p.moveTo(*pts[0])
    p.lineTo(*pts[1])
    p.lineTo(*pts[2])
    p.close()

    c.drawPath(
        p,
        stroke=1,
        fill=1
    )

def draw_dimension_horizontal(c, x1, x2, y, text):

    c.setLineWidth(0.6)

    EXT = 6
    ARROW = 3

    # extension lines
    c.line(x1, y, x1, y + EXT)
    c.line(x2, y, x2, y + EXT)

    # dimension line
    c.line(x1, y, x2, y)

    draw_filled_arrow(
        c,
        x1,
        y,
        "RIGHT",
        5
    )

    draw_filled_arrow(
        c,
        x2,
        y,
        "LEFT",
        5
    )

    # text ON dimension line
    c.setFont("Helvetica", 6)

    text_x = (x1 + x2) / 2

    # white mask behind text
    txt_w = c.stringWidth(str(text), "Helvetica", 6)

    c.setFillColor(colors.white)
    c.rect(
        text_x - (txt_w / 2) - 2,
        y - 3,
        txt_w + 4,
        6,
        stroke=0,
        fill=1
    )

    c.setFillColor(colors.black)

    c.drawCentredString(
        text_x,
        y - 2,
        str(text)
    )
    
    
def draw_dimension_vertical(c, y1, y2, x, text):

    c.setLineWidth(0.6)

    EXT = 6
    ARROW = 3

    # extension lines
    c.line(x, y1, x + EXT, y1)
    c.line(x, y2, x + EXT, y2)

    # dimension line
    c.line(x, y1, x, y2)

    draw_filled_arrow(
        c,
        x,
        y1,
        "UP",
        5
    )

    draw_filled_arrow(
        c,
        x,
        y2,
        "DOWN",
        5
    )

    c.saveState()

    c.translate(
        x - 2,
        (y1 + y2) / 2
    )

    c.rotate(90)

    txt_w = c.stringWidth(str(text), "Helvetica", 6)

    c.setFillColor(colors.white)

    c.rect(
        -txt_w / 2 - 2,
        -3,
        txt_w + 4,
        6,
        stroke=0,
        fill=1
    )

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 6)

    c.drawCentredString(
        0,
        -2,
        str(text)
    )

    c.restoreState()
    
    
# ==========================================================
# MINIMUM CLEARANCE DIMENSION
# ==========================================================

def draw_min_clearance_horizontal(
    c,
    x1,
    x2,
    y
):

    c.setLineWidth(0.8)

    # extension lines
    c.line(x1, y - 10, x1, y + 10)
    c.line(x2, y - 10, x2, y + 10)

    # dimension line
    c.line(x1, y, x2, y)

    draw_filled_arrow(c, x1, y, "RIGHT", 6)
    draw_filled_arrow(c, x2, y, "LEFT", 6)

    text_x = (x1 + x2) / 2

    c.setFont("Helvetica-Bold", 6)

    c.drawCentredString(
        text_x,
        y + 12,
        "MIN. 500"
    )

     


def draw_min_clearance_vertical(
    c,
    y1,
    y2,
    x
):

    c.setLineWidth(0.8)

    # extension lines
    c.line(x - 10, y1, x + 10, y1)
    c.line(x - 10, y2, x + 10, y2)

    # dimension line
    c.line(x, y1, x, y2)

    draw_filled_arrow(c, x, y1, "UP", 6)
    draw_filled_arrow(c, x, y2, "DOWN", 6)

    c.saveState()

    text_x = x - 10
    text_y = (y1 + y2) / 2

    c.translate(text_x, text_y)

    c.rotate(90)

    c.setFont("Helvetica-Bold", 7)

    # place text above and below center
    c.drawCentredString(
        5,
        0,
        "MIN. 500"
    )

     

    c.restoreState()
# ==========================================================
# PLAN VIEW
# ==========================================================

def draw_plan_view(c, data, x=70, y=450):

    # ======================================================
    # SCALE
    # ======================================================
    
    available_w = 220 * mm
    available_h = 110 * mm

    scale_x = available_w / data["length"]
    scale_y = available_h / data["width"]

    scale = min(
        scale_x,
        scale_y
    )

    tank_len = data["length"] * scale
    tank_wid = data["width"] * scale
    
    # ======================================================
    # TITLE
    # ======================================================

    title = "PLAN VIEW"

    c.setFont(
        "Helvetica-Bold",
        20
    )

    text_width = c.stringWidth(
        title,
        "Helvetica-Bold",
        20
    )

    # Center over tank
    center_x = x + (tank_len / 2)

    # Position above tank
    title_y = y - 50

    c.drawCentredString(
        center_x,
        title_y,
        title
    )

    # Underline
    c.setLineWidth(1.5)

    c.line(
        center_x - (text_width / 2),
        title_y - 3,
        center_x + (text_width / 2),
        title_y - 3
    )

    # ======================================================
    # PANEL GRID (ACTUAL TANK)
    # ======================================================

    cols = data["length_panels"]
    rows = data["width_panels"]
    
    black1_offset = 4
    black2_offset = 4

    grid_x = x
    grid_y = y

    grid_len = tank_len
    grid_wid = tank_wid


    black1_offset = 4
    black2_offset = 4

    # Total offset from outer tank edge
    tank_offset =  4

    # Actual cube grid area
    grid_x = x + tank_offset
    grid_y = y + tank_offset

    grid_len = tank_len - (tank_offset * 2)
    grid_wid = tank_wid - (tank_offset * 2)

    # Cube size

    cell_w = grid_len / cols
    cell_h = grid_wid / rows

    # ======================================================
    # ATLANCUBE GRID
    # ======================================================

    draw_panel_grid(
        c,
        grid_x,
        grid_y,
        grid_len,
        grid_wid,
        cols,
        rows
    )

    # ======================================================
    # BORDERS
    # ======================================================

    corner_radius = 8

    # Excavation clearance drives red border
    red_offset = (
        data["excavation_clearance"]
        * scale * 0.5
    )

    # ------------------------------------------
    # BLACK BORDER #1
    # ------------------------------------------

    c.setStrokeColor(colors.black)
    c.setLineWidth(2.5)

    draw_round_rect(
        c,
        x - black1_offset,
        y - black1_offset,
        tank_len + (2 * black1_offset),
        tank_wid + (2 * black1_offset),
        corner_radius
    )

    # ------------------------------------------
    # BLACK BORDER #2
    # ------------------------------------------

    c.setLineWidth(2.5)

    draw_round_rect(
        c,
        x - black1_offset - black2_offset,
        y - black1_offset - black2_offset,
        tank_len + (
            2 * (black1_offset + black2_offset)
        ),
        tank_wid + (
            2 * (black1_offset + black2_offset)
        ),
        corner_radius
    )

    # ------------------------------------------
    # RED EXCAVATION BORDER
    # ------------------------------------------

    c.setStrokeColor(colors.red)
    c.setLineWidth(2.0)

    c.rect(
        x - black1_offset - black2_offset - red_offset,
        y - black1_offset - black2_offset - red_offset,
        tank_len + (
            2 * (
                black1_offset +
                black2_offset +
                red_offset
            )
        ),
        tank_wid + (
            2 * (
                black1_offset +
                black2_offset +
                red_offset
            )
        ),
        stroke=1,
        fill=0
    )

    # Restore defaults
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    
    # ======================================================
    # MINIMUM 500 CLEARANCE DIMENSIONS
    # ======================================================

    red_left = (
        x
        - black1_offset
        - black2_offset
        - red_offset
    )

    red_right = (
        x
        + tank_len
        + black1_offset
        + black2_offset
        + red_offset
    )

    red_bottom = (
        y
        - black1_offset
        - black2_offset
        - red_offset
    )

    red_top = (
        y
        + tank_wid
        + black1_offset
        + black2_offset
        + red_offset
    )

    tank_left = x
    tank_right = x + tank_len
    tank_bottom = y
    tank_top = y + tank_wid


    # ------------------------------------------
    # TOP RIGHT CLEARANCE
    # ------------------------------------------

    draw_min_clearance_horizontal(
        c,
        tank_right,
        red_right,
        red_top + 18
    )

    # ------------------------------------------
    # TOP LEFT CLEARANCE
    # ------------------------------------------

    draw_min_clearance_horizontal(
        c,
        red_left,
        tank_left,
        red_top + 18
    )

    # ------------------------------------------
    # BOTTOM RIGHT CLEARANCE
    # ------------------------------------------

    draw_min_clearance_vertical(
        c,
        red_bottom,
        tank_bottom,
        red_right + 18
    )

    # ======================================================
    # STORAGE INFORMATION
    # ======================================================

    box_w = 180
    box_h = 80

    bx = (
        x
        + (tank_len / 2)
        - (box_w / 2)
    )

    by = (
        y
        + (tank_wid / 2)
        - (box_h / 2)
    )

    c.setFillColor(colors.white)

    c.rect(
        bx,
        by,
        box_w,
        box_h,
        stroke=1,
        fill=1
    )

    c.setFillColor(colors.black)

    info = [
        f"{data['length_panels']} CUBES x {data['width_panels']} CUBES",
        f"{data['levels']} LAYERS",
        f"STORAGE = {data['tank_storage']:.1f} m³",
        f"FSL = {data['fsl']:.2f}",
        f"BASE RL = {data['base_rl']:.2f}"
    ]

    yy = by + box_h - 15

    c.setFont(
        "Helvetica",
        8
    )

    for line in info:

        c.drawCentredString(
            bx + (box_w / 2),
            yy,
            line
        )

        yy -= 13


    horizontal_dims = []
    vertical_dims = []
    # ======================================================
    # MANHOLES
    # ======================================================

    for mh in data.get(
        "manholes",
        []
    ):

        offset_x = get_position_from_offset(
            mh["horizontal_offset"],
            data["length"],
            tank_len
        )

        mx = x + offset_x

        side = mh.get(
            "side",
            "top"
        ).lower()

        if side == "top":

            my = (
                y
                + tank_wid
                - (cell_h / 2)
            )

        elif side == "bottom":

            my = (
                y
                + (cell_h / 2)
            )

        else:

            my = (
                y
                + (tank_wid / 2)
            )

        c.circle(
            mx,
            my,
            10,
            stroke=1,
            fill=0
        )

        c.setFont(
            "Helvetica",
            7
        )

        c.drawCentredString(
            mx,
            my - 2,
            mh["label"]
        )

    # ======================================================
    # PIPES
    # ======================================================

    PIPE_EXTENSION = 30

    for pipe in data.get("pipes", []):

        side = pipe["side"].lower()

        # --------------------------------------------------
        # PIPE CUBE LOCATION
        # --------------------------------------------------

        cube_x = (
            grid_x
            + (pipe["panel_x"] * cell_w)
        )

        cube_y = (
            grid_y
            + (pipe["panel_y"] * cell_h)
        )

        cube_center_x = cube_x + (cell_w / 2)
        cube_center_y = cube_y + (cell_h / 2)
        
        if side in ["top", "bottom"]:

            offset_mm = (
                pipe["panel_x"] * data["panel_length"]
            ) + (data["panel_length"] / 2)

            horizontal_dims.append({
                "x": cube_center_x,
                "offset": offset_mm
            })

        elif side in ["left", "right"]:

            offset_mm = (
                pipe["panel_y"] * data["panel_width"]
            ) + (data["panel_width"] / 2)

            vertical_dims.append({
                "y": cube_center_y,
                "offset": offset_mm
            })
        
        # ==========================================
        # PIPE DISTANCES
        # ==========================================

        distance_from_left_mm = (
            pipe["panel_x"] * data["panel_length"]
        )

        distance_from_right_mm = (
            data["length"]
            - (
                (pipe["panel_x"] + 1)
                * data["panel_length"]
            )
        )

        distance_from_bottom_mm = (
            pipe["panel_y"] * data["panel_width"]
        )

        distance_from_top_mm = (
            data["width"]
            - (
                (pipe["panel_y"] + 1)
                * data["panel_width"]
            )
        )

        '''# --------------------------------------------------
        # REFERENCE PIT
        # --------------------------------------------------

        pit_size = min(
            cell_w,
            cell_h
        ) * 0.70

        pit_x = cube_x + (
            (cell_w - pit_size) / 2
        )

        pit_y = cube_y + (
            (cell_h - pit_size) / 2
        )

        c.setFillColor(colors.white)

        c.rect(
            pit_x,
            pit_y,
            pit_size,
            pit_size,
            stroke=1,
            fill=1
        )

        c.setLineWidth(1.5)

        c.rect(
            pit_x,
            pit_y,
            pit_size,
            pit_size,
            stroke=1,
            fill=0
        )'''

        # --------------------------------------------------
        # PIPE SIZE
        # --------------------------------------------------

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

        # --------------------------------------------------
        # LEFT SIDE PIPE
        # --------------------------------------------------

        if side == "left":

            pipe_x = (
                grid_x
                - PIPE_EXTENSION
            )

            pipe_y = (
                cube_center_y
                - (pipe_w / 2)
            )

            pipe_len = (
                cube_x
                - pipe_x
            )

            c.rect(
                pipe_x,
                pipe_y,
                pipe_len,
                pipe_w,
                stroke=1,
                fill=1
            )

            # FLOW ARROW
            draw_flow_arrow(
                c,
                grid_x,
                cube_center_y,
                "WEST",
                pipe.get("type", "INLET"),
                pipe_extension=PIPE_EXTENSION
            )

            
            px = pipe_x
            py = cube_center_y

        # --------------------------------------------------
        # RIGHT SIDE PIPE
        # --------------------------------------------------

        elif side == "right":

            pipe_x = (
                cube_x
                + cell_w
            )

            pipe_y = (
                cube_center_y
                - (pipe_w / 2)
            )

            pipe_len = (
                (
                    grid_x
                    + grid_len
                    + PIPE_EXTENSION
                )
                - pipe_x
            )

            c.rect(
                pipe_x,
                pipe_y,
                pipe_len,
                pipe_w,
                stroke=1,
                fill=1
            )
            
            
            
            draw_flow_arrow(
            c,
            pipe_x + pipe_len,
            cube_center_y,
            "EAST",
            pipe.get("type", "OUTLET"),
            pipe_extension=0
        )

            px = (
                grid_x
                + grid_len
                + PIPE_EXTENSION
            )

            py = cube_center_y

        # --------------------------------------------------
        # TOP SIDE PIPE
        # --------------------------------------------------

        elif side == "top":

            pipe_x = (
                cube_center_x
                - (pipe_w / 2)
            )

            pipe_y = (
                cube_y
                + cell_h
            )

            pipe_h = (
                (
                    grid_y
                    + grid_wid
                    + PIPE_EXTENSION
                )
                - pipe_y
            )

            c.rect(
                pipe_x,
                pipe_y,
                pipe_w,
                pipe_h,
                stroke=1,
                fill=1
            )

            draw_flow_arrow(
                c,
                cube_center_x,
                grid_y + grid_wid,
                "NORTH",
                pipe.get("type", "INLET"),
                pipe_extension=PIPE_EXTENSION
            )
            px = cube_center_x

            py = (
                grid_y
                + grid_wid
                + PIPE_EXTENSION
            )

        # --------------------------------------------------
        # BOTTOM SIDE PIPE
        # --------------------------------------------------

        elif side == "bottom":

            pipe_x = (
                cube_center_x
                - (pipe_w / 2)
            )

            pipe_y = (
                grid_y
                - PIPE_EXTENSION
            )

            pipe_h = (
                cube_y
                - pipe_y
            )

            c.rect(
                pipe_x,
                pipe_y,
                pipe_w,
                pipe_h,
                stroke=1,
                fill=1
            )
            
            draw_flow_arrow(
                c,
                cube_center_x,
                grid_y,
                "SOUTH",
                pipe.get("type", "OUTLET"),
                pipe_extension=PIPE_EXTENSION
            )

            px = cube_center_x
            py = pipe_y

        else:
            continue

        # --------------------------------------------------
        # CENTER LINE
        # --------------------------------------------------

        c.setStrokeColorRGB(
            0.60,
            0.60,
            0.60
        )

        c.setDash(3, 2)

        if side in ["left", "right"]:

            c.line(
                pipe_x,
                cube_center_y,
                pipe_x + pipe_len,
                cube_center_y
            )

        else:

            c.line(
                cube_center_x,
                pipe_y,
                cube_center_x,
                pipe_y + pipe_h
            )

        c.setDash()
        c.setStrokeColor(colors.black)

        '''# ==========================================
        # DISTANCE TEXT
        # ==========================================

        c.setFont("Helvetica", 6)

        if side == "left":

            c.drawString(
                pipe_x - 40,
                cube_center_y + 18,
                f"{distance_from_bottom_mm:.0f}"
            )

        elif side == "right":

            c.drawString(
                pipe_x + pipe_len + 5,
                cube_center_y + 18,
                f"{distance_from_bottom_mm:.0f}"
            )

        elif side == "top":

            c.drawString(
                cube_center_x + 10,
                pipe_y + pipe_h + 5,
                f"{distance_from_left_mm:.0f}"
            )

        elif side == "bottom":

            c.drawString(
                cube_center_x + 10,
                pipe_y - 10,
                f"{distance_from_left_mm:.0f}"
            )'''
            
        # --------------------------------------------------
        # PIPE LABEL
        # --------------------------------------------------

        c.setFont(
            "Helvetica",
            6
        )

        if side == "left":

            label_x = px - 55
            label_y = py + 10

        elif side == "right":

            label_x = px + 10
            label_y = py + 10

        elif side == "top":

            label_x = px + 10
            label_y = py + 10

        else:

            label_x = px + 10
            label_y = py - 15

        c.drawString(
            label_x,
            label_y,
            f"{pipe['id']} Ø{pipe['diameter']}"
        )

        # Restore defaults

        c.setFillColor(colors.black)
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)

    # ======================================================
    # PIPE DIMENSIONS
    # ======================================================

    tank_left = grid_x
    tank_right = grid_x + grid_len

    tank_bottom = grid_y
    tank_top = grid_y + grid_wid
    
    
    # ==========================================
    # HORIZONTAL PIPE DIMENSIONS
    # ==========================================

    for i, dim in enumerate(horizontal_dims):

        dim_y = (
            tank_bottom
            - red_offset
            - 12
            - (i * 12)
        )

        draw_dimension_horizontal(
            c,
            tank_left,
            dim["x"],
            dim_y,
            f"{dim['offset']:.0f}"
        )

        draw_dimension_horizontal(
            c,
            dim["x"],
            tank_right,
            dim_y,
            f"{data['length'] - dim['offset']:.0f}"
        )

    # ==========================================
    # VERTICAL PIPE DIMENSIONS
    # ==========================================
    VERTICAL_DIM_CLEARANCE = 55
    LEFT_ARROW_ZONE = PIPE_EXTENSION + 10

    vertical_dimension_start = (
        grid_x
        - LEFT_ARROW_ZONE
        - 30
    )
    for i, dim in enumerate(vertical_dims):

        dim_x = (
            vertical_dimension_start
            - (i * 18)
        )

        draw_dimension_vertical(
            c,
            tank_bottom,
            dim["y"],
            dim_x,
            f"{dim['offset']:.0f}"
        )

        draw_dimension_vertical(
            c,
            dim["y"],
            tank_top,
            dim_x,
            f"{data['width'] - dim['offset']:.0f}"
        )
    # ======================================================
    # DIMENSIONS
    # ======================================================

    c.setFont(
        "Helvetica",
        8
    )

    c.drawCentredString(
        x + (tank_len / 2),
        y - 28,
        f"{data['length'] / 1000:.2f} m"
    )

    c.saveState()

    c.rotate(90)

    c.drawCentredString(
        y + (tank_wid / 2),
        -x + 20,
        f"{data['width'] / 1000:.2f} m"
    )

    c.restoreState()
    
        
    # ======================================================
    # OVERALL TANK GRID DIMENSIONS
    # ======================================================

    overall_dim_y = (
        grid_y
        - red_offset
        - 70
    )

    draw_dimension_horizontal(
        c,
        grid_x,
        grid_x + grid_len,
        overall_dim_y,
        f"{data['length'] / 1000:.2f} m"
    )

    overall_dim_x = (
        grid_x
        - red_offset
        - 70
    )

    draw_dimension_vertical(
        c,
        grid_y,
        grid_y + grid_wid,
        overall_dim_x,
        f"{data['width'] / 1000:.2f} m"
    )