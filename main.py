# main.py — Atlan Stormwater PDF Generator

import os

from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import black, white, HexColor
from reportlab.pdfbase.pdfmetrics import stringWidth

from page1 import draw_page1_tables, draw_page1_diagrams
from page2 import draw_page2_image
from page3 import draw_page3_annotations, draw_page3_image
import data_mapper

_HERE  = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(_HERE, "accurate_titleblock_fixed.pdf")
PAGES  = 3

PW, PH = landscape(A3)


IM  = 10 * mm
ILW = 1.5

IX0 = IM;   IX1 = PW - IM;   IW = IX1 - IX0
IY0 = IM;   IY1 = PH - IM;   IH = IY1 - IY0

ROW_H  = IH / 4
TBAR_H = 6 * mm
TB_H   = 45 * mm

TB_BOT   = IY0
TB_TOP   = TB_BOT + TB_H
TBAR_BOT = TB_TOP
TBAR_TOP = TBAR_BOT + TBAR_H

TB_L = IX0
TB_R = IX1
TB_W = IW

C1W = TB_W * 0.285
C2W = TB_W * 0.297
C3W = TB_W * 0.075
C4W = TB_W * 0.132
C5W = TB_W - C1W - C2W - C3W - C4W

X1 = TB_L
X2 = X1 + C1W
X3 = X2 + C2W
X4 = X3 + C3W
X5 = X4 + C4W

CLW        = 0.5
ATLAN_BLUE = HexColor("#003087")
FN  = "Helvetica"
FB  = "Helvetica-Bold"
FBO = "Helvetica-BoldOblique"
PAD = 1.0 * mm


def clip_text(text, font, size, max_width):
    while len(text) > 1 and stringWidth(text, font, size) > max_width:
        text = text[:-1]
    return text


def draw_cell(c, x, y, w, h, lw=CLW, fill=None):
    c.setStrokeColor(black)
    c.setLineWidth(lw)
    if fill:
        c.setFillColor(fill)
        c.rect(x, y, w, h, stroke=1, fill=1)
        c.setFillColor(black)
    else:
        c.rect(x, y, w, h, stroke=1, fill=0)


