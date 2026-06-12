import React, { useState } from 'react';
import { Music, Play, Loader2 } from 'lucide-react';
import MidiPlayer from './MidiPlayer';

const MusicGenerator = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [numNotes, setNumNotes] = useState(100);
  const [midiData, setMidiData] = useState(null);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError(null);
    setMidiData(null);

    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ n_notes: numNotes }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to generate music');
      }

      const data = await response.json();
      setMidiData({
        url: `http://localhost:8000${data.url}`,
        filename: data.filename
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="glass-panel">
      <div className="control-group">
        <div className="control-header">
          <label htmlFor="notes-length">Sequence Length</label>
          <span className="value-badge">{numNotes} Notes</span>
        </div>
        <input 
          id="notes-length"
          type="range" 
          min="20" 
          max="300" 
          value={numNotes} 
          onChange={(e) => setNumNotes(parseInt(e.target.value))}
          className="range-slider"
        />
      </div>

      <button 
        className="btn-primary"
        onClick={handleGenerate}
        disabled={isGenerating}
      >
        {isGenerating ? (
          <>
            <div className="sound-waves">
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
            </div>
            Composing Symphony...
          </>
        ) : (
          <>
            <Music size={24} />
            Generate Composition
          </>
        )}
      </button>

      {error && (
        <div style={{ color: '#ef4444', marginTop: '1.5rem', textAlign: 'center', fontWeight: '500' }}>
          {error}
        </div>
      )}

      {midiData && !isGenerating && (
        <MidiPlayer midiUrl={midiData.url} filename={midiData.filename} />
      )}
    </div>
  );
};

export default MusicGenerator;
