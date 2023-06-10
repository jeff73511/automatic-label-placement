import random
from drawsvg import Drawing, Circle, Rectangle
import webbrowser

width, height = 500, 500
d = Drawing(width, height)

num_points = 10
radius = 1

# Randomly select 5 points
selected_points = random.sample(range(num_points), 5)

# Box dimensions
label_width = 50
label_height = 6
label_distance = 1

for i in range(num_points):
    x = random.uniform(radius, width - radius)
    y = random.uniform(radius, height - radius)
    point = Circle(x, y, radius, fill='black')

    # Check if the current point is in the selected points list
    if i in selected_points:
        # Randomly select a position for the label box
        position = random.choice(['right', 'above', 'below', 'left'])

        # Initialize label position variables
        label_x = None
        label_y = None

        while True:
            if position == 'right':
                label_x = x + radius + label_distance
                label_y = y - label_height / 2
            elif position == 'above':
                label_x = x - label_width / 2
                label_y = y + radius + label_distance
            elif position == 'below':
                label_x = x - label_width / 2
                label_y = y - radius - label_distance - label_height
            else:  # position == 'left'
                label_x = x - radius - label_distance - label_width
                label_y = y - label_height / 2

            # Check if the label box crosses the outer boundary
            if (
                label_x >= 0 and
                label_y >= 0 and
                label_x + label_width <= width and
                label_y + label_height <= height
            ):
                break  # Valid position found, exit the loop

            # Randomly choose another position
            position = random.choice(['right', 'above', 'below', 'left'])

        label_box = Rectangle(label_x, label_y, label_width, label_height, fill='none', stroke='black')
        d.append(label_box)

    d.append(point)

d.set_render_size(700, 700)  # pixel scale
d.save_svg('point_label_placement.svg')

webbrowser.open('point_label_placement.svg')