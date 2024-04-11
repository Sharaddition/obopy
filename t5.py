import time
import asyncio
import threading
import websockets
import numpy as np
import openwakeword
from wit import Wit
from wav import save_audio
from openwakeword.model import Model
from vad import SileroVoiceActivityDetector

CHUNK_SIZE = 1280 * 2

openwakeword.utils.download_models(['melspectrogram', 'embedding'])
MODEL_NAME = 'hey_mycroft_v0.1'
owwModel = Model(
    wakeword_models=[f'models/{MODEL_NAME}.onnx'],
    inference_framework='onnx'
    )
vad = SileroVoiceActivityDetector()
wit = Wit('ZVUD4TKFMZC3L2MXNEKNZFBBKJDBF63U')

raw_audio = None

async def receive_data(websocket):
  buffer = b''
  global raw_audio
  while True:
    try:
      async for message in websocket:
        data = message
        if data == "EOF":
            print("End of audio stream")
            # save_audio(aud, 2, 'test.wav')
            # aud = []
        elif isinstance(data, str):
            # Handle JSON or text data
            print(f"Received text data: {data}")
        else:
            # Chunk audio data
            buffer += data
            while len(buffer) >= CHUNK_SIZE:
                chunk = buffer[:CHUNK_SIZE]
                buffer = buffer[CHUNK_SIZE:]
                raw_audio = chunk
    except websockets.ConnectionClosed:
      print("WebSocket connection closed.")

def owwd():
    global raw_audio
    prev_audio = None
    print('OWWD     : Done')
    while True:
        if raw_audio != prev_audio:
            prev_audio = raw_audio
            audio = np.frombuffer(raw_audio, dtype=np.int16)
            print(f"Received audio data with length: {len(audio)} bytes")
            # Wake word detection
            prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
            score = prediction[MODEL_NAME]
            if score > 0.22:
                print("Wake word detected!")
                asyncio.create_task(listen_user())
                print("Ready for wake word again...")

def listen_user(MIN_VAD = 0.5, MAX_SILENCE = 25):
    global raw_audio
    prev_audio = None
    record_audio = []
    last_spoke = time.time()
    while True:
        if raw_audio != prev_audio:
            prev_audio = raw_audio
            voice = raw_audio
            if vad(voice) >= MIN_VAD:
                print('speaking...')
                record_audio.append(voice)
                MIN_VAD = 0.55
                last_spoke = time.time()
            else:
                MIN_VAD = 0.45
                silent_for = time.time() - last_spoke
                if silent_for > 5:
                    print("User stopped speaking.")
                    break
    # Process user audio
    if record_audio:
        save_audio(record_audio, 2, 'test2.wav')
        with open('test2.wav', 'rb') as f:
            user_text = wit.speech(f, {'Content-Type': 'audio/wav'})
            print(user_text)
            if user_text['text']:
                confidence = user_text['speech']['confidence']*100
                print(f"Confidence: {confidence}%")
                print(f"Intent: {user_text['intents'][0]['name']}")
                print(f"Dialogue: {user_text['text']}")
                if confidence > 65:
                    # ai(user_text['text'])
                    listen_user(MAX_SILENCE=60)


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
        print('WS       : Done')
        # asyncio.create_task(owwd())
        await asyncio.Future()  # Run the server indefinitely

async def main():
    # Choose a port number for your WebSocket server
    port = 6969

    # Create and start the server coroutine
    server_task = asyncio.create_task(start_server(port))
    new_thread = threading.Thread(target=owwd)
    new_thread.start()

    # Run the event loop in the main thread
    await asyncio.gather(server_task)  # Wait for both server and printing to finish
    print("Server stopped.")

if __name__ == "__main__":
    asyncio.run(main())