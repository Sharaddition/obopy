import asyncio
import threading
import time
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

raw_audio = b''
isFree = True
async def listen_user(MIN_VAD = 0.33, MAX_SILENCE = 25):
    silence = 0
    global isFree
    global raw_audio
    recorded_audio = []
    isFree = False
    print("Listening for user input...")
    last_spoke = time.time()
    while True:
        # voice = np.frombuffer(raw_audio, dtype=np.int16)
        voice = raw_audio
        if vad(voice) >= MIN_VAD:
            print('Listening...')
            recorded_audio.append(voice)
            MIN_VAD = 0.55
            silence = MAX_SILENCE * 0.65
            last_spoke = time.time()
        else:
            silence += 1
            MIN_VAD = 0.4
            silent_for = time.time() - last_spoke
            if silent_for > 10:
                print("User stopped speaking.")
                break
    
    # Process user audio
    if recorded_audio:
        save_audio(recorded_audio, 2, 'test2.wav')
        with open('user.wav', 'rb') as f:
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
    isFree = True


async def owwd():
    global isFree
    global raw_audio
    prev_audio = b''
    print('OWWD online')
    while True:
        if prev_audio != raw_audio:
            print('1st')
            prev_audio = raw_audio
            if isFree:
                audio = np.frombuffer(raw_audio, dtype=np.int16)
                print(f"Received audio data with length: {len(audio)} bytes")
                # Wake word detection
                prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
                score = prediction[MODEL_NAME]
                if score > 0.55 and isFree:
                    print("Wake word detected!")
                    isFree = False
                    await listen_user()
                    print("Ready for wake word again...")


aud = []
async def audio_stream(websocket, path):
    global aud
    global raw_audio
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
                    raw_audio = chunk
                    # aud.append(chunk)
                    # await owwd()
                    # if vad(chunk) >= 0.25:
                    #     print('Listening...')
                # Process the audio data here, you can save it to a file or perform real-time processing
        except websockets.exceptions.ConnectionClosedError:
            print("Connection closed.")
            break

# start_server = websockets.serve(audio_stream, "localhost", 6969)
print('Server started...')
# async def main():
#     # async with start_server:
#     #     await start_server.serve_forever()
#     # await start_server.serve_forever()
#     await owwd()

async def start_websocket_server():
    async with websockets.serve(audio_stream, "localhost", 6969):
        print('WebSocket server started...')
        await asyncio.Future()
# Function to run owwd() asynchronously
async def run_owwd():
    await owwd()

    # Main function to start both tasks concurrently
async def main():
    websocket_task = asyncio.create_task(start_websocket_server())
    owwd_task = asyncio.create_task(run_owwd())
    await asyncio.gather(websocket_task, owwd_task)

# Start the event loop in a separate thread
def start_event_loop():
    asyncio.run(main())


# Create and start a thread for the event loop
event_loop_thread = threading.Thread(target=start_event_loop)
event_loop_thread.start()

# Join the thread to the main thread
event_loop_thread.join()
# asyncio.run(main())
# main()

# start_server = websockets.serve(echo, "localhost", PORT)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()