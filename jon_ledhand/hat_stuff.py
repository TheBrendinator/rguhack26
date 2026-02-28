# This file will convert images to the sense hat displays as well as provide the ability to sync and connect across multiple sense hats


SINGLE_PI_RES_X: int = 8
SINGLE_PI_RES_Y: int = 8
node_list: list[dict[str,int]] = []
image_res: list[int] = [SINGLE_PI_RES_X,SINGLE_PI_RES_Y]


def example_func(print_string: str):
        print(print_string)


def create_node_list(pi_count_x: int, pi_count_y: int):
        for i in range(pi_count_x):
                for j in range(pi_count_y):
                        node: dict[str,int] = {
                                "x": i,
                                "y": j,
                        }
                        node_list.append(node)
        image_res = [(pi_count_x * SINGLE_PI_RES_X) + (pi_count_y * SINGLE_PI_RES_X)]
        return node_list, image_res