# Run the following commands on the terminal when setting up the RPi for the first time
# sudo apt update
# sudo apt install python3-numpy
# sudo apt install python3-matplotlib 
# sudo apt install python3-scipy

import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import os

# Suppress WavFileWarning (error associated with unnecessary metadata)
warnings.filterwarnings("ignore", category=wavfile.WavFileWarning)

# User inputs the file path
filename = input("Please enter the full path of the WAV file: ")

# Check if the file exists
if not os.path.isfile(filename):
    print("File not found. Please make sure the file path is correct.")
    exit()

# Load the WAV file
sample_rate, data = wavfile.read(filename)

# If stereo, take only one channel
if len(data.shape) > 1:
    data = data[:, 0]

# Compute the spectrogram using scipy
frequencies, times, spectrogram = signal.spectrogram(data, sample_rate)

# Plot the spectrogram
plt.figure(figsize=(10, 6))
plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='gouraud')
plt.colorbar(label='Intensity [dB]')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')
plt.title('Spectrogram')
plt.show()