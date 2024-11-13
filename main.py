import data_storage
from data_generator import simulate_data_stream
import threading
import asyncio
import websockets

# Start the data stream in a separate thread
thread = threading.Thread(target=simulate_data_stream, args=(10,))
thread.start()

orders = []
client_ws = None  # Global variable to hold the WebSocket connection

async def handle_data_generator(ws):
    async for message in ws:
        print("Received from data_generator:", message)
        await send_to_client(message)

async def send_to_client(message):
    global client_ws
    if client_ws is None:
        try:
            client_ws = await websockets.connect('ws://localhost:8766')  # Persistent connection
        except Exception as e:
            print(f"Failed to connect to client WebSocket: {e}")
            return

    try:
        await client_ws.send(message)
        response = await client_ws.recv()
        print("Received from client:", response)
        # store_order(response)
    except Exception as e:
        print(f"Error in communication with client WebSocket: {e}")
        client_ws = None  # Reset connection to try again next time

async def main():
    server = await websockets.serve(handle_data_generator, 'localhost', 8765)
    await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())
