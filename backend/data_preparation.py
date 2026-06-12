import os
import pickle
import numpy as np
from music21 import converter, instrument, note, chord, corpus

PROCESSED_DIR = "processed_data"

def get_notes():
    """ Get all the notes and chords from the music21 built-in corpus """
    notes = []
    
    print("Loading Bach chorales from music21 built-in corpus...")
    # Get a list of bach chorales from the corpus
    paths = corpus.getComposer('bach')
    
    if not paths:
        print("No files found in corpus.")
        return []
        
    print(f"Found {len(paths)} files. Loading a massive subset to take advantage of your RTX 4080...")

    # Maximize dataset size for RTX 4080 (up to 1000 if available)
    paths = paths[:1000] 

    for i, file_path in enumerate(paths):
        try:
            print(f"Parsing file {i+1}/{len(paths)}: {os.path.basename(file_path)}")
            midi = corpus.parse(file_path)
            
            notes_to_parse = None

            try: # file has instrument parts
                s2 = instrument.partitionByInstrument(midi)
                if s2:
                    # Just take the first part
                    notes_to_parse = s2.parts[0].recurse()
                else:
                    notes_to_parse = midi.flat.notes
            except: # file has notes in a flat structure
                notes_to_parse = midi.flat.notes

            if notes_to_parse:
                for element in notes_to_parse:
                    if isinstance(element, note.Note):
                        notes.append(str(element.pitch))
                    elif isinstance(element, chord.Chord):
                        notes.append('.'.join(str(n) for n in element.normalOrder))
        except Exception as e:
            print(f"Error parsing file: {e}")

    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    with open(os.path.join(PROCESSED_DIR, 'notes.pkl'), 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes

def prepare_sequences(notes, n_vocab):
    """ Prepare the sequences used by the Neural Network """
    sequence_length = 100

    # get all pitch names
    pitchnames = sorted(set(item for item in notes))

    # create a dictionary to map pitches to integers
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

    network_input = []
    network_output = []

    # create input sequences and the corresponding outputs
    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])

    n_patterns = len(network_input)

    # reshape the input into a format compatible with LSTM layers
    network_input = np.reshape(network_input, (n_patterns, sequence_length))
    network_output = np.array(network_output)

    with open(os.path.join(PROCESSED_DIR, 'network_input.pkl'), 'wb') as filepath:
        pickle.dump(network_input, filepath)
    with open(os.path.join(PROCESSED_DIR, 'network_output.pkl'), 'wb') as filepath:
        pickle.dump(network_output, filepath)

    return network_input, network_output

if __name__ == '__main__':
    notes = get_notes()
    n_vocab = len(set(notes))
    print(f"Vocabulary size: {n_vocab}")
    if n_vocab > 0:
        prepare_sequences(notes, n_vocab)
        print("Data preparation complete.")
    else:
        print("No notes parsed. Check the dataset.")
