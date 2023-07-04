import configparser

config = configparser.ConfigParser()
config.read("../config.ini")

# PIXEL
pixel_size = config["PIXEL"].getint("pixel_size")

# BOUNDARY
boundary_width = config["BOUNDARY"].getint("boundary_width")
boundary_height = config["BOUNDARY"].getint("boundary_height")

# POINT
num_points_generated = config["POINT"].getint("num_points_generated")
num_points_selected = config["POINT"].getint("num_points_selected")
point_radius = config["POINT"].getint("point_radius")

# LABEL
box_width = config["LABEL"].getint("box_width")
box_height = config["LABEL"].getint("box_height")
box_point_distance = config["LABEL"].getint("box_point_distance")

# CONVERGE
num_converge = config["CONVERGE"].getint("num_converge")
