<div align="center">
  <img src="https://raw.githubusercontent.com/yahyaegz/AI-Maestro/main/frontend/public/icons.svg" alt="AI Maestro Logo" width="100"/>

  # 🎼 AI Maestro

  **Experience the Future of Music Generation**

  <p>
    <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
    <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-yellow.svg" />
    <img alt="React" src="https://img.shields.io/badge/React-18.x-61dafb.svg" />
    <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-0.100+-009688.svg" />
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </p>

  <p>
    AI Maestro is an advanced Deep Learning application that generates unique, infinite melodies. By analyzing classical masterpieces through a powerful Long Short-Term Memory (LSTM) neural network, AI Maestro composes original music that you can listen to and download instantly.
  </p>

  <br />
</div>

---

## ✨ Key Features

- **🧠 Deep Learning Core:** Powered by a customized LSTM neural network trained on classical MIDI files.
- **🎵 Instant Generation:** Generate complex, harmonious musical sequences in seconds.
- **🎧 Interactive Player:** A beautiful, glassmorphic UI built with React to preview your generated tracks directly in the browser.
- **💾 MIDI Export:** Download the AI-generated compositions as standard MIDI `.mid` files to use in your favorite DAW (Ableton, FL Studio, Logic, etc.).
- **⚡ High-Performance API:** Lightning-fast backend powered by FastAPI.

---

## 🛠️ Tech Stack

**Frontend**
- **Framework:** React + Vite
- **Styling:** Custom CSS (Modern Glassmorphism, CSS Variables, Animations)
- **Icons:** Lucide React

**Backend**
- **Framework:** Python / FastAPI
- **AI/ML:** PyTorch / TensorFlow (LSTM Networks)
- **Data Processing:** `mido`, `music21` for MIDI manipulation

---

## 🚀 Getting Started

Follow these steps to run AI Maestro on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/yahyaegz/AI-Maestro.git
cd AI-Maestro
```

### 2. Setup the Backend (Python / FastAPI)
Open a new terminal and navigate to the backend folder:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```
*The API will start running on `http://localhost:8000`*

### 3. Setup the Frontend (React / Vite)
Open another terminal and navigate to the frontend folder:
```bash
cd frontend
npm install
npm run dev
```
*The web application will open on `http://localhost:5173`*

---

## 🌐 Deployment

- **Frontend:** Ready to be deployed on [Vercel](https://vercel.com/) (Just select the `frontend` folder as the Root Directory).
- **Backend:** Can be hosted on platforms like Render, Railway, or AWS.

---

## 👨‍💻 Author

**Yahya el gzouli**
- GitHub: [@yahyaegz](https://github.com/yahyaegz)

<br />

<div align="center">
  <i>Made with ❤️ by Yahya el gzouli • Copyright &copy; 2026</i>
</div>
