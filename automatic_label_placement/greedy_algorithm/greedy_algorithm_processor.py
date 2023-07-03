from automatic_label_placement.config_reader import *
from drawsvg import Circle, Rectangle
from typing import List, Tuple


def label_boxes_for_positions(
        selected_point: Tuple[Circle, bool],
        width: int = boundary_width,
        height: int = boundary_height,
        radius: int = point_radius,
        label_width: int = box_width,
        label_height: int = box_height,
        label_distance: int = box_point_distance,
) -> List[Rectangle]:
    """Generate a list of four label boxes for a selected point for each position.

    Args:
        selected_point: A tuple where the first element is a Circle object and
            the second element is a boolean indicating if the point is selected.
        width:  width of the boundary (default 2000).
        height: height of the boundary within which the points are generated (default 2000).
        radius: radius of each point (default 4).
        label_width: Width of the label boxes (default 88).
        label_height: Height of the label boxes (default 23).
        label_distance: Distance between the label boxes and the points (default 1).

    Returns:
        label_boxes: A list of four boxes for each position.
    """

    x, y = selected_point[0].args["cx"], selected_point[0].args["cy"]
    positions = ["right", "above", "below", "left"]
    label_boxes = []

    for p in positions:
        if p == "right":
            label_x = x + radius + label_distance
            label_y = y - label_height / 2
        elif p == "above":
            label_x = x - label_width / 2
            label_y = y + radius + label_distance
        elif p == "below":
            label_x = x - label_width / 2
            label_y = y - radius - label_distance - label_height
        else:
            label_x = x - radius - label_distance - label_width
            label_y = y - label_height / 2

        if (  # Check if a box is cut by boundary
            label_x >= 0
            and label_y >= 0
            and label_x + label_width <= width
            and label_y + label_height <= height
        ):
            label_boxes.append(
                Rectangle(label_x, label_y, label_width, label_height, fill="none", stroke="black")
            )
        else:
            label_boxes.append(None)

    return label_boxes

