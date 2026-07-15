import pandas as pd
from pathlib import Path

def load_topic_mapping(csv_path, encoder=None):
    """
    Loads question-to-topic mapping.
    If encoder (LabelEncoder) is provided, it maps encoded question IDs to topics.
    Returns:
        mapping: dict of {question_id: topic}
        encoded_mapping: dict of {encoded_question_id: topic} (if encoder is provided)
    """
    print(f"Loading topic mapping from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # 1. Base mapping (string question_id -> topic)
    mapping = dict(zip(df['question_id'].astype(str), df['topic'].astype(str)))
    
    encoded_mapping = {}
    if encoder is not None:
        # Fit-transform encoded ids to verify
        # Map encoder classes to topics
        for idx, q_str in enumerate(encoder.classes_):
            if q_str in mapping:
                encoded_mapping[idx] = mapping[q_str]
            else:
                encoded_mapping[idx] = "Unknown"  # Fallback
        print(f"  Mapped {len(encoded_mapping)} encoded question IDs to topics.")
        
    return mapping, encoded_mapping

if __name__ == "__main__":
    import pickle
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    m4_dir = workspace_dir / "Model4_WeakTopicDetection"
    csv_path = m4_dir / "data" / "question_to_topic.csv"
    
    # Load encoder
    with open(m4_dir / "models" / "question_encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
        
    mapping, encoded_mapping = load_topic_mapping(csv_path, encoder)
    print("Example string mapping (q1):", mapping.get("q1"))
    print("Example encoded mapping (0):", encoded_mapping.get(0))
