from fastapi import APIRouter, HTTPException
import logging
from app.schemas.predict import KnowledgeRequest, KnowledgeResponse
from app.services.knowledge import KnowledgeTracingService
from app.core.exceptions import StudentNotFoundError, PredictionError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/knowledge", tags=["Knowledge Tracing"])

@router.post("", response_model=KnowledgeResponse)
def predict_knowledge(request: KnowledgeRequest):
    logger.info(f"Received knowledge tracing request for student {request.student_id}")
    try:
        service = KnowledgeTracingService()
        response = service.predict(request.student_id, request.history)
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
