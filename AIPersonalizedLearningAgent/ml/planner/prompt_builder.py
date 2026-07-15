from pathlib import Path

def build_study_plan_prompt(student_id, predicted_performance, risk_score, weak_topics, profile_info, output_dir=None):
    """
    Constructs a highly structured and personalized prompt for the LLM.
    Saves the prompt to prompts/study_plan_prompt.txt if output_dir is provided.
    """
    print("Building personalized prompt for LLM...")
    
    # 1. Format inputs
    weak_topics_str = "\n".join([f"- {topic}" for topic in weak_topics]) if weak_topics else "- None identified"
    available_hours = profile_info.get("available_hours_per_day", 3.0)
    goal = profile_info.get("learning_goal", "Prepare for final assessments.")
    course = profile_info.get("current_course", "General Course")
    days_away = profile_info.get("target_exam_days_away", 7)
    
    # 2. Template prompt
    prompt = f"""You are an educational mentor.

Student Profile
- Student ID: {student_id}
- Current Course: {course}
- Predicted Performance: {predicted_performance}
- Risk Score: {risk_score:.2f} (Scale 0-1, high score indicates student is at risk of failing)
- Weak Topics:
{weak_topics_str}

Study Details
- Available Study Time: {available_hours} hours/day
- Target Exam: {days_away} days away
- Learning Goal: {goal}

Generate a practical 7-day study plan.

Requirements:
1. Daily schedule (Day 1 to Day 7)
2. Focus topics and priorities (heavily prioritize weak topics)
3. Revision sessions and practice question blocks
4. Suggested rest breaks
5. Estimated study time per task
6. Return the response in both structured text and specify the JSON output format matches the schema:
{{
  "student_id": {student_id},
  "plan": [
    {{
      "day": 1,
      "tasks": [
        {{ "topic": "Topic Name", "duration": "Duration (e.g. 90 min)" }},
        ...
      ]
    }},
    ...
  ]
}}
"""
    
    # 3. Save prompt to file if path is specified
    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = output_dir / "study_plan_prompt.txt"
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"  Saved LLM prompt to: {prompt_path}")
        
    return prompt

if __name__ == "__main__":
    profile = {
        "available_hours_per_day": 3.0,
        "learning_goal": "Improve understanding before the final exam.",
        "current_course": "Mathematics",
        "target_exam_days_away": 7
    }
    prompt = build_study_plan_prompt(1001, "Pass", 0.84, ["Algebra", "Geometry"], profile, "PersonalizedLearningAgent/prompts")
    print("\nPrompt Preview:")
    print(prompt[:300] + "...")
