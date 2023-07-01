import random
from drawsvg import Drawing, Circle, Rectangle
from typing import List, Tuple, Optional
import configparser


config = configparser.ConfigParser()
config.read("../config.ini")

pixel_size = config["PIXEL"].getint("pixel_size")

boundary_width = config["BOUNDARY"].getint("boundary_width")
boundary_height = config["BOUNDARY"].getint("boundary_height")

num_points_generated = config["POINT"].getint("num_points_generated")
num_points_selected = config["POINT"].getint("num_points_selected")
point_radius = config["POINT"].getint("point_radius")

box_width = config["LABEL"].getint("box_width")
box_height = config["LABEL"].getint("box_height")
box_point_distance = config["LABEL"].getint("box_point_distance")


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
    for random_point, is_selected in random_points:
        x, y = random_point.args["cx"], random_point.args["cy"]
        if is_selected:
            position = random.choice(["right", "above", "below", "left"])
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

                if (  # Check if a box is cut by boundary
                    label_x >= 0
                    and label_y >= 0
                    and label_x + label_width <= width
                    and label_y + label_height <= height
                ):
                    break

                position = random.choice(["right", "above", "below", "left"])

            label_box = Rectangle(
                label_x, label_y, label_width, label_height, fill="none", stroke="black"
            )
            label_boxes.append(label_box)

    return label_boxes


def calculate_overlaps(
    points: List[Tuple[Circle, bool]], boxes: List[Rectangle]
) -> Tuple[int, int]:
    """Calculate the number of overlaps between label boxes and between label boxes and points and
        color any overlaps red.

    Args:
        points: A list of tuples where the first element of a tuple is a Circle object and
            the second element is a boolean indicating if the point is selected.
        boxes: A list of label boxes.

    Returns:
        A tuple with two integers:
        - num_label_overlaps: Number of overlaps between label boxes.
        - num_label_point_overlaps: Number of overlaps between label boxes and points.
    """

    num_label_overlaps = 0
    num_label_point_overlaps = 0

    for i in range(len(boxes)):
        label_box = boxes[i]
        label_x, label_y = label_box.args["x"], label_box.args["y"]
        label_width, label_height = label_box.args["width"], label_box.args["height"]

        for j in range(i + 1, len(boxes)):
            other_box = boxes[j]
            other_x, other_y = other_box.args["x"], other_box.args["y"]
            other_width, other_height = (
                other_box.args["width"],
                other_box.args["height"],
            )

            if (
                label_x < other_x + other_width
                and label_x + label_width > other_x
                and label_y < other_y + other_height
                and label_y + label_height > other_y
            ):
                num_label_overlaps += 1
                label_box.args["stroke"] = "red"
                other_box.args["stroke"] = "red"

        for point, is_selected in points:
            point_x, point_y = point.args["cx"], point.args["cy"]
            radius = point.args["r"]

            if (
                label_x < point_x + radius
                and label_x + label_width > point_x - radius
                and label_y < point_y + radius
                and label_y + label_height > point_y - radius
            ):
                num_label_point_overlaps += 1
                label_box.args["stroke"] = "red"
                point.args["fill"] = "red"

    return num_label_overlaps, num_label_point_overlaps


def find_red_boxes(d: Drawing) -> Tuple[List[int], List[int]]:
    """Find all the indexes of red boxes and their corresponding points in the given list of elements.

    Args:
        d: A Drawing object.

    Returns:
        A tuple with two lists:
            - red_box_indexes: A list of indexes of red boxes.
            - corresponding_point_indexes: A list of corresponding point indexes.
    """

    red_box_indexes: List[int] = []
    corresponding_point_indexes: List[int] = []

    for index, element in enumerate(d.elements):
        if isinstance(element, Rectangle) and element.args.get("stroke") == "red":
            red_box_indexes.append(index)
            corresponding_point_indexes.append(index + 1)

    return red_box_indexes, corresponding_point_indexes


def process_position(
    d: Drawing,
    i: int,
    label_x: float,
    label_y: float,
    width: int = boundary_width,
    height: int = boundary_height,
    label_height: int = box_height,
    label_width: int = box_width,
) -> Optional[int]:
    """Process the position of a label within specified boundaries, update element positions, reset colors,
        and calculate overlaps.

    Args:
        d: A Drawing object.
        i: The index of the element in d.elements.
        label_x: The x-coordinate of the label.
        label_y: The y-coordinate of the label.
        width: The width of the boundaries (defaults 2000).
        height: The height of the boundaries (defaults 2000).
        label_height: The height of the label (defaults 23).
        label_width: The width of the label (defaults 88).

    Returns:
        Optional[int]: The total number of label overlaps and label-point overlaps, or
            None if the label is outside the boundaries.
    """

    if (  # Check if a box is cut by boundary
        label_x >= 0
        and label_y >= 0
        and label_x + label_width <= width
        and label_y + label_height <= height
    ):
        d.elements[i - 1].args["x"] = label_x
        d.elements[i - 1].args["y"] = label_y

        # Reset colors to black
        for element in d.elements:
            if isinstance(element, Circle):
                element.args["fill"] = "black"
            elif isinstance(element, Rectangle):
                element.args["stroke"] = "black"

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

        label_right = label_above = label_below = label_left = None
        for p in positions:
            if p == "right":
                label_x_right = x + radius + label_distance
                label_y_right = y - label_height / 2
                label_right = (
                    p,
                    process_position(d, i, label_x_right, label_y_right),
                    (label_x_right, label_y_right),
                )
            elif p == "above":
                label_x_above = x - label_width / 2
                label_y_above = y + radius + label_distance
                label_above = (
                    p,
                    process_position(d, i, label_x_above, label_y_above),
                    (label_x_above, label_y_above),
                )
            elif p == "below":
                label_x_below = x - label_width / 2
                label_y_below = y - radius - label_distance - label_height
                label_below = (
                    p,
                    process_position(d, i, label_x_below, label_y_below),
                    (label_x_below, label_y_below),
                )
            else:
                label_x_left = x - radius - label_distance - label_width
                label_y_left = y - label_height / 2
                label_left = (
                    p,
                    process_position(d, i, label_x_left, label_y_left),
                    (label_x_left, label_y_left),
                )

        list_tuples = [label_right, label_above, label_below, label_left]
        list_tuples = [t for t in list_tuples if t[1] is not None]
        min_value = min(list_tuples, key=lambda x: x[1])[1]
        min_tuples = [t for t in list_tuples if t[1] == min_value]
        selected_tuple = random.choice(min_tuples)
        process_position(d, i, float(selected_tuple[2][0]), float(selected_tuple[2][1]))
