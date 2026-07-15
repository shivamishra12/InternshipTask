import sys
from pathlib import Path
# Dynamically append workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import json
import pickle
import torch
from PersonalizedLearningAgent.ml.dkt.model import DKTModel

def load_dkt_resources(models_dir):
    print(f"Loading DKT resources from {models_dir}...")
    models_dir = Path(models_dir)
    
    # 1. Load config
    config_path = models_dir / "dkt_config.json"
    with open(config_path, "r") as f:
        config = json.load(f)
    print("  Loaded config.json successfully.")
    
    # 2. Load Question Encoder
    encoder_path = models_dir / "dkt_question_encoder.pkl"
    with open(encoder_path, "rb") as f:
        encoder = pickle.load(f)
    print("  Loaded question_encoder.pkl successfully.")
    
    # 3. Initialize Model and Load State Dict
    model = DKTModel(
        num_questions=config['num_questions'],
        embedding_dim=config['embedding_dim'],
        hidden_dim=config['hidden_dim'],
        num_layers=config['num_layers'],
        dropout=config['dropout']
    )
    
    model_path = models_dir / "dkt_model.pt"
    # Load state dict
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    print("  Initialized and loaded dkt_model.pt successfully.")
    
    return model, encoder, config

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    models_dir = workspace_dir / "Model4_WeakTopicDetection" / "models"
    model, encoder, config = load_dkt_resources(models_dir)
    print("Successfully loaded model. Parameters count:", sum(p.numel() for p in model.parameters()))
