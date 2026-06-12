import torch
import torch.nn as nn

class MusicLSTM(nn.Module):
    def __init__(self, vocab_size, embedding_dim=256, hidden_dim=512, n_layers=2):
        super(MusicLSTM, self).__init__()
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, n_layers, batch_first=True, dropout=0.3)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_dim, vocab_size)
        
    def forward(self, x, hidden):
        # x: (batch_size, seq_length)
        embeds = self.embedding(x)
        # embeds: (batch_size, seq_length, embedding_dim)
        lstm_out, hidden = self.lstm(embeds, hidden)
        # lstm_out: (batch_size, seq_length, hidden_dim)
        
        # We only care about the output of the last time step for each sequence
        out = lstm_out[:, -1, :] 
        out = self.dropout(out)
        out = self.fc(out)
        return out, hidden
        
    def init_hidden(self, batch_size, device):
        weight = next(self.parameters()).data
        hidden = (weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device),
                  weight.new(self.n_layers, batch_size, self.hidden_dim).zero_().to(device))
        return hidden
