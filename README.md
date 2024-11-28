Scientific Python Interactive Data Acoustic Modeling (SPIDAM)

Description:

SPIDAM is a Python-based tool designed to analyze reverberation (RT60) in enclosed spaces to improve acoustic comfort and intelligibility. The project features a graphical user interface (GUI) that allows users to import audio files, visualize waveforms, calculate RT60 for different frequency ranges (low, mid, high), and display spectrograms.

Features:

User-Friendly GUI: Load audio files, visualize waveforms, and plot RT60 values for low, mid, and high frequencies.

Audio Formats Supported: .wav, .mp3, .m4a.

RT60 Visualization: Analyze the reverberation time for different frequency ranges to determine the acoustic quality of a given space.

Toggle RT60 Plots: Extra functionality to display/hide RT60 plots for better user interactivity.

Installation/ Dependencies:

Python 3.7 or higher

Required Python packages:

librosa

scipy

matplotlib

tkinter

pydub

soundfile

FFmpeg: Required for audio format conversion (e.g., .mp3, .m4a to .wav). FFmpeg must be installed and added to the system's PATH for compatibility.

Contributors:

Alec: GUI development, visualization integration, and README documentation.

Ines: Data analysis and RT60 calculation.

Diego: File handling, audio format compatibility, and conversion.

M: Documentation and implementation of the extra credit toggle feature.

