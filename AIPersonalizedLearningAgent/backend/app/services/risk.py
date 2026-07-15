import pickle
from pathlib import Path
import pandas as pd
from typing import Optional
from app.core.exceptions import PredictionError
from app.services.model_loader import ModelLoader
from app.services.features_loader import FeaturesLoader
from app.schemas.predict import RiskResponse
from app.config.logging_config import get_logger

logger = get_logger("risk_service")

class RiskPredictionService:


    @classmethod
    def predict(cls, student_id: int, student_features: Optional[dict] = None) -> RiskResponse:
        """Predicts student failure/dropout risk score."""
        logger.info(f"Predicting risk for student {student_id}...")
        
        try:
            # 1. Retrieve features if not passed
            if student_features is None:
                student_features = FeaturesLoader.get_student_features(student_id)
            
            # 2. Extract model from loader
            model = ModelLoader.get_risk_model()
            
            if model is None:
                raise PredictionError("Risk model is not loaded in memory.")
            
            # 3. Align features
            feature_names = list(model.feature_names_in_)
            X = pd.DataFrame([student_features])
            
            # Check if any expected columns are missing and fill with defaults
            for col in feature_names:
                if col not in X.columns:
                    X[col] = 0
            X_aligned = X[feature_names]
            
            # 4. Run prediction (model is a pipeline, so no manual transform needed)
            risk_prob = float(model.predict_proba(X_aligned)[0, 1])
            is_at_risk = risk_prob >= 0.50
            
            logger.info(f"Risk prediction complete for student {student_id}: score={risk_prob:.4f} (at_risk={is_at_risk})")
            
            return RiskResponse(
                student_id=student_id,
                risk_score=risk_prob,
                is_at_risk=is_at_risk
            )
            
        except Exception as e:
            logger.error(f"Error predicting risk for student {student_id}: {str(e)}", exc_info=True)
            if "not found" in str(e).lower():
                raise e
            raise PredictionError(f"Risk prediction failed: {str(e)}")
