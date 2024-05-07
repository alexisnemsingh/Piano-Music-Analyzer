import mido
from mido import MidiFile
import numpy as np
import os

def load_midi_files(directory='Dataset'):
    # Load all MIDI files in the given directory
    files = [f for f in os.listdir(directory) if f.endswith('.mid')]
    
    # Print files and their corresponding numbers
    for i, file in enumerate(files):
        print(f"{i+1}: {file}")
    print("0: Use all files")
    print("*: Exit")

    # Prompt user to select files
    selection = input("Enter the number of the file you want to use: ")

    # Handle selection
    if selection == '0':
        # Use all files
        mids = [MidiFile(os.path.join(directory, file)) for file in files]
    elif selection == '*':
        # Exit
        print("Exiting...")
        return []
    else:
        # Use selected file
        selected_file = files[int(selection)-1]
        mids = [MidiFile(os.path.join(directory, selected_file))]

    return mids

def extract_tempo(mid):
    # Extract tempo information
    tempos = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'set_tempo':
                tempos.append(msg.tempo)
    return tempos

def convert_to_bpm(tempos):
    # Convert to BPM
    bpms = mido.tempo2bpm(np.array(tempos))
    return bpms

if __name__ == "__main__":
    mids = load_midi_files()
    for mid in mids:
        tempos = extract_tempo(mid)
        bpms = convert_to_bpm(tempos)
        avg_bpm = np.mean(bpms)  # Calculate average BPM
        print(avg_bpm)