# audio scripts used in preparation for wav2vec model

check_sample_rate.py - checks for sample rate of all files within the folder.

resample_wav_audio.py - resamples all the files in the current folder. Sample rate used in the script is 16000

split_wav_file.py - split wav file into smaller bits. Here it is set to 10 second files.

data_preparation.py - check audio  for/convert from stereo to mono. check for sample rate and if necessary resample it as well.  Then combine line from text files with combine 10 second wav files and lines from text files in HDF5 format to store data. 
Text files must have "_clean" at the end of their file names and audio files must be in folders with "_audio" at the end. First script gathers the names of the files with "_clean" in their name, that are in the current folder and then look for folders with the same name, that have "_audio" in their names.