def draw_page_border(c):
    GAP    = IM
    BDR_X1 = GAP
    BDR_Y1 = GAP
    BDR_X2 = PW - GAP
    BDR_Y2 = PH - GAP
    BDR_W  = BDR_X2 - BDR_X1
    BDR_H  = BDR_Y2 - BDR_Y1

    NUM_COLS = 6
    NUM_ROWS = 4
    COL_W = BDR_W / NUM_COLS
    ROW_H = BDR_H / NUM_ROWS

    def col_x(n): return BDR_X1 + n * COL_W
    def row_y(n): return BDR_Y1 + n * ROW_H

    TICK   = 6
    FONT_B = "Helvetica-Bold"

    c.setStrokeColor(black)
    c.setLineWidth(ILW)
    c.rect(BDR_X1, BDR_Y1, BDR_W, BDR_H)

    col_labels = [6, 5, 4, 3, 2, 1]
    for i in range(NUM_COLS):
        lx = col_x(i) + COL_W / 2
        c.setFont(FONT_B, 8)
        c.setFillColor(black)
        c.drawCentredString(lx, BDR_Y2 + 5, str(col_labels[i]))
        c.drawCentredString(lx, BDR_Y1 - 12, str(col_labels[i]))
        if i > 0:
            tx = col_x(i)
            c.setLineWidth(0.6)
            c.setStrokeColor(black)
            c.line(tx, BDR_Y2, tx, BDR_Y2 + TICK)
            c.line(tx, BDR_Y1, tx, BDR_Y1 - TICK)

    row_labels = ["A", "B", "C", "D"]
    for j in range(NUM_ROWS):
        ly = row_y(j) + ROW_H / 2
        c.setFont(FONT_B, 8)
        c.setFillColor(black)
        c.drawCentredString(BDR_X1 - 8, ly, row_labels[j])
        c.drawCentredString(BDR_X2 + 8, ly, row_labels[j])
        if j > 0:
            ty = row_y(j)
            c.setLineWidth(0.6)
            c.setStrokeColor(black)
            c.line(BDR_X1, ty, BDR_X1 - TICK, ty)
            c.line(BDR_X2, ty, BDR_X2 + TICK, ty)

    mid_x = BDR_X1 + BDR_W / 2
    mid_y = BDR_Y1 + BDR_H / 2
    s = 7

    def hollow_arrow(cx, cy, direction):
        c.setFillColor(white)
        c.setStrokeColor(black)
        c.setLineWidth(0.8)
        p = c.beginPath()
        if direction == "down":
            p.moveTo(cx-s, cy+s); p.lineTo(cx+s, cy+s); p.lineTo(cx, cy-s)
        elif direction == "up":
            p.moveTo(cx-s, cy-s); p.lineTo(cx+s, cy-s); p.lineTo(cx, cy+s)
        elif direction == "right":
            p.moveTo(cx-s, cy+s); p.lineTo(cx-s, cy-s); p.lineTo(cx+s, cy)
        elif direction == "left":
            p.moveTo(cx+s, cy+s); p.lineTo(cx+s, cy-s); p.lineTo(cx-s, cy)
        p.close()
        c.drawPath(p, fill=1, stroke=1)
        c.setFillColor(black)

    c.setLineWidth(0.6)
    c.setStrokeColor(black)

    c.line(mid_x, PH - 2, mid_x, BDR_Y2 + s + 1)
    hollow_arrow(mid_x, BDR_Y2 + s, "down")

    c.line(mid_x, 2, mid_x, BDR_Y1 - s - 1)
    hollow_arrow(mid_x, BDR_Y1 - s, "up")

    c.line(2, mid_y, BDR_X1 - s - 1, mid_y)
    hollow_arrow(BDR_X1 - s, mid_y, "right")

    c.line(PW - 2, mid_y, BDR_X2 + s + 1, mid_y)
    hollow_arrow(BDR_X2 + s, mid_y, "left")


def draw_tolerance_bar(c):
    bar_end_x = IX0 + IW / 2 + 8 * mm
    draw_cell(c, TB_L, TBAR_BOT, bar_end_x - TB_L, TBAR_H)

    divider_x = X1 + (C1W * 0.55)
    c.line(divider_x, TBAR_BOT, divider_x, TBAR_TOP)

    fs = 6.0
    mid = TBAR_BOT + TBAR_H / 2
    text_y = mid - fs * 0.35

    c.setFont(FB, fs)
    c.drawCentredString(
        (TB_L + divider_x) / 2, text_y,
        "TOLERANCE: All Dimensions to Closest 10 mm & +/- 30 mm"
    )

    c.setFont(FB, 9.5)
    text_y2 = mid - 11.16 * 0.35
    c.drawCentredString(
        (divider_x + bar_end_x) / 2, text_y2,
        "ALL INTERCONNECTING PIPEWORK, PITS AND ASSOCIATED DRAINAGE BY OTHERS"
    )


