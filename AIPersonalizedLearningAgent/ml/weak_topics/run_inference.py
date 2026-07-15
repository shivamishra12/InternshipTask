import sys
from pathlib import Path
# Dynamically append workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[3]))

from PersonalizedLearningAgent.ml.weak_topics.load_model import load_dkt_resources
from PersonalizedLearningAgent.ml.weak_topics.topic_mapping import load_topic_mapping
from PersonalizedLearningAgent.ml.weak_topics.inference import predict_question_mastery
from PersonalizedLearningAgent.ml.weak_topics.mastery import calculate_topic_mastery, detect_weak_topics
from PersonalizedLearningAgent.ml.weak_topics.export_json import export_results

def run_weak_topic_detection(student_id=1001):
    print("==================================================")
    print("STARTING WEAK TOPIC DETECTION PIPELINE (MODEL 4)")
    print("==================================================")
    
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    m4_dir = workspace_dir / "PersonalizedLearningAgent"
    models_dir = m4_dir / "models"
    data_path = m4_dir / "data" / "question_to_topic.csv"
    output_path = m4_dir / "outputs" / "weak_topics.json"
    
    # 1. Load resources
    model, encoder, config = load_dkt_resources(models_dir)
    
    # 2. Load topic mappings
    mapping, encoded_mapping = load_topic_mapping(data_path, encoder)
    
    # 3. Simulate Student history
    # Let's simulate student 1001 who:
    # - Has mastered Algebra (10 correct)
    # - Struggles with Geometry (10 incorrect)
    # - Has moderate performance in Statistics (6 correct, 4 incorrect)
    student_history = [
        # Algebra: 10 questions answered correctly
        ("q1", 1), ("q2", 1), ("q3", 1), ("q4", 1), ("q5", 1),
        ("q6", 1), ("q7", 1), ("q8", 1), ("q9", 1), ("q10", 1),
        # Geometry: 10 questions answered incorrectly
        ("q181", 0), ("q182", 0), ("q183", 0), ("q184", 0), ("q185", 0),
        ("q186", 0), ("q187", 0), ("q188", 0), ("q189", 0), ("q190", 0),
        # Statistics: mixed (6 correct, 4 incorrect)
        ("q351", 1), ("q352", 0), ("q353", 1), ("q354", 0), ("q355", 1),
        ("q356", 0), ("q357", 1), ("q358", 0), ("q359", 1), ("q360", 1)
    ]
    
    print("\nSimulated Student Interaction History:")
    for q_str, c in student_history:
        topic = mapping.get(q_str, "Unknown")
        result = "Correct" if c == 1 else "Incorrect"
        print(f"  Question: {q_str:<6} | Topic: {topic:<12} | Result: {result}")
        
    # 4. Predict Question Mastery
    question_mastery = predict_question_mastery(model, student_history, config['num_questions'], encoder)
    
    # 5. Calculate Topic Mastery
    topic_mastery = calculate_topic_mastery(question_mastery, mapping, student_history)
    
    # 6. Detect Weak Topics
    weak_topics, topic_status = detect_weak_topics(topic_mastery)
    
    # Print status report
    print("\nTopic Mastery Status Report:")
    for topic, score in topic_mastery.items():
        if topic != "Unknown":
            print(f"  Topic: {topic:<12} | Score: {score:.2f} | Status: {topic_status.get(topic)}")
            
    # 7. Export to JSON
    json_path = export_results(student_id, topic_mastery, weak_topics, output_path)
    
    # 8. Verify and display exported file contents
    print("\n================ EXPORTED JSON CONTENTS ================")
    with open(json_path, "r") as f:
        print(f.read())
    print("========================================================")
    
if __name__ == "__main__":
    run_weak_topic_detection()
