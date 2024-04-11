import asyncio
import websockets
import time
import websockets
import numpy as np
import openwakeword
from wit import Wit
from wav import save_audio
from openwakeword.model import Model
from vad import SileroVoiceActivityDetector

openwakeword.utils.download_models(['melspectrogram', 'embedding'])
MODEL_NAME = 'hey_mycroft_v0.1'
owwModel = Model(
    wakeword_models=[f'models/{MODEL_NAME}.onnx'],
    inference_framework='onnx'
    )
vad = SileroVoiceActivityDetector()
wit = Wit('ZVUD4TKFMZC3L2MXNEKNZFBBKJDBF63U')


class AudioReceiver:
    def __init__(self):
        self.CHUNK_SIZE = 1280 * 2
        self.aud_data = None
        self.processing = False  # Flag to indicate if processing is ongoing

    async def receive_audio(self, websocket, path):
        buffer = b''
        async for data in websocket:
            if data:
                # Decode audio data (replace with your specific decoding logic)
                audio_data = data  # Placeholder for decoding
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
                    while len(buffer) >= self.CHUNK_SIZE:
                        chunk = buffer[:self.CHUNK_SIZE]
                        buffer = buffer[self.CHUNK_SIZE:]
                        self.aud_data = chunk
                        if not self.processing:
                            audio = np.frombuffer(chunk, dtype=np.int16)
                            print(f"Received audio data with length: {len(audio)} bytes")
                            # Wake word detection
                            prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
                            score = prediction[MODEL_NAME]
                            if score > 0.55:
                                print("Wake word detected!")
                                asyncio.create_task(self.process_audio())
                                print("Ready for wake word again...")

    async def process_audio(self, MIN_VAD = 0.33, MAX_SILENCE = 25):
        self.processing = True
        
        silence = 0
        recorded_audio = []
        print("Listening for user input...")
        last_spoke = time.time()
        while True:
            # voice = np.frombuffer(raw_audio, dtype=np.int16)
            voice = self.aud_data
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
                if silent_for > 7:
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
                        await self.process_audio(MAX_SILENCE=60)
        
        self.processing = False

    async def run(self):
        async with websockets.serve(self.receive_audio, "localhost", 6969):
            await asyncio.Future()  # Wait for server to close

if __name__ == "__main__":
    receiver = AudioReceiver()
    asyncio.run(receiver.run())
