import time
import asyncio
import threading
import websockets

# Global variable to store received data
data = None

async def receive_data(websocket):
  global data
  while True:
    try:
      async for message in websocket:
        data = message
        # print(f"Received data: {data}")  # Optional: Print received data here (for debugging)
    except websockets.ConnectionClosed:
      print("WebSocket connection closed.")


async def print_data():
    global data
    print('server started...')
    while True:
        # Check for updated data to avoid unnecessary prints
        if data:
            print(f"Updated data:  {data}")
        # Adjust the sleep time as needed to control the printing frequency
        await asyncio.sleep(2)


async def start_server(port):
    async with websockets.serve(receive_data, "localhost", port):
        await asyncio.Future()  # Run the server indefinitely

async def main():
    # Choose a port number for your WebSocket server
    port = 6969

    # Create and start the server coroutine
    server_task = asyncio.create_task(start_server(port))

    # Create and start the printing thread
    # printing_thread = threading.Thread(target=print_data)
    # printing_thread.start()
    # Create an async task for printing data
    printing_task = asyncio.create_task(print_data())

    # Run the event loop in the main thread
    await asyncio.gather(server_task, printing_task)  # Wait for both server and printing to finish
    print("Server stopped.")

if __name__ == "__main__":
    asyncio.run(main())