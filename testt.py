import asyncio
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        print(f'Recieved msg: {message}')
        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 6969):
        print('Started server')
        await asyncio.Future()  # run forever

asyncio.run(main())