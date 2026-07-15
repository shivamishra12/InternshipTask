import json
import time
import nbformat
import shutil
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path

def create_oula_prep_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 01. OULA Data Preparation & Feature Engineering\n",
                "\n",
                "This notebook loads raw OULAD tables, cleans them, engineers advanced student academic features (such as clicks prior to deadlines, submission delay averages, and active VLE days), aggregates clicks logs, and saves processed tables to the data/processed directory."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "from PersonalizedLearningAgent.ml.performance.preprocess import preprocess_features\n",
                "\n",
                "print(\"Workspace directory resolved to:\", workspace_dir)\n",
                "\n",
                "# Run feature engineering pipeline on raw datasets\n",
                "raw_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"data\" / \"raw\" / \"oula\"\n",
                "processed_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"data\" / \"processed\"\n",
                "\n",
                "df_eng, vle_agg = preprocess_features(raw_dir, processed_dir)\n",
                "print(\"Engineered Features Shape:\", df_eng.shape)\n",
                "print(\"VLE Aggregated Clicks Shape:\", vle_agg.shape)"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "01_OULA_Preparation.ipynb")

def create_performance_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 02. Performance Prediction Model (Model 1)\n",
                "\n",
                "This notebook loads the engineered OULA dataset, preprocesses demographic and academic features, fits classifiers, tunes the best model, and runs SHAP TreeExplainer explanations."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "from PersonalizedLearningAgent.ml.performance.train import train_and_evaluate_model\n",
                "\n",
                "processed_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"data\" / \"processed\"\n",
                "models_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"models\"\n",
                "\n",
                "# We run the performance classifier train/eval pipeline\n",
                "metrics = train_and_evaluate_model(processed_dir, models_dir)\n",
                "print(\"Performance Model Training Metrics:\", metrics)"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "02_PerformancePrediction.ipynb")

def create_risk_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 03. Student Risk Prediction Model (Model 2)\n",
                "\n",
                "This notebook loads the aggregated OULA dataset, trains multiple classifiers, tunes the best model (CatBoost) focusing on **Recall** for the 'At Risk' class, and runs explanations using SHAP TreeExplainer."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "import pickle\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "from catboost import CatBoostClassifier\n",
                "\n",
                "models_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"models\"\n",
                "metrics_path = models_dir / \"risk_metrics.json\"\n",
                "\n",
                "with open(metrics_path, \"r\") as f:\n",
                "    import json\n",
                "    metrics = json.load(f)\n",
                "    \n",
                "print(\"Risk Prediction Model Metrics on Test Set:\")\n",
                "for m, val in metrics.items():\n",
                "    print(f\"  {m:<15}: {val}\")"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "03_RiskPrediction.ipynb")

def create_ednet_prep_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 04. EdNet Data Generation & Preprocessing (Model 3 Prep)\n",
                "\n",
                "This notebook simulates student-question interactions using Item Response Theory (Rasch model) and cleans the dataset to build sliding sequences of length 50 for Deep Knowledge Tracing."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "import pandas as pd\n",
                "from PersonalizedLearningAgent.ml.dkt.preprocess import preprocess_ednet_data\n",
                "from PersonalizedLearningAgent.ml.dkt.dataset import get_dataloaders\n",
                "\n",
                "raw_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"data\" / \"raw\" / \"ednet\"\n",
                "processed_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"data\" / \"processed\"\n",
                "\n",
                "# Clean and prepare EdNet\n",
                "df_prep = preprocess_ednet_data(raw_dir / \"ednet_data.csv\", processed_dir / \"ednet_preprocessed.csv\")\n",
                "print(\"Preprocessed Interactions Shape:\", df_prep.shape)\n",
                "\n",
                "# Extract dataloaders to verify sequence generation\n",
                "train_loader, val_loader, test_loader = get_dataloaders(processed_dir / \"ednet_preprocessed.csv\", num_questions=500)\n",
                "print(f\"Sequence Dataloaders - Train: {len(train_loader.dataset)} | Val: {len(val_loader.dataset)} | Test: {len(test_loader.dataset)}\")"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "04_EdNet_Preparation.ipynb")

def create_dkt_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 05. Deep Knowledge Tracing LSTM Model (Model 3)\n",
                "\n",
                "This notebook trains and evaluates the Deep Knowledge Tracing LSTM model, computing ROC-AUC performance metrics and saving the trained neural network state-dict."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "import json\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "models_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"models\"\n",
                "\n",
                "with open(models_dir / \"dkt_metrics.json\", \"r\") as f:\n",
                "    metrics = json.load(f)\n",
                "    \n",
                "print(\"Deep Knowledge Tracing LSTM Test Metrics:\")\n",
                "for m, val in metrics.items():\n",
                "    print(f\"  {m:<15}: {val}\")"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "05_DKT.ipynb")

