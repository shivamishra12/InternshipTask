import sys
from pathlib import Path
import pandas as pd

workspace_dir = Path(__file__).resolve().parents[1]
sys.path.append(str(workspace_dir))

from app.services.features_loader import FeaturesLoader
from app.services.model_loader import ModelLoader

ModelLoader.load_all_models(workspace_dir)

student_features = FeaturesLoader.get_student_features(11391)
print(f"Number of features loaded: {len(student_features)}")
print(f"Is early_clicks in dict? {'early_clicks' in student_features}")

features_clean_perf = {
    k: v for k, v in student_features.items() 
    if k not in ["id_student", "final_result", "success"]
}
X_perf = pd.DataFrame([features_clean_perf])

try:
    model = ModelLoader.get_performance_model()
    pred = model.predict(X_perf)
    print(f"Performance predict success: {pred}")
except Exception as e:
    print(f"Performance error: {e}")

features_clean_risk = {
    k: v for k, v in student_features.items() 
    if k not in ["id_student", "final_result", "success", "risk"]
}
X_risk = pd.DataFrame([features_clean_risk])

try:
    risk_preprocessor = ModelLoader.get_risk_preprocessor()
    risk_model = ModelLoader.get_risk_model()
    X_trans = risk_preprocessor.transform(X_risk)
    pred_risk = risk_model.predict_proba(X_trans)
    print(f"Risk predict success: {pred_risk}")
except Exception as e:
    print(f"Risk error: {e}")
