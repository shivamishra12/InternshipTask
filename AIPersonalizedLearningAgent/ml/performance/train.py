import os
import pandas as pd
import numpy as np
from pathlib import Path
import pickle

from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay, roc_curve, precision_recall_curve
)

# Classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

import matplotlib.pyplot as plt
import seaborn as sns

def train_and_evaluate_model(processed_dir=None, models_dir=None, reports_dir=None):
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    if processed_dir is None:
        processed_dir = workspace_dir / "data"
    if models_dir is None:
        models_dir = workspace_dir
    if reports_dir is None:
        reports_dir = workspace_dir / "PersonalizedLearningAgent" / "reports"
        
    processed_dir = Path(processed_dir)
    models_dir = Path(models_dir)
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    models_dir.mkdir(parents=True, exist_ok=True)

    print("Loading engineered features...")
    df = pd.read_csv(processed_dir / "engineered_features.csv")

    # Define target and features
    y = df['success']
    
    # Exclude non-predictive and target-leaking columns
    exclude_cols = ['id_student', 'final_result', 'success']
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    X = df[feature_cols]

    print(f"Total features: {len(feature_cols)}")
    
    # Categorical and numerical column split
    categorical_cols = ['code_module', 'code_presentation', 'gender', 'region', 
                        'highest_education', 'imd_band', 'age_band', 'disability']
    
    numeric_cols = [col for col in feature_cols if col not in categorical_cols]
    
    print(f"Numerical features ({len(numeric_cols)}): {numeric_cols[:5]}...")
    print(f"Categorical features ({len(categorical_cols)}): {categorical_cols}")

    # Train/Test Split (Stratified, 80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")

    # Preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_cols),
            ('cat', categorical_transformer, categorical_cols)
        ]
    )

    # ------------------ Model Comparison ------------------
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42, n_jobs=-1),
        'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=-1),
        'LightGBM': LGBMClassifier(random_state=42, verbose=-1, n_jobs=-1)
    }

    results = []

    print("\nComparing models...")
    for model_name, model in models.items():
        print(f"Training {model_name}...")
        clf = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('model', model)
        ])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        y_prob = clf.predict_proba(X_test)[:, 1] if hasattr(clf, "predict_proba") else y_pred
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        
        print(f"  Accuracy: {acc:.4f} | F1-Score: {f1:.4f} | ROC-AUC: {roc_auc:.4f}")
        
        results.append({
            'Model': model_name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1,
            'ROC-AUC': roc_auc,
            'PR-AUC': pr_auc
        })

    results_df = pd.DataFrame(results)
    print("\n--- Model Comparison Results ---")
    print(results_df.to_string(index=False))
    results_df.to_csv(reports_dir / "model_comparison_results.csv", index=False)

    # Identify the best model based on F1-Score
    best_model_name = results_df.loc[results_df['F1-Score'].idxmax()]['Model']
    print(f"\nBest Model identified by F1-Score: {best_model_name}")

    # ------------------ Hyperparameter Tuning ------------------
    print(f"\nTuning hyperparameters for {best_model_name}...")
    
    # We will define tuning space for XGBoost / LightGBM / RF
    if best_model_name == 'LightGBM':
        base_model = LGBMClassifier(random_state=42, verbose=-1, n_jobs=-1)
        param_grid = {
            'model__n_estimators': [50, 100, 200, 300],
            'model__learning_rate': [0.01, 0.05, 0.1, 0.2],
            'model__num_leaves': [15, 31, 63, 127],
            'model__subsample': [0.7, 0.8, 0.9, 1.0],
            'model__colsample_bytree': [0.7, 0.8, 0.9, 1.0]
        }
    elif best_model_name == 'XGBoost':
        base_model = XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=-1)
        param_grid = {
            'model__n_estimators': [50, 100, 200, 300],
            'model__learning_rate': [0.01, 0.05, 0.1, 0.2],
            'model__max_depth': [3, 5, 7, 9],
            'model__subsample': [0.7, 0.8, 0.9, 1.0],
            'model__colsample_bytree': [0.7, 0.8, 0.9, 1.0]
        }
    else:  # Random Forest
        base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        param_grid = {
            'model__n_estimators': [50, 100, 200, 300],
            'model__max_depth': [10, 20, 30, None],
            'model__min_samples_split': [2, 5, 10],
            'model__min_samples_leaf': [1, 2, 4]
        }

    tune_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', base_model)
    ])

    # Randomized Search with 3-fold cross validation
    search = RandomizedSearchCV(
        tune_pipeline,
        param_distributions=param_grid,
        n_iter=10,
        scoring='f1',
        cv=3,
        random_state=42,
        n_jobs=-1
    )
    
    search.fit(X_train, y_train)
    best_clf = search.best_estimator_
    print(f"Best parameters found: {search.best_params_}")

    # ------------------ Final Evaluation ------------------
    print("\nEvaluating the best tuned model on the test set...")
    y_pred = best_clf.predict(X_test)
    y_prob = best_clf.predict_proba(X_test)[:, 1]

    # Metrics
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred))
    
    # Save Confusion Matrix Plot
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False,
                xticklabels=['Unsuccessful', 'Successful'],
                yticklabels=['Unsuccessful', 'Successful'])
    plt.title('Confusion Matrix (Tuned Model)')
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.tight_layout()
    plt.savefig(reports_dir / "performance_confusion_matrix.png", dpi=300)
    plt.close()

    # Save ROC Curve Plot
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = roc_auc_score(y_test, y_prob)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(reports_dir / "performance_roc_curve.png", dpi=300)
    plt.close()

    # Save PR Curve Plot
    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)
    plt.figure()
    plt.plot(recall_vals, precision_vals, color='green', lw=2, label=f'PR curve (AP = {pr_auc:.4f})')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.tight_layout()
    plt.savefig(reports_dir / "performance_pr_curve.png", dpi=300)
    plt.close()

    # ------------------ Serialize Deliverables ------------------
    print("\nSerializing artifacts...")
    
    # Fit the standalone preprocessor on training data to save it separately as requested
    fitted_preprocessor = best_clf.named_steps['preprocessor']
    
    # Save preprocessor
    with open(models_dir / "performance_preprocessor.pkl", "wb") as f:
        pickle.dump(fitted_preprocessor, f)
    print(f"Saved performance_preprocessor.pkl to: {models_dir / 'performance_preprocessor.pkl'}")
    
    # Save the performance model (full pipeline for ease of deployment, or model only)
    with open(models_dir / "performance_model.pkl", "wb") as f:
        pickle.dump(best_clf, f)
    print(f"Saved performance_model.pkl to: {models_dir / 'performance_model.pkl'}")

    # Extract and save feature names
    feature_names = fitted_preprocessor.get_feature_names_out().tolist()
    with open(models_dir / "performance_feature_names.pkl", "wb") as f:
        pickle.dump(feature_names, f)
    print(f"Saved performance_feature_names.pkl to: {models_dir / 'performance_feature_names.pkl'}")
    print(f"Total features after preprocessing: {len(feature_names)}")

    test_metrics = {
        "Accuracy": float(accuracy_score(y_test, y_pred)),
        "Precision": float(precision_score(y_test, y_pred)),
        "Recall": float(recall_score(y_test, y_pred)),
        "F1 Score": float(f1_score(y_test, y_pred)),
        "ROC AUC": float(roc_auc_score(y_test, y_prob))
    }
    return test_metrics

if __name__ == "__main__":
    train_and_evaluate_model()
