# This file will connect all the other python files. It should have effectively no direct interaction with the pi's

import hat_stuff as hs
import music_player as mp
import visualizer as v
from typing import TypedDict
import numpy as np
from time import sleep
from PIL import ImageGrab

image_res: list[int]
node = TypedDict("node", {"x": int, "y": int, "colors": list[list[int]]})
node_list: list[node]
image = np.array([])

pi_count_x: int = 1
pi_count_y: int = 1



def check_modules():
        hs.example_func("hat_stuff")
        mp.example_func("music_player")
        v.example_func("visualizer")


# check_modules()


# Resize image and split across multiple pi's (nodes)
node_list, image_res = hs.create_node_list(pi_count_x,pi_count_y)


# The Frog
image = hs.load_image("jon_ledhand/frog.jpg")


# Resize and slice for pi's
image = hs.resize_image(image, image_res)
image = hs.get_image_as_array(image)
node_list = hs.slice_image(image, node_list, pi_count_x, pi_count_y)
