from typing import List
from pydantic import BaseModel, Field
from app.schemas.student import StudentResponse
from app.schemas.predict import (
    PerformanceResponse,
    RiskResponse,
    KnowledgeResponse,
    RecommendationItem,
    StudyPlanResponse
)

class WeakTopicResponse(BaseModel):
    topic: str = Field(..., description="Name of the weak topic identified", examples=["Geometry"])
    mastery: float = Field(..., description="Average mastery level of the topic (0.0 to 1.0)", examples=[0.24])

class DashboardResponse(BaseModel):
    student: StudentResponse = Field(..., description="Student profile details")
    performance: PerformanceResponse = Field(..., description="Performance prediction results")
    risk: RiskResponse = Field(..., description="Risk assessment results")
    knowledge: KnowledgeResponse = Field(..., description="DKT knowledge mastery details")
    weak_topics: List[WeakTopicResponse] = Field(..., description="Identified weak topics requiring study focus")
    recommendations: List[RecommendationItem] = Field(..., description="Ranked list of recommended learning resource sites")
    study_plan: StudyPlanResponse = Field(..., description="Personalized 7-day study plan program")
