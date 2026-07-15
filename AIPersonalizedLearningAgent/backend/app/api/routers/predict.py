from fastapi import APIRouter, HTTPException
import logging
from app.schemas.predict import PerformanceRequest, PerformanceResponse, RiskRequest, RiskResponse
from app.services.performance import PerformancePredictionService
from app.services.risk import RiskPredictionService
from app.core.exceptions import StudentNotFoundError, PredictionError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/predict", tags=["Predictions"])

@router.post("/performance", response_model=PerformanceResponse)
def predict_performance(request: PerformanceRequest):
    logger.info(f"Received performance prediction request for student {request.student_id}")
    try:
        response = PerformancePredictionService.predict(
            request.student_id, 
            study_hours=request.study_hours, 
            quiz_score=request.quiz_score
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

@router.post("/risk", response_model=RiskResponse)
def predict_risk(request: RiskRequest):
    logger.info(f"Received risk prediction request for student {request.student_id}")
    try:
        response = RiskPredictionService.predict(request.student_id)
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
