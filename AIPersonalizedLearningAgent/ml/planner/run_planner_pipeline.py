import sys
from pathlib import Path
import argparse
import json

# Dynamically append workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[3]))

from PersonalizedLearningAgent.ml.planner.planner import generate_and_export_plan
from PersonalizedLearningAgent.ml.planner.utils import format_section_header, check_api_credentials

def main():
    parser = argparse.ArgumentParser(description="Model 6 — AI Study Planner Pipeline")
    parser.add_argument("--student_id", type=int, default=1001, help="Student ID to generate plan for")
    parser.add_argument("--hours", type=float, default=3.0, help="Available study hours per day")
    parser.add_argument("--goal", type=str, default="Review core concepts and prepare for the final assessment.", help="Learning goal")
    parser.add_argument("--course", type=str, default="Mathematics Foundations", help="Current student course")
    parser.add_argument("--days", type=int, default=7, help="Days until exam")
    
    args = parser.parse_args()
    
    print(format_section_header("STARTING STUDY PLAN ORCHESTRATION PIPELINE (MODEL 6)"))
    
    # Check credentials
    creds = check_api_credentials()
    print("API Credentials Status:")
    print(f"  OpenAI API Available: {creds['openai_available']}")
    print(f"  Gemini API Available: {creds['gemini_available']}")
    if not creds['any_available']:
        print("  --> No live API keys detected. Pipeline will utilize local structured plan generator fallback.")
        
    profile_info = {
        "available_hours_per_day": args.hours,
        "learning_goal": args.goal,
        "current_course": args.course,
        "target_exam_days_away": args.days
    }
    
    # Run the pipeline
    raw_markdown, plan_dict = generate_and_export_plan(args.student_id, profile_info)
    
    workspace_dir = Path(__file__).resolve().parents[3]
    outputs_dir = workspace_dir / "Model6_StudyPlanner" / "outputs"
    
    # Print Markdown overview
    print(format_section_header("GENERATED STUDY PLAN OVERVIEW"))
    print(raw_markdown[:1000])
    if len(raw_markdown) > 1000:
        print("\n... [plan truncated in console print, see outputs/study_plan.md] ...\n")
        
    # Verify JSON structure
    json_path = outputs_dir / "study_plan.json"
    with open(json_path, "r", encoding="utf-8") as f:
        loaded_json = json.load(f)
        
    print(format_section_header("JSON SCHEAM VERIFICATION"))
    print(f"Loaded successfully from: {json_path}")
    print(f"Student ID: {loaded_json.get('student_id')}")
    print(f"Number of days planned: {len(loaded_json.get('plan', []))}")
    print("Example Day 1 Tasks:")
    for task in loaded_json['plan'][0]['tasks']:
        print(f"  - {task['topic']} ({task['duration']})")
        
    print(format_section_header("PIPELINE COMPLETED SUCCESSFULLY"))

if __name__ == "__main__":
    main()
