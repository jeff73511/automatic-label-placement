import random
from drawsvg import Drawing, Circle, Rectangle
from typing import List, Tuple
from .config_reader import *


def generate_random_points(
        num_points: int = num_points_generated,
        width: int = boundary_width,
        height: int = boundary_height,
        radius: int = point_radius,
        label_height: int = box_height,
        num_selected: int = num_points_selected,
) -> List[Tuple[Circle, bool]]:
    """Generate random points with a number of points randomly selected.

    Args:
        num_points: Total number of random points to generate (default 1000).
        width:  width of the boundary (default 2000).
        height: height of the boundary within which the points are generated (default 2000).
        radius: radius of each point (default 4).
        label_height: Height of the label boxes (default 23).
        num_selected: Number of points to select from the generated random points (default 200).
    Returns:
        random_points: A list of tuples where the first element of a tuple is a Circle object and
        the second element is a boolean indicating if the point is selected.
    """

    random_points = []
    selected_points = random.sample(range(num_points), num_selected)

    if 2 * radius >= label_height:
        y_start = radius
        y_end = height - radius
    else:
        y_start = label_height / 2
        y_end = height - label_height / 2

    for i in range(num_points):
        x = random.uniform(radius, width - radius)
        y = random.uniform(y_start, y_end)
        point = Circle(x, y, radius, fill="black")

        random_points.append((point, i in selected_points))

    return random_points


def reset_colors(d: Drawing) -> None:
    """Reset the colors of Circle and Rectangle objects to black.

    Args:
        d: A Drawing object.
    """

    for element in d.elements:
        if isinstance(element, Circle):
            element.args["fill"] = "black"
        elif isinstance(element, Rectangle):
            element.args["stroke"] = "black"
