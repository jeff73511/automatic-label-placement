from automatic_label_placement.label_placement_utils import (
    generate_random_points,
    reset_colors,
    calculate_overlaps,
)
from local_search_algorithm_processor import (
    generate_label_boxes,
    move_red_boxes,
)
from drawsvg import Drawing, Rectangle
import webbrowser
import os
from automatic_label_placement.config_reader import *

if __name__ == "__main__":
    # Prepare the svg graph
    d = Drawing(boundary_width, boundary_height)
    boundary = Rectangle(
        0, 0, width=boundary_width, height=boundary_height, fill="none", stroke="black"
    )
    d.append(boundary)
    d.set_render_size(pixel_size, pixel_size)

    points = generate_random_points()
    boxes = generate_label_boxes(points)
    num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
    print(
        f"Numer of overlaps from random placement: {num_label_overlaps + num_label_point_overlaps}"
    )
    # A selected Circle object always goes after a Rectangle object
    for point, is_selected in points:
        if is_selected:
            d.append(boxes.pop(0))
        d.append(point)

    d.save_svg("local_search_algorithm.svg")
    webbrowser.open(f"file://{os.path.abspath('local_search_algorithm.svg')}")
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

        num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
        print(
            f"Minimal numer of overlaps after moving red boxes: {num_label_overlaps + num_label_point_overlaps}"
        )

        d.save_svg("local_search_algorithm.svg")
        webbrowser.open(f"file://{os.path.abspath('local_search_algorithm.svg')}")

        if min_num_overlaps == num_label_overlaps + num_label_point_overlaps:
            converge += 1
            if converge == 4:
                break
        else:
            min_num_overlaps = num_label_overlaps + num_label_point_overlaps
            converge = 0
