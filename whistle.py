from build123d import *
from ocp_vscode import show
from math import *
import sys

# Dimensions
TOTAL_LENGTH = 48.0 # mm
TOTAL_WIDTH = 10.0
TOTAL_HEIGHT = TOTAL_WIDTH

WALL_THICKNESS = 1.2

HOLE_WALL_THICKNESS = 2.0
HOLE_DIAMETER = TOTAL_HEIGHT - 2 * HOLE_WALL_THICKNESS

CUTOUT_HEIGHT = TOTAL_HEIGHT * 0.4
CUTOUT_LENGTH = 6
CUTOUT_OFFSET = 13

TOOTH_OFFSET = 1
TOOTH_HEIGHT = 0.8
TOOTH_LENGTH = 2

TUNNEL_MOUTH_X_RADIUS = TOTAL_WIDTH / 2 - WALL_THICKNESS
TUNNEL_CUTOUT_LENGTH = 2
TUNNEL_CUTOUT_HEIGHT = 1.5
TUNNEL_CUTOUT_WIDTH = TOTAL_WIDTH - 2 * WALL_THICKNESS - 2 * 1

CHAMFER = 1.0
CHAMFER_INNER = (CHAMFER * sqrt(2) / 2 + WALL_THICKNESS - WALL_THICKNESS * sqrt(2)) * sqrt(2) # Chamfer to ensure min wall thickness in corners
HOLE_CHAMFER = 0.6

NAME_SIZE = TOTAL_HEIGHT * 0.6 # Default name size. If the name is too long,the size will be reduced to fit.
NAME_MARGIN = 0.4
NAME_EXTRUDE_HEIGHT = 0.4

name = sys.argv[1] if len(sys.argv) > 1 else None
if not name: name = "N A M E" # For demo purposes

EPSILON = 1e-3


assert TUNNEL_CUTOUT_LENGTH < CUTOUT_OFFSET, "Tunnel cutout too long!"


def find_colinear_edges(part, reference_edges, tolerance=0.01):
    collinear_edges = []
    for ref_edge in reference_edges:
        ref_pos = ref_edge @ 0.5  # midpoint
        for edge in part.edges():
            edge_pos = edge @ 0.5
            if abs(edge_pos.Y - ref_pos.Y) < tolerance and abs(edge_pos.Z - ref_pos.Z) < tolerance:
                collinear_edges.append(edge)
    return list(set(collinear_edges))

