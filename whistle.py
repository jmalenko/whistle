from build123d import *
from ocp_vscode import show

# Dimensions from drawing
TOTAL_LENGTH = 48.0 # mm
TOTAL_HEIGHT = 10.0
LEFT_CIRCLE_DIAMETER = 10.0
MIDDLE_CIRCLE_DIAMETER = 10.0
STEP_WIDTH = 6.0
STEP_HEIGHT = 0.7
TOP_NOTCH_WIDTH = 13.0
TOP_NOTCH_HEIGHT = 2.0
RIGHT_NOTCH_WIDTH = 2.0
RIGHT_NOTCH_HEIGHT = 1.0
EXTRUSION_DEPTH = 20.0

# Calculate positions
left_circle_radius = LEFT_CIRCLE_DIAMETER / 2
middle_circle_radius = MIDDLE_CIRCLE_DIAMETER / 2
center_y = TOTAL_HEIGHT / 2

with BuildPart() as part:
    with BuildSketch() as sketch:
        # Main body outline
        with BuildLine() as outline:
            # Start from bottom left of main rectangle
            l1 = Line((left_circle_radius, 0), (TOTAL_LENGTH, 0))
            l2 = Line(l1 @ 1, (TOTAL_LENGTH, TOTAL_HEIGHT))
            l3 = Line(l2 @ 1, (left_circle_radius, TOTAL_HEIGHT))
            l4 = Line(l3 @ 1, l1 @ 0)
        
        make_face()
        
        # Add left circle
        with Locations((left_circle_radius, center_y)):
            Circle(left_circle_radius)
        
        # Add middle circle (estimated position around 1/4 of length)
        with Locations((TOTAL_LENGTH / 4, center_y)):
            Circle(middle_circle_radius)
    
    extrude(amount=EXTRUSION_DEPTH)
    
    # # Add step on top left
    # with BuildSketch(Plane.XY.offset(EXTRUSION_DEPTH)):
    #     with Locations((TOTAL_LENGTH - TOP_NOTCH_WIDTH - STEP_WIDTH, TOTAL_HEIGHT)):
    #         Rectangle(STEP_WIDTH, STEP_HEIGHT, align=(Align.MIN, Align.MIN))
    # extrude(amount=-STEP_HEIGHT)
    
    # # Add top notch
    # with BuildSketch(Plane.XY.offset(EXTRUSION_DEPTH)):
    #     with Locations((TOTAL_LENGTH - TOP_NOTCH_WIDTH, TOTAL_HEIGHT)):
    #         Rectangle(TOP_NOTCH_WIDTH, TOP_NOTCH_HEIGHT, align=(Align.MIN, Align.MIN))
    # extrude(amount=-TOP_NOTCH_HEIGHT)
    
    # # Add right side notch
    # with BuildSketch(Plane.XY.offset(EXTRUSION_DEPTH)):
    #     with Locations((TOTAL_LENGTH - RIGHT_NOTCH_WIDTH, TOTAL_HEIGHT - RIGHT_NOTCH_HEIGHT)):
    #         Rectangle(RIGHT_NOTCH_WIDTH, RIGHT_NOTCH_HEIGHT, align=(Align.MIN, Align.MIN))
    # extrude(amount=-RIGHT_NOTCH_HEIGHT)

export_step(part.part, "whistle.step")

show(part)

