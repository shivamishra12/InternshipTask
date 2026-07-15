import os
from pathlib import Path
import nbformat as nbf

def create_notebooks():
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    risk_dir = workspace_dir / "Model2_RiskPrediction"
    notebooks_dir = risk_dir / "notebooks"
    notebooks_dir.mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # 1. CREATE 01_EDA.ipynb
    # =========================================================================
    print("Creating 01_EDA.ipynb...")
    nb1 = nbf.v4.new_notebook()
    
    nb1.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 2 — Student Risk Prediction\n"
            "## 01: Exploratory Data Analysis (EDA)\n\n"
            "This notebook performs Exploratory Data Analysis (EDA) on the merged student analytics dataset "
            "to understand the distribution of our binary target variable (`risk`) and its relationship "
            "with various student demographics, academic history, and engagement features."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from pathlib import Path\n\n"
            "# Set aesthetic style\n"
            "sns.set_theme(style='whitegrid')\n"
            "plt.rcParams['figure.figsize'] = (10, 6)\n"
            "plt.rcParams['font.size'] = 11"
        ),
        nbf.v4.new_code_cell(
            "# Setup directories\n"
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "data_dir = workspace_dir / 'data'\n"
            "reports_dir = workspace_dir / 'Model2_RiskPrediction' / 'reports'\n"
            "reports_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "print('Loading dataset...')\n"
            "df = pd.read_csv(data_dir / 'engineered_features.csv')\n"
            "print(f'Dataset Shape: {df.shape}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 1. Target Variable (Risk) Distribution\n"
            "We examine the imbalance in the target variable `risk`.\n"
            "- `risk = 1`: Student failed or withdrew (`final_result` in ['Fail', 'Withdrawn'])\n"
            "- `risk = 0`: Student passed or achieved distinction (`final_result` in ['Pass', 'Distinction'])"
        ),
        nbf.v4.new_code_cell(
            "# Calculate class counts and percentages\n"
            "risk_counts = df['risk'].value_counts()\n"
            "risk_pct = df['risk'].value_counts(normalize=True) * 100\n\n"
            "print('Target Distribution:')\n"
            "for val, count in risk_counts.items():\n"
            "    label = 'At Risk (Fail/Withdrawn)' if val == 1 else 'Safe (Pass/Distinction)'\n"
            "    print(f'  {label}: {count} ({risk_pct[val]:.2f}%)')\n\n"
            "# Plot target distribution\n"
            "plt.figure(figsize=(6, 5))\n"
            "sns.barplot(x=risk_counts.index, y=risk_counts.values, palette='coolwarm')\n"
            "plt.xticks([0, 1], ['Safe (0)', 'At Risk (1)'])\n"
            "plt.title('Distribution of Student Risk Status')\n"
            "plt.xlabel('Class')\n"
            "plt.ylabel('Count')\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'eda_target_distribution.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "### 2. Numerical Features Analysis\n"
            "We look at the distribution of various numerical features across 'Safe' and 'At Risk' students:\n"
            "- `studied_credits`\n"
            "- `num_of_prev_attempts`\n"
            "- `total_clicks`\n"
            "- `avg_score`\n"
            "- `active_days`\n"
            "- `days_registered`\n"
            "- `late_submission_count`"
        ),
        nbf.v4.new_code_cell(
            "num_features = [\n"
            "    'studied_credits', 'num_of_prev_attempts', 'total_clicks',\n"
            "    'avg_score', 'active_days', 'days_registered', 'late_submission_count'\n"
            "]\n\n"
            "print('Numerical Features Summary Statistics:')\n"
            "display(df[num_features].describe())"
        ),
        nbf.v4.new_code_cell(
            "# Plot boxplots of numerical features vs risk\n"
            "fig, axes = plt.subplots(4, 2, figsize=(14, 18))\n"
            "axes = axes.flatten()\n\n"
            "for i, col in enumerate(num_features):\n"
            "    # Log transform heavily skewed features for better visualization\n"
            "    if col in ['total_clicks', 'studied_credits']:\n"
            "        sns.boxplot(data=df, x='risk', y=np.log1p(df[col]), ax=axes[i], palette='coolwarm')\n"
            "        axes[i].set_ylabel(f'Log({col} + 1)')\n"
            "    else:\n"
            "        sns.boxplot(data=df, x='risk', y=df[col], ax=axes[i], palette='coolwarm')\n"
            "        axes[i].set_ylabel(col)\n"
            "        \n"
            "    axes[i].set_title(f'{col} by Risk Status')\n"
            "    axes[i].set_xticklabels(['Safe (0)', 'At Risk (1)'])\n"
            "    axes[i].set_xlabel('Risk')\n\n"
            "# Hide the last unused axis if we have odd number of subplots\n"
            "if len(num_features) < len(axes):\n"
            "    axes[-1].axis('off')\n"
            "    \n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'eda_numerical_vs_risk.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "### 3. Categorical Features Analysis\n"
            "We analyze demographic categorical features vs the target risk rate:\n"
            "- `gender`\n"
            "- `region`\n"
            "- `highest_education`\n"
            "- `imd_band`\n"
            "- `age_band`\n"
            "- `disability`"
        ),
        nbf.v4.new_code_cell(
            "cat_features = ['gender', 'region', 'highest_education', 'imd_band', 'age_band', 'disability']\n\n"
            "for col in cat_features:\n"
            "    risk_table = df.groupby(col)['risk'].agg(['count', 'mean']).sort_values(by='mean', ascending=False)\n"
            "    risk_table['mean'] = risk_table['mean'] * 100\n"
            "    risk_table.rename(columns={'mean': 'Risk Rate (%)', 'count': 'Student Count'}, inplace=True)\n"
            "    print(f'\\n--- Risk Rate by {col} ---')\n"
            "    print(risk_table.to_string())"
        ),
        nbf.v4.new_code_cell(
            "# Visualizing categorical relationships with risk rate\n"
            "fig, axes = plt.subplots(3, 2, figsize=(14, 16))\n"
            "axes = axes.flatten()\n\n"
            "for i, col in enumerate(cat_features):\n"
            "    # Calculate mean risk rate per category\n"
            "    group_df = df.groupby(col)['risk'].mean().reset_index().sort_values(by='risk', ascending=False)\n"
            "    group_df['risk'] = group_df['risk'] * 100\n"
            "    \n"
            "    sns.barplot(data=group_df, y=col, x='risk', ax=axes[i], palette='viridis')\n"
            "    axes[i].set_title(f'Risk Rate (%) by {col}')\n"
            "    axes[i].set_xlabel('Risk Rate (%)')\n"
            "    axes[i].set_ylabel('')\n"
            "    \n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'eda_categorical_vs_risk.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "### 4. Correlation Analysis\n"
            "We analyze the correlation among numerical features."
        ),
        nbf.v4.new_code_cell(
            "corr_matrix = df[num_features].corr(method='spearman')\n"
            "plt.figure(figsize=(8, 7))\n"
            "sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1, square=True)\n"
            "plt.title('Spearman Correlation Matrix of Numerical Features')\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'eda_correlation_matrix.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "### 5. Missing Values Analysis\n"
            "We analyze and visualize missing values in our features."
        ),
        nbf.v4.new_code_cell(
            "# Missing percentages\n"
            "missing_pct = df.isnull().mean() * 100\n"
            "missing_cols = missing_pct[missing_pct > 0].sort_values(ascending=False)\n"
            "print('Columns with missing values (percentage):')\n"
            "print(missing_cols)\n\n"
            "# Missing value heatmap\n"
            "plt.figure(figsize=(10, 6))\n"
            "sns.heatmap(df[num_features].isnull(), cbar=False, yticklabels=False, cmap='viridis')\n"
            "plt.title('Missing Value Locations (Yellow indicates missing)')\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'eda_missing_values_heatmap.png', dpi=300)\n"
            "plt.show()"
        )
    ]
    
    with open(notebooks_dir / "01_EDA.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb1, f)
    print("01_EDA.ipynb created successfully.")
    
    # =========================================================================
    # 2. CREATE 02_Training.ipynb
    # =========================================================================
    print("Creating 02_Training.ipynb...")
    nb2 = nbf.v4.new_notebook()
    
    nb2.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 2 — Student Risk Prediction\n"
            "## 02: Model Training and Evaluation\n\n"
            "This notebook trains multiple machine learning classifiers, compares their performance, "
            "tunes the hyperparameters of the best performing model, and saves the final deliverables. "
            "The primary focus is optimizing **Recall for the 'At Risk' class** to ensure we catch "
            "as many students needing intervention as possible."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import json\n"
            "import pickle\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "import seaborn as sns\n"
            "from pathlib import Path\n\n"
            "from sklearn.model_selection import train_test_split, RandomizedSearchCV\n"
            "from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder\n"
            "from sklearn.impute import SimpleImputer\n"
            "from sklearn.compose import ColumnTransformer\n"
            "from sklearn.pipeline import Pipeline\n"
            "from sklearn.metrics import (\n"
            "    accuracy_score, precision_score, recall_score, f1_score,\n"
            "    roc_auc_score, average_precision_score, classification_report,\n"
            "    confusion_matrix, roc_curve, precision_recall_curve\n"
            ")\n\n"
            "# Models to compare\n"
            "from sklearn.linear_model import LogisticRegression\n"
            "from sklearn.tree import DecisionTreeClassifier\n"
            "from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier\n"
            "from xgboost import XGBClassifier\n"
            "from lightgbm import LGBMClassifier\n"
            "from catboost import CatBoostClassifier\n\n"
            "sns.set_theme(style='whitegrid')"
        ),
        nbf.v4.new_code_cell(
            "# Setup directories\n"
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "data_dir = workspace_dir / 'data'\n"
            "models_dir = workspace_dir / 'Model2_RiskPrediction' / 'models'\n"
            "reports_dir = workspace_dir / 'Model2_RiskPrediction' / 'reports'\n"
            "models_dir.mkdir(parents=True, exist_ok=True)\n"
            "reports_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "print('Loading dataset...')\n"
            "df = pd.read_csv(data_dir / 'engineered_features.csv')\n"
            "print(f'Dataset Shape: {df.shape}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 1. Feature Selection and Preprocessing\n"
            "We extract the target `risk` and define the feature subsets. "
            "We split categorical and numerical features for proper preprocessing in `ColumnTransformer`."
        ),
        nbf.v4.new_code_cell(
            "# Define target\n"
            "y = df['risk']\n\n"
            "# Exclude non-predictive and target-leaking columns\n"
            "exclude_cols = ['id_student', 'final_result', 'success', 'risk', 'date_registration', 'mean_score', 'avg_submission_delay']\n"
            "feature_cols = [col for col in df.columns if col not in exclude_cols]\n"
            "X = df[feature_cols]\n\n"
            "print(f'Total features for modeling: {len(feature_cols)}')\n\n"
            "categorical_cols = ['code_module', 'code_presentation', 'gender', 'region', \n"
            "                    'highest_education', 'imd_band', 'age_band', 'disability']\n"
            "numeric_cols = [col for col in feature_cols if col not in categorical_cols]\n\n"
            "print(f'Numerical features count: {len(numeric_cols)}')\n"
            "print(f'Categorical features count: {len(categorical_cols)}')"
        ),
        nbf.v4.new_code_cell(
            "# Split data into Train and Test sets (80% Train, 20% Test, stratified on target)\n"
            "X_train, X_test, y_train, y_test = train_test_split(\n"
            "    X, y, test_size=0.2, stratify=y, random_state=42\n"
            ")\n"
            "print(f'Train set: {X_train.shape[0]} samples')\n"
            "print(f'Test set: {X_test.shape[0]} samples')"
        ),
        nbf.v4.new_code_cell(
            "# Define preprocessing pipelines\n"
            "numeric_transformer = Pipeline(steps=[\n"
            "    ('imputer', SimpleImputer(strategy='median')),\n"
            "    ('scaler', StandardScaler())\n"
            "])\n\n"
            "categorical_transformer = Pipeline(steps=[\n"
            "    ('imputer', SimpleImputer(strategy='most_frequent')),\n"
            "    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))\n"
            "])\n\n"
            "preprocessor = ColumnTransformer(\n"
            "    transformers=[\n"
            "        ('num', numeric_transformer, numeric_cols),\n"
            "        ('cat', categorical_transformer, categorical_cols)\n"
            "    ]\n"
            ")"
        ),
        nbf.v4.new_markdown_cell(
            "### 2. Model Comparison\n"
            "We train and compare 8 classification models on the training dataset."
        ),
        nbf.v4.new_code_cell(
            "models = {\n"
            "    'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),\n"
            "    'Decision Tree': DecisionTreeClassifier(random_state=42),\n"
            "    'Random Forest': RandomForestClassifier(random_state=42, n_jobs=-1),\n"
            "    'Extra Trees': ExtraTreesClassifier(random_state=42, n_jobs=-1),\n"
            "    'Gradient Boosting': GradientBoostingClassifier(random_state=42),\n"
            "    'XGBoost': XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=-1),\n"
            "    'LightGBM': LGBMClassifier(random_state=42, verbose=-1, n_jobs=-1),\n"
            "    'CatBoost': CatBoostClassifier(random_state=42, verbose=0)\n"
            "}\n\n"
            "comparison_results = []\n\n"
            "for name, model in models.items():\n"
            "    print(f'Training {name}...')\n"
            "    pipeline = Pipeline(steps=[\n"
            "        ('preprocessor', preprocessor),\n"
            "        ('model', model)\n"
            "    ])\n"
            "    \n"
            "    pipeline.fit(X_train, y_train)\n"
            "    y_pred = pipeline.predict(X_test)\n"
            "    y_prob = pipeline.predict_proba(X_test)[:, 1]\n"
            "    \n"
            "    acc = accuracy_score(y_test, y_pred)\n"
            "    prec = precision_score(y_test, y_pred)\n"
            "    rec = recall_score(y_test, y_pred) # Recall for class 1\n"
            "    f1 = f1_score(y_test, y_pred)\n"
            "    roc_auc = roc_auc_score(y_test, y_prob)\n"
            "    \n"
            "    comparison_results.append({\n"
            "        'Model': name,\n"
            "        'Accuracy': acc,\n"
            "        'Precision': prec,\n"
            "        'Recall (At Risk)': rec,\n"
            "        'F1-Score': f1,\n"
            "        'ROC-AUC': roc_auc\n"
            "    })\n\n"
            "comparison_df = pd.DataFrame(comparison_results).sort_values(by='Recall (At Risk)', ascending=False)\n"
            "display(comparison_df)"
        ),
        nbf.v4.new_code_cell(
            "# Save comparison results\n"
            "comparison_df.to_csv(reports_dir / 'model_comparison_results.csv', index=False)"
        ),
        nbf.v4.new_markdown_cell(
            "### 3. Hyperparameter Tuning\n"
            "We tune the best model based on Recall for the 'At Risk' class. "
            "LightGBM or XGBoost or CatBoost typically perform best. "
            "We will pick the top-performing model dynamically."
        ),
        nbf.v4.new_code_cell(
            "best_model_name = comparison_df.iloc[0]['Model']\n"
            "print(f'Best model identified for tuning: {best_model_name}')\n\n"
            "# Define hyperparameter spaces for search\n"
            "if best_model_name == 'LightGBM':\n"
            "    base_model = LGBMClassifier(random_state=42, verbose=-1, n_jobs=-1)\n"
            "    param_grid = {\n"
            "        'model__n_estimators': [100, 200, 300],\n"
            "        'model__learning_rate': [0.01, 0.05, 0.1, 0.2],\n"
            "        'model__num_leaves': [15, 31, 63],\n"
            "        'model__subsample': [0.8, 0.9, 1.0],\n"
            "        'model__colsample_bytree': [0.8, 0.9, 1.0]\n"
            "    }\n"
            "elif best_model_name == 'XGBoost':\n"
            "    base_model = XGBClassifier(random_state=42, eval_metric='logloss', n_jobs=-1)\n"
            "    param_grid = {\n"
            "        'model__n_estimators': [100, 200, 300],\n"
            "        'model__learning_rate': [0.01, 0.05, 0.1, 0.2],\n"
            "        'model__max_depth': [3, 5, 7],\n"
            "        'model__subsample': [0.8, 0.9, 1.0],\n"
            "        'model__colsample_bytree': [0.8, 0.9, 1.0]\n"
            "    }\n"
            "elif best_model_name == 'CatBoost':\n"
            "    base_model = CatBoostClassifier(random_state=42, verbose=0)\n"
            "    param_grid = {\n"
            "        'model__iterations': [100, 200, 300],\n"
            "        'model__learning_rate': [0.01, 0.05, 0.1, 0.2],\n"
            "        'model__depth': [4, 6, 8]\n"
            "    }\n"
            "else:\n"
            "    base_model = RandomForestClassifier(random_state=42, n_jobs=-1)\n"
            "    param_grid = {\n"
            "        'model__n_estimators': [100, 200, 300],\n"
            "        'model__max_depth': [10, 20, None],\n"
            "        'model__min_samples_split': [2, 5, 10]\n"
            "    }\n\n"
            "tune_pipeline = Pipeline(steps=[\n"
            "    ('preprocessor', preprocessor),\n"
            "    ('model', base_model)\n"
            "])\n\n"
            "# Run RandomizedSearchCV focusing on RECALL metric\n"
            "print('Running RandomizedSearchCV...')\n"
            "search = RandomizedSearchCV(\n"
            "    tune_pipeline,\n"
            "    param_distributions=param_grid,\n"
            "    n_iter=10,\n"
            "    scoring='recall',\n"
            "    cv=3,\n"
            "    random_state=42,\n"
            "    n_jobs=-1\n"
            ")\n"
            "search.fit(X_train, y_train)\n"
            "best_clf = search.best_estimator_\n"
            "print(f'Best parameters: {search.best_params_}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 4. Final Evaluation\n"
            "We evaluate the final tuned model on the unseen test set."
        ),
        nbf.v4.new_code_cell(
            "y_pred = best_clf.predict(X_test)\n"
            "y_prob = best_clf.predict_proba(X_test)[:, 1]\n\n"
            "print('--- Classification Report ---')\n"
            "print(classification_report(y_test, y_pred))\n\n"
            "acc = accuracy_score(y_test, y_pred)\n"
            "prec = precision_score(y_test, y_pred)\n"
            "rec = recall_score(y_test, y_pred)\n"
            "f1 = f1_score(y_test, y_pred)\n"
            "roc_auc = roc_auc_score(y_test, y_prob)\n"
            "pr_auc = average_precision_score(y_test, y_prob)"
        ),
        nbf.v4.new_code_cell(
            "# Save Confusion Matrix\n"
            "cm = confusion_matrix(y_test, y_pred)\n"
            "plt.figure(figsize=(6, 5))\n"
            "sns.heatmap(cm, annot=True, fmt='d', cmap='Oranges', cbar=False,\n"
            "            xticklabels=['Safe', 'At Risk'], yticklabels=['Safe', 'At Risk'])\n"
            "plt.title('Confusion Matrix (Tuned Model)')\n"
            "plt.ylabel('Actual')\n"
            "plt.xlabel('Predicted')\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'confusion_matrix.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_code_cell(
            "# Save ROC Curve\n"
            "fpr, tpr, _ = roc_curve(y_test, y_prob)\n"
            "plt.figure(figsize=(6, 5))\n"
            "plt.plot(fpr, tpr, color='red', lw=2, label=f'ROC Curve (AUC = {roc_auc:.4f})')\n"
            "plt.plot([0, 1], [0, 1], color='navy', linestyle='--')\n"
            "plt.xlabel('False Positive Rate')\n"
            "plt.ylabel('True Positive Rate')\n"
            "plt.title('ROC Curve')\n"
            "plt.legend(loc='lower right')\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'roc_curve.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_code_cell(
            "# Save Precision-Recall Curve\n"
            "prec_vals, rec_vals, _ = precision_recall_curve(y_test, y_prob)\n"
            "plt.figure(figsize=(6, 5))\n"
            "plt.plot(rec_vals, prec_vals, color='purple', lw=2, label=f'PR Curve (AP = {pr_auc:.4f})')\n"
            "plt.xlabel('Recall')\n"
            "plt.ylabel('Precision')\n"
            "plt.title('Precision-Recall Curve')\n"
            "plt.legend(loc='lower left')\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'pr_curve.png', dpi=300)\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "### 5. Serialize Deliverables\n"
            "We save all required models and metadata."
        ),
        nbf.v4.new_code_cell(
            "# Extract fitted preprocessor and model\n"
            "fitted_preprocessor = best_clf.named_steps['preprocessor']\n"
            "model_only = best_clf.named_steps['model']\n\n"
            "# Save Preprocessor\n"
            "with open(models_dir / 'preprocessor.pkl', 'wb') as f:\n"
            "    pickle.dump(fitted_preprocessor, f)\n"
            "print('Saved preprocessor.pkl')\n\n"
            "# Save Risk Model (Full pipeline for easy predictions)\n"
            "with open(models_dir / 'risk_model.pkl', 'wb') as f:\n"
            "    pickle.dump(best_clf, f)\n"
            "print('Saved risk_model.pkl')\n\n"
            "# Extract and Save Feature Names\n"
            "feature_names = fitted_preprocessor.get_feature_names_out().tolist()\n"
            "with open(models_dir / 'feature_names.pkl', 'wb') as f:\n"
            "    pickle.dump(feature_names, f)\n"
            "print('Saved feature_names.pkl')\n\n"
            "# Save Label Encoder placeholder (since target is already binary, we store class mappings)\n"
            "label_mapping = {0: 'Safe (Pass/Distinction)', 1: 'At Risk (Fail/Withdrawn)'}\n"
            "with open(models_dir / 'label_encoder.pkl', 'wb') as f:\n"
            "    pickle.dump(label_mapping, f)\n"
            "print('Saved label_encoder.pkl')\n\n"
            "# Save Metrics JSON\n"
            "metrics = {\n"
            "    'accuracy': acc,\n"
            "    'precision': prec,\n"
            "    'recall': rec,\n"
            "    'f1_score': f1,\n"
            "    'roc_auc': roc_auc,\n"
            "    'pr_auc': pr_auc\n"
            "}\n"
            "with open(models_dir / 'metrics.json', 'w') as f:\n"
            "    json.dump(metrics, f, indent=4)\n"
            "print('Saved metrics.json')"
        )
    ]
    
    with open(notebooks_dir / "02_Training.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb2, f)
    print("02_Training.ipynb created successfully.")
    
    # =========================================================================
    # 3. CREATE 03_SHAP.ipynb
    # =========================================================================
    print("Creating 03_SHAP.ipynb...")
    nb3 = nbf.v4.new_notebook()
    
    nb3.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 2 — Student Risk Prediction\n"
            "## 03: Explainability via SHAP\n\n"
            "This notebook uses SHAP (SHapley Additive exPlanations) to interpret our student risk prediction model. "
            "We generate Summary, Bar, Waterfall, and Dependence plots to explain the feature importances "
            "and individual student predictions."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import pickle\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "import matplotlib.pyplot as plt\n"
            "from pathlib import Path\n"
            "import shap\n\n"
            "plt.rcParams['figure.figsize'] = (10, 6)"
        ),
        nbf.v4.new_code_cell(
            "# Setup directories\n"
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "data_dir = workspace_dir / 'data'\n"
            "models_dir = workspace_dir / 'Model2_RiskPrediction' / 'models'\n"
            "reports_dir = workspace_dir / 'Model2_RiskPrediction' / 'reports'\n\n"
            "print('Loading serialized risk model...')\n"
            "with open(models_dir / 'risk_model.pkl', 'rb') as f:\n"
            "    pipeline = pickle.load(f)\n\n"
            "print('Loading engineered features...')\n"
            "df = pd.read_csv(data_dir / 'engineered_features.csv')\n"
            "print(f'Dataset Shape: {df.shape}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 1. Preprocess Sample Data\n"
            "We take a representative sample of 2000 students to speed up SHAP calculations."
        ),
        nbf.v4.new_code_cell(
            "# Exclude non-predictive and target-leaking columns\n"
            "exclude_cols = ['id_student', 'final_result', 'success', 'risk', 'date_registration', 'mean_score', 'avg_submission_delay']\n"
            "feature_cols = [col for col in df.columns if col not in exclude_cols]\n\n"
            "# Sample 2000 students for SHAP calculation\n"
            "sample_df = df.sample(n=2000, random_state=42)\n"
            "X_sample = sample_df[feature_cols]\n\n"
            "# Extract preprocessor and model\n"
            "preprocessor = pipeline.named_steps['preprocessor']\n"
            "model = pipeline.named_steps['model']\n\n"
            "# Preprocess the sample\n"
            "X_preprocessed = preprocessor.transform(X_sample)\n"
            "raw_feature_names = preprocessor.get_feature_names_out()\n\n"
            "# Clean feature names (replace brackets and other special characters)\n"
            "clean_feature_names = []\n"
            "for name in raw_feature_names:\n"
            "    clean_name = name.replace('<', '_').replace('>', '_').replace('[', '_').replace(']', '_')\n"
            "    clean_feature_names.append(clean_name)\n"
            "    \n"
            "X_preprocessed_df = pd.DataFrame(X_preprocessed, columns=clean_feature_names)"
        ),
        nbf.v4.new_markdown_cell(
            "### 2. Calculate SHAP Values\n"
            "We initialize the SHAP explainer and compute SHAP values for the preprocessed sample."
        ),
        nbf.v4.new_code_cell(
            "print('Initializing SHAP explainer...')\n"
            "# Try TreeExplainer (works for XGBoost, LightGBM, CatBoost, RandomForest)\n"
            "try:\n"
            "    explainer = shap.TreeExplainer(model)\n"
            "    shap_values = explainer(X_preprocessed_df)\n"
            "    # For multi-class or some tree explainers, shap_values might have an extra dimension\n"
            "    if len(shap_values.shape) == 3 and shap_values.shape[2] == 2:\n"
            "        # Binary classification, select class 1 (At Risk)\n"
            "        # Convert the Explainer output object slice\n"
            "        shap_values = shap_values[:, :, 1]\n"
            "except Exception as e:\n"
            "    print(f'TreeExplainer failed or not applicable, falling back to Explainer: {e}')\n"
            "    explainer = shap.Explainer(model, X_preprocessed_df)\n"
            "    shap_values = explainer(X_preprocessed_df)\n\n"
            "print('SHAP values calculated successfully. Shape:', shap_values.shape)"
        ),
        nbf.v4.new_markdown_cell(
            "### 3. Generate Interpretability Plots"
        ),
        nbf.v4.new_markdown_cell(
            "#### A. Summary Plot (Beeswarm)"
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(10, 8))\n"
            "shap.summary_plot(shap_values, X_preprocessed_df, show=False)\n"
            "plt.title('SHAP Feature Importance Summary (Beeswarm)', fontsize=14, pad=15)\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'shap_summary.png', dpi=300, bbox_inches='tight')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "#### B. Bar Plot"
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(10, 6))\n"
            "shap.plots.bar(shap_values, show=False)\n"
            "plt.title('SHAP Global Feature Importance (Bar)', fontsize=14, pad=15)\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'shap_bar.png', dpi=300, bbox_inches='tight')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "#### C. Waterfall Plot (Individual student explanation)\n"
            "We explain why a specific student is predicted to be at risk (sample index 0)."
        ),
        nbf.v4.new_code_cell(
            "plt.figure(figsize=(10, 6))\n"
            "# Handle single sample extraction for waterfall\n"
            "shap.plots.waterfall(shap_values[0], show=False)\n"
            "plt.title('SHAP Waterfall Plot for Student Sample 1', fontsize=14, pad=15)\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'shap_waterfall.png', dpi=300, bbox_inches='tight')\n"
            "plt.show()"
        ),
        nbf.v4.new_markdown_cell(
            "#### D. Dependence Plot\n"
            "We plot the dependence of the target prediction on a key feature, for example `engagement_score` or its standardized representation."
        ),
        nbf.v4.new_code_cell(
            "# Identify key numerical feature name from preprocess columns\n"
            "score_col = [col for col in X_preprocessed_df.columns if 'engagement_score' in col][0]\n"
            "print(f'Plotting dependence plot for feature: {score_col}')\n\n"
            "plt.figure(figsize=(8, 6))\n"
            "shap.dependence_plot(score_col, shap_values.values, X_preprocessed_df, show=False)\n"
            "plt.title(f'SHAP Dependence Plot for {score_col}', fontsize=14, pad=15)\n"
            "plt.tight_layout()\n"
            "plt.savefig(reports_dir / 'shap_dependence.png', dpi=300, bbox_inches='tight')\n"
            "plt.show()"
        )
    ]
    
    with open(notebooks_dir / "03_SHAP.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb3, f)
    print("03_SHAP.ipynb created successfully.")

if __name__ == "__main__":
    create_notebooks()
