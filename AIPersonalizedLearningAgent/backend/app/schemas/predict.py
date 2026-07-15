from typing import List, Dict, Optional
from pydantic import BaseModel, Field

# --- Performance Prediction ---
class PerformanceRequest(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    study_hours: Optional[float] = Field(None, description="Dynamic weekly study hours to override historical sum_clicks")
    quiz_score: Optional[float] = Field(None, description="Dynamic quiz score to override historical score")

class PerformanceResponse(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    predicted_performance: str = Field(..., description="Predicted status (Pass or Fail)", examples=["Pass"])
    success_probability: float = Field(..., description="Probability of passing (0.0 to 1.0)", examples=[0.85])

# --- Risk Prediction ---
class RiskRequest(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])

class RiskResponse(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    risk_score: float = Field(..., description="Probability of failure/dropout (0.0 to 1.0)", examples=[0.15])
    is_at_risk: bool = Field(..., description="True if risk_score exceeds safety threshold (e.g. 0.5)", examples=[False])

# --- Knowledge Tracing ---
class HistoryItem(BaseModel):
    question_id: str = Field(..., description="Identifier of the question answered", examples=["q15"])
    correctness: int = Field(..., description="Did the student answer correctly? 1 = Yes, 0 = No", ge=0, le=1, examples=[1])

class KnowledgeRequest(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    history: Optional[List[HistoryItem]] = Field(
        None, 
        description="Optional list of interactive questions answered recently to override database records"
    )

class KnowledgeResponse(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    question_mastery: Dict[str, float] = Field(
        ..., 
        description="Map of question IDs to predicted mastery probabilities"
    )

class WeakTopicRequest(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    question_mastery: Dict[str, float] = Field(
        ..., 
        description="Map of question IDs to predicted mastery probabilities"
    )

# --- Recommendation ---
class RecommendationRequest(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    k: int = Field(5, description="Number of recommendations to retrieve", ge=1, le=20, examples=[5])

class RecommendationItem(BaseModel):
    rank: int = Field(..., description="Recommendation ranking", examples=[1])
    id_site: int = Field(..., description="Learning resource ID (site ID)", examples=[546876])
    score: float = Field(..., description="Recommendation similarity/popularity score", examples=[0.985])
    type: str = Field(..., description="Recommendation algorithm source", examples=["Collaborative Filtering"])

class RecommendationResponse(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    recommendations: List[RecommendationItem] = Field(..., description="Ranked list of recommended resource items")

# --- Study Planner ---
class StudyPlanRequest(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])

class TaskItem(BaseModel):
    topic: str = Field(..., description="Study topic or task name", examples=["Algebra Fundamentals"])
    duration: str = Field(..., description="Duration of study session", examples=["90 min"])

class DayPlan(BaseModel):
    day: int = Field(..., description="Target study day number (1 to 7)", ge=1, le=7, examples=[1])
    tasks: List[TaskItem] = Field(..., description="List of tasks scheduled for this day")

class StudyPlanResponse(BaseModel):
    student_id: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    plan: List[DayPlan] = Field(..., description="7-Day structured tasks schedule")
    markdown_plan: str = Field(..., description="Full text study plan rendered in markdown format")
