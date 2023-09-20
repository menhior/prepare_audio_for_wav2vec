import os
import librosa
import pandas as pd
import numpy as np
from scipy.io import wavfile

def downsample_and_convert_to_mono(input_path, output_path, target_sample_rate):
    # Read the WAV file
    sample_rate, audio_data = wavfile.read(input_path)
    print(sample_rate)
    # Check if the file is stereo (2 channels)
    if len(audio_data.shape) > 1 and audio_data.shape[1] == 2:
        # Convert stereo to mono by taking the average of the two channels
        audio_data = np.mean(audio_data, axis=1, dtype=audio_data.dtype)

    # Downsample the audio if the sample rate is different from the target rate
    if sample_rate != target_sample_rate:
        ratio = target_sample_rate / sample_rate
        audio_data = np.interp(
            np.arange(0, len(audio_data), ratio),
            np.arange(0, len(audio_data)),
            audio_data
        ).astype(audio_data.dtype)

    # Save the downsampled and mono audio as a new WAV file
    wavfile.write(output_path, target_sample_rate, audio_data)

# Example usage
#input_file = "input_audio.wav"
#output_file = "output_audio_mono.wav"
target_sample_rate = 16000  # You can choose your desired sample rate

#downsample_and_convert_to_mono(input_file, output_file, target_sample_rate)

def get_files_with_string(directory_path, search_string):
    matching_files = []
    matching_folders_for_audio = []

    # List all files in the current directory
    files = os.listdir(directory_path)

    # Check if the search string is present in each file's name
    for file_name in files:
        if search_string in file_name and ".py" not in file_name:
            matching_files.append(file_name)
            if 'text' in file_name:
                matching_folders_for_audio.append(file_name[:-15] + "_audio")
            else:
                matching_folders_for_audio.append(file_name[:-10] + "_audio")

    return matching_files, matching_folders_for_audio

# Example usage
current_directory = "."  # Use "." for the current directory
search_string = "clean"  # Replace this with the desired search string

matching_files, matching_folders_for_audio = get_files_with_string(current_directory, search_string)

print(matching_files)
print(matching_folders_for_audio)

audio_arrays = []
sample_arrays = []
len_audio_arrays = []

def load_wav_files_as_numpy_arrays(folder_path):

    # List all files in the selected folder
    files = os.listdir(folder_path)
    clean_files = []
    for file in files:
        if "clean" in file:
            clean_files.append(file)

    files = clean_files

    def get_integer_value(element):
        return int(element.split('_')[1])  # Assuming the integer value is at the beginning of each element

    # Sort the list based on the extracted integer value
    files = sorted(files, key=get_integer_value)

    # Filter and process only the WAV files
    print(files)
    for file_name in files:
        #print(file_name)
        #print(file_name.split('_')[1])
        if file_name.lower().endswith(".wav") and "clean" in file_name:
            #print(file_name)
            file_path = os.path.join(folder_path, file_name)
            audio_data, sample_rate = librosa.load(file_path, sr=None, mono=False)
            # Convert stereo to mono by taking the average of the two channels
            ##print(sample_rate)
            if len(audio_data.shape) > 1 and audio_data.shape[0] == 2:
                audio_data = librosa.to_mono(audio_data)

            # Append the NumPy array to the list
            audio_arrays.append(audio_data)
            #sample_arrays.append(sample_rate)
            len_audio_arrays.append(len(audio_data))


# Example usage
for audio_folder in matching_folders_for_audio:
    load_wav_files_as_numpy_arrays(audio_folder)


def append_lines_to_list(folder_path, matching_files):
    lines_list = []

    # List all files in the folder

    # Iterate through each file and read its lines
    for file_name in matching_files:
        if file_name.lower().endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                for line in file:
                    # Append each line to the list
                    if line.strip() == "":
                        lines_list.append("          ")
                    else:
                        lines_list.append(line.strip())

    return lines_list

# Example usage
lines = append_lines_to_list(current_directory, matching_files)

def find_indices(list_to_check, item_to_find):
    indices = []
    for idx, value in enumerate(lines):
        if value == item_to_find:
            indices.append(idx)
    return indices

def remove_elements_by_index(lst, indices_to_remove):
    # Create a new list using list comprehension with elements not in the specified indices
    new_lst = [elem for idx, elem in enumerate(lst) if idx not in indices_to_remove]
    return new_lst

indices_to_remove = find_indices(lines, '          ')
lines = remove_elements_by_index(lines, indices_to_remove)
audio_arrays = remove_elements_by_index(audio_arrays, indices_to_remove)
#sample_arrays = remove_elements_by_index(sample_arrays, indices_to_remove)
len_audio_arrays = remove_elements_by_index(len_audio_arrays, indices_to_remove)


print(len(lines), len(audio_arrays), len(len_audio_arrays))
#print(len(lines), len(audio_arrays), len(sample_arrays), len(len_audio_arrays))
final_dict = {"sentence":lines, "audio":audio_arrays, 'len_data':len_audio_arrays}
#final_dict = {"sentence":lines, "audio":audio_arrays, "sampling_rate": sample_arrays, 'len_data':len_audio_arrays}
print(type(audio_arrays[0]))
print(audio_arrays[0])
print(len(audio_arrays[0]))
df = pd.DataFrame(final_dict)

# Display the DataFrame

output_hdf_file = 'new_ready_data.h5'
df.to_hdf(output_hdf_file, key='df', mode='w')

print(f'DataFrame saved to {output_hdf_file} in HDF5 format.')
'''# Save the DataFrame to a CSV file
output_csv_file = "ready_data.csv"
df.to_csv(output_csv_file, index=False)

print(f"DataFrame saved to '{output_csv_file}' in CSV format.")'''