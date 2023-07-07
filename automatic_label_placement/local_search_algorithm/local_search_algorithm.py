from automatic_label_placement.label_placement_utils import (
    generate_random_points,
    reset_colors,
    calculate_overlaps,
)
from automatic_label_placement.local_search_algorithm.local_search_algorithm_processor import (
    generate_label_boxes,
    move_red_boxes,
)
from drawsvg import Drawing, Rectangle
import webbrowser
import os
import random
from automatic_label_placement.config_reader import *


def local_search_algorithm(seed_value: int) -> None:
    """Run the local search algorithm for label placement.

    Args:
        seed_value: The seed value for random number generation.
    """

    # Prepare the svg graph
    d = Drawing(boundary_width, boundary_height)
    boundary = Rectangle(
        0, 0, width=boundary_width, height=boundary_height, fill="none", stroke="black"
    )
    d.append(boundary)
    d.set_render_size(pixel_size, pixel_size)

    # Save the current state of the random number generator
    original_state = random.getstate()
    random.seed(seed_value)
    points = generate_random_points()
    random.setstate(original_state)
    boxes = generate_label_boxes(points)
    num_overlaps = calculate_overlaps(points, boxes)

    # A selected Circle object always goes after a Rectangle object
    for point, is_selected in points:
        if is_selected:
            d.append(boxes.pop(0))
        d.append(point)

    # Re-adjust the position of red boxes
    min_num_overlaps = float("inf")
    converge = 0
    while True:
        move_red_boxes(d)
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

        num_overlaps = calculate_overlaps(points, boxes)

        if min_num_overlaps == num_overlaps:
            converge += 1
            if converge == 4:
                print(f"Numer of overlaps from local search algorithm: {num_overlaps}")
                d.save_svg("local_search_algorithm.svg")
                webbrowser.open(
                    f"file://{os.path.abspath('local_search_algorithm.svg')}"
                )
                break
        else:
            min_num_overlaps = num_overlaps
            converge = 0


if __name__ == "__main__":
    local_search_algorithm(seed_value=seeds[0])
