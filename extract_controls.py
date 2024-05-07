from mido import MidiFile
from tempo import load_midi_files
import numpy as np

def extract_control_changes(mid):
    control_changes = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'control_change':
                control_changes.append((msg.control, msg.value))
    return control_changes

def calculate_control_averages(control_changes):
    control_numbers = [control[0] for control in control_changes]
    values = [control[1] for control in control_changes]
    return {'avg_control_number': np.mean(control_numbers), 'avg_value': np.mean(values)}

if __name__ == "__main__":
    mids = load_midi_files()
    for mid in mids:
        control_changes = extract_control_changes(mid)
        control_averages = calculate_control_averages(control_changes)
        print(control_averages)