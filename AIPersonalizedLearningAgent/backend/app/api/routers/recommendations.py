from fastapi import APIRouter, HTTPException
import logging
from app.schemas.predict import RecommendationRequest, RecommendationResponse
from app.services.recommendation import RecommendationService
from app.core.exceptions import PredictionError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.post("", response_model=RecommendationResponse)
def get_recommendations(request: RecommendationRequest):
    logger.info(f"Received recommendations request for student {request.student_id}")
    try:
        service = RecommendationService()
        response = service.predict(request.student_id, k=request.k)
        return response
    except PredictionError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
