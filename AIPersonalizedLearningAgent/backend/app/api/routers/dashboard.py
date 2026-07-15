from fastapi import APIRouter, HTTPException, Path
from typing import Optional
from app.schemas.dashboard import DashboardResponse
from app.schemas.student import StudentResponse
from app.services.features_loader import FeaturesLoader
from app.services.performance import PerformancePredictionService
from app.services.risk import RiskPredictionService
from app.services.knowledge import KnowledgeTracingService
from app.services.weak_topics import WeakTopicService
from app.services.recommendation import RecommendationService
from app.services.study_planner import StudyPlannerService
from app.core.exceptions import StudentNotFoundError, PredictionError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/{student_id}", response_model=DashboardResponse)
def get_dashboard(student_id: int = Path(..., description="Unique OULAD student ID")):
    logger.info(f"Fetching dashboard for student {student_id}")
    
    try:
        # 1. Fetch student features (acting as our student database for now)
        student_features = FeaturesLoader.get_student_features(student_id)
        
        # Build StudentResponse
        # Some fields might be missing in features, so we provide defaults or extract them safely
        student_resp = StudentResponse(
            id_student=student_id,
            gender=str(student_features.get("gender", "Unknown")),
            region=str(student_features.get("region", "Unknown")),
            highest_education=str(student_features.get("highest_education", "Unknown")),
            imd_band=str(student_features.get("imd_band", "Unknown")),
            age_band=str(student_features.get("age_band", "Unknown")),
            num_of_prev_attempts=int(student_features.get("num_of_prev_attempts", 0)),
            disability=str(student_features.get("disability", "N")),
            available_hours_per_day=3.0,  # Mock default for study planner
            learning_goal="Pass the course",
            current_course=str(student_features.get("code_module", "Unknown")),
            target_exam_days_away=14
        )
        
        # 2. Run Predictions
        performance_resp = PerformancePredictionService.predict(student_id, student_features)
        risk_resp = RiskPredictionService.predict(student_id, student_features)
        
        # 3. Knowledge Tracing & Weak Topics
        knowledge_resp = KnowledgeTracingService().predict(student_id)
        
        # Convert dictionary to List[WeakTopicResponse]
        weak_topics_resp = WeakTopicService().predict(
            student_id, 
            knowledge_resp.question_mastery
        )
        
        weak_topic_names = [wt.topic for wt in weak_topics_resp if wt.mastery < 0.40] # assuming < 0.40 is weak
        
        # 4. Recommendations
        recommendations_resp = RecommendationService().predict(student_id, k=5)
        
        # 5. Study Planner
        profile_info = {
            "available_hours_per_day": student_resp.available_hours_per_day,
            "learning_goal": student_resp.learning_goal,
            "current_course": student_resp.current_course,
            "target_exam_days_away": student_resp.target_exam_days_away
        }
        
        study_plan_resp = StudyPlannerService().generate(
            student_id=student_id,
            predicted_performance=performance_resp.predicted_performance,
            risk_score=risk_resp.risk_score,
            weak_topics=weak_topic_names,
            profile_info=profile_info
        )
        
        # Build final unified response
        dashboard = DashboardResponse(
            student=student_resp,
            performance=performance_resp,
            risk=risk_resp,
            knowledge=knowledge_resp,
            weak_topics=weak_topics_resp,
            recommendations=recommendations_resp.recommendations,
            study_plan=study_plan_resp
        )
        
        return dashboard

    except StudentNotFoundError as e:
        logger.warning(f"Student {student_id} not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except PredictionError as e:
        logger.error(f"Prediction error for student {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating dashboard for student {student_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
