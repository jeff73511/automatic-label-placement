from automatic_label_placement.label_placement_utils import (
    generate_random_points,
    reset_colors,
    create_drawing
)
from automatic_label_placement.local_search_algorithm.local_search_algorithm_processor import (
    calculate_overlaps,
)
from automatic_label_placement.greedy_algorithm.greedy_algorithm_processor import (
    label_boxes_for_positions,
)
import random
import webbrowser
import os
from automatic_label_placement.config_reader import *


def greedy_algorithm(seed_value: int) -> None:
    """Run the greedy algorithm for label placement.

    Args:
        seed_value: Seed value for random number generation.
    """

    # Prepare the svg graph
    d = create_drawing()

    points = generate_random_points(seed_value)

    for point in points:
        d.append(point[0])

    boxes = []
    # Add a box with minimal numer of overlaps
    for point in points:
        if point[1]:
            list_tuples = []
            boxes_for_positions = label_boxes_for_positions(selected_point=point)

            # Calculate the number of overlaps for each position
            for box in boxes_for_positions:
                num_overlaps = (
                    calculate_overlaps(points, boxes + [box])
                    if box is not None
                    else None
                )
                list_tuples.append((box, num_overlaps))

            list_tuples = [t for t in list_tuples if t[1] is not None]
            min_value = min(list_tuples, key=lambda x: x[1])[1]
            selected_tuple = random.choice(
                [t for t in list_tuples if t[1] == min_value]
            )
            box = selected_tuple[0]
            boxes.append(box)
            box_location = d.elements.index(point[0])
            d.insert(box_location, box)

            reset_colors(d)

    num_overlaps = calculate_overlaps(points, boxes)
    print(f"Numer of overlaps from greedy algorithm: {num_overlaps}")
    d.save_svg("greedy_algorithm.svg")
    webbrowser.open(f"file://{os.path.abspath('greedy_algorithm.svg')}")


if __name__ == "__main__":
    greedy_algorithm(seed_value=seeds[0])
