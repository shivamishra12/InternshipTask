import os
import json

def generate_study_plan(prompt, student_id, weak_topics, profile_info, config):
    """
    Orchestrates the LLM API call. If no keys are found or if the call fails,
    calls the local structured plan generation engine to output the final plan.
    Returns:
        raw_text: markdown formatted study plan
        plan_dict: structured plan dictionary matching JSON schema
    """
    provider = config.get("llm", {}).get("provider", "mock")
    api_key_env = config.get("llm", {}).get("api_key_env_var", "OPENAI_API_KEY")
    api_key = os.environ.get(api_key_env)
    
    if api_key and provider != "mock":
        print(f"API key found for {provider}. Attempting live API request...")
        try:
            if provider == "openai":
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=config.get("llm", {}).get("model", "gpt-4o"),
                    messages=[{"role": "user", "content": prompt}],
                    temperature=config.get("llm", {}).get("temperature", 0.2),
                    response_format={"type": "json_object"}
                )
                raw_json = response.choices[0].message.content
                plan_dict = json.loads(raw_json)
                
                # Render markdown from dict dynamically
                raw_text = render_markdown_plan(plan_dict, weak_topics, profile_info)
                return raw_text, plan_dict
            elif provider == "gemini":
                # Implement Gemini call if requested
                pass
        except Exception as e:
            print(f"  Live API call failed: {e}. Falling back to local generation...")
            
    # Fallback / Local Generation Engine
    print("Running Local Study Plan Generation Engine...")
    return generate_local_plan(student_id, weak_topics, profile_info)

def generate_local_plan(student_id, weak_topics, profile_info):
    """
    Generates a personalized 7-day study plan programmatically based on the student profile.
    """
    hours = profile_info.get("available_hours_per_day", 3.0)
    total_mins = int(hours * 60)
    
    # Distribute minutes: e.g. 50% weak topic, 25% other revision, 15% quiz, 10% review
    weak_mins = int(total_mins * 0.5)
    rev_mins = int(total_mins * 0.25)
    quiz_mins = int(total_mins * 0.15)
    break_mins = int(total_mins * 0.1)
    
    weak_topic_label = weak_topics[0] if weak_topics else "General Revision"
    other_topic_label = "Algebra" if "Geometry" in weak_topics else "Geometry"
    
    plan_dict = {
        "student_id": student_id,
        "plan": []
    }
    
    markdown_lines = [
        f"# 7-Day Personalized Study Plan — Student {student_id}\n",
        f"**Profile Overview:**",
        f"- **Focus Areas (Weak Topics):** {', '.join(weak_topics) if weak_topics else 'None identified'}",
        f"- **Daily Study Budget:** {hours} hours/day ({total_mins} mins)",
        f"- **Learning Goal:** {profile_info.get('learning_goal')}\n",
        "---"
    ]
    
    # 7-day loop
    for day in range(1, 8):
        day_tasks = []
        markdown_lines.append(f"\n## Day {day}\n")
        
        if day == 7:
            # Day 7 is Mock Test & review
            mock_mins = int(total_mins * 0.6)
            review_mins = int(total_mins * 0.3)
            break_t = total_mins - mock_mins - review_mins
            
            day_tasks.append({"topic": "Mock Exam (Full Length)", "duration": f"{mock_mins} min"})
            day_tasks.append({"topic": "Review Mistakes & Final Revision", "duration": f"{review_mins} min"})
            day_tasks.append({"topic": "Rest & Relaxation", "duration": f"{break_t} min"})
            
            markdown_lines.append(f"- **Mock Exam:** {mock_mins} min focus on simulated tests.")
            markdown_lines.append(f"- **Review Mistakes:** {review_mins} min review.")
            markdown_lines.append(f"- **Rest:** {break_t} min rest breaks.")
            
        elif day % 2 == 1:
            # Odd Days: Theory & core topic study
            day_tasks.append({"topic": f"{weak_topic_label} Fundamentals", "duration": f"{weak_mins} min"})
            day_tasks.append({"topic": f"{other_topic_label} Basics", "duration": f"{rev_mins} min"})
            day_tasks.append({"topic": "Active Recall Quiz", "duration": f"{quiz_mins} min"})
            day_tasks.append({"topic": "Rest Break", "duration": f"{break_mins} min"})
            
            markdown_lines.append(f"- **Core Topic ({weak_topic_label}):** {weak_mins} min reviewing core concepts.")
            markdown_lines.append(f"- **Secondary Topic ({other_topic_label}):** {rev_mins} min basics review.")
            markdown_lines.append(f"- **Practice:** {quiz_mins} min quiz block.")
            markdown_lines.append(f"- **Breaks:** {break_mins} min rest break.")
        else:
            # Even Days: Practice & Exercises
            day_tasks.append({"topic": f"{weak_topic_label} Practice Problems", "duration": f"{weak_mins} min"})
            day_tasks.append({"topic": f"{other_topic_label} Advanced Exercises", "duration": f"{rev_mins} min"})
            day_tasks.append({"topic": "Review Mistakes & Feedback", "duration": f"{quiz_mins + break_mins} min"})
            
            markdown_lines.append(f"- **Core Practice ({weak_topic_label}):** {weak_mins} min active problem-solving.")
            markdown_lines.append(f"- **Secondary Practice ({other_topic_label}):** {rev_mins} min practice.")
            markdown_lines.append(f"- **Review:** {quiz_mins + break_mins} min reviewing errors.")
            
        plan_dict["plan"].append({
            "day": day,
            "tasks": day_tasks
        })
        
    raw_text = "\n".join(markdown_lines)
    return raw_text, plan_dict

def render_markdown_plan(plan_dict, weak_topics, profile_info):
    """
    Renders a markdown study plan from the JSON model output.
    """
    student_id = plan_dict.get("student_id", 1001)
    markdown_lines = [
        f"# 7-Day Personalized Study Plan — Student {student_id}\n",
        f"**Profile Overview:**",
        f"- **Focus Areas (Weak Topics):** {', '.join(weak_topics) if weak_topics else 'None identified'}",
        f"- **Daily Study Budget:** {profile_info.get('available_hours_per_day')} hours/day",
        f"- **Learning Goal:** {profile_info.get('learning_goal')}\n",
        "---"
    ]
    for day_info in plan_dict.get("plan", []):
        markdown_lines.append(f"\n## Day {day_info['day']}\n")
        for task in day_info.get("tasks", []):
            markdown_lines.append(f"- **{task['topic']}**: {task['duration']}")
            
    return "\n".join(markdown_lines)
