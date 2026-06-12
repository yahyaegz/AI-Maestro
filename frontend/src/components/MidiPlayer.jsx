import React, { useEffect, useRef } from 'react';
import { Download } from 'lucide-react';
import 'html-midi-player';

const MidiPlayer = ({ midiUrl, filename }) => {
  const playerRef = useRef(null);

  useEffect(() => {
    // When URL changes, we can reset the player if needed
    // The web component handles most of the binding automatically
  }, [midiUrl]);

  return (
    <div className="player-section">
      <div className="player-header">
        <h3>Generated Track</h3>
        <a 
          href={midiUrl} 
          download={filename || "generated-music.mid"}
          className="btn-secondary"
        >
          <Download size={16} />
          Download MIDI
        </a>
      </div>
      
      {/* 
        html-midi-player web components. 
        Using SGM Plus SoundFont for highly realistic piano audio
      */}
      <midi-player
        ref={playerRef}
        src={midiUrl}
        sound-font="https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus"
        visualizer="#myVisualizer">
      </midi-player>
      
      <midi-visualizer type="piano-roll" id="myVisualizer"></midi-visualizer>
    </div>
  );
};

export default MidiPlayer;
