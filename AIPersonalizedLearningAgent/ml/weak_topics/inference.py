import torch
import numpy as np

def predict_question_mastery(model, student_history, num_questions, encoder, seq_len=50):
    """
    Runs DKT inference on student history to predict mastery for all questions in the bank.
    Pads the sequence at the beginning to match the training sequence length (seq_len).
    
    student_history: list of tuples (question_id_str, correctness)
                     e.g. [("q12", 1), ("q15", 0), ("q18", 1)]
    num_questions: total number of questions (excluding padding)
    encoder: fitted LabelEncoder for question IDs
    seq_len: standard sequence length of the DKT model (default 50)
    
    Returns:
        mastery_dict: dict of {question_id_str: mastery_probability}
    """
    print(f"Running DKT inference on student history of length {len(student_history)}...")
    
    # 1. Parse and encode student history
    encoded_history_q = []
    history_c = []
    
    for q_str, c in student_history:
        try:
            q_enc = encoder.transform([q_str])[0]
            encoded_history_q.append(q_enc)
            history_c.append(float(c))
        except ValueError:
            # Skip unknown questions silently
            continue
            
    k = len(encoded_history_q)
    if k == 0:
        # Fallback: if no history, predict baseline mastery (0.5) for all questions
        print("  Warning: Empty or invalid student history. Returning baseline mastery.")
        return {q_str: 0.5 for q_str in encoder.classes_}
        
    # Truncate history if it exceeds the maximum sequence length (minus 1 step for candidate question)
    if k > seq_len - 1:
        encoded_history_q = encoded_history_q[-(seq_len - 1):]
        history_c = history_c[-(seq_len - 1):]
        k = len(encoded_history_q)
        
    # 2. Build padded tensors of shape (num_questions, seq_len)
    questions_tensor = torch.full((num_questions, seq_len), num_questions, dtype=torch.long)
    prev_c_tensor = torch.zeros((num_questions, seq_len), dtype=torch.float)
    
    # Calculate offset for padding at the beginning
    pad_len = seq_len - k - 1
    
    # Fill history questions in the slice [pad_len : pad_len+k]
    questions_tensor[:, pad_len:pad_len+k] = torch.tensor(encoded_history_q, dtype=torch.long)
    # Fill the last timestep with the candidate question indices (0 to num_questions - 1)
    questions_tensor[:, seq_len - 1] = torch.arange(num_questions, dtype=torch.long)
    
    # Shift correctness: prev_c_tensor at pad_len is 0.0, pad_len+1..pad_len+k is history_c[0..k-1]
    prev_c_tensor[:, pad_len+1:pad_len+k+1] = torch.tensor(history_c, dtype=torch.float)
    
    # 3. Model forward pass
    with torch.no_grad():
        # logits shape: (num_questions, seq_len)
        logits = model(questions_tensor, prev_c_tensor)
        # Extract the probability at the final timestep
        probs = torch.sigmoid(logits[:, -1])
        
    # 4. Map probabilities back to question ID strings
    mastery_dict = {}
    for idx, q_str in enumerate(encoder.classes_):
        mastery_dict[q_str] = float(probs[idx].item())
        
    print(f"  Inference complete. Predicted mastery for {len(mastery_dict)} questions.")
    return mastery_dict

if __name__ == "__main__":
    from pathlib import Path
    from PersonalizedLearningAgent.ml.weak_topics.load_model import load_dkt_resources
    
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    models_dir = workspace_dir / "Model4_WeakTopicDetection" / "models"
    model, encoder, config = load_dkt_resources(models_dir)
    
    # Simulate history: student has answered 5 Algebra questions successfully, and 5 Geometry questions incorrectly
    sim_history = [
        ("q1", 1), ("q2", 1), ("q3", 1), ("q4", 1), ("q5", 1), # Algebra
        ("q190", 0), ("q191", 0), ("q192", 0), ("q193", 0), ("q194", 0) # Geometry
    ]
    
    mastery = predict_question_mastery(model, sim_history, config['num_questions'], encoder)
    # Print some examples
    print("Mastery for q1 (Algebra):", mastery.get("q1"))
    print("Mastery for q190 (Geometry):", mastery.get("q190"))
    print("Mastery for q360 (Statistics):", mastery.get("q360"))
