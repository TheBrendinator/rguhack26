import asyncio
import websockets
import json
from sense_hat import SenseHat
from time import sleep


s = SenseHat()


async def connect_to_server():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        id: int = 0

        # Send an ID to the server
        await websocket.send(json.dumps({"id": id}))
        
        # Receive data from the server
        response = await websocket.recv()
        s.set_pixels(response["colors"])

while True:
        sleep(0.01)
        asyncio.run(connect_to_server())