# data_mapper.py
# Takes raw JSON (from API or file) and returns a clean drawing_data dict.
# No PDF logic here — pure data mapping.
#
# FIXED fields (never in JSON):
#   drawn_by  -> always "R.R."
#   size      -> always "A3"
#   scale     -> always "N.T.S"
#   rev       -> derived from rev_history[0][0]
#   page2_image -> fixed to isometric.jpeg
#   page3_image -> auto-generated from stack_key (withdimension folder)
#
# DYNAMIC fields (come from JSON):
#   customer_code, dwg_no, request_no, drawn_date
#   project_lines
#   stack_key, wide, long, storage_m3
#   rev_history     (list of rows — drives rev number automatically)
#   parts_list      (full rows, varies per stack)


import os


# =============================================================================
# STACK LABEL LOOKUP
# =============================================================================

_HERE = os.path.dirname(os.path.abspath(__file__))
PAGE3_IMAGES_DIR = os.path.join(_HERE, "withdimension", "withdimension")

STACK_META = {
    "0.5": {"label": "HALF STACK"},
    "1":   {"label": "SINGLE STACK"},
    "1.5": {"label": "1.5 STACK"},
    "2":   {"label": "DOUBLE STACK"},
    "2.5": {"label": "2.5 STACK"},
    "3":   {"label": "TRIPLE STACK"},
}


# =============================================================================
# PIPE / MANHOLE BUILDERS
# =============================================================================

def _build_pipes(raw_list: list, pipe_type: str) -> list:
    pipes = []
    for idx, p in enumerate(raw_list):
        pipes.append({
            "id":                p.get("id",    f"{pipe_type}-{idx+1}"),
            "label":             f"{pipe_type}-{idx+1}",
            "type":              pipe_type,
            "side":              p.get("side",   "left" if pipe_type == "INLET" else "right"),
            "panel_x":           p.get("panel_x", 0),
            "panel_y":           p.get("panel_y", 0),
            "diameter":          p.get("diameter", 375),
            "horizontal_offset": p.get("horizontal_offset", 0.0),
            "invert_level":      p.get("invert_level", 0.0),
        })
    return pipes


def _build_manholes(raw_list: list) -> list:
    manholes = []
    for idx, m in enumerate(raw_list):
        manholes.append({
            "id":                m.get("id",    f"MH-{idx+1}"),
            "label":             f"MH-{idx+1}",
            "side":              m.get("side",   "top"),
            "panel_x":           m.get("panel_x", 0),
            "panel_y":           m.get("panel_y", 0),
            "horizontal_offset": m.get("horizontal_offset", 0.0),
            "invert_level":      m.get("invert_level", 0.0),
        })
    return manholes


# =============================================================================
# MAIN MAPPER
# =============================================================================

def build(raw: dict) -> dict:
    """
    Map raw API/JSON dict -> clean drawing_data dict.

    Expected raw keys:
        customer_code   str
        dwg_no          str
        request_no      str
        drawn_date      str           e.g. "2/04/2026"
        project_lines   list[str]     1 or 2 lines
        stack_key       str           "0.5" | "1" | "1.5" | "2" | "2.5" | "3"
        wide            int
        long            int
        storage_m3      float
        rev_history     list of [rev, date, by, description]
        parts_list      list of [item, description, qty, remarks]
        page2_image     str           path to isometric image

    Auto-generated fields:
        page3_image     str           auto-selected from withdimension folder based on stack_key
    """

    stack_key   = str(raw["stack_key"])
    stack_label = STACK_META[stack_key]["label"]

    # rev is always the top row of rev_history — never stored separately
    rev_history = raw["rev_history"]
    rev         = str(rev_history[0][0])

    wide    = raw["wide"]
    long    = raw["long"]
    storage = raw["storage_m3"]

    # ==========================================================
    # PLAN VIEW / ELEVATION VIEW MAPPING
    # ==========================================================

    STACK_CONFIG = {
        "0.5": {
            "layers": 1,
            "stack_name": "half",
            "stack_length": 390
        },
        "1": {
            "layers": 1,
            "stack_name": "single",
            "stack_length": 780
        },
        "1.5": {
            "layers": 2,
            "stack_name": "one_half",
            "stack_length": 1170
        },
        "2": {
            "layers": 2,
            "stack_name": "double",
            "stack_length": 1560
        },
        "2.5": {
            "layers": 3,
            "stack_name": "two_half",
            "stack_length": 1950
        },
        "3": {
            "layers": 3,
            "stack_name": "triple",
            "stack_length": 2340
        }
    }

    cfg = STACK_CONFIG[stack_key]

    length_mm = long * 1150
    breadth_mm = wide * 1150

    title_lines = [
        "ATLAN CUBE",
        f"ATLAN CUBE 1000L MODULE ({stack_label})",
        f"{wide}-CUBES WIDE x {long}-CUBES LONG - {storage}m3",
        "GENERAL ARRANGEMENT",
    ]

    # Auto-generate page3_image path based on stack_key (page 2 uses fixed isometric.jpeg)
    page2_image_path = os.path.join(_HERE, "isometric.jpeg")
    
    page3_image_filename = f"{stack_key}stack.png"
    page3_image_path = os.path.join(PAGE3_IMAGES_DIR, page3_image_filename)

    return {
    "customer_code": raw.get("customer_code", ""),
    "dwg_no":        raw.get("dwg_no", ""),
    "request_no":    raw.get("request_no", ""),
    "drawn_date":    raw.get("drawn_date", ""),

    "drawn_by":      "R.R.",
    "scale":         "N.T.S",
    "size":          "A3",

    "rev":           rev,
    "rev_history":   rev_history,

    "project_lines": raw.get("project_lines", [""]),
    "title_lines":   title_lines,

    "stack_key":     stack_key,
    "stack_label":   stack_label,

    "wide":          wide,
    "long":          long,

    "storage_m3":    storage,

    "parts_list":    raw.get("parts_list", []),

    "page2_image":   page2_image_path,
    "page3_image":   page3_image_path,



    # =====================================================
    # PLAN VIEW / ELEVATION VIEW
    # =====================================================

    "length": length_mm,
    "width": breadth_mm,

    "length_panels": long,
    "width_panels": wide,

    "panel_length": 1150,
    "panel_width": 1150,

    "levels": cfg["layers"],
    "height": cfg["stack_length"],

    "stack_number": cfg["stack_name"],
    "stack_length": cfg["stack_length"],

    "tank_storage": storage,

    # =====================================================
    # HARDCODED PLAN VIEW VALUES
    # =====================================================

    "excavation_clearance": 500,

    "cover_depth": 950,
    "minimum_cover_depth": 500,

    "fsl": 100.0,
    "base_rl": 97.0,

    # =====================================================
    # PIPE DATA  (from JSON inlets / outlets)
    # =====================================================

    "inlets":   _build_pipes(raw.get("inlets",  []), "INLET"),
    "outlets":  _build_pipes(raw.get("outlets", []), "OUTLET"),
    "manholes": _build_manholes(raw.get("manholes", [])),
    "pipes":    _build_pipes(raw.get("inlets", []), "INLET") +
                _build_pipes(raw.get("outlets", []), "OUTLET"),
}