def draw_rev_table(c, rev_history):
    x = X1
    y = TB_BOT
    w = C1W
    h = TB_H

    draw_cell(c, x, y, w, h)

    COL_W_ZONE = IW / 6
    x_lbl_6   = IX0 + 0.5 * COL_W_ZONE
    x_tick_65 = IX0 + 1.0 * IW / 8.5
    x_lbl_5   = IX0 + 1.5 * 1125 / 6

    rev_w  = 12 * mm
    x_rev  = x + rev_w
    x_date = x_lbl_6
    date_w = x_date - x_rev
    x_by   = x_tick_65
    by_w   = x_by - x_date
    x_chk  = x_lbl_5
    desc_w = x_chk - x_by
    chk_w  = (x + w) - x_chk

    header_h = 6 * mm
    row_h    = 5 * mm
    n_rows   = len(rev_history)
    grid_top = y + header_h + row_h * n_rows

    c.line(x_rev,  y, x_rev,  grid_top)
    c.line(x_date, y, x_date, grid_top)
    c.line(x_by,   y, x_by,   grid_top)
    c.line(x_chk,  y, x_chk,  grid_top)

    c.line(x, y + header_h, x + w, y + header_h)
    for i in range(1, n_rows + 1):
        yy = y + header_h + row_h * i
        c.line(x, yy, x + w, yy)

    fs_hdr     = 7.0
    hdr_text_y = y + (header_h - fs_hdr) / 2

    c.setFont(FN, fs_hdr)
    c.setFillColor(black)
    c.drawCentredString(x + rev_w / 2,      hdr_text_y, "REV")
    c.drawCentredString(x_rev + date_w / 2, hdr_text_y, "DATE")
    c.drawCentredString(x_date + by_w / 2,  hdr_text_y, "BY")
    c.drawCentredString(x_by + desc_w / 2,  hdr_text_y, "DESCRIPTION")
    c.drawCentredString(x_chk + chk_w / 2,  hdr_text_y, "CHK")

    fs_data = 6.5
    c.setFont(FN, fs_data)
    c.setFillColor(black)

    for i, row in enumerate(rev_history):
        row_bot   = y + header_h + (n_rows - 1 - i) * row_h
        row_mid_y = row_bot + (row_h - fs_data) / 2
        c.drawCentredString(x + rev_w / 2,      row_mid_y, row[0])
        c.drawCentredString(x_rev + date_w / 2, row_mid_y, row[1])
        c.drawCentredString(x_date + by_w / 2,  row_mid_y, row[2])
        c.drawCentredString(x_by + desc_w / 2,  row_mid_y, row[3])


def draw_client_col(c, client_name=""):
    x, y, w, h = X2, TB_BOT, C2W, TB_H
    tick4_x  = IX0 + 2 * (IW / 6) + 35 * mm
    client_w = tick4_x - x
    conf_w   = w - client_w
    conf_x   = x + client_w

    draw_cell(c, x, y, client_w, h)
    fs_label = 7.5
    c.setFont(FB, fs_label)
    c.setFillColor(black)
    c.drawString(x + PAD, y + h - PAD - fs_label, "CLIENT:")
    if client_name:
        c.setFont(FN, 6.5)
        c.drawString(x + PAD, y + h - PAD - fs_label - 8, client_name)

    draw_cell(c, conf_x, y, conf_w, h)
    confidential_lines = [
        "CONFIDENTIAL - The drawings must not be disclosed to any third",
        "parties without written permission from ATLAN STORMWATER .",
        "Unauthorised disclosure may result in prosecution.",
        "© ATLAN STORMWATER - This drawing is the property of ATLAN",
        "STORMWATER ABN: 83 151 832 629 and is subject to return on",
        "demand. It is submitted for the use only in connection with the",
        "proposal and contracts of ATLAN STORMWATER with the expressed",
        "conditions that it is not to be reproduced or copied in any form.",
        "This data must only be used in accordance with our standard",
        "terms and conditions.",
        "© Copyright",
        "ATLAN STORMWATER accepts no responsibility for any loss or",
        "damage resulting from any person acting on this information.",
        "The details and dimensions contained in this document may change,",
        "please check with ATLAN STORMWATER for confirmation of current",
        "specifications.",
    ]
    fs = 5.5
    line_h  = fs * 1.4
    start_y = y + h - PAD - fs
    c.setFont(FN, fs)
    c.setFillColor(black)
    for i, line in enumerate(confidential_lines):
        ly = start_y - i * line_h
        if ly < y + PAD:
            break
        c.drawString(conf_x + PAD, ly, line)


