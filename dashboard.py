import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import os
from mido import MidiFile
from tempo import extract_tempo, convert_to_bpm
from extract_notes import extract_note_info, calculate_averages
from extract_controls import extract_control_changes, calculate_control_averages
import numpy as np

# Function to load all MIDI files
def load_all_midi_files(directory='Dataset'):
    files = [f for f in os.listdir(directory) if f.endswith('.mid')]
    mids = [MidiFile(os.path.join(directory, file)) for file in files]
    return mids

# Load MIDI files and extract tempo information
mids = load_all_midi_files()
mid_info = {mid.filename: convert_to_bpm(extract_tempo(mid)) for mid in mids}

# Extract note and control change information
note_info = {mid.filename: extract_note_info(mid) for mid in mids}
control_info = {mid.filename: extract_control_changes(mid) for mid in mids}

# Calculate averages for each MIDI file
note_averages = {filename: calculate_averages(notes) for filename, notes in note_info.items()}
control_averages = {filename: calculate_control_averages(controls) for filename, controls in control_info.items()}

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='file-dropdown',
        options=[{'label': filename, 'value': filename} for filename in mid_info.keys()],
        value=list(mid_info.keys())[0]
    ),
    dcc.Graph(id='tempo-stats'),
    dcc.Graph(id='note-stats'),
    dcc.Graph(id='control-stats')
])

@app.callback(
    Output('tempo-stats', 'figure'),
    [Input('file-dropdown', 'value')]
)
def update_tempo_graph(selected_file):
    data = mid_info[selected_file]
    return go.Figure(data=[
        go.Bar(x=list(range(len(data))), y=data)
    ])

@app.callback(
    Output('note-stats', 'figure'),
    [Input('file-dropdown', 'value')]
)
def update_note_graph(selected_file):
    data = note_averages[selected_file]
    return go.Figure(data=[
        go.Bar(x=list(data.keys()), y=list(data.values()))
    ])

@app.callback(
    Output('control-stats', 'figure'),
    [Input('file-dropdown', 'value')]
)
def update_control_graph(selected_file):
    data = control_averages[selected_file]
    return go.Figure(data=[
        go.Bar(x=list(data.keys()), y=list(data.values()))
    ])

if __name__ == '__main__':
    app.run_server(debug=True)