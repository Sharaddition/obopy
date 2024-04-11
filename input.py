import asyncio
import numpy as np
import websockets
import openwakeword
from openwakeword.model import Model
from wav import save_audio

openwakeword.utils.download_models(['melspectrogram', 'embedding'])

CHUNK_SIZE = 1280 * 2

MODEL_NAME = 'hey_mycroft_v0.1'
owwModel = Model(
    wakeword_models=[f'models/{MODEL_NAME}.onnx'],
    inference_framework='onnx'
    )

aud = []
async def audio_stream(websocket, path):
    buffer = b''
    while True:
        try:
            # Receive data from the client
            data = await websocket.recv()
            if data == "EOF":
                print("End of audio stream")
                save_audio(aud, 2, 'test.wav')
                aud = []
            elif isinstance(data, str):
                # Handle JSON or text data
                print(f"Received text data: {data}")
            else:
                # Chunk audio data
                buffer += data
                while len(buffer) >= CHUNK_SIZE:
                    chunk = buffer[:CHUNK_SIZE]
                    buffer = buffer[CHUNK_SIZE:]
                    aud.append(chunk)
                    audio = np.frombuffer(chunk, dtype=np.int16)
                    print(f"Received audio data with length: {len(chunk)} bytes")
                    # Wake word detection
                    prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
                    score = prediction[MODEL_NAME]
                    if score > 0.55:
                        print("Wake word detected!")
                # Process the audio data here, you can save it to a file or perform real-time processing
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed.")
            break

start_server = websockets.serve(audio_stream, "localhost", 6969)
print('Server started...')
async def main():
    # async with start_server:
    #     await start_server.serve_forever()
    await start_server.serve_forever()

# asyncio.run(main())
# main()

# start_server = websockets.serve(echo, "localhost", PORT)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()