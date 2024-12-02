# Import necessary libraries
import numpy as np
import scipy.signal as signal
import librosa
import librosa.display
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
import os
from pydub import AudioSegment
import soundfile as sf
import shutil
import io

# Set path for FFmpeg (use local version if available)
ffmpeg_path = os.path.join(os.getcwd(), 'ffmpeg.exe')
if os.path.isfile(ffmpeg_path):
    AudioSegment.converter = ffmpeg_path

# GUI Setup
class SPIDAMApp:
    def __init__(self, root):
        self.root = root
        self.root.title('SPIDAM - Acoustic Modeling Tool')

        # Add buttons for functionality
        self.load_button = tk.Button(root, text='Load Audio File', command=self.load_audio)
        self.load_button.pack()

        self.plot_waveform_button = tk.Button(root, text='Plot Waveform', command=self.plot_waveform)
        self.plot_waveform_button.pack()

        self.plot_rt60_button = tk.Button(root, text='Plot RT60 (Low, Mid, High)', command=self.plot_rt60)
        self.plot_rt60_button.pack()

        self.combined_plot_button = tk.Button(root, text='Combined RT60 Plot', command=self.combined_rt60_plot)
        self.combined_plot_button.pack()

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[('Audio Files', '*.wav *.mp3 *.m4a')])
        if file_path:
            self.file_path = file_path
            try:
                if file_path.endswith('.mp3') or file_path.endswith('.m4a'):
                    # Convert mp3 or m4a to wav using Pydub
                    if shutil.which('ffmpeg') is None and not os.path.isfile(ffmpeg_path):
                        print("Error: FFmpeg is required for audio conversion but was not found. Please download FFmpeg and place it in your PATH or the working directory.")
                        return
                    audio = AudioSegment.from_file(file_path)
                    wav_io = io.BytesIO()
                    audio.export(wav_io, format='wav')
                    wav_io.seek(0)
                    self.audio, self.sr = sf.read(wav_io, always_2d=False)
                elif file_path.endswith('.wav'):
                    # Load wav directly using Soundfile
                    self.audio, self.sr = sf.read(file_path, always_2d=False)
                else:
                    print("Unsupported file format.")
                    return

                if len(self.audio.shape) > 1:
                    # If the audio has more than one channel, convert to mono
                    self.audio = np.mean(self.audio, axis=1)
            except Exception as e:
                print(f"Error loading audio file: {e}. Please use a supported audio format such as WAV, MP3, or M4A.")
                return

    def plot_waveform(self):
        if hasattr(self, 'audio'):
            plt.figure(figsize=(10, 4))
            librosa.display.waveshow(self.audio, sr=self.sr)
            plt.title('Waveform')
            plt.xlabel('Time (s)')
            plt.ylabel('Amplitude')
            plt.show()

    def plot_rt60(self):
        if hasattr(self, 'audio'):
            # Calculate RT60 for different frequency bands
            rt60_low = self.calculate_rt60(self.audio, self.sr, (60, 250))
            rt60_mid = self.calculate_rt60(self.audio, self.sr, (800, 1200))
            rt60_high = self.calculate_rt60(self.audio, self.sr, (5000, 10000))

            # Plot RT60 for each frequency range
            frequencies = ['Low', 'Mid', 'High']
            rt60_values = [rt60_low, rt60_mid, rt60_high]
            plt.bar(frequencies, rt60_values, color=['b', 'g', 'r'])
            plt.title('RT60 for Low, Mid, and High Frequencies')
            plt.ylabel('Time (s)')
            plt.show()

    def combined_rt60_plot(self):
        if hasattr(self, 'audio'):
            # Calculate RT60 for each frequency range
            rt60_low = self.calculate_rt60(self.audio, self.sr, (60, 250))
            rt60_mid = self.calculate_rt60(self.audio, self.sr, (800, 1200))
            rt60_high = self.calculate_rt60(self.audio, self.sr, (5000, 10000))

            # Plot combined RT60 values for Low, Mid, and High frequencies
            frequencies = ['Low', 'Mid', 'High']
            rt60_values = [rt60_low, rt60_mid, rt60_high]
            plt.plot(frequencies, rt60_values, marker='o')
            plt.title('Combined RT60 Plot')
            plt.ylabel('Time (s)')
            plt.xlabel('Frequency Range')
            plt.show()

    def calculate_rt60(self, audio, sr, freq_range):
        try:
            # Apply a bandpass filter to isolate the desired frequency range
            sos = signal.butter(4, freq_range, btype='bandpass', fs=sr, output='sos')
            filtered_audio = signal.sosfilt(sos, audio)

            # Calculate energy decay
            energy = filtered_audio ** 2
            cumulative_energy = np.cumsum(energy[::-1])[::-1]
            initial_energy = cumulative_energy[0]
            target_energy = initial_energy / 1000
            below_target = np.where(cumulative_energy <= target_energy)[0]

            if len(below_target) == 0:
                return np.nan  # No point found where energy has decayed sufficiently

            t60_index = below_target[0]
            rt60 = t60_index / sr
            return rt60
        except Exception as e:
            print(f"Error calculating RT60: {e}")
            return np.nan

# Main application entry point
if __name__ == '__main__':
    root = tk.Tk()
    app = SPIDAMApp(root)
    root.mainloop()
