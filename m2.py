import time
# import pyaudio
import numpy as np
import openwakeword
from ai import ai
from wit import Wit
from wav import save_audio
from openwakeword.model import Model
from vad import SileroVoiceActivityDetector

import sounddevice as sd

wit = Wit('ZVUD4TKFMZC3L2MXNEKNZFBBKJDBF63U')
openwakeword.utils.download_models(['melspectrogram', 'embedding'])

MODEL_NAME = 'hey_mycroft_v0.1'
owwModel = Model(
    wakeword_models=[f'models/{MODEL_NAME}.onnx'],
    inference_framework='onnx'
    )

# Set parameters
RATE = 16000
CHUNK = 1280
CHANNELS = 1
# FORMAT = pyaudio.paInt16

# Initialize PyAudio
# pya = pyaudio.PyAudio()

# Open an audio stream
MIN_VAD = 0.4
MAX_SILENCE = 25
# stream = pya.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

stream2 = sd.InputStream(channels=CHANNELS, samplerate=RATE, dtype=np.int16, blocksize=CHUNK)


vad = SileroVoiceActivityDetector()

def listen_user(stm, MIN_VAD = 0.4, MAX_SILENCE = 25):
    silence = 0
    recorded_audio = []
    print("Listening for user input...")
    with stm:
        while True:
            audio, _ = stm.read(CHUNK)
            voice = np.frombuffer(audio, dtype=np.int16)
            if vad(voice) >= MIN_VAD:
                print('Listening...')
                recorded_audio.append(voice)
                MIN_VAD = 0.55
                silence = MAX_SILENCE * 0.65
            else:
                silence += 1
                MIN_VAD = 0.4
                if silence > MAX_SILENCE:
                    print("User stopped speaking.")
                    break
    
    # Process user audio
    if recorded_audio:
        sam = stm.samplesize
        save_audio(recorded_audio, sam)
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
                    listen_user(stream2,MAX_SILENCE=60)



def ww2():
    """Continuously listens for wake word, performs speech recognition with VAD,
    and processes user audio input."""

    print("Listening for wake word...")

    user_text = ''

    # Start listening for audio data
    with stream2:
        while True:
            voice, _ = stream2.read(CHUNK)
            audio = np.frombuffer(voice, dtype=np.int16)

            # Wake word detection
            prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
            score = prediction[MODEL_NAME]
            # print('MY:', score)
            if score > 0.55:
                print("Wake word detected!")

                # Listen for user input with VAD
                listen_user(stream2)

                print("Ready for wake word again...")
                # break



# def detect_wake_word_and_recognize_speech():
#     """Continuously listens for wake word, performs speech recognition with VAD,
#     and processes user audio input."""

#     print("Listening for wake word...")

#     user_text = ''

#     # Start listening for audio data
#     while True:
#         audio = np.frombuffer(stream.read(CHUNK), dtype=np.int16)

#         # Wake word detection
#         prediction = owwModel.predict(audio, debounce_time=1, threshold={MODEL_NAME:0.5})
#         score = prediction[MODEL_NAME]
#         # print('MY:', score)
#         if score > 0.55:
#             print("Wake word detected!")

#             # Listen for user input with VAD
#             listen_user()

#             print("Ready for wake word again...")
#             # break

if __name__ == "__main__":
    # Start recording
    # with sd.InputStream(channels=CHANNELS, samplerate=RATE, blocksize=CHUNK, dtype=np.int16, callback=callback):
    #     sd.sleep(int(50 * 1000))
    # detect_wake_word_and_recognize_speech()
    ww2()

# Close audio stream and PyAudio
# stream.stop_stream()
# stream.close()
# pya.terminate()
