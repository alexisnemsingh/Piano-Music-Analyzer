from mido import MidiFile
from tempo import load_midi_files
import numpy as np

def extract_note_info(mid):
    note_info = []
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                note_info.append((msg.note, msg.velocity, msg.time))
    return note_info

def calculate_averages(note_info):
    pitches = [info[0] for info in note_info]
    velocities = [info[1] for info in note_info]
    times = [info[2] for info in note_info]
    return {'avg_pitch': np.mean(pitches), 'avg_velocity': np.mean(velocities), 'avg_duration': np.mean(times)}

if __name__ == "__main__":
    mids = load_midi_files()
    for mid in mids:
        note_info = extract_note_info(mid)
        averages = calculate_averages(note_info)
        print(f"Average pitch: {averages['avg_pitch']}, Average velocity: {averages['avg_velocity']}, Average time: {averages['avg_duration']}")