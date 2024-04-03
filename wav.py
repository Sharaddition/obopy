import wave
import pyaudio

# Set parameters
RATE = 16000
CHUNK = 1280
CHANNELS = 1
FORMAT = pyaudio.paInt16
WAVE_OUTPUT_FILENAME = 'user.wav'

def save_audio(frames, sample_size):
    print('Sample Size:', sample_size)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(sample_size)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()