import os
import json
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import roc_auc_score, accuracy_score
import matplotlib.pyplot as plt

# Import custom modules
from PersonalizedLearningAgent.ml.dkt.dataset import get_dataloaders
from PersonalizedLearningAgent.ml.dkt.model import DKTModel

def train_dkt(preprocessed_csv_path, output_dir, num_questions=500, seq_len=50, epochs=30, batch_size=64, lr=0.001, patience=5):
    print("Initializing Datalloaders...")
    train_loader, val_loader, test_loader = get_dataloaders(
        preprocessed_df_path=preprocessed_csv_path,
        window_size=seq_len,
        step_size=20,
        batch_size=batch_size,
        num_questions=num_questions
    )
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Initialize model
    model = DKTModel(
        num_questions=num_questions,
        embedding_dim=128,
        hidden_dim=128,
        num_layers=2,
        dropout=0.3
    ).to(device)
    
    # Loss function with reduction='none' for masking
    loss_fn = nn.BCEWithLogitsLoss(reduction='none')
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    # Save hyperparameters config
    config = {
        'num_questions': num_questions,
        'seq_len': seq_len,
        'embedding_dim': 128,
        'hidden_dim': 128,
        'num_layers': 2,
        'dropout': 0.3,
        'learning_rate': lr,
        'batch_size': batch_size
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Saved hyperparameters config.json")
    
    # Track training history
    history = {
        'train_loss': [],
        'val_loss': [],
        'val_auc': []
    }
    
    best_val_auc = 0.0
    epochs_no_improve = 0
    best_model_path = output_dir / "dkt_model.pt"
    
    for epoch in range(1, epochs + 1):
        # --- Training Epoch ---
        model.train()
        total_train_loss = 0.0
        total_train_steps = 0
        
        for batch in train_loader:
            questions = batch['questions'].to(device)
            prev_correctness = batch['prev_correctness'].to(device)
            targets = batch['targets'].to(device)
            
            optimizer.zero_grad()
            
            logits = model(questions, prev_correctness)
            
            # Mask out padding elements where question is num_questions
            mask = (questions != num_questions).float()
            
            raw_loss = loss_fn(logits, targets)
            masked_loss = raw_loss * mask
            
            # Compute mean loss over active elements
            loss = masked_loss.sum() / (mask.sum() + 1e-8)
            
            loss.backward()
            optimizer.step()
            
            total_train_loss += loss.item()
            total_train_steps += 1
            
        avg_train_loss = total_train_loss / total_train_steps
        
        # --- Validation Epoch ---
        model.eval()
        total_val_loss = 0.0
        total_val_steps = 0
        
        val_preds_list = []
        val_targets_list = []
        
        with torch.no_grad():
            for batch in val_loader:
                questions = batch['questions'].to(device)
                prev_correctness = batch['prev_correctness'].to(device)
                targets = batch['targets'].to(device)
                
                logits = model(questions, prev_correctness)
                
                mask = (questions != num_questions).float()
                
                raw_loss = loss_fn(logits, targets)
                masked_loss = raw_loss * mask
                loss = masked_loss.sum() / (mask.sum() + 1e-8)
                
                total_val_loss += loss.item()
                total_val_steps += 1
                
                # Get valid predictions and targets (un-padded)
                probs = torch.sigmoid(logits)
                val_preds_list.extend(probs[mask == 1].cpu().numpy())
                val_targets_list.extend(targets[mask == 1].cpu().numpy())
                
        avg_val_loss = total_val_loss / total_val_steps
        
        # Compute validation AUC
        val_preds_arr = np.array(val_preds_list)
        val_targets_arr = np.array(val_targets_list)
        
        if len(np.unique(val_targets_arr)) > 1:
            avg_val_auc = roc_auc_score(val_targets_arr, val_preds_arr)
        else:
            avg_val_auc = 0.5
            
        history['train_loss'].append(avg_train_loss)
        history['val_loss'].append(avg_val_loss)
        history['val_auc'].append(avg_val_auc)
        
        print(f"Epoch {epoch:02d}/{epochs:02d} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Val AUC: {avg_val_auc:.4f}")
        
        # --- Early Stopping & Model Checkpointing ---
        if avg_val_auc > best_val_auc:
            best_val_auc = avg_val_auc
            epochs_no_improve = 0
            # Save best model
            torch.save(model.state_dict(), best_model_path)
            print(f"  --> Best model checkpointed with Val AUC: {best_val_auc:.4f}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                print(f"Early stopping triggered at epoch {epoch}. No validation AUC improvement for {patience} epochs.")
                break
                
    # Save training curve plot
    reports_dir = output_dir.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Val Loss')
    plt.title('Loss Curves')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.plot(history['val_auc'], label='Val AUC', color='orange')
    plt.title('Validation ROC-AUC')
    plt.xlabel('Epoch')
    plt.ylabel('ROC-AUC')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(reports_dir / "training_curve.png", dpi=300)
    plt.close()
    print(f"Saved training curve to {reports_dir / 'training_curve.png'}")
    
    return best_val_auc

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    model_3_dir = workspace_dir / "Model3_KnowledgeTracing"
    preprocessed_path = model_3_dir / "data" / "ednet_preprocessed.csv"
    output_dir = model_3_dir / "models"
    train_dkt(preprocessed_path, output_dir)
