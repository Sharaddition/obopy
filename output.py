import asyncio
import websockets

async def send_audio_stream():
    async with websockets.connect("ws://localhost:6969") as websocket:
        # Open the audio file and send its data in chunks
        with open("user.wav", "rb") as audio_file:
            while True:
                # Read audio data from the file
                audio_chunk = audio_file.read(1024)
                if not audio_chunk:
                    break  # If there's no more data, break the loop
                # Send the audio data to the server
                await websocket.send(audio_chunk)
        # Signal the end of the audio stream
        await websocket.send("something else")
        await websocket.send("EOF")

asyncio.get_event_loop().run_until_complete(send_audio_stream())
