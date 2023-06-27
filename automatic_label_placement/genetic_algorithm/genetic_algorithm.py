from automatic_label_placement.random_point_generator import generate_random_points
from genetic_algorithm_processor import (
    generate_label_boxes,
    calculate_overlaps,
    move_red_boxes,
)
from drawsvg import Drawing, Circle, Rectangle
import webbrowser
import os
import configparser

if __name__ == "__main__":
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

    num_converge = config["CONVERGE"].getint("num_converge")

    points = generate_random_points()
    boxes = generate_label_boxes(points)
    num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
    num_overlaps = num_label_overlaps + num_label_point_overlaps
    print(f"Numer of overlaps from random placement: {num_overlaps}")

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
    d.save_svg("genetic_algorithm.svg")
    webbrowser.open(f"file://{os.path.abspath('genetic_algorithm.svg')}")

    min_num_overlaps = float("inf")
    converge = 0
    while True:
        move_red_boxes(d)
        # Reset box and point color to black
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

        d.save_svg("genetic_algorithm.svg")
        webbrowser.open(f"file://{os.path.abspath('genetic_algorithm.svg')}")
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