def draw_confidential(c, request_no="", drawn_by="", drawn_date=""):
    x, y, w, h = X3, TB_BOT, C3W, TB_H
    draw_cell(c, x, y, w, h)

    label_w = w * 0.50
    date_x  = x + label_w
    req_h   = h * 0.22
    sig_h   = (h - req_h) / 4
    fs_lbl  = 8
    fs_val  = 7.5

    rows = [
        ("Drawn",    drawn_by,   drawn_date),
        ("Check",    "",         ""),
        ("Verified", "",         ""),
        ("Approved", "",         ""),
    ]
    sig_top = y + h

    for i, (label, val, date_val) in enumerate(rows):
        row_top = sig_top - i * sig_h
        row_bot = row_top - sig_h

        c.setLineWidth(0.4); c.setStrokeColor(black)
        c.line(x, row_bot, x + w, row_bot)
        c.setLineWidth(CLW); c.setStrokeColor(black)
        c.line(date_x, row_bot, date_x, row_top)

        lbl_y = row_top - PAD - fs_lbl
        c.setFont(FN, fs_lbl); c.setFillColor(black)
        c.drawString(x + PAD, lbl_y, label)

        if val:
            val_y = row_bot + PAD + 0.5
            c.setFont(FN, fs_val); c.setFillColor(black)
            c.drawString(x + PAD, val_y, val)

        c.setFont(FN, fs_lbl); c.setFillColor(black)
        c.drawString(date_x + PAD, lbl_y, "Date")

        if date_val:
            c.setFont(FN, fs_val); c.setFillColor(black)
            c.drawString(date_x + PAD, row_bot + PAD + 0.5, date_val)

    req_top = y + req_h
    c.setFont(FN, fs_lbl); c.setFillColor(black)
    c.drawString(x + PAD, req_top - PAD - fs_lbl, "Request No.")
    c.setFont(FN, fs_val); c.setFillColor(black)
    c.drawString(x + PAD, y + PAD + 0.5, request_no)


def draw_signatures(c, drawn_by="", drawn_date=""):
    x, y, w, h = X4, TB_BOT, C4W, TB_H
    draw_cell(c, x, y, w, h)

    logo_path = r"C:\Users\shrad\OneDrive\Documents\Desktop\pdf gen\Atlan-Stormwater-LogoR.png"
    logo_w = w * 0.90
    logo_h = h * 0.70
    logo_x = x + (w - logo_w) / 2
    logo_y = y + (h - logo_h) / 2

    if os.path.isfile(logo_path):
        c.drawImage(logo_path, logo_x, logo_y,
                    width=logo_w, height=logo_h,
                    preserveAspectRatio=True, mask='auto')
    else:
        ATLAN_BRAND_BLUE = HexColor("#1F6BFF")
        cx = x + w / 2
        cy = y + h / 2
        atlan_size = min(logo_h * 0.55, 28)
        c.setFillColor(ATLAN_BRAND_BLUE)
        c.setFont(FB, atlan_size)
        c.drawCentredString(cx, cy - atlan_size * 0.10, "Atlan")
        sw_size = min(logo_h * 0.18, 7.5)
        c.setFont(FB, sw_size)
        c.drawCentredString(cx, cy - atlan_size * 0.70, "STORMWATER")
        c.setFillColor(black)


