import React from 'react';
import MusicGenerator from './components/MusicGenerator';
import { Sparkles } from 'lucide-react';

function App() {
  return (
    <>
      {/* Animated Floating Orbs Background */}
      <div className="ambient-bg"></div>
      
      <div className="app-container">
        <header>
          <h1 className="title-gradient">
            <Sparkles className="inline-block mr-4 mb-2" size={48} color="#f472b6" />
            AI Maestro
          </h1>
          <p className="subtitle">
            Experience the future of music generation. Our advanced LSTM neural network analyzes classical masterpieces to compose unique, infinite melodies.
          </p>
        </header>
        
        <main>
          <MusicGenerator />
        </main>
        
        <footer style={{ textAlign: 'center', marginTop: '2rem', padding: '1rem', color: 'rgba(255,255,255,0.6)', fontSize: '0.9rem' }}>
          &copy; 2026 Made with ❤️ by Yahya el gzouli
        </footer>
      </div>
    </>
  );
}

export default App;
