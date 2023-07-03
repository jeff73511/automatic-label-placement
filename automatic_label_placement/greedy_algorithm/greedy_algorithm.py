from automatic_label_placement.label_placement_utils import generate_random_points
from automatic_label_placement.local_search_algorithm.local_search_algorithm_processor import calculate_overlaps
from greedy_algorithm_processor import label_boxes_for_positions
from drawsvg import Drawing, Circle, Rectangle
import random
import webbrowser
import os
from automatic_label_placement.config_reader import *


d = Drawing(boundary_width, boundary_height)
boundary = Rectangle(
    0, 0, width=boundary_width, height=boundary_height, fill="none", stroke="black"
)
d.append(boundary)


points = generate_random_points()
for point in points:
    d.append(point[0])

boxes = []

for point in points:
    if point[1]:
        list_tuples = []
        boxes_for_positions = label_boxes_for_positions(selected_point=point)

        # Calculate the number of overlaps for each position
        for box in boxes_for_positions:
            if box is not None:
                num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes+[box])
                num_overlaps = num_label_overlaps + num_label_point_overlaps
            else:
                num_overlaps = None
            list_tuples.append((box, num_overlaps))

        # Add a box with minimal numer of overlaps
        list_tuples = [t for t in list_tuples if t[1] is not None]

        min_value = min(list_tuples, key=lambda x: x[1])[1]
        min_tuples = [t for t in list_tuples if t[1] == min_value]
        selected_tuple = random.choice(min_tuples)
        box = selected_tuple[0]
        boxes.append(box)
        box_location = d.elements.index(point[0])
        d.insert(box_location, box)

        for element in d.elements:
            if isinstance(element, Circle):
                element.args["fill"] = "black"
            elif isinstance(element, Rectangle):
                element.args["stroke"] = "black"

num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
d.set_render_size(pixel_size, pixel_size)
d.save_svg("greedy_algorithm.svg")
webbrowser.open(f"file://{os.path.abspath('greedy_algorithm.svg')}")
print(f"Numer of overlaps from greedy algorithm: {num_label_overlaps + num_label_point_overlaps}")
