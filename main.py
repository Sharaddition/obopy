import time
import pyaudio
import numpy as np
import openwakeword
# import sounddevice as sd
from openwakeword.model import Model
from vad import SileroVoiceActivityDetector

# Set parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1280

audio = pyaudio.PyAudio()
mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)


# openwakeword.utils.download_models()

owwModel = Model(
    wakeword_models=['models/hey_mycroft_v0.1.onnx'],
    inference_framework='onnx'
    )
n_models = len(owwModel.models.keys())
vad = SileroVoiceActivityDetector()

is_wake = False
status = 'sleep'
silence = 0
speech = 0
if __name__ == "__main__":
    # Generate output string header
    print("\n\n")
    print("#"*65)
    print("Listening for wakewords...")
    print("#"*65)
    print("\n"*(n_models*3))

    while True:
        # Get audio
        if mic_stream:
            audio = np.frombuffer(mic_stream.read(CHUNK), dtype=np.int16)

            if is_wake:
                # If user wakes the device
                if vad(mic_stream.read(CHUNK)) >= 0.5 and status == 'sleep':
                    # Listen to users instruction
                    print('>> Speech...')
                    silence = 5
                    speech += 1
                else:
                    if silence > 10:
                        # status = 'process'
                        if speech > 2:
                            print('wait')
                            status = 'stop'
                            speech = 0
                        else:
                            # Start listening for wakeup call again
                            is_wake = False
                            status = 'sleep'
                            silence = 0
                            speech = 0
                            print('>> Going to sleep.')
                    else:
                        print('silent')
                        silence += 1
            else:
                # Feed to openWakeWord model
                prediction = owwModel.predict(audio)

                # Column titles
                n_spaces = 16
                output_string_header = """
                    Model Name         | Score | Wakeword Status
                    --------------------------------------
                    """

                for modl in owwModel.prediction_buffer.keys():
                    # Add scores in formatted table
                    print(modl)
                    scores = list(owwModel.prediction_buffer[modl])
                    curr_score = format(scores[-1], '.20f').replace("-", "")

                    output_string_header += f"""{modl}{" "*(n_spaces - len(modl))}   | {curr_score[0:5]} | {"--"+" "*20 if scores[-1] <= 0.45 else "Wakeword Detected!"}
                    """
                    if scores[-1] >= 0.45:
                        is_wake = True

                # Print results table
                print("\033[F"*(4*n_models+1))
                print(output_string_header, "                             ", end='\r')
