import os
import pickle
import numpy as np
import torch
from music21 import instrument, note, stream, chord
from model import MusicLSTM
import uuid

PROCESSED_DIR = "processed_data"
OUTPUT_DIR = "generated_midi"

def generate_music(n_notes=100, seed_idx=None):
    try:
        with open(os.path.join(PROCESSED_DIR, 'network_input.pkl'), 'rb') as f:
            network_input = pickle.load(f)
        with open(os.path.join(PROCESSED_DIR, 'notes.pkl'), 'rb') as f:
            notes = pickle.load(f)
    except FileNotFoundError:
        print("Preprocessed data not found.")
        return None

    pitchnames = sorted(set(item for item in notes))
    n_vocab = len(set(notes))
    
    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    if not torch.cuda.is_available():
        print("CRITICAL WARNING: PyTorch is not compiled with CUDA enabled. Falling back to CPU.")
        device = torch.device("cpu")
    else:
        device = torch.device("cuda")
    model = MusicLSTM(n_vocab).to(device)
    
    weights_path = 'weights/music_lstm.pth'
    if not os.path.exists(weights_path):
        print(f"Weights not found at {weights_path}")
        return None
        
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.eval()

    if seed_idx is None:
        seed_idx = np.random.randint(0, len(network_input)-1)
    
    pattern = network_input[seed_idx].tolist()
    prediction_output = []

    # Generate notes
    hidden = model.init_hidden(1, device)
    
    for note_index in range(n_notes):
        prediction_input = torch.tensor([pattern], dtype=torch.long).to(device)
        
        with torch.no_grad():
            output, hidden = model(prediction_input, hidden)
            
        # Because our loss dropped to 0.04, the AI is "too confident" and gets stuck in repetitive loops.
        # We increase the temperature to 1.3 to force it to take more creative risks.
        temperature = 1.3
        output = output / temperature
        probs = torch.nn.functional.softmax(output, dim=1)
        index = torch.multinomial(probs, 1).item()
        
        result = int_to_note[index]
        prediction_output.append(result)
        
        pattern.append(index)
        pattern = pattern[1:]

    # Convert output back to MIDI
    offset = 0
    output_notes = []

    for pattern_note in prediction_output:
        # pattern is a chord
        if ('.' in pattern_note) or pattern_note.isdigit():
            notes_in_chord = pattern_note.split('.')
            notes_list = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes_list.append(new_note)
            new_chord = chord.Chord(notes_list)
            new_chord.offset = offset
            output_notes.append(new_chord)
        # pattern is a note
        else:
            new_note = note.Note(pattern_note)
            new_note.offset = offset
            new_note.storedInstrument = instrument.Piano()
            output_notes.append(new_note)

        # increase offset each iteration so that notes do not stack
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    filename = f"output_{uuid.uuid4().hex[:8]}.mid"
    filepath = os.path.join(OUTPUT_DIR, filename)
    midi_stream.write('midi', fp=filepath)
    
    return filename

if __name__ == '__main__':
    filename = generate_music(n_notes=50)
    print(f"Generated: {filename}")
