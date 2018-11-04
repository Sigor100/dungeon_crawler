import os

# changeable
display_height = 800
display_width = 1600
fps = 30

# unchangeable
box_size = 32
backpack_width = 15
backpack_height = 7
directory = os.getcwd() + '/resources'

# colors
background = (0, 0, 0)
black = (0, 0, 0)
grey = (128, 128, 128)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# additional
directions = ([-1, -1], [0, -1], [1, -1], [-1, 0], [0, 0], [1, 0], [-1, 1], [0, 1], [1, 1])
#                NW        N        NE       W      Mid       E       SE       S       SE
dirnodiag = ((0, -1), (1, 0), (0, 1), (-1, 0))

