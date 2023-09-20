import os
import librosa
import numpy as np
from scipy.io import wavfile

def split_wav_into_segments(input_path, segment_duration=10):
    # Create a subfolder with the same name as the audio file
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = os.path.join(os.path.dirname(input_path), file_name)
    os.makedirs(output_dir, exist_ok=True)

    # Load the audio file
    audio_data, sample_rate = librosa.load(input_path, sr=None, mono=False)

    # Check if the file is stereo (2 channels)
    if len(audio_data.shape) > 1 and audio_data.shape[0] == 2:
        # Convert stereo to mono by taking the average of the two channels
        audio_data = librosa.to_mono(audio_data)

    # Calculate the number of samples corresponding to the desired segment duration
    segment_samples = int(segment_duration * sample_rate)

    # Calculate the total number of segments
    total_segments = len(audio_data) // segment_samples

    # Split the audio data into segments
    segments = np.array_split(audio_data, total_segments)

    # Save each segment as a separate WAV file in the subfolder
    for i, segment in enumerate(segments):
        output_file = os.path.join(output_dir, f"segment_{i+1}.wav")
        wavfile.write(output_file, sample_rate, segment.astype(np.float32))

# Function to process all WAV files in the current folder
def process_wav_files_in_folder(folder_path=".", segment_duration=10):
    # List all files in the current folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Iterate through each file and process WAV files
    for file_name in files:
        if file_name.lower().endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            split_wav_into_segments(file_path, segment_duration)

# Example usage
current_folder = "."  # Use "." for the current folder
segment_duration = 10  # seconds

process_wav_files_in_folder(current_folder, segment_duration)