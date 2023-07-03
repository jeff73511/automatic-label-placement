from automatic_label_placement.label_placement_utils import generate_random_points, reset_colors
from local_search_algorithm_processor import (
    generate_label_boxes,
    calculate_overlaps,
    move_red_boxes,
)
from drawsvg import Drawing, Circle, Rectangle
import webbrowser
import os
from automatic_label_placement.config_reader import *

if __name__ == "__main__":
    points = generate_random_points()
    boxes = generate_label_boxes(points)
    num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
    print(f"Numer of overlaps from random placement: {num_label_overlaps + num_label_point_overlaps}")

    d = Drawing(boundary_width, boundary_height)
    boundary = Rectangle(
        0, 0, width=boundary_width, height=boundary_height, fill="none", stroke="black"
    )
    d.append(boundary)

    index = 0
    for point in points:
        if point[1]:
            d.append(boxes[index])
            index += 1
        d.append(point[0])

    d.set_render_size(pixel_size, pixel_size)
    d.save_svg("local_search_algorithm.svg")
    webbrowser.open(f"file://{os.path.abspath('local_search_algorithm.svg')}")

    min_num_overlaps = float("inf")
    converge = 0
    while True:
        move_red_boxes(d)
        # Reset box and point color to black
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

        d.save_svg("local_search_algorithm.svg")
        webbrowser.open(f"file://{os.path.abspath('local_search_algorithm.svg')}")
        print(
            f"Minimal numer of overlaps after moving red boxes: {num_label_overlaps + num_label_point_overlaps}"
        )

        if min_num_overlaps == num_label_overlaps + num_label_point_overlaps:
            converge += 1
            if converge == 4:
                break
        else:
            min_num_overlaps = num_label_overlaps + num_label_point_overlaps
            converge = 0
