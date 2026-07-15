import os
import pandas as pd
import numpy as np
from pathlib import Path
import time

def generate_synthetic_ednet(output_path, num_users=200, num_questions=500):
    print("Generating synthetic EdNet dataset...")
    np.random.seed(42)
    
    # 1. Question metadata
    question_ids = [f"q{i}" for i in range(1, num_questions + 1)]
    # True difficulty level in [0.2, 0.8] (probability of correct answer for average student)
    # Higher difficulty means harder question, i.e., lower baseline correct rate
    q_difficulty = {q: np.random.uniform(0.1, 0.9) for q in question_ids}
    
    # Assign tags (knowledge concepts) to each question
    tags_pool = [f"tag_{i}" for i in range(1, 15)]
    q_tags = {q: np.random.choice(tags_pool) for q in question_ids}
    
    # 2. User metadata
    user_ids = [f"u{i}" for i in range(1, num_users + 1)]
    # True student skill level from normal distribution
    u_skill = {u: np.random.normal(0, 1.2) for u in user_ids}
    
    records = []
    
    # 3. Simulate interactions
    for u in user_ids:
        skill = u_skill[u]
        # Number of interactions per user (50 to 180)
        num_interactions = np.random.randint(50, 180)
        
        start_time = int(time.time()) - np.random.randint(1000000, 5000000)
        
        for i in range(num_interactions):
            q = np.random.choice(question_ids)
            diff = q_difficulty[q]
            
            # IRT Rasch model: P(correct) = 1 / (1 + exp(-(skill - diff)))
            # We scale the exponent to make skill differences more distinct
            p_correct = 1 / (1 + np.exp(-(skill - (diff - 0.5) * 3)))
            correct = int(np.random.rand() < p_correct)
            
            elapsed_time = np.random.randint(5, 50) * 1000  # in ms
            timestamp = start_time + i * np.random.randint(30, 200)
            
            records.append({
                'user_id': u,
                'question_id': q,
                'correct': correct,
                'timestamp': timestamp,
                'elapsed_time': elapsed_time,
                'tags': q_tags[q],
                'difficulty': diff
            })
            
    df = pd.DataFrame(records)
    # Sort chronologically by student and timestamp
    df.sort_values(by=['user_id', 'timestamp'], inplace=True)
    
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic EdNet dataset with {len(df)} records.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    data_path = workspace_dir / "Model3_KnowledgeTracing" / "data" / "ednet_data.csv"
    generate_synthetic_ednet(data_path)
