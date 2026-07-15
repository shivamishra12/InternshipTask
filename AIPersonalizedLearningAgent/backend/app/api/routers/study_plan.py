from fastapi import APIRouter, HTTPException
import logging
from app.schemas.predict import StudyPlanRequest, StudyPlanResponse
from app.schemas.student import StudentResponse
from app.services.study_planner import StudyPlannerService
from app.services.features_loader import FeaturesLoader
from app.services.performance import PerformancePredictionService
from app.services.risk import RiskPredictionService
from app.services.knowledge import KnowledgeTracingService
from app.services.weak_topics import WeakTopicService
from app.core.exceptions import StudentNotFoundError, PredictionError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/study-plan", tags=["Study Planner"])

@router.post("", response_model=StudyPlanResponse)
def generate_study_plan(request: StudyPlanRequest):
    logger.info(f"Received study plan generation request for student {request.student_id}")
    try:
        student_id = request.student_id
        
        # 1. Fetch features
        student_features = FeaturesLoader.get_student_features(student_id)
        
        # 2. Get predictions
        performance_resp = PerformancePredictionService.predict(student_id, student_features)
        risk_resp = RiskPredictionService.predict(student_id, student_features)
        knowledge_resp = KnowledgeTracingService().predict(student_id)
        weak_topics_resp = WeakTopicService().predict(student_id, knowledge_resp.question_mastery)
        weak_topic_names = [wt.topic for wt in weak_topics_resp if wt.mastery < 0.40]
        
        # 3. Setup profile info
        profile_info = {
            "available_hours_per_day": 3.0,
            "learning_goal": "Pass the course",
            "current_course": str(student_features.get("code_module", "Unknown")),
            "target_exam_days_away": 14
        }
        
        # 4. Generate plan
        service = StudyPlannerService()
        response = service.generate(
            student_id=student_id,
            predicted_performance=performance_resp.predicted_performance,
            risk_score=risk_resp.risk_score,
            weak_topics=weak_topic_names,
            profile_info=profile_info
        )
        return response
        
    except StudentNotFoundError as e:
        logger.warning(str(e))
        raise HTTPException(status_code=404, detail=str(e))
    except PredictionError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
