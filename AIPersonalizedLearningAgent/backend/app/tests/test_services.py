import sys
from pathlib import Path
import pytest
from unittest.mock import patch

# Append the app directory's parent to path so app can be imported
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.services.model_loader import ModelLoader
from app.services.performance import PerformancePredictionService
from app.services.risk import RiskPredictionService
from app.services.knowledge import KnowledgeTracingService
from app.services.recommendation import RecommendationService
from app.services.weak_topics import WeakTopicService
from app.services.study_planner import StudyPlannerService

from app.schemas.predict import (
    PerformanceResponse,
    RiskResponse,
    KnowledgeResponse,
    RecommendationResponse,
    StudyPlanResponse
)

# Load models once for all tests
workspace_dir = Path(__file__).resolve().parents[3]
try:
    ModelLoader.load_all_models(workspace_dir)
    MODELS_LOADED = True
except Exception as e:
    MODELS_LOADED = False
    print(f"Warning: Models could not be loaded: {e}")

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_performance_service():
    service = PerformancePredictionService()
    # Test with dummy student 11391 (or any integer)
    response = service.predict(11391)
    
    assert isinstance(response, PerformanceResponse)
    assert response.student_id == 11391
    assert response.predicted_performance in ["Pass", "Fail", "Distinction", "Withdrawn"]
    assert 0.0 <= response.success_probability <= 1.0

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_risk_service():
    service = RiskPredictionService()
    response = service.predict(11391)
    
    assert isinstance(response, RiskResponse)
    assert response.student_id == 11391
    assert 0.0 <= response.risk_score <= 1.0
    assert isinstance(response.is_at_risk, bool)

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_knowledge_tracing_service():
    service = KnowledgeTracingService()
    response = service.predict(11391)
    
    assert isinstance(response, KnowledgeResponse)
    assert response.student_id == 11391
    assert isinstance(response.question_mastery, dict)

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_weak_topics_service():
    service = WeakTopicService()
    
    dummy_mastery = {
        "q1": 0.2,
        "q2": 0.8,
        "q3": 0.3
    }
    
    responses = service.predict(11391, dummy_mastery)
    assert isinstance(responses, list)
    # The output should be a list of WeakTopicResponse
    if len(responses) > 0:
        assert hasattr(responses[0], "topic")
        assert hasattr(responses[0], "mastery")

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_recommendation_service():
    service = RecommendationService()
    response = service.predict(11391, k=3)
    
    assert isinstance(response, RecommendationResponse)
    assert response.student_id == 11391
    assert len(response.recommendations) <= 3

def test_study_planner_service():
    # Set to mock provider for consistent testing
    with patch("app.services.study_planner.settings.LLM_PROVIDER", "mock"):
        service = StudyPlannerService()
        response = service.generate(
            student_id=11391,
            predicted_performance="Fail",
            risk_score=0.75,
            weak_topics=["Algebra", "Geometry"],
            profile_info={"study_hours": 10}
        )
        
        assert isinstance(response, StudyPlanResponse)
        assert response.student_id == 11391
        assert len(response.plan) == 7
        assert "Personalized 7-Day Study Plan" in response.markdown_plan
        assert "Algebra" in response.markdown_plan or "Geometry" in response.markdown_plan

if __name__ == "__main__":
    test_performance_service()
    test_risk_service()
    test_knowledge_tracing_service()
    test_weak_topics_service()
    test_recommendation_service()
    test_study_planner_service()
    print("All service tests passed successfully!")
