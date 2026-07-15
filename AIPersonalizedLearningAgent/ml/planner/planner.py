import yaml
import sys
from pathlib import Path

# Dynamically append workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from PersonalizedLearningAgent.ml.planner.load_models import get_student_predictions
from PersonalizedLearningAgent.ml.planner.prompt_builder import build_study_plan_prompt
from PersonalizedLearningAgent.ml.planner.llm_client import generate_study_plan
from PersonalizedLearningAgent.ml.planner.export_json import export_study_plan

def generate_and_export_plan(student_id, profile_info=None, config_path=None):
    """
    Main orchestrator for Model 6. Combines predictions from Models 1, 2, 4,
    builds the prompt, queries the LLM client, and saves the output files.
    """
    workspace_dir = Path(__file__).resolve().parents[3]
    m6_dir = workspace_dir / "PersonalizedLearningAgent"
    
    # 1. Load config
    if config_path is None:
        config_path = m6_dir / "config" / "settings.yaml"
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        
    print("Orchestrating AI Study Plan Generation...")
    
    # Merge default profile details if not provided
    if profile_info is None:
        profile_info = {}
    
    defaults = config.get("defaults", {})
    for key, val in defaults.items():
        if key not in profile_info:
            profile_info[key] = val
            
    # 2. Load model predictions
    perf, risk, weak = get_student_predictions(student_id)
    
    # 3. Construct prompt
    prompts_dir = m6_dir / "prompts"
    prompt = build_study_plan_prompt(student_id, perf, risk, weak, profile_info, prompts_dir)
    
    # 4. Run LLM inference or fallback
    raw_markdown, plan_dict = generate_study_plan(prompt, student_id, weak, profile_info, config)
    
    # 5. Export deliverables
    outputs_dir = m6_dir / "outputs"
    export_study_plan(plan_dict, raw_markdown, outputs_dir)
    
    print("AI Study Plan Orchestration Complete.")
    return raw_markdown, plan_dict

if __name__ == "__main__":
    profile = {
        "available_hours_per_day": 3.0,
        "learning_goal": "Review core concepts and prepare for the final assessment.",
        "current_course": "Mathematics Foundations",
        "target_exam_days_away": 7
    }
    generate_and_export_plan(1001, profile)
