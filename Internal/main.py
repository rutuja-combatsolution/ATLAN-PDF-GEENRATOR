# ==========================================================
# main.py
# ==========================================================

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.units import mm

from plan_view import draw_plan_view
from elevation_view import draw_elevation_view

# ==========================================================
# PAGE SETUP
# ==========================================================

PAGE_W, PAGE_H = landscape(A3)

# ==========================================================
# SOURCE DATA
# ==========================================================

SOURCE_DATA = {
    "geometry": {
        "breadth_mm": 6950.0,
        "cover_depth": 660.0,
        "finished_surface_level": 3000.0,
        "height_mm": 3000.0,
        "length_mm": 15000.0,
        "minimum_cover_depth": 100.0,
        "outlet_invert_level": 3000.0,
        "stack_length": 2340.0,
        "stack_number":"double"
    },

    "input": {
        "project_name": "Stormwater Project 001",
        "available_depth_to_invert": 3.0,
        "base_of_tank_level": 97.0,
        "constraining_dimension": 15.0,
        "constraining_factor": "length",
        "fsl_user_input": 100.0,
        "include_liner": None,
        "layers_in_system": 3,
        "max_layers_possible": 3,#stack name value 
        "number_of_inlets": 2,
        "number_of_manholes": 1,
        "number_of_outlets": 1,
        "project_created": True,
        "target_storage_volume": 201.0,
        "volumn_provided": None
    },

    "material": {
        "cubes_long": 13,
        "cubes_wide": 6,

        "excavation_volume": 456.45,
        "final_backfill_required": 85.2,
        "initial_backfill_required": 127.3,

        "inlet": [
            {
                "horizontal_offset": 0.0,
                "id": "INLET-1",
                "invert_level": 0.0,
                "side": "left",
                "diameter": 375,
                  "panel_x": 0,
                "panel_y": 2
            },
            {
                "horizontal_offset": 2.78,
                "id": "INLET-2",
                "invert_level": 0.0,
                "side": "left",
                "diameter": 375,
                  "panel_x": 0,
                "panel_y": 4
            }
        ],

        "manhole": [
            {
                "horizontal_offset": 0.0,
                "id": "MH-1",
                "invert_level": 0.0,
                "side": "top"
            }
        ],

        "outlet": [
            {
                "horizontal_offset": 0.0,
                "id": "OUTLET-1",
                "invert_level": 0.0,
                "side": "right",
                "diameter": 375,
                  "panel_x": 12,
                "panel_y": 2
            }
        ],

        "tank_storage": 234.0
    }
}

# ==========================================================
# BUILD DRAWING DATA
# ==========================================================

