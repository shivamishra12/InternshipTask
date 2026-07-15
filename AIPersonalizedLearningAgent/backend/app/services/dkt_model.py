import torch
import torch.nn as nn

class DKTModel(nn.Module):
    def __init__(self, num_questions, embedding_dim=128, hidden_dim=128, num_layers=2, dropout=0.3):
        super(DKTModel, self).__init__()
        self.num_questions = num_questions
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Embedding layer (+1 to account for the padding token)
        self.embedding = nn.Embedding(num_questions + 1, embedding_dim, padding_idx=num_questions)
        
        # LSTM input size: embedding_dim + 1 (previous correctness)
        self.lstm = nn.LSTM(
            input_size=embedding_dim + 1,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0
        )
        
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(hidden_dim, 1)
        
    def forward(self, questions, prev_correctness):
        """
        questions: tensor of shape (batch_size, seq_len)
        prev_correctness: tensor of shape (batch_size, seq_len)
        """
        # 1. Embed question IDs: shape (batch_size, seq_len, embedding_dim)
        embedded_q = self.embedding(questions)
        
        # 2. Expand dimensions of prev_correctness: shape (batch_size, seq_len, 1)
        prev_c = prev_correctness.unsqueeze(-1)
        
        # 3. Concatenate question embeddings and previous correctness: shape (batch_size, seq_len, embedding_dim + 1)
        lstm_input = torch.cat([embedded_q, prev_c], dim=-1)
        
        # 4. Forward pass through LSTM: shape (batch_size, seq_len, hidden_dim)
        lstm_out, _ = self.lstm(lstm_input)
        
        # 5. Apply dropout and linear output layer: shape (batch_size, seq_len)
        out = self.dropout(lstm_out)
        logits = self.linear(out).squeeze(-1)
        
        return logits
