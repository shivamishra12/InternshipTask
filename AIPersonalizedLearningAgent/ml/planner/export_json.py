import json
from pathlib import Path

def export_study_plan(plan_dict, raw_markdown, outputs_dir):
    """
    Exports both the JSON and Markdown study plans to the outputs directory.
    """
    print(f"Exporting study plan files to {outputs_dir}...")
    outputs_dir = Path(outputs_dir)
    outputs_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Export JSON
    json_path = outputs_dir / "study_plan.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(plan_dict, f, indent=4)
    print(f"  Saved JSON study plan: {json_path}")
    
    # 2. Export Markdown
    md_path = outputs_dir / "study_plan.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(raw_markdown)
    print(f"  Saved Markdown study plan: {md_path}")
    
    return json_path, md_path

if __name__ == "__main__":
    plan = {
        "student_id": 1001,
        "plan": [
            {
                "day": 1,
                "tasks": [{"topic": "Algebra", "duration": "90 min"}]
            }
        ]
    }
    export_study_plan(plan, "# Day 1: Algebra Fundamentals (90 min)", "PersonalizedLearningAgent/outputs")
