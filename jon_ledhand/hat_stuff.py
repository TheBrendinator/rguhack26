# This file will convert images to the sense hat displays as well as provide the ability to sync and connect across multiple sense hats

from typing import TypedDict
import itertools

SINGLE_PI_RES_X: int = 8
SINGLE_PI_RES_Y: int = 8
node = TypedDict("node", {"x": int, "y": int, "colors": list[list[int]]})
node_list: list[node] = []
image_res: list[int] = [SINGLE_PI_RES_X,SINGLE_PI_RES_Y]


def example_func(print_string: str):
        print(print_string)


def create_node_list(pi_count_x: int, pi_count_y: int):
        colors: list[list[int]] = list(itertools.repeat([255,255,255], SINGLE_PI_RES_X * SINGLE_PI_RES_Y))
        for i in range(pi_count_x):
                for j in range(pi_count_y):
                        temp_node: node = {
                                "x": i,
                                "y": j,
                                "colors": colors
                        }
                        node_list.append(temp_node)
        image_res = [(pi_count_x * SINGLE_PI_RES_X) + (pi_count_y * SINGLE_PI_RES_X)]
        return node_list, image_res