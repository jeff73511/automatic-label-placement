import random
from drawsvg import Drawing, Circle, Rectangle
import webbrowser
import os


WIDTH = 500
HEIGHT = 500
R = 1


def generate_random_points(
    num_points=1000, width=WIDTH, height=HEIGHT, radius=R, num_selected=200
):

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
    random_points,
    width=WIDTH,
    height=HEIGHT,
    radius=R,
    label_width=50,
    label_height=6,
    label_distance=1,
):

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

                if (  # if a box is cut by boundary
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


def calculate_overlaps(points, boxes):

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

        for point, _ in points:
            point_x, point_y = point.args["cx"], point.args["cy"]
            radius = point.args["r"]

            if (
                label_x < point_x + radius
                and label_x + label_width > point_x - radius
                and label_y < point_y + radius
                and label_y + label_height > point_y - radius
            ):
                num_label_point_overlaps += 1

    return num_label_overlaps, num_label_point_overlaps


points = generate_random_points()
boxes = generate_label_boxes(points)
num_label_overlaps, num_label_point_overlaps = calculate_overlaps(points, boxes)
print(f"Number of overlaps between labels: {num_label_overlaps}")
print(f"Number of overlaps between labels and points: {num_label_point_overlaps}")
print(f"Number of total overlaps: {num_label_overlaps + num_label_point_overlaps}")


d = Drawing(500, 500)

index = 0
for point in points:
    if point[1]:
        d.append(boxes[index])
        index += 1
    d.append(point[0])

d.set_render_size(700, 700)
d.save_svg("point_label_placement.svg")
webbrowser.open(f"file://{os.path.abspath('point_label_placement.svg')}")
