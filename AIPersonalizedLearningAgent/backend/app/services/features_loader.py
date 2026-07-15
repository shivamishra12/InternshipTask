import pandas as pd
from pathlib import Path
from app.core.exceptions import StudentNotFoundError
from app.config.logging_config import get_logger

logger = get_logger("features_loader")

class FeaturesLoader:
    _df = None

    @classmethod
    def get_student_features(cls, student_id: int) -> dict:
        """Looks up a student ID in the engineered features dataset."""
        if cls._df is None:
            # Resolve workspace dir (4 levels up from this file)
            workspace_dir = Path(__file__).resolve().parents[3]
            csv_path = workspace_dir / "data" / "processed" / "engineered_features.csv"
            
            if not csv_path.exists():
                logger.error(f"Engineered features CSV not found at: {csv_path}")
                raise FileNotFoundError(f"Feature store file not found at {csv_path}")
            
            logger.info(f"Loading feature store from {csv_path}...")
            cls._df = pd.read_csv(csv_path)

        # Filter by student_id
        student_row = cls._df[cls._df["id_student"] == student_id]
        if student_row.empty:
            logger.warning(f"Student ID {student_id} not found in feature store.")
            raise StudentNotFoundError(student_id)

        # Return as dictionary
        return student_row.iloc[0].to_dict()
