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

# # Dictionary to track: {websocket: client_id}
# clients = {}

# async def handle_client(websocket, path):
#     """Handles client connections and ID registration"""
#     try:
#         # Client must send their ID FIRST (this is critical!)
#         client_id = await websocket.recv()
#         print(f"Client {client_id} connected ✅")
#         clients[websocket] = client_id  # Store ID with websocket
#     except Exception as e:
#         print(f"Connection error: {e}")
#         return

#     try:
#         # Process messages from client (optional)
#         async for message in websocket:
#             if message == "ping":
#                 await websocket.send(f"pong_{clients[websocket]}")
#     except websockets.ConnectionClosed:
#         pass

#     # Cleanup on disconnect
#     if websocket in clients:
#         del clients[websocket]

# async def broadcast_personalized_message(message_template: str):
#     """
#     Broadcasts a message to ALL connected clients,
#     with data personalized per client's ID.
    
#     Example template: "Hello {client_id}! Your special message: {special_content}"
#     """
#     for websocket, client_id in list(clients.items()):
#         try:
#             # Customize message for THIS client
#             personalized_message = message_template.format(
#                 client_id=client_id,
#                 special_content=f"Custom data for {client_id}"
#             )
            
#             # Send as JSON (recommended for real-world apps)
#             await websocket.send(json.dumps({
#                 "type": "personalized_broadcast",
#                 "message": personalized_message,
#                 "client_id": client_id
#             }))
#         except Exception as e:
#             print(f"Error sending to {client_id}: {e}")
#             # Remove disconnected clients
#             del clients[websocket]

# # Start server (port 8765)
# start_server = websockets.serve(handle_client, "localhost", :8765)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()