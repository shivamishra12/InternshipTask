import torch
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np
from pathlib import Path

class EdNetDataset(Dataset):
    def __init__(self, questions, prev_correctness, targets):
        """
        questions: tensor of shape (num_samples, seq_len)
        prev_correctness: tensor of shape (num_samples, seq_len)
        targets: tensor of shape (num_samples, seq_len)
        """
        self.questions = torch.tensor(questions, dtype=torch.long)
        self.prev_correctness = torch.tensor(prev_correctness, dtype=torch.float)
        self.targets = torch.tensor(targets, dtype=torch.float)
        
    def __len__(self):
        return len(self.questions)
        
    def __getitem__(self, idx):
        return {
            'questions': self.questions[idx],
            'prev_correctness': self.prev_correctness[idx],
            'targets': self.targets[idx]
        }

def prepare_sequences(preprocessed_df_path, window_size=50, step_size=20, num_questions=500):
    print(f"Loading preprocessed data from {preprocessed_df_path}...")
    df = pd.read_csv(preprocessed_df_path)
    
    # Group interactions by user
    user_groups = df.groupby('user_id')
    
    questions_list = []
    prev_correctness_list = []
    targets_list = []
    
    # We will use num_questions as the padding token for questions
    padding_q = num_questions 
    padding_c = 0.0 # padding for correctness
    
    for user_id, group in user_groups:
        q_seq = group['question_id_encoded'].values
        c_seq = group['correct'].values
        
        L = len(q_seq)
        
        if L < 2:
            continue
            
        # Case 1: Sequence is shorter than the window size
        if L < window_size:
            # Pad sequences
            pad_len = window_size - L
            
            # Question sequence: pad with padding_q at the beginning
            padded_q = np.full(window_size, padding_q)
            padded_q[pad_len:] = q_seq
            
            # Correctness sequence: pad with padding_c
            padded_c = np.full(window_size, padding_c)
            padded_c[pad_len:] = c_seq
            
            # Construct prev_correctness (shifted right by 1, filled with 0.0)
            prev_c = np.zeros(window_size)
            prev_c[pad_len+1:] = c_seq[:-1]
            # Use 0.5 as indicator for the first active step if we want, or just leave as 0.0
            
            questions_list.append(padded_q)
            prev_correctness_list.append(prev_c)
            targets_list.append(padded_c)
            
        # Case 2: Sequence is longer than the window size, extract sliding windows
        else:
            for start_idx in range(0, L - window_size + 1, step_size):
                end_idx = start_idx + window_size
                
                sub_q = q_seq[start_idx:end_idx]
                sub_c = c_seq[start_idx:end_idx]
                
                # Construct prev_correctness (shifted by 1)
                prev_c = np.zeros(window_size)
                prev_c[1:] = sub_c[:-1]
                
                questions_list.append(sub_q)
                prev_correctness_list.append(prev_c)
                targets_list.append(sub_c)
                
    questions = np.array(questions_list)
    prev_correctness = np.array(prev_correctness_list)
    targets = np.array(targets_list)
    
    print(f"Generated {len(questions)} sequences of length {window_size}.")
    return questions, prev_correctness, targets

def get_dataloaders(preprocessed_df_path, window_size=50, step_size=20, batch_size=64, test_size=0.2, val_size=0.1, num_questions=500):
    questions, prev_correctness, targets = prepare_sequences(
        preprocessed_df_path, window_size, step_size, num_questions
    )
    
    num_samples = len(questions)
    indices = np.arange(num_samples)
    np.random.seed(42)
    np.random.shuffle(indices)
    
    # Split indices: Train, Val, Test
    test_split = int(test_size * num_samples)
    val_split = int(val_size * num_samples)
    
    test_idx = indices[:test_split]
    val_idx = indices[test_split:test_split + val_split]
    train_idx = indices[test_split + val_split:]
    
    print(f"Train samples: {len(train_idx)} | Val samples: {len(val_idx)} | Test samples: {len(test_idx)}")
    
    train_dataset = EdNetDataset(questions[train_idx], prev_correctness[train_idx], targets[train_idx])
    val_dataset = EdNetDataset(questions[val_idx], prev_correctness[val_idx], targets[val_idx])
    test_dataset = EdNetDataset(questions[test_idx], prev_correctness[test_idx], targets[test_idx])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    return train_loader, val_loader, test_loader
