import os
import soundfile as sf

# Current folder
input_folder = '.'  # Current folder

# Get a list of all WAV files in the input folder
wav_files = [file for file in os.listdir(input_folder) if file.lower().endswith('.wav')]

# Print the sample rate of each WAV file
for wav_file in wav_files:
    input_path = os.path.join(input_folder, wav_file)
    
    # Get the sample rate using soundfile
    sample_rate = sf.info(input_path).samplerate
    
    print(f"File: {wav_file}, Sample Rate: {sample_rate}")