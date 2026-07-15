import sys
from pathlib import Path
import pytest
import torch
from scipy.sparse import csr_matrix

# Append the app directory's parent to path so app can be imported
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.services.model_loader import ModelLoader
from app.services.dkt_model import DKTModel

def test_model_loader():
    # Resolve workspace dir (4 levels up from this test file)
    workspace_dir = Path(__file__).resolve().parents[3]
    
    # Run loader
    ModelLoader.load_all_models(workspace_dir)
    
    # 1. Performance Model Getters
    perf_model = ModelLoader.get_performance_model()
    assert perf_model is not None, "Performance model should not be None"
    
    perf_prep = ModelLoader.get_performance_preprocessor()
    assert perf_prep is not None, "Performance preprocessor should not be None"
    
    # 2. Risk Model Getters
    risk_model = ModelLoader.get_risk_model()
    assert risk_model is not None, "Risk model should not be None"
    
    risk_prep = ModelLoader.get_risk_preprocessor()
    assert risk_prep is not None, "Risk preprocessor should not be None"
    
    # 3. DKT Model Getters
    dkt_model = ModelLoader.get_dkt_model()
    assert dkt_model is not None, "DKT model should not be None"
    assert isinstance(dkt_model, DKTModel), "DKT model should be an instance of DKTModel"
    
    dkt_encoder = ModelLoader.get_dkt_encoder()
    assert dkt_encoder is not None, "DKT encoder should not be None"
    assert hasattr(dkt_encoder, "classes_"), "DKT encoder should have classes_ attribute"
    
    dkt_config = ModelLoader.get_dkt_config()
    assert dkt_config is not None, "DKT config should not be None"
    assert "num_questions" in dkt_config, "DKT config should contain num_questions key"
    
    # 4. Recommendation Model Getters
    rec_package = ModelLoader.get_recommendation_package()
    assert rec_package is not None, "Recommendation package should not be None"
    assert "S" in rec_package, "Recommendation package should contain similarity matrix S"
    assert "student_to_idx" in rec_package, "Recommendation package should contain student_to_idx mapping"
    
    rec_R = ModelLoader.get_recommendation_matrix_R()
    assert rec_R is not None, "Reconstructed matrix R should not be None"
    assert isinstance(rec_R, csr_matrix), "Matrix R should be a scipy csr_matrix"

    print("All ModelLoader assertions passed successfully!")

if __name__ == "__main__":
    test_model_loader()
