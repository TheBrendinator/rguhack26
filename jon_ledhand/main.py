# This file will connect all the other python files. It should have effectively no direct interaction with the pi's

import hat_stuff as hs
import music_player as mp
import visualizer as v


def check_modules():
        hs.example_func("hat_stuff")
        mp.example_func("music_player")
        v.example_func("visualizer")


check_modules()