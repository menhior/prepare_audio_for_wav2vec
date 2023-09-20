import os
import soundfile as sf
from scipy.signal import resample
import time

# Current folder
input_folder = '.'  # Current folder
output_folder = 'resampled_wav_files'  # Folder to save resampled files

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get a list of all WAV files in the input folder
wav_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.wav')]

# Resample and save each WAV file in the output folder
for wav_file in wav_files:
    input_path = os.path.join(input_folder, wav_file)
    output_path = os.path.join(output_folder, f"resampled_{wav_file}")
    
    # Read the original audio and sample rate using soundfile
    audio_data, original_sample_rate = sf.read(input_path)
    
    # Calculate the resampling factor
    resample_factor = 16000 / original_sample_rate
    
    # Perform resampling using scipy.signal.resample
    resampled_audio = resample(audio_data, int(len(audio_data) * resample_factor))
    
    # Save the resampled audio to a new WAV file in the output folder
    sf.write(output_path, resampled_audio, 16000, format='WAV')
    time.sleep(100)
