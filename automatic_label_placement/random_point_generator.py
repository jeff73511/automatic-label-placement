import random
from drawsvg import Circle
from typing import List, Tuple
import configparser

import os

print(os.getcwd())
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


def generate_random_points(
    num_points: int = num_points_generated,
    width: int = boundary_width,
    height: int = boundary_height,
    radius: int = point_radius,
    num_selected: int = num_points_selected,
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