def draw_project_info(c, project_lines=None, title_lines=None,
                      scale="N.T.S", size="A3", sheet_of="1 OF 2", rev="",
                      customer_code="", dwg_no=""):
    x, y, w, h = X5, TB_BOT, C5W, TB_H
    draw_cell(c, x, y, w, h)

    if project_lines is None:
        project_lines = [""]
    if title_lines is None:
        title_lines = []

    fs_label = 9.0
    fs_val   = 8
    fs_title = 8
    fs_foot  = 7

    foot2_h = h * 0.16
    foot1_h = h * 0.16
    foot_h  = foot1_h + foot2_h
    foot1_y = y + foot2_h

    c.setLineWidth(CLW); c.setStrokeColor(black)
    c.line(x, y + foot_h,  x + w, y + foot_h)
    c.line(x, y + foot2_h, x + w, y + foot2_h)

    sub_props  = [0.35, 0.20, 0.30, 0.15]
    sub_widths = [w * p for p in sub_props]
    sub_lefts  = [x]
    for sw in sub_widths[:-1]:
        sub_lefts.append(sub_lefts[-1] + sw)

    c.setLineWidth(0.3); c.setStrokeColor(black)
    for i in range(1, 4):
        c.line(sub_lefts[i], y + foot2_h, sub_lefts[i], y + foot_h)

    for i, (lbl, val) in enumerate(zip(["SCALE", "SIZE", "SHEET", "REV"],
                                        [scale, size, sheet_of, rev])):
        col_cx = sub_lefts[i] + sub_widths[i] / 2
        lbl_y  = foot1_y + foot1_h - PAD - fs_foot
        val_y  = foot1_y + PAD
        c.setFont(FN, fs_foot); c.setFillColor(black)
        c.drawCentredString(col_cx, lbl_y, lbl)
        c.setFont(FN, fs_foot); c.setFillColor(black)
        c.drawCentredString(col_cx, val_y, val)

    cc_w = w * 0.30
    c.setLineWidth(0.3); c.setStrokeColor(black)
    c.line(x + cc_w, y, x + cc_w, y + foot2_h)

    cc_lbl_y = y + foot2_h - PAD - fs_foot
    cc_val_y = y + PAD

    c.setFont(FN, fs_foot); c.setFillColor(black)
    c.drawString(x + PAD, cc_lbl_y, "CUSTOMER CODE")
    c.setFont(FN, fs_foot); c.setFillColor(black)
    c.drawString(x + PAD, cc_val_y, customer_code)

    dwg_x = x + cc_w
    dwg_w = w - cc_w

    c.setFont(FN, 7)
    c.setFillColor(black)
    c.drawString(dwg_x + PAD, cc_lbl_y, "DWG No.")

    c.setFont(FN, 11)

    dwg_mid_y = y + (foot2_h / 2) - 6

    c.drawCentredString(
        dwg_x + dwg_w / 2,
        dwg_mid_y,
        clip_text(dwg_no, FN, 18, dwg_w - 4 * PAD)
    )

    content_top = y + h
    content_bot = y + foot_h
    content_h   = content_top - content_bot

    proj_row_h  = content_h * 0.30
    proj_y      = content_top - proj_row_h

    c.setLineWidth(CLW); c.setStrokeColor(black)
    c.line(x, proj_y, x + w, proj_y)

    proj_text_y = proj_y + (proj_row_h - fs_label) / 2
    lbl_str     = "PROJECT :"
    lbl_w       = stringWidth(lbl_str, FB, fs_label)
    val_gap     = 2
    val_x       = x + PAD + lbl_w + val_gap
    val_max_w   = w - PAD - lbl_w - val_gap - PAD

    c.setFont(FB, fs_label); c.setFillColor(black)
    c.drawString(x + PAD, proj_text_y, lbl_str)
    c.setFont(FN, fs_val); c.setFillColor(black)
    c.drawString(val_x, proj_text_y,
                 clip_text(project_lines[0] if project_lines else "",
                           FN, fs_val, val_max_w))

    title_row_h = content_h * 0.22
    title_y     = proj_y - title_row_h

    c.setLineWidth(CLW); c.setStrokeColor(black)

    title_lbl_y = title_y + (title_row_h - fs_label) / 2
    c.setFont(FB, fs_label); c.setFillColor(black)
    c.drawString(x + PAD, title_lbl_y, "TITLE")

    title_content_h = title_y - content_bot
    line_sp         = fs_title * 1.35
    total_block_h   = (len(title_lines) - 1) * line_sp + fs_title
    start_ty        = title_y - (title_content_h - total_block_h) / 2 - fs_title

    for i, line in enumerate(title_lines):
        ty = start_ty - i * line_sp
        if ty < content_bot + PAD:
            break
        c.setFont(FN, 10)
        c.setFillColor(black)
        c.drawCentredString(x + w / 2, ty,
                            clip_text(line, FB, fs_title, w - 2 * PAD))


