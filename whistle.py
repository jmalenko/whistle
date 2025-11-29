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

with BuildPart() as part:
    with BuildSketch() as sketch:
        h2 = TOTAL_HEIGHT / 2
        Circle(h2)

        mouth = TOTAL_LENGTH - h2
        Rectangle(mouth, TOTAL_HEIGHT, align=(Align.MIN, Align.CENTER))

        Circle(h2 - HOLE_WALL_THICKNESS, mode=Mode.SUBTRACT)

        with Locations((mouth - CUTOUT_OFFSET, h2)):
            Polygon(
                (0, 0), 
                (0, -CUTOUT_HEIGHT), 
                (-CUTOUT_LENGTH, 0),
                align=(Align.MAX, Align.MAX), 
                mode=Mode.SUBTRACT)

        with Locations([
            (mouth - TOOTH_OFFSET, h2),
            (mouth - TOOTH_OFFSET, -h2+TOOTH_HEIGHT)
        ]):
            Rectangle(TOOTH_LENGTH, TOOTH_HEIGHT, 
                align=(Align.MAX, Align.MAX), 
                mode=Mode.SUBTRACT)
    
    extrude(amount=TOTAL_WIDTH)


export_step(part.part, "whistle.step")

show(part, reset_camera=False)

