import json
import logging
from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.predict import StudyPlanResponse, DayPlan, TaskItem

logger = logging.getLogger(__name__)

class StudyPlannerService:
    def __init__(self):
        self.llm_provider = settings.LLM_PROVIDER.lower()
        self.api_key = settings.OPENAI_API_KEY
        
    def generate(
        self,
        student_id: int,
        predicted_performance: str,
        risk_score: float,
        weak_topics: List[str],
        profile_info: Dict[str, Any]
    ) -> StudyPlanResponse:
        logger.info(f"Generating study plan for student {student_id} using provider: {self.llm_provider}")
        
        if self.llm_provider == "openai" and self.api_key:
            try:
                return self._generate_with_openai(
                    student_id, predicted_performance, risk_score, weak_topics, profile_info
                )
            except Exception as e:
                logger.error(f"OpenAI generation failed: {e}. Falling back to mock generator.")
        
        return self._generate_mock_plan(
            student_id, predicted_performance, risk_score, weak_topics, profile_info
        )

    def _generate_with_openai(
        self,
        student_id: int,
        predicted_performance: str,
        risk_score: float,
        weak_topics: List[str],
        profile_info: Dict[str, Any]
    ) -> StudyPlanResponse:
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        
        system_prompt = (
            "You are an expert AI tutor. Generate a personalized 7-day study plan for a student. "
            "Output MUST be a JSON object with a single key 'plan', which maps to an array of 7 daily plans. "
            "Each daily plan must have a 'day' (integer 1-7) and 'tasks', where 'tasks' is an array of objects "
            "with 'topic' (string) and 'duration' (string like '60 min')."
        )
        
        user_prompt = (
            f"Student Info:\n"
            f"- Predicted Performance: {predicted_performance}\n"
            f"- Risk Score: {risk_score:.2f}\n"
            f"- Weak Topics: {', '.join(weak_topics) if weak_topics else 'None specific'}\n"
            f"- Profile: {json.dumps(profile_info)}\n\n"
            "Create a focused 7-day plan addressing the weak topics and mitigating risk."
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        parsed = json.loads(content)
        
        days_data = parsed.get("plan", [])
        
        plan_objects = []
        markdown_lines = [f"# Personalized 7-Day Study Plan\n\n**Risk Score:** {risk_score:.2f} | **Predicted:** {predicted_performance}\n"]
        
        for d in days_data:
            day_num = d.get("day")
            tasks = d.get("tasks", [])
            
            task_items = []
            markdown_lines.append(f"## Day {day_num}")
            for t in tasks:
                topic = t.get("topic", "General Study")
                duration = t.get("duration", "30 min")
                task_items.append(TaskItem(topic=topic, duration=duration))
                markdown_lines.append(f"- **{topic}**: {duration}")
            markdown_lines.append("")
                
            plan_objects.append(DayPlan(day=day_num, tasks=task_items))
            
        markdown_plan = "\n".join(markdown_lines)
        
        return StudyPlanResponse(
            student_id=student_id,
            plan=plan_objects,
            markdown_plan=markdown_plan
        )
        
    def _generate_mock_plan(
        self,
        student_id: int,
        predicted_performance: str,
        risk_score: float,
        weak_topics: List[str],
        profile_info: Dict[str, Any]
    ) -> StudyPlanResponse:
        # Programmatic fallback
        plan_objects = []
        markdown_lines = [f"# Personalized 7-Day Study Plan\n\n**Risk Score:** {risk_score:.2f} | **Predicted:** {predicted_performance}\n"]
        
        topics_to_cover = weak_topics if weak_topics else ["General Review", "Practice Test"]
        
        for day in range(1, 8):
            topic = topics_to_cover[(day - 1) % len(topics_to_cover)]
            duration = "60 min" if risk_score > 0.5 else "45 min"
            
            task_items = [TaskItem(topic=topic, duration=duration)]
            if day in [3, 6]:
                task_items.append(TaskItem(topic="Review & Quiz", duration="30 min"))
                
            plan_objects.append(DayPlan(day=day, tasks=task_items))
            
            markdown_lines.append(f"## Day {day}")
            for t in task_items:
                markdown_lines.append(f"- **{t.topic}**: {t.duration}")
            markdown_lines.append("")
            
        markdown_plan = "\n".join(markdown_lines)
        
        return StudyPlanResponse(
            student_id=student_id,
            plan=plan_objects,
            markdown_plan=markdown_plan
        )