def draw_full_page(c, page_num=1, total_pages=3, image_path="",
                   drawn_by="", drawn_date="",
                   scale="N.T.S", size="A3",
                   customer_code="", dwg_no="",
                   rev="", request_no="", client_name="",
                   project_lines=None, title_lines=None, rev_history=None,
                   drawing_data=None):

    if project_lines is None:
        project_lines = [""]
    if rev_history is None:
        rev_history = []

    sheet_of = f"{page_num} OF {total_pages}"

    draw_page_border(c)
    draw_tolerance_bar(c)
    draw_rev_table(c, rev_history)
    draw_client_col(c, client_name)
    draw_confidential(c, request_no, drawn_by, drawn_date)
    draw_signatures(c, drawn_by, drawn_date)
    draw_project_info(c, project_lines=project_lines, title_lines=title_lines,
                      scale=scale, size=size, sheet_of=sheet_of, rev=rev,
                      customer_code=customer_code, dwg_no=dwg_no)

    if page_num == 1:
        draw_page1_tables(c, parts_list=drawing_data.get("parts_list") if drawing_data else None)
        draw_page1_diagrams(c, drawing_data=drawing_data)
    elif page_num == 2:
        if image_path:
            draw_page2_image(c, image_path)
    elif page_num == 3:
        draw_page3_annotations(c)
        draw_page3_image(c, image_path=image_path)
    else:
        draw_y_centre = (TBAR_TOP + IY1) / 2
        c.setFont(FN, 16)
        c.setFillColor(HexColor("#BBBBBB"))
        c.drawCentredString(PW / 2, draw_y_centre,
                            f"Drawing Content — Page {page_num} of {total_pages}")
        c.setFillColor(black)


def generate(raw_data: dict, output=OUTPUT, num_pages=PAGES):
    dd = data_mapper.build(raw_data)

    c = rl_canvas.Canvas(output, pagesize=landscape(A3))
    c.setTitle("Atlan Stormwater - Title Block Template")
    for i in range(1, num_pages + 1):
        draw_full_page(
            c,
            page_num=i,
            total_pages=num_pages,
            image_path=dd["page2_image"] if i == 2 else dd["page3_image"],
            title_lines=dd["title_lines"],
            drawn_by=dd["drawn_by"],
            scale=dd["scale"],
            size=dd["size"],
            customer_code=dd["customer_code"],
            dwg_no=dd["dwg_no"],
            rev=dd["rev"],
            request_no=dd["request_no"],
            project_lines=dd["project_lines"],
            rev_history=dd["rev_history"],
            drawing_data=dd,
        )
        c.showPage()
    c.save()
    print(f"Saved: {output}  -  {num_pages} pages, A3 landscape")


if __name__ == "__main__":
    try:
        import json, sys

        if len(sys.argv) > 1:
            with open(sys.argv[1], encoding="utf-8") as f:
                raw = json.load(f)
        else:
            raw = {
                "customer_code": "24-59314",
                "dwg_no":        "59314.P.01.10.GA",
                "request_no":    "RN236248",
                "drawn_date":    "2/04/2026",
                "project_lines": [
                    "BAROSSA GLENORCHY PARK LODGE - STAGE 2",
                    "- 17A CLYDESDALE AVENUE, GLENORCHY",
                ],
                "stack_key":   "1",
                "wide":        5,
                "long":        12,
                "storage_m3":  60,
                "rev_history": [
                    ["1", "2/04/2026", "R.R.", "INITIAL RELEASE"],
                ],
                "parts_list": [
                    ["1", "1000L MODULE - HALF CUBE",              "18", ""],
                    ["2", "1000L MODULE - SIDE PANEL FULL HEIGHT", "32", ""],
                    ["3", "SINGLE CONNECTOR",                      "101", ""],
                ],
            }

        generate(raw_data=raw)
        print("Done! PDF saved to:", OUTPUT)
    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        input("\nPress Enter to close...")

