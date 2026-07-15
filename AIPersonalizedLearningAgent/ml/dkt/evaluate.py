import os
import json
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, classification_report, roc_curve
)
import matplotlib.pyplot as plt

# Import custom modules
from PersonalizedLearningAgent.ml.dkt.dataset import get_dataloaders
from PersonalizedLearningAgent.ml.dkt.model import DKTModel

def evaluate_dkt(preprocessed_csv_path, models_dir, num_questions=500, seq_len=50, batch_size=64):
    print("Evaluating DKT Model on test set...")
    _, _, test_loader = get_dataloaders(
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
    
    # Load weights
    weights_path = models_dir / "dkt_model.pt"
    if not weights_path.exists():
        raise FileNotFoundError(f"Model weights file not found at: {weights_path}")
        
    model.load_state_dict(torch.load(weights_path, map_location=device))
    model.eval()
    
    test_preds_list = []
    test_targets_list = []
    
    with torch.no_grad():
        for batch in test_loader:
            questions = batch['questions'].to(device)
            prev_correctness = batch['prev_correctness'].to(device)
            targets = batch['targets'].to(device)
            
            logits = model(questions, prev_correctness)
            mask = (questions != num_questions).float()
            
            probs = torch.sigmoid(logits)
            
            # Mask out padding elements
            test_preds_list.extend(probs[mask == 1].cpu().numpy())
            test_targets_list.extend(targets[mask == 1].cpu().numpy())
            
    test_preds = np.array(test_preds_list)
    test_targets = np.array(test_targets_list)
    
    # Binarize predictions for classification report
    test_preds_binary = (test_preds >= 0.5).astype(int)
    
    acc = accuracy_score(test_targets, test_preds_binary)
    prec = precision_score(test_targets, test_preds_binary)
    rec = recall_score(test_targets, test_preds_binary)
    f1 = f1_score(test_targets, test_preds_binary)
    auc = roc_auc_score(test_targets, test_preds)
    
    print("\n================ TEST SET METRICS ================")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {auc:.4f}")
    print("==================================================")
    
    print("\nClassification Report:")
    print(classification_report(test_targets, test_preds_binary, target_names=["Incorrect", "Correct"]))
    
    # Save ROC Curve Plot
    reports_dir = models_dir.parent / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    fpr, tpr, _ = roc_curve(test_targets, test_preds)
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color='blue', lw=2, label=f'DKT ROC Curve (AUC = {auc:.4f})')
    plt.plot([0, 1], [0, 1], color='grey', linestyle='--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('DKT LSTM Model ROC Curve')
    plt.legend(loc='lower right')
    plt.tight_layout()
    
    plt.savefig(reports_dir / "roc_curve.png", dpi=300)
    plt.close()
    print(f"Saved ROC curve plot to: {reports_dir / 'roc_curve.png'}")
    
    # Save evaluation metrics
    metrics = {
        'test_accuracy': acc,
        'test_precision': prec,
        'test_recall': rec,
        'test_f1': f1,
        'test_auc': auc
    }
    with open(models_dir / "metrics_test.json", "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"Saved test metrics to: {models_dir / 'metrics_test.json'}")
    
    return metrics

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    model_3_dir = workspace_dir / "Model3_KnowledgeTracing"
    preprocessed_path = model_3_dir / "data" / "ednet_preprocessed.csv"
    models_dir = model_3_dir / "models"
    evaluate_dkt(preprocessed_path, models_dir)
