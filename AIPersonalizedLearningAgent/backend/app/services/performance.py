import pandas as pd
from typing import Optional
from app.core.exceptions import PredictionError
from app.services.model_loader import ModelLoader
from app.services.features_loader import FeaturesLoader
from app.schemas.predict import PerformanceResponse
from app.config.logging_config import get_logger

logger = get_logger("performance_service")

class PerformancePredictionService:
    @classmethod
    def predict(cls, student_id: int, student_features: Optional[dict] = None, study_hours: Optional[float] = None, quiz_score: Optional[float] = None) -> PerformanceResponse:
        """Predicts student performance (Pass or Fail) and success probability."""
        logger.info(f"Predicting performance for student {student_id}...")
        
        try:
            # 1. Retrieve features if not passed
            if student_features is None:
                student_features = FeaturesLoader.get_student_features(student_id)
            
            # 2. Extract model from loader
            model = ModelLoader.get_performance_model()
            if model is None:
                raise PredictionError("Performance model is not loaded in memory.")
            
            # 3. Prepare features DataFrame
            # Align features exactly with what the pipeline expects
            feature_names = list(model.feature_names_in_)
            
            # --- DATA MAPPING STRATEGY ---
            # If dynamic UI parameters are passed, overwrite the static historical database features
            if study_hours is not None:
                # Map 1 hour of study to roughly 50 clicks (a reasonable heuristic for the OULAD dataset)
                student_features['sum_click'] = study_hours * 50
            if quiz_score is not None:
                # Map quiz score directly to the average assessment score
                student_features['score'] = quiz_score
                
            X = pd.DataFrame([student_features])
            
            for col in feature_names:
                if col not in X.columns:
                    X[col] = 0
            X_aligned = X[feature_names]
            
            # 4. Run prediction
            predicted_class = int(model.predict(X_aligned)[0])
            prob_success = float(model.predict_proba(X_aligned)[0, 1])
            
            # 1 = Pass/Distinction, 0 = Fail/Withdrawn
            predicted_label = "Pass" if predicted_class == 1 else "Fail"
            
            logger.info(f"Performance prediction complete for student {student_id}: {predicted_label} (Success Prob: {prob_success:.4f})")
            
            return PerformanceResponse(
                student_id=student_id,
                predicted_performance=predicted_label,
                success_probability=prob_success
            )
            
        except Exception as e:
            logger.error(f"Error predicting performance for student {student_id}: {str(e)}", exc_info=True)
            if "not found" in str(e).lower():
                raise e
            raise PredictionError(f"Performance prediction failed: {str(e)}")
