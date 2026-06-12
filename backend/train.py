import os
import pickle
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from model import MusicLSTM

PROCESSED_DIR = "processed_data"

def train_model(epochs=10, batch_size=64):
    print("Loading preprocessed data...")
    try:
        with open(os.path.join(PROCESSED_DIR, 'network_input.pkl'), 'rb') as f:
            network_input = pickle.load(f)
        with open(os.path.join(PROCESSED_DIR, 'network_output.pkl'), 'rb') as f:
            network_output = pickle.load(f)
        with open(os.path.join(PROCESSED_DIR, 'notes.pkl'), 'rb') as f:
            notes = pickle.load(f)
    except FileNotFoundError:
        print("Preprocessed data not found. Please run data_preparation.py first.")
        return False

    n_vocab = len(set(notes))
    
    if not torch.cuda.is_available():
        print("CRITICAL WARNING: The installed version of PyTorch is NOT compiled with CUDA enabled. Falling back to CPU. To fix this, you need to install the CUDA version of PyTorch.")
        device = torch.device("cpu")
    else:
        device = torch.device("cuda")
        
    print(f"Using device: {device}")

    # Convert to tensors
    x_tensor = torch.tensor(network_input, dtype=torch.long)
    y_tensor = torch.tensor(network_output, dtype=torch.long)
    
    dataset = TensorDataset(x_tensor, y_tensor)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, drop_last=True)

    model = MusicLSTM(n_vocab).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Dynamic Learning Rate Scheduler to act as the "Brakes"
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', factor=0.5, patience=5, verbose=True)

    print("Starting training...")
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        hidden = model.init_hidden(batch_size, device)
        
        for batch_i, (inputs, targets) in enumerate(dataloader):
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Detach hidden states
            hidden = tuple([each.data for each in hidden])
            
            model.zero_grad()
            output, hidden = model(inputs, hidden)
            
            loss = criterion(output, targets)
            loss.backward()
            
            # Prevent exploding gradients
            nn.utils.clip_grad_norm_(model.parameters(), 5)
            optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss/len(dataloader)
        print(f"Epoch {epoch+1}/{epochs} - Loss: {avg_loss:.4f}")
        
        # Apply the brakes if the loss stops going down
        scheduler.step(avg_loss)

    if not os.path.exists("weights"):
        os.makedirs("weights")
    torch.save(model.state_dict(), 'weights/music_lstm.pth')
    print("Training complete. Model saved to weights/music_lstm.pth")
    return True

if __name__ == '__main__':
    # Set to 200 epochs: The optimal sweet spot for GPU training to balance harmony and creativity
    train_model(epochs=200)