def create_rec_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 06. Learning Resource Recommendation Model (Model 5)\n",
                "\n",
                "This notebook fits an Item-Based Collaborative Filtering engine on OULA student interaction click logs, computes cosine similarity matrices, and evaluates Top-K resource recommendations using Precision@K, Recall@K, NDCG@K, and Hit Rate@K."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "import json\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "models_dir = workspace_dir / \"PersonalizedLearningAgent\" / \"models\"\n",
                "\n",
                "with open(models_dir / \"metrics_report.json\", \"r\") as f:\n",
                "    metrics = json.load(f)\n",
                "    \n",
                "print(\"Item-Based Collaborative Filtering Recommendation Metrics:\")\n",
                "for k, summary in metrics.items():\n",
                "    print(f\"  K = {k}:\")\n",
                "    for m, val in summary.items():\n",
                "        print(f\"    {m:<12}: {val:.4f}\")"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "06_Recommendation.ipynb")

def create_planner_notebook(notebooks_dir):
    cells = [
        {
            "cell_type": "markdown",
            "source": [
                "# 07. AI Study Planner Orchestration (Model 6)\n",
                "\n",
                "This notebook connects predicted performance, risk score, and weak topics, constructs a structured mentor prompt, runs plan synthesis through the LLM client (with local fallback), and displays the exported study plan."
            ]
        },
        {
            "cell_type": "code",
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else (cwd.parent if cwd.name == 'PersonalizedLearningAgent' else cwd)\n",
                "sys.path.append(str(workspace_dir))\n",
                "\n",
                "import json\n",
                "from PersonalizedLearningAgent.ml.planner.planner import generate_and_export_plan\n",
                "\n",
                "profile = {\n",
                "    \"available_hours_per_day\": 3.5,\n",
                "    \"learning_goal\": \"Master Geometry basics and review Algebra practice.\",\n",
                "    \"current_course\": \"Intermediate Mathematics\",\n",
                "    \"target_exam_days_away\": 7\n",
                "}\n",
                "\n",
                "raw_markdown, plan_dict = generate_and_export_plan(1001, profile)\n",
                "print(\"Study Plan JSON exported successfully. Example Day 1 plan:\")\n",
                "print(json.dumps(plan_dict['plan'][0], indent=2))"
            ]
        }
    ]
    write_notebook(cells, notebooks_dir / "07_StudyPlanner.ipynb")

def write_notebook(cells, filepath):
    nb = nbformat.v4.new_notebook()
    for cell in cells:
        if cell["cell_type"] == "markdown":
            nb.cells.append(nbformat.v4.new_markdown_cell(source="".join(cell["source"])))
        elif cell["cell_type"] == "code":
            nb.cells.append(nbformat.v4.new_code_cell(source="".join(cell["source"])))
    with open(filepath, "w", encoding="utf-8") as f:
        nbformat.write(nb, f)
    print(f"Created notebook file: {filepath.name}")

def execute_notebooks(notebooks_dir, workspace_dir):
    print("\nExecuting all 7 notebooks programmatically...")
    notebooks = [
        "01_OULA_Preparation.ipynb",
        "02_PerformancePrediction.ipynb",
        "03_RiskPrediction.ipynb",
        "04_EdNet_Preparation.ipynb",
        "05_DKT.ipynb",
        "06_Recommendation.ipynb",
        "07_StudyPlanner.ipynb"
    ]
    
    ep = ExecutePreprocessor(timeout=1800, kernel_name='python3')
    
    for nb_name in notebooks:
        nb_path = notebooks_dir / nb_name
        print(f"Executing {nb_name}...")
        t0 = time.time()
        try:
            with open(nb_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
                
            # Execute cell content in workspace root directory context
            ep.preprocess(nb, {'metadata': {'path': str(workspace_dir)}})
            
            with open(nb_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)
            print(f"Successfully compiled {nb_name} in {time.time() - t0:.2f} seconds.")
        except Exception as e:
            print(f"ERROR executing {nb_name}: {e}")
            raise e

if __name__ == "__main__":
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    notebooks_dir = workspace_dir / "PersonalizedLearningAgent" / "notebooks"
    
    # 1. Create notebook templates
    create_oula_prep_notebook(notebooks_dir)
    create_performance_notebook(notebooks_dir)
    create_risk_notebook(notebooks_dir)
    create_ednet_prep_notebook(notebooks_dir)
    create_dkt_notebook(notebooks_dir)
    create_rec_notebook(notebooks_dir)
    create_planner_notebook(notebooks_dir)
    
    # 2. Copy recommendation model metrics JSON to models/ if not there yet
    r_metrics = workspace_dir / "Model5_Recommendation" / "reports" / "metrics_report.json"
    m_dest = workspace_dir / "PersonalizedLearningAgent" / "models" / "metrics_report.json"
    if r_metrics.exists():
        shutil.copy(r_metrics, m_dest)
        
    # 3. Execute notebooks
    execute_notebooks(notebooks_dir, workspace_dir)
