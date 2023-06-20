import random
from drawsvg import Drawing, Circle, Rectangle
import webbrowser
import os
from typing import List, Tuple


def generate_random_points(
    num_points: int = 1000,
    width: int = 2000,
    height: int = 2000,
    radius: int = 4,
    num_selected: int = 200,
) -> List[Tuple[Circle, bool]]:
    """Generate random points with a number of points randomly selected.

    Args:
        num_points: Total number of random points to generate (default 1000).
        width:  width of the boundary (default 2000).
        height: height of the boundary within which the points are generated (default 2000).
        radius: radius of each point (default 4).
        num_selected: Number of points to select from the generated random points (default 200).
    Returns:
        random_points: A list of tuples where the first element of a tuple is a Circle object and
        the second element is a boolean indicating if the point is selected.
    """

    random_points = []
    selected_points = random.sample(range(num_points), num_selected)

    for i in range(num_points):
        x = random.uniform(radius, width - radius)
        y = random.uniform(radius, height - radius)
        point = Circle(x, y, radius, fill="black")

        if i in selected_points:
            random_points.append((point, True))
        else:
            random_points.append((point, False))

    return random_points


def generate_label_boxes(
    random_points: List[Tuple[Circle, bool]],
    width: int = 2000,
    height: int = 2000,
    radius: int = 4,
    label_width: int = 88,
    label_height: int = 23,
    label_distance: int = 1,
) -> List[Rectangle]:
    """Generate label boxes for the selected points.

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
    """Calculate the number of overlaps between label boxes and between label boxes and points.

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


def monte_carlo_simulation(
    points: List[Tuple[Circle, bool]], num_sim: int = 10
) -> tuple[int, list[Rectangle]]:
    """Perform a Monte Carlo simulation to find the optimal configuration of label boxes.

    Args:
        points: A list of tuples where the first element of a tuple is a Circle object and
            the second element is a boolean indicating if the point is selected.
        num_sim: The number of simulations to perform (default 10).

    Returns:
        A tuple with two elements:
        - num_overlaps: Minimal number of overlaps found in the simulations.
        - boxes: A list of label boxes.
    """

    results = []
    for _ in range(num_sim):
        boxes = generate_label_boxes(points)

        if any(boxes == result[1] for result in results):
            boxes = generate_label_boxes(points)

        num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
        num_overlaps = num_label_overlaps + num_label_point_overlaps
        results.append((num_overlaps, boxes))

        for point, _ in points:
            point.args["fill"] = "black"

    # Sort the results based on num_overlaps
    results.sort(key=lambda x: x[0])
    return results[0]


points = generate_random_points()
optimal_result = monte_carlo_simulation(points, 100)
print(f"Minimal num_overlaps: {optimal_result[0]}")


d = Drawing(2000, 2000)
boundary = Rectangle(0, 0, width=2000, height=2000, fill="none", stroke="black")
d.append(boundary)

# Color the points and boxes of the optimal result from simulations
calculate_overlaps(points, optimal_result[1])
index = 0
for point in points:
    if point[1]:
        d.append(optimal_result[1][index])
        index += 1
    d.append(point[0])

d.set_render_size(740, 740)
d.save_svg("point_label_placement.svg")
webbrowser.open(f"file://{os.path.abspath('point_label_placement.svg')}")

# Find all the indexes of red boxes and their corresponding points in d
red_box_indexes = []
corresponding_point_indexes = []

for index, element in enumerate(d.elements):
    if isinstance(element, Rectangle) and element.args.get("stroke") == "red":
        red_box_indexes.append(index)
        corresponding_point_indexes.append(index + 1)


positions = ["right", "above", "below", "left"]
radius = 4
label_distance = 1
label_height = 23
label_width = 88
width = height = 2000


def process_position(label_x, label_y):
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


for i in corresponding_point_indexes:
    x = d.elements[i].args["cx"]
    y = d.elements[i].args["cy"]

    label_right = label_above = label_below = label_left = None
    for p in positions:
        if p == "right":
            label_x_right = x + radius + label_distance
            label_y_right = y - label_height / 2
            label_right = (p, process_position(label_x_right, label_y_right), (label_x_right, label_y_right))
        elif p == "above":
            label_x_above = x - label_width / 2
            label_y_above = y + radius + label_distance
            label_above = (p, process_position(label_x_above, label_y_above), (label_x_above, label_y_above))
        elif p == "below":
            label_x_below = x - label_width / 2
            label_y_below = y - radius - label_distance - label_height
            label_below = (p, process_position(label_x_below, label_y_below), (label_x_below, label_y_below))
        else:
            label_x_left = x - radius - label_distance - label_width
            label_y_left = y - label_height / 2
            label_left = (p, process_position(label_x_left, label_y_left), (label_x_left, label_y_left))

    tuples = [label_right, label_above, label_below, label_left]
    tuples = [t for t in tuples if t[1] is not None]
    min_value = min(tuples, key=lambda x: x[1])[1]
    min_tuples = [t for t in tuples if t[1] == min_value]
    selected_tuple = random.choice(min_tuples)

    process_position(selected_tuple[2][0], selected_tuple[2][1])

    # d.save_svg("point_label_placement.svg")
    # webbrowser.open(f"file://{os.path.abspath('point_label_placement.svg')}")

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
        points.append((d.elements[j+1], True))
    else:
        points.append((d.elements[j], False))

num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)

d.save_svg("point_label_placement.svg")
webbrowser.open(f"file://{os.path.abspath('point_label_placement.svg')}")
print(f"Minimal num_overlaps after adjustment: {num_label_overlaps + num_label_point_overlaps}")