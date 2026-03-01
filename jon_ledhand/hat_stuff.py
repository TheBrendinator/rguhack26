# This file will convert images to the sense hat displays as well as provide the ability to sync and connect across multiple sense hats

import itertools
import numpy as np
from PIL import Image
from typing import TypedDict


SINGLE_PI_RES_X: int = 8
SINGLE_PI_RES_Y: int = 8
node = TypedDict("node", {"x": int, "y": int, "colors": list[list[int]]})
np.set_printoptions(threshold=np.iinfo(np.int64).max)


def example_func(print_string: str):
        print(print_string)


def create_node_list(pi_count_x: int, pi_count_y: int):
        node_list: list[node] = []

        for i in range(pi_count_x):
                for j in range(pi_count_y):
                        temp_node: node = {
                                "x": i,
                                "y": j,
                                "colors": []
                        }
                        node_list.append(temp_node)
        image_res = [(pi_count_x * SINGLE_PI_RES_X), (pi_count_y * SINGLE_PI_RES_X)]
        return node_list, image_res


def load_image(image_location: str):
        return Image.open(image_location)


def resize_image(image, image_res):
        return image.resize((image_res[0],image_res[1]))


def get_image_as_array(image):
        return np.asarray(image)


def slice_image(frame = np.array([list[list[int]]]), node_list: list[node] = [], pi_count_x: int = 0, pi_count_y: int = 0): # type: ignore
        for ax in range(pi_count_x):
                for ay in range(pi_count_y):
                        for y in range(SINGLE_PI_RES_Y):
                                for x in range(SINGLE_PI_RES_X):
                                        vertical_offset: int = ay * SINGLE_PI_RES_Y
                                        horizontal_offset: int = ax * SINGLE_PI_RES_X
                                        pixel = frame[y + vertical_offset][x + horizontal_offset]
                                        red_channel = int(pixel[0])
                                        green_channel = int(pixel[1])
                                        blue_channel = int(pixel[2])
                                        for i in range(len(node_list)):
                                                if node_list[i]["x"] == ax and node_list[i]["y"] == ay:
                                                        node_list[i]["colors"].append((red_channel, green_channel, blue_channel))
        return node_list