import random
from drawsvg import Drawing, Circle, Rectangle
from typing import List, Tuple
from .config_reader import *
from itertools import combinations


def generate_random_points(
    seed_value: int,
    num_points: int = num_points_generated,
    width: int = boundary_width,
    height: int = boundary_height,
    radius: int = point_radius,
    label_height: int = box_height,
    num_selected: int = num_points_selected,
) -> List[Tuple[Circle, bool]]:
    """Generate random points with a number of points randomly selected.
    Args:
        seed_value: Seed value for random number generation.
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

    original_state = random.getstate()
    random.seed(seed_value)

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

    random.setstate(original_state)

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


def box_within_boundary(
    label_x: float,
    label_y: float,
    label_width: int = box_width,
    label_height: int = box_height,
    width: int = boundary_width,
    height: int = boundary_height,
) -> bool:
    """Check if a box is within the boundary.

    Args:
        label_x: X-coordinate of the box.
        label_y: Y-coordinate of the box.
        label_width: Width of the label boxes (default 88).
        label_height: Height of the label boxes (default 23).
        width:  width of the boundary (default 2000).
        height: height of the boundary within which the points are generated (default 2000).

    Returns:
        True if the box is within the boundary, False otherwise.
    """

    return 0 <= label_x <= width - label_width and 0 <= label_y <= height - label_height


def calculate_overlaps(
    points: List[Tuple[Circle, bool]],
    boxes: List[Rectangle],
    radius: int = point_radius,
    label_width: int = box_width,
    label_height: int = box_height,
) -> int:
    """Calculate the number of overlaps between label boxes and between label boxes and points and
        color any overlaps red.

    Args:
        points: A list of tuples where the first element of a tuple is a Circle object and
            the second element is a boolean indicating if the point is selected.
        boxes: A list of label boxes.
        radius: The radius of the points (default 4).
        label_width: The width of the label (default 88).
        label_height: The height of the label (default 23).

    Returns:
        Number of overlaps between label boxes and between label boxes and points.
    """

    num_label_overlaps = 0
    num_label_point_overlaps = 0

    for box1, box2 in combinations(boxes, 2):
        bx1, by1 = box1.args["x"], box1.args["y"]
        bx2, by2 = box2.args["x"], box2.args["y"]

        if (
            bx1 < bx2 + label_width
            and bx1 + label_width > bx2
            and by1 < by2 + label_height
            and by1 + label_height > by2
        ):
            num_label_overlaps += 1
            box1.args["stroke"] = "red"
            box2.args["stroke"] = "red"

    for point, is_selected in points:
        px, py = point.args["cx"], point.args["cy"]

        for box in boxes:
            bx, by = box.args["x"], box.args["y"]

            if (
                bx < px + radius
                and bx + label_width > px - radius
                and by < py + radius
                and by + label_height > py - radius
            ):
                num_label_point_overlaps += 1
                box.args["stroke"] = "red"
                point.args["fill"] = "red"

    return num_label_overlaps + num_label_point_overlaps


def create_drawing(
    boundary_width: int = boundary_width,
    boundary_height: int = boundary_height,
    pixel_size: int = pixel_size,
):
    """Creates a Drawing object with a boundary rectangle and sets the render size.

    Args:
        boundary_width: Width of the boundary rectangle.
        boundary_height: Height of the boundary rectangle.
        pixel_size (int): Size of the rendering pixels.

    Returns:
        Drawing: A Drawing object.
    """

    d = Drawing(boundary_width, boundary_height)
    boundary = Rectangle(
        0, 0, width=boundary_width, height=boundary_height, fill="none", stroke="black"
    )
    d.append(boundary)
    d.set_render_size(pixel_size, pixel_size)

    return d


import random
from automatic_label_placement.config_reader import *
from typing import List


class Coordinates:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Point(Coordinates):
    radius = point_radius

    def __init__(self, x: float, y: float):
        super().__init__(x, y)


class LabelBox(Coordinates):
    width = box_width
    height = box_height

    def __init__(self, x: float, y: float):
        super().__init__(x, y)


class PointBoxGenerator:
    area_width = boundary_width
    area_height = boundary_height

    def __init__(self,
                 num_points=num_points_generated,
                 label_point_distance=box_point_distance):

        self.num_points = num_points
        self.label_point_distance = label_point_distance

        self.points: List[Point] = []
        self.label_boxes: List[LabelBox] = []

    def generate_points(self):

        if 2 * Point.radius >= LabelBox.height:
            y_start = Point.radius
            y_end = self.area_height - Point.radius
        else:
            y_start = LabelBox.height / 2
            y_end = self.area_height - LabelBox.height / 2

        for _ in range(self.num_points):
            x = random.uniform(Point.radius, self.area_width - Point.radius)
            y = random.uniform(y_start, y_end)
            point = Point(x, y)
            self.points.append(point)

    def add_a_label_box(self, selected_point: Point) -> LabelBox:

        pre_dir = None
        directions = ['right', 'above', 'below', 'left']
        while True:
            if pre_dir is not None:
                directions.remove(pre_dir)

            direction = random.choice(directions)

            if direction == 'right':
                x = selected_point.x + Point.radius + self.label_point_distance
                y = selected_point.y - (LabelBox.height / 2)
            elif direction == 'above':
                x = selected_point.x - (LabelBox.width / 2)
                y = selected_point.y + Point.radius + self.label_point_distance
            elif direction == 'below':
                x = selected_point.x - (LabelBox.width / 2)
                y = selected_point.y - Point.radius - self.label_point_distance - LabelBox.height
            else:  # Left
                x = selected_point.x - Point.radius - self.label_point_distance - LabelBox.width
                y = selected_point.y - (LabelBox.height / 2)

            # Check if a box is within the boundary.
            if 0 <= x <= self.area_width - LabelBox.width and 0 <= y <= self.area_height - LabelBox.height:
                break
            pre_dir = direction

        label_box_point = Coordinates(x, y)
        return LabelBox(label_box_point.x, label_box_point.y)

    def add_label_boxes(self, num_label_boxes=num_points_selected):

        selected_points = random.sample(self.points, num_label_boxes)

        for point in selected_points:
            label_box = self.add_a_label_box(selected_point=point)
            self.label_boxes.append(label_box)

    def print_label_boxes(self):
        for label_box in self.label_boxes:
            print(f"Label Box Point: ({label_box.x}, {label_box.y})")

        print(f"Total Label Boxes: {len(self.label_boxes)}")


# Create an instance of PointGenerator
generator = PointBoxGenerator()

# Generate random points
generator.generate_points()

# Add label boxes to a random selection of points
generator.add_label_boxes(200)

# Print the coordinates of the label boxes
generator.print_label_boxes()