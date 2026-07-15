import os
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from pathlib import Path
import shap

def run_shap_analysis():
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    data_dir = workspace_dir / "data"
    artifacts_dir = workspace_dir / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    print("Loading serialized performance model...")
    with open(workspace_dir / "performance_model.pkl", "rb") as f:
        pipeline = pickle.load(f)

    print("Loading engineered features...")
    df = pd.read_csv(data_dir / "engineered_features.csv")

    # Exclude non-predictive and target-leaking columns
    exclude_cols = ['id_student', 'final_result', 'success']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    # Take a representative sample of 2000 students for SHAP calculation to keep it fast
    sample_df = df.sample(n=2000, random_state=42)
    X_sample = sample_df[feature_cols]

    print("Extracting preprocessing pipeline and model...")
    preprocessor = pipeline.named_steps['preprocessor']
    model = pipeline.named_steps['model']

    print("Preprocessing the sample data...")
    X_preprocessed = preprocessor.transform(X_sample)
    raw_feature_names = preprocessor.get_feature_names_out()
    
    # Sanitize feature names to meet XGBoost's requirements: no [, ], or <
    clean_feature_names = []
    for name in raw_feature_names:
        clean_name = name.replace("<", "_").replace(">", "_").replace("[", "_").replace("]", "_")
        clean_feature_names.append(clean_name)
    
    # Convert preprocessed numpy array back to DataFrame for SHAP labels
    X_preprocessed_df = pd.DataFrame(X_preprocessed, columns=clean_feature_names)

    print("Initializing SHAP TreeExplainer...")
    # Initialize explainer on the underlying XGBoost model
    explainer = shap.TreeExplainer(model)
    
    print("Calculating SHAP values...")
    # Compute shap values
    shap_values = explainer(X_preprocessed_df)

    print("Generating SHAP summary plot...")
    plt.figure(figsize=(10, 8))
    # SHAP summary plot
    shap.summary_plot(shap_values, X_preprocessed_df, show=False)
    plt.title('SHAP Feature Importance Summary', fontsize=14, pad=15)
    plt.tight_layout()
    
    output_path = artifacts_dir / "shap_summary.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"SHAP summary plot saved to: {output_path}")

    # Print top 10 most influential features based on mean absolute SHAP value
    print("\nTop 10 Most Influential Features (mean |SHAP|):")
    # Take mean of absolute SHAP values across rows for each feature
    mean_abs_shap = np.mean(np.abs(shap_values.values), axis=0)
    shap_importance = pd.DataFrame({
        'Feature': clean_feature_names,
        'Mean_Abs_SHAP': mean_abs_shap
    }).sort_values(by='Mean_Abs_SHAP', ascending=False)
    
    print(shap_importance.head(10).to_string(index=False))
    shap_importance.to_csv(artifacts_dir / "shap_feature_importance.csv", index=False)

if __name__ == "__main__":
    run_shap_analysis()
