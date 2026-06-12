import os
import threading
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import train
import generate

app = FastAPI(title="AI Music Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    n_notes: int = 100

training_in_progress = False

@app.post("/train")
def start_training(background_tasks: BackgroundTasks):
    global training_in_progress
    if training_in_progress:
        return {"status": "Training already in progress."}
    
    def run_training():
        global training_in_progress
        training_in_progress = True
        try:
            train.train_model(epochs=3) # short epoch for demo
        except Exception as e:
            print(f"Training failed: {e}")
        finally:
            training_in_progress = False

    background_tasks.add_task(run_training)
    return {"status": "Training started in background."}

@app.get("/train/status")
def get_training_status():
    return {"is_training": training_in_progress}

@app.post("/generate")
def generate_music(req: GenerateRequest):
    if not os.path.exists("weights/music_lstm.pth"):
        raise HTTPException(status_code=400, detail="Model weights not found. Please train the model first.")
        
    filename = generate.generate_music(n_notes=req.n_notes)
    if not filename:
        raise HTTPException(status_code=500, detail="Failed to generate music.")
        
    return {"filename": filename, "url": f"/midi/{filename}"}

@app.get("/midi/{filename}")
def get_midi(filename: str):
    filepath = os.path.join("generated_midi", filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath, media_type="audio/midi", filename=filename)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