with BuildPart() as whistle:
    h2 = TOTAL_HEIGHT / 2
    hole_r = h2 - HOLE_WALL_THICKNESS
    mouth_x = TOTAL_LENGTH - h2
    cutout_x = mouth_x - CUTOUT_OFFSET

    # Body

    with BuildSketch() as side_sketch:
        Circle(h2)

        Rectangle(mouth_x, TOTAL_HEIGHT, align=(Align.MIN, Align.CENTER))

        Circle(hole_r, mode=Mode.SUBTRACT)

        with Locations((cutout_x, h2)):
            Polygon(
                (0, 0), 
                (0, -CUTOUT_HEIGHT), 
                (-CUTOUT_LENGTH, 0),
                align=(Align.MAX, Align.MAX), 
                mode=Mode.SUBTRACT)

        # Cutout for teeth
        with Locations([
            (mouth_x - TOOTH_OFFSET, h2),
            (mouth_x - TOOTH_OFFSET, -h2+TOOTH_HEIGHT)
        ]):
            Rectangle(TOOTH_LENGTH, TOOTH_HEIGHT, 
                align=(Align.MAX, Align.MAX), 
                mode=Mode.SUBTRACT)
    
    extrude(amount=TOTAL_WIDTH)

    # Save the circular hole edges from the extrusion
    hole_edges = []
    for e in whistle.edges():
        if e.geom_type == GeomType.CIRCLE:
            if e.radius == hole_r:
                hole_edges.append(e)

    # Inner space

    h3 = TOTAL_HEIGHT / 2 - WALL_THICKNESS
    with BuildSketch(Plane.XY.offset(WALL_THICKNESS)) as inner_sketch:
        inner_x = hole_r + WALL_THICKNESS + h3
        with Locations((inner_x, 0)):
            Circle(h3)
            Rectangle(cutout_x - inner_x, 2 * h3, 
                      align=(Align.MIN, Align.CENTER))

    extrude(amount=TOTAL_WIDTH - 2*WALL_THICKNESS, mode=Mode.SUBTRACT)

    # Tunnel - straight by cutout
    with BuildSketch(Plane.YZ.offset(cutout_x)) as tunnel_sketch:
        with Locations((h2 - WALL_THICKNESS, h2)):
            Rectangle(TUNNEL_CUTOUT_HEIGHT, TUNNEL_CUTOUT_WIDTH,
                      align=(Align.MAX, Align.CENTER))

    extrude(amount=TUNNEL_CUTOUT_LENGTH, mode=Mode.SUBTRACT)

    # Tunnel - loft
    tunnel_start_face = whistle.faces().filter_by(Plane.YZ.offset(cutout_x - TUNNEL_CUTOUT_LENGTH)).sort_by(Axis.X)[1]

    circle_wire = Wire.make_circle(
        TUNNEL_MOUTH_X_RADIUS, 
        plane=Plane(origin=(mouth_x, 0, h2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    )
    circle_face = Face(circle_wire)

    loft(sections=[tunnel_start_face, circle_face], mode=Mode.SUBTRACT)

    # Chamfer

    # Chamfer the long outside edges
    # Get the 4 longest edges parallel to X axis
    longest_edges = whistle.edges().filter_by(Axis.X).sort_by(SortBy.LENGTH)[-4:]
    chamfer_edges = find_colinear_edges(whistle.part, longest_edges)
    # Filter out edges that are too short for chamfering
    chamfer_edges = [e for e in chamfer_edges if 2*CHAMFER < e.length]
    chamfer(chamfer_edges, length=CHAMFER)

    # Chamfer the inner edges - this needed to ensure wall thiskness in the corners
    # Filter edges that are in the middle (not on top or bottom faces)
    inner_edges = whistle.edges().filter_by(Axis.X)
    inner_edges = [e for e in inner_edges if WALL_THICKNESS - EPSILON < (e @ 0.5).Z < TOTAL_WIDTH - WALL_THICKNESS + EPSILON]
    # To avoid chamfering short edges in the tunnel
    inner_edges = [e for e in inner_edges if TUNNEL_CUTOUT_LENGTH + EPSILON< e.length]
    chamfer(inner_edges, length=CHAMFER_INNER)

    # Chamfer the circular hole edges
    chamfer(hole_edges, length=HOLE_CHAMFER)

    # Add name text if provided
    
    if name:
        text_min_x = HOLE_DIAMETER / 2 + HOLE_CHAMFER
        
        # Start with desired font size and reduce until text fits
        font_size = NAME_SIZE
        font="Arial"
        font_style=FontStyle.BOLD 
        
        while font_size > 1:
            temp_text = Compound.make_text(
                name, 
                font_size=font_size, 
                font=font, 
                font_style=font_style
            )
            text_bbox = temp_text.bounding_box()
            text_width = text_bbox.max.X - text_bbox.min.X
            text_height = text_bbox.max.Y - text_bbox.min.Y

            margin = (TOTAL_HEIGHT - text_height) / 2
            text_max_x = cutout_x - CUTOUT_LENGTH + CUTOUT_LENGTH * margin / CUTOUT_HEIGHT
            available_width = text_max_x - text_min_x - 2 * NAME_MARGIN

            if text_width <= available_width:
                break
            else:
                font_size -= 0.1
        
        print(f"Using font size {font_size:.1f} for name '{name}'")
        text_center_x = text_min_x + (text_max_x - text_min_x) / 2

        with BuildSketch(Plane.XY.offset(TOTAL_HEIGHT)):
            with Locations((text_center_x, 0)):
                Text(name, font_size=font_size, font=font, font_style=font_style, 
                    align=(Align.CENTER, Align.CENTER))

        extrude(amount=NAME_EXTRUDE_HEIGHT)


export_step(whistle.part, "whistle.step")

show(whistle, reset_camera=False)

