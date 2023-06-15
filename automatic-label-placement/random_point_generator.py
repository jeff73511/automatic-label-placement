import random
from drawsvg import Drawing, Circle, Rectangle
import webbrowser
import os
from typing import List, Tuple


def generate_random_points(
    num_points: int = 1000,
    width: int = 750,
    height: int = 750,
    radius: int = 1,
    num_selected: int = 200,
) -> List[Tuple[Circle, bool]]:
    """Generate random points with a number of points randomly selected.

    Args:
        num_points: Total number of random points to generate (default 1000).
        width:  width of the boundary (default 750).
        height: height of the boundary within which the points are generated (default 750).
        radius: radius of each point (default 1).
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
    width: int = 750,
    height: int = 750,
    radius: int = 1,
    label_width: int = 50,
    label_height: int = 6,
    label_distance: int = 1,
) -> List[Rectangle]:
    """Generate label boxes for the selected points.

    Args:
        random_points: A list of tuples where the first element of a tuple is a Circle object and
            the second element is a boolean indicating if the point is selected.
        width:  width of the boundary (default 750).
        height: height of the boundary within which the points are generated (default 750).
        radius: radius of each point (default 1).
        label_width: Width of the label boxes (default 50).
        label_height: Height of the label boxes (default 6).
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
                else:  # left
                    label_x = x - radius - label_distance - label_width
                    label_y = y - label_height / 2

                if (  # check if a box is cut by boundary
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

    # sort the results based on num_overlaps
    results.sort(key=lambda x: x[0])
    return results[0]


points = generate_random_points()
optimal_result = monte_carlo_simulation(points, 50)
print(f"Minimal num_overlaps: {optimal_result[0]}")


d = Drawing(750, 750)
boundary = Rectangle(0, 0, width=750, height=750, fill="none", stroke="black")
d.append(boundary)

# color the points and boxes of the optimal result from simulations
calculate_overlaps(points, optimal_result[1])
index = 0
for point in points:
    if point[1]:
        d.append(optimal_result[1][index])
        index += 1
    d.append(point[0])

d.set_render_size(750, 750)
d.save_svg("point_label_placement.svg")
webbrowser.open(f"file://{os.path.abspath('point_label_placement.svg')}")
