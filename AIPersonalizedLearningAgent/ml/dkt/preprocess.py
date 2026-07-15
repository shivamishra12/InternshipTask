import os
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from sklearn.preprocessing import LabelEncoder

def preprocess_ednet_data(data_path, output_path):
    data_path = Path(data_path)
    output_path = Path(output_path)
    
    print("Preprocessing EdNet data...")
    # Load dataset
    df = pd.read_csv(data_path)
    print(f"Original shape: {df.shape}")
    
    # 1. Clean missing values and duplicates
    df.dropna(subset=['user_id', 'question_id', 'correct', 'timestamp'], inplace=True)
    df.drop_duplicates(subset=['user_id', 'timestamp', 'question_id'], inplace=True)
    print(f"Shape after cleaning: {df.shape}")
    
    # 2. Sort interactions chronologically per student
    df.sort_values(by=['user_id', 'timestamp'], ascending=[True, True], inplace=True)
    
    # 3. Label encode question IDs
    print("Encoding Question IDs...")
    le = LabelEncoder()
    df['question_id_encoded'] = le.fit_transform(df['question_id'].astype(str))
    
    # Save LabelEncoder to PersonalizedLearningAgent/models/
    models_dir = output_path.parents[1] / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    encoder_path = models_dir / "dkt_question_encoder.pkl"
    with open(encoder_path, "wb") as f:
        pickle.dump(le, f)
    print(f"Saved Question Encoder to: {encoder_path}")
    print(f"Total Unique Questions: {len(le.classes_)}")
    
    # 4. Save preprocessed dataset
    df.to_csv(output_path, index=False)
    print(f"Saved preprocessed data to: {output_path}")
    return df

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    data_path = workspace_dir / "PersonalizedLearningAgent" / "data" / "raw" / "ednet" / "ednet_data.csv"
    output_path = workspace_dir / "PersonalizedLearningAgent" / "data" / "processed" / "ednet_preprocessed.csv"
    preprocess_ednet_data(data_path, output_path)
