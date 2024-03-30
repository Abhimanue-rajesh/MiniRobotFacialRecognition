import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

def record_audio(duration, filename):
    fs = 48000  # Sample rate
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    wav.write(filename, fs, recording)  # Save the recorded audio to a WAV file

# Example usage:
record_duration = 5  # Duration in seconds
output_filename = 'output.wav'
record_audio(record_duration, output_filename)
