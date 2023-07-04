import random
from drawsvg import Drawing, Circle, Rectangle
from typing import List, Tuple, Optional
from automatic_label_placement.config_reader import *
from automatic_label_placement.label_placement_utils import (
    reset_colors,
    box_within_boundary,
    calculate_overlaps,
)


def generate_label_boxes(
    random_points: List[Tuple[Circle, bool]],
    width: int = boundary_width,
    height: int = boundary_height,
    radius: int = point_radius,
    label_width: int = box_width,
    label_height: int = box_height,
    label_distance: int = box_point_distance,
) -> List[Rectangle]:
    """Generate label boxes for the selected points and the position of a box to the respective point
        is randomly generated.

    Args:
        random_points: A list of tuples where the first element of a tuple is a Circle object and
            the second element is a boolean indicating if the point is selected.
        width:  width of the boundary (default 2000).
        height: height of the boundary within which the points are generated (default 2000).
        radius: radius of each point (default 4).
        label_width: Width of the label boxes (default 88).
        label_height: Height of the label boxes (default 23).
        label_distance: Distance between the label boxes and the points (default 1).

    Returns:
        label_boxes: A list of label boxes.
    """

    label_boxes = []
    positions = ["right", "above", "below", "left"]

    for random_point, is_selected in random_points:
        x, y = random_point.args["cx"], random_point.args["cy"]

        if is_selected:
            position = random.choice(positions)

            while True:
                if position == "right":
                    label_x = x + radius + label_distance
                    label_y = y - label_height / 2
                elif position == "above":
                    label_x = x - label_width / 2
                    label_y = y + radius + label_distance
                elif position == "below":
                    label_x = x - label_width / 2
                    label_y = y - radius - label_distance - label_height
                else:  # Left
                    label_x = x - radius - label_distance - label_width
                    label_y = y - label_height / 2

                if box_within_boundary(label_x, label_y):
                    break

                position = random.choice(positions)

            label_box = Rectangle(
                label_x, label_y, label_width, label_height, fill="none", stroke="black"
            )
            label_boxes.append(label_box)

    return label_boxes


def find_red_boxes(d: Drawing) -> Tuple[List[int], List[int]]:
    """Find all the indexes of red boxes and their corresponding points in the given list of elements.

    Args:
        d: A Drawing object.

    Returns:
        A tuple with two lists:
            - red_box_indexes: A list of indexes of red boxes.
            - corresponding_point_indexes: A list of corresponding point indexes.
    """

    red_box_indexes = [
        index
        for index, element in enumerate(d.elements)
        if isinstance(element, Rectangle) and element.args.get("stroke") == "red"
    ]

    corresponding_point_indexes = [index + 1 for index in red_box_indexes]

    return red_box_indexes, corresponding_point_indexes


def process_position(
    d: Drawing,
    i: int,
    label_x: float,
    label_y: float,
) -> Optional[int]:
    """Process the position of a label within specified boundaries, update element positions, reset colors,
        and calculate overlaps.

    Args:
        d: A Drawing object.
        i: The index of the element in d.elements.
        label_x: The x-coordinate of the label.
        label_y: The y-coordinate of the label.

    Returns:
        Optional[int]: The total number of label overlaps and label-point overlaps, or
            None if the label is outside the boundaries.
    """

    if box_within_boundary(label_x, label_y):
        d.elements[i - 1].args["x"] = label_x
        d.elements[i - 1].args["y"] = label_y

        reset_colors(d)
        points = []
        boxes = []

        for j in range(1, len(d.elements)):
            element = d.elements[j]
            # A selected Circle object always goes after a Rectangle object
            if isinstance(element, Rectangle):
                boxes.append(element)
                points.append((d.elements[j + 1], True))
            else:
                points.append((d.elements[j], False))

        num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)

        return num_label_overlaps + num_label_point_overlaps
    else:
        return None


def move_red_boxes(
    d: Drawing,
    label_height: int = box_height,
    label_width: int = box_width,
    radius: int = point_radius,
    label_distance: int = box_point_distance,
) -> None:
    """Move red boxes around corresponding points to a position with minimal number
        of overlaps.

    Args:
        d: A Drawing object.
        label_height: The height of the label (default 23).
        label_width: The width of the label (default 88).
        radius: The radius of the points (default 4).
        label_distance: The distance between labels and points (default 1).
    """

    corresponding_point_indexes = find_red_boxes(d)[1]
    positions = ["right", "above", "below", "left"]

    for i in corresponding_point_indexes:
        x = d.elements[i].args["cx"]
        y = d.elements[i].args["cy"]
        label_positions = []

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

            result = process_position(d, i, label_x, label_y)
            if result is not None:
                label_positions.append((p, result, (label_x, label_y)))

        min_value = min(label_positions, key=lambda x: x[1])[1]
        min_positions = [pos for pos in label_positions if pos[1] == min_value]
        selected_position = random.choice(min_positions)
        process_position(
            d, i, float(selected_position[2][0]), float(selected_position[2][1])
        )
