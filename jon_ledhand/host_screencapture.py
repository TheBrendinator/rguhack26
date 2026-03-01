# This file will connect all the other python files. It should have effectively no direct interaction with the pi's

import hat_stuff as hs
# import music_player as mp
# import visualizer as v
from typing import TypedDict
import numpy as np
from time import sleep
from PIL import ImageGrab
import asyncio
import websockets
import json

image_res: list[int] = []
node = TypedDict("node", {"x": int, "y": int, "colors": list[list[int]]})
node_list: list[node] = []
image = np.array([])


clients = {}

# Function to handle each client connection
async def handle_client(websocket):

        # Forces updates on a rate of 10ms
        sleep(0.01)

        pi_count_x: int = 1
        pi_count_y: int = 1

        # Resize image and split across multiple pi's (nodes)
        node_list, image_res = hs.create_node_list(pi_count_x,pi_count_y)

        # Screencapture
        image = ImageGrab.grab()

        # Resize and slice for pi's
        image = hs.resize_image(image, image_res)
        image = hs.get_image_as_array(image)
        node_list = hs.slice_image(image, node_list, pi_count_x, pi_count_y)

        # Store the new client in the dictionary
        clients[websocket] = await websocket.recv()
        print(f"New client connected: {clients[websocket]}")

        client = json.loads(clients[websocket])
        client["colors"] = node_list[client["id"]]["colors"]
        await websocket.send(json.dumps(client))


# Main function to start the WebSocket server
async def main():

        server = await websockets.serve(handle_client, 'localhost', 8765)
        await server.wait_closed()


# Run the server
if __name__ == "__main__":
        asyncio.run(main())