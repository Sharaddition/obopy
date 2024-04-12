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

print("\033[92m OPEN:       Server")

raw_audio = None
state = 'Free'
async def receive_data(websocket):
  buffer = b''
  global state
  global raw_audio
  while True:
    try:
      async for message in websocket:
        data = message
        if data == "EOF":
            print("End of audio stream")
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
                audio = np.frombuffer(raw_audio, dtype=np.int16)
                # Wake word detection
                prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
                score = prediction[MODEL_NAME]
                if score > 0.55 and state == 'Free':
                    print("Wake word detected!")
                    # Thread for listening query
                    new_thread = threading.Thread(target=listen_user)
                    new_thread.start()
                    print("Ready for wake word again...")
    except websockets.ConnectionClosed:
      print("WebSocket connection closed.")


def listen_user(MIN_VAD = 0.42, MAX_SILENCE = 25):
    global state
    global raw_audio
    record_audio = []
    last_spoke = time.time()
    print('Start Listening...')
    voice = None
    state = 'Busy'
    while True:
        if raw_audio != voice:
            voice = raw_audio
            if vad(voice) >= MIN_VAD:
                print('Speaking...')
                record_audio.append(voice)
                last_spoke = time.time()
            else:
                silent_for = time.time() - last_spoke
                if silent_for > 2.25:
                    print("User stopped speaking.")
                    break
    # Process user audio
    if record_audio:
        save_audio(record_audio, 2, 'test.wav')
        with open('test.wav', 'rb') as f:
            user_text = wit.speech(f, {'Content-Type': 'audio/wav'})
            print(user_text)
            if user_text['text']:
                confidence = user_text['speech']['confidence']*100
                print(f"Confidence: {confidence}%")
                print(f"Intent: {user_text['intents'][0]['name']}")
                print(f"Dialogue: {user_text['text']}")
                if confidence > 65:
                    # ai(user_text['text'])
                    time.sleep(0.75)
                    listen_user(MAX_SILENCE=60)
    state = 'Free'



async def start_server(port):
    try:
        async with websockets.serve(receive_data, "localhost", port):
            print("\033[92m OPEN:       Websocket \033[0m")
            await asyncio.Future()  # Run the server indefinitely
    except Exception as e:
        print(f"Error starting server: {e}")

async def main():
    # Choose a port number for your WebSocket server
    port = 6969

    # Create and start the server coroutine
    server_task = asyncio.create_task(start_server(port))

    # Run the event loop in the main thread
    await asyncio.gather(server_task)  # Wait for both server and printing to finish
    print("Server stopped.")

# if __name__ == "__main__":
asyncio.run(main())