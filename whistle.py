from build123d import *
from ocp_vscode import show

# Dimensions
TOTAL_LENGTH = 48.0 # mm
TOTAL_WIDTH = 10.0
TOTAL_HEIGHT = TOTAL_WIDTH

WALL_THICKNESS = 1.2

HOLE_WALL_THICKNESS = 2.0
HOLE_DIAMETER = 10.0

CUTOUT_HEIGHT = TOTAL_HEIGHT * 0.4
CUTOUT_LENGTH = 6
CUTOUT_OFFSET = 13

TOOTH_OFFSET = 1
TOOTH_HEIGHT = 0.8
TOOTH_LENGTH = 2

TUNNEL_mouth_x_RADIUS = TOTAL_WIDTH / 2 - WALL_THICKNESS
TUNNEL_CUTOUT_LENGTH = 2
TUNNEL_CUTOUT_HEIGHT = 1.5
TUNNEL_CUTOUT_WIDTH = TOTAL_WIDTH - 2 * WALL_THICKNESS - 2 * 1

assert TUNNEL_CUTOUT_LENGTH < CUTOUT_OFFSET, "Tunnel cutout too long!"

with BuildPart() as whistle:
    h2 = TOTAL_HEIGHT / 2
    hole_r = h2 - HOLE_WALL_THICKNESS
    mouth_x = TOTAL_LENGTH - h2
    cutout_x = mouth_x - CUTOUT_OFFSET

    # Body

    with BuildSketch() as sketch:
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

    # Inner space

    h3 = TOTAL_HEIGHT / 2 - WALL_THICKNESS
    with BuildSketch(Plane.XY.offset(WALL_THICKNESS)) as sketch:
        inner_x = hole_r + WALL_THICKNESS + h3
        with Locations((inner_x, 0)):
            Circle(h3)
            Rectangle(cutout_x - inner_x, 2 * h3, 
                      align=(Align.MIN, Align.CENTER))

    extrude(amount=TOTAL_WIDTH - 2*WALL_THICKNESS, mode=Mode.SUBTRACT)

    # Tunnel - straight by cutout
    with BuildSketch(Plane.YZ.offset(cutout_x)) as sketch:
        with Locations((h2 - WALL_THICKNESS, h2)):
            Rectangle(TUNNEL_CUTOUT_HEIGHT, TUNNEL_CUTOUT_WIDTH,
                      align=(Align.MAX, Align.CENTER))

    extrude(amount=TUNNEL_CUTOUT_LENGTH, mode=Mode.SUBTRACT)

    # Tunnel - loft
    tunnel_start_face = whistle.faces().filter_by(Plane.YZ.offset(cutout_x - TUNNEL_CUTOUT_LENGTH)).sort_by(Axis.X)[1]

    circle_wire = Wire.make_circle(
        TUNNEL_mouth_x_RADIUS, 
        plane=Plane(origin=(mouth_x, 0, h2), x_dir=(0, 1, 0), z_dir=(1, 0, 0))
    )
    circle_face = Face(circle_wire)

    loft(sections=[tunnel_start_face, circle_face], mode=Mode.SUBTRACT)


export_step(whistle.part, "whistle.step")

show(whistle, reset_camera=False)

