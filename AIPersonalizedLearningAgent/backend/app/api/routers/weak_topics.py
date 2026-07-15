from fastapi import APIRouter, HTTPException
import logging
from typing import List
from app.schemas.predict import WeakTopicRequest
from app.schemas.dashboard import WeakTopicResponse
from app.services.weak_topics import WeakTopicService
from app.core.exceptions import PredictionError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/weak-topics", tags=["Weak Topics"])

@router.post("", response_model=List[WeakTopicResponse])
def get_weak_topics(request: WeakTopicRequest):
    logger.info(f"Received weak topics request for student {request.student_id}")
    try:
        service = WeakTopicService()
        response = service.predict(request.student_id, request.question_mastery)
        return response
    except PredictionError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
