import asyncio
import websockets

async def send_test_message():
    uri = "ws://localhost:6969"  # Change to your Docker container's IP if not running locally

    async with websockets.connect(uri) as websocket:
        # Send a test message
        message = "Hello, WebSocket!"
        await websocket.send(message)
        print(f"Sent: {message}")

asyncio.get_event_loop().run_until_complete(send_test_message())