def build_drawing_data(data):

    geometry = data["geometry"]
    material = data["material"]
    inputs = data["input"]

    drawing = {}

    # ------------------------------------------------------
    # PROJECT INFO
    # ------------------------------------------------------

    drawing["project_name"] = inputs.get(
        "project_name",
        "STORMWATER PROJECT"
    )

    # ------------------------------------------------------
    # GEOMETRY
    # ------------------------------------------------------

    drawing["length"] = geometry["length_mm"]
    drawing["width"] = geometry["breadth_mm"] 

    drawing["length"] = geometry["length_mm"]
    drawing["width"] = geometry["breadth_mm"]

    drawing["levels"] = int(
        inputs["layers_in_system"]
    )

    drawing["panel_height"] = 1000   # fixed Atlancube layer height

    drawing["height"] = (
        drawing["levels"] *
        drawing["panel_height"]
    )

    drawing["length_panels"] = material["cubes_long"]
    drawing["width_panels"] = material["cubes_wide"]
    drawing["panel_length"] = (
    drawing["length"] /
    drawing["length_panels"]
    )

    drawing["panel_width"] = (
        drawing["width"] /
        drawing["width_panels"]
    )

    # ------------------------------------------------------
    # LEVELS
    # ------------------------------------------------------

    drawing["fsl"] = inputs["fsl_user_input"]

    drawing["base_rl"] = (
        inputs["base_of_tank_level"]
    )

    drawing["cover_depth"] = (
        geometry["cover_depth"]
    )

    drawing["minimum_cover_depth"] = (
        geometry["minimum_cover_depth"]
    )

    drawing["finished_surface_level"] = (
        geometry["finished_surface_level"]
    )

    # ------------------------------------------------------
    # STORAGE
    # ------------------------------------------------------

    drawing["tank_storage"] = (
        material["tank_storage"]
    )

    drawing["target_storage_volume"] = (
        inputs["target_storage_volume"]
    )

    # ------------------------------------------------------
    # CONSTRUCTION DATA
    # ------------------------------------------------------

    drawing["excavation_volume"] = (
        material["excavation_volume"]
    )

    drawing["initial_backfill_required"] = (
        material["initial_backfill_required"]
    )

    drawing["final_backfill_required"] = (
        material["final_backfill_required"]
    )

    drawing["stack_number"] = (
        geometry["stack_number"]
    )

    drawing["stack_length"] = (
        geometry["stack_length"]
    )

    drawing["excavation_clearance"] = 500

    # ------------------------------------------------------
    # MANHOLES
    # ------------------------------------------------------

    drawing["manholes"] = []

    manholes = material.get("manhole", [])

    for idx, mh in enumerate(manholes):

        drawing["manholes"].append(
            {
                "id": mh["id"],
                "label": f"MH-{idx + 1}",
                "side": mh.get("side", "top"),
                "horizontal_offset": mh.get(
                    "horizontal_offset",
                    0
                ),
                "invert_level": mh.get(
                    "invert_level",
                    0
                )
            }
        )

    # ------------------------------------------------------
    # INLETS
    # ------------------------------------------------------

    drawing["inlets"] = []

    for idx, inlet in enumerate(
        material.get("inlet", [])
    ):

        drawing["inlets"].append(
            {
                "id": inlet["id"],
                "label": f"INLET-{idx + 1}",
                "side": inlet.get(
                    "side",
                    "left"
                ),
                "horizontal_offset": inlet.get(
                    "horizontal_offset",
                    0
                ),
                "invert_level": inlet.get(
                    "invert_level",
                    0
                ),
                "diameter": inlet.get(
                    "diameter",
                    375
                ),

                # NEW
                "panel_x": inlet.get(
                    "panel_x",
                    0
                ),
                "panel_y": inlet.get(
                    "panel_y",
                    0
                )
            }
        )

    # ------------------------------------------------------
    # OUTLETS
    # ------------------------------------------------------

    drawing["outlets"] = []

    for idx, outlet in enumerate(
        material.get("outlet", [])
    ):

        drawing["outlets"].append(
            {
                "id": outlet["id"],
                "label": f"OUTLET-{idx + 1}",
                "side": outlet.get(
                    "side",
                    "right"
                ),
                "horizontal_offset": outlet.get(
                    "horizontal_offset",
                    0
                ),
                "invert_level": outlet.get(
                    "invert_level",
                    0
                ),
                "diameter": outlet.get(
                    "diameter",
                    375
                ),

                # NEW
                "panel_x": outlet.get(
                    "panel_x",
                    0
                ),
                "panel_y": outlet.get(
                    "panel_y",
                    0
                )
            }
        )

    # ------------------------------------------------------
    # LEGACY PIPE LIST
    # (Optional for compatibility)
    # ------------------------------------------------------

    drawing["pipes"] = []

    for inlet in drawing["inlets"]:
        drawing["pipes"].append(
            {
                **inlet,
                "type": "INLET"
            }
        )

    for outlet in drawing["outlets"]:
        drawing["pipes"].append(
            {
                **outlet,
                "type": "OUTLET"
            }
        )

    return drawing


# ==========================================================
# BORDER
# ==========================================================

def draw_border(c):

    margin = 5 * mm

    c.setLineWidth(1)

    c.rect(
        margin,
        margin,
        PAGE_W - (margin * 2),
        PAGE_H - (margin * 2)
    )


'''# ==========================================================
# HEADER
# ==========================================================

def draw_header(c, drawing_data):

    c.setFont(
        "Helvetica-Bold",
        10
    )

    c.drawCentredString(
        PAGE_W / 2,
        PAGE_H - 20,
        f"{drawing_data['project_name']} - GENERAL ARRANGEMENT"
    )'''


# ==========================================================
# PDF GENERATOR
# ==========================================================

def create_pdf():

    drawing_data = build_drawing_data(
        SOURCE_DATA
    )

    filename = (
        drawing_data["project_name"]
        .replace(" ", "_")
        + ".pdf"
    )

    c = canvas.Canvas(
        filename,
        pagesize=landscape(A3)
    )

    draw_border(c)

    '''draw_header(
        c,
        drawing_data
    )'''

    draw_plan_view(
        c,
        drawing_data,
        x=140,
        y=420
    )

    
    draw_elevation_view(
        c,
        drawing_data,
        x=140,
        y=100
    )

    c.save()

    print(
        f"{filename} generated successfully"
    )


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":
    create_pdf()