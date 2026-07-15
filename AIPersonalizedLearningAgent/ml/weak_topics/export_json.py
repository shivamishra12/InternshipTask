import json
from pathlib import Path

def export_results(student_id, topic_mastery, weak_topics, output_path):
    """
    Exports the mastery scores and weak topics to a JSON file.
    
    student_id: student identifier (int or str)
    topic_mastery: dict of {topic_str: average_mastery}
    weak_topics: list of dicts [{"topic": topic_str, "mastery": score}]
    output_path: Path to save the JSON file
    """
    print(f"Exporting results for student {student_id} to JSON...")
    
    # 1. Clean mastery scores (remove "Unknown" if present)
    clean_mastery = {k: round(v, 2) for k, v in topic_mastery.items() if k != "Unknown"}
    
    # 2. Clean weak topics list
    clean_weak = []
    for wt in weak_topics:
        if wt['topic'] != "Unknown":
            clean_weak.append({
                "topic": wt['topic'],
                "mastery": round(wt['mastery'], 2)
            })
            
    # 3. Create payload
    payload = {
        "student_id": student_id,
        "mastery_scores": clean_mastery,
        "weak_topics": clean_weak
    }
    
    # 4. Save to file
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)
        
    print(f"  Saved weak topics JSON report to: {output_path}")
    return output_path

if __name__ == "__main__":
    import sys
    # Test export
    test_tm = {"Algebra": 0.9134, "Geometry": 0.3012, "Statistics": 0.7645}
    test_wt = [{"topic": "Geometry", "mastery": 0.3012}]
    out_file = Path("PersonalizedLearningAgent/outputs/weak_topics.json")
    export_results(1001, test_tm, test_wt, out_file)
    
    # Print content
    with open(out_file, "r") as f:
        print(f.read())
