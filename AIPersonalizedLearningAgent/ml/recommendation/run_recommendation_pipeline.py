import sys
import os
import json
import pickle
import time
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path
import pandas as pd
import numpy as np

# Dynamically append workspace root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[3]))

def generate_notebook_structures(m5_dir):
    notebooks_dir = m5_dir / "notebooks"
    notebooks_dir.mkdir(parents=True, exist_ok=True)
    
    # ----------------------------------------------------
    # 01_EDA.ipynb
    # ----------------------------------------------------
    eda_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 01. Exploratory Data Analysis — Learning Resource Recommendation\n",
                "\n",
                "This notebook explores the OULAD Virtual Learning Environment (VLE) interaction data to understand how students engage with various online course resources."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else cwd\n",
                "sys.path.append(str(workspace_dir))\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "data_dir = workspace_dir / \"data\"\n",
                "\n",
                "# Load raw vle descriptors\n",
                "vle_df = pd.read_csv(data_dir / \"vle.csv\")\n",
                "print(\"VLE Descriptors Shape:\", vle_df.shape)\n",
                "print(vle_df.head())\n",
                "\n",
                "# Load pre-aggregated student interactions to optimize memory\n",
                "agg_df = pd.read_csv(workspace_dir / \"Model5_Recommendation\" / \"data\" / \"vle_interactions_aggregated.csv\")\n",
                "print(\"Aggregated Interactions Shape:\", agg_df.shape)\n",
                "print(agg_df.head())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Click distributions and active students statistics"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "num_students = agg_df['id_student'].nunique()\n",
                "num_sites = agg_df['id_site'].nunique()\n",
                "\n",
                "print(f\"Unique active students: {num_students}\")\n",
                "print(f\"Unique learning resources (sites): {num_sites}\")\n",
                "\n",
                "# Clicks per student distribution\n",
                "student_clicks = agg_df.groupby('id_student')['sum_click'].sum()\n",
                "print(\"\\nClicks per student statistics:\")\n",
                "print(student_clicks.describe())"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Popularity of activity types"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "activity_clicks = agg_df.groupby('activity_type')['sum_click'].sum().sort_values(ascending=False)\n",
                "activity_counts = agg_df.groupby('activity_type')['id_student'].count().sort_values(ascending=False)\n",
                "\n",
                "plt.figure(figsize=(12, 5))\n",
                "sns.barplot(x=activity_clicks.values, y=activity_clicks.index, palette='viridis')\n",
                "plt.title('Total Clicks by Learning Activity Type')\n",
                "plt.xlabel('Total Clicks')\n",
                "plt.ylabel('Activity Type')\n",
                "plt.tight_layout()\n",
                "plt.savefig(workspace_dir / \"Model5_Recommendation\" / \"reports\" / \"activity_clicks.png\")\n",
                "plt.show()"
            ]
        }
    ]
    
    # ----------------------------------------------------
    # 02_Preprocessing.ipynb
    # ----------------------------------------------------
    prep_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 02. Data Preprocessing & Stratified Train/Test Split\n",
                "\n",
                "This notebook loads the aggregated interactions, applies log-scaling to click counts to reduce skewness, and runs a student-stratified train/test split (80/20) so that each student in the test set has an interaction history in the train set."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else cwd\n",
                "sys.path.append(str(workspace_dir))\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "\n",
                "from PersonalizedLearningAgent.ml.recommendation.preprocess import split_interactions\n",
                "\n",
                "m5_dir = workspace_dir / \"Model5_Recommendation\"\n",
                "\n",
                "# Load aggregated interactions\n",
                "agg_df = pd.read_csv(m5_dir / \"data\" / \"vle_interactions_aggregated.csv\")\n",
                "\n",
                "# Perform stratified split\n",
                "train_df, test_df = split_interactions(agg_df, test_ratio=0.2, seed=42)\n",
                "\n",
                "# Save splits to CSV\n",
                "train_df.to_csv(m5_dir / \"data\" / \"train_interactions.csv\", index=False)\n",
                "test_df.to_csv(m5_dir / \"data\" / \"test_interactions.csv\", index=False)\n",
                "\n",
                "print(\"Saved train and test interaction files successfully.\")"
            ]
        }
    ]
    
    # ----------------------------------------------------
    # 03_Recommendation.ipynb
    # ----------------------------------------------------
    rec_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 03. Model Training — Item-Based Collaborative Filtering\n",
                "\n",
                "This notebook builds the User-Item matrix and calculates the Item-Item cosine similarity matrix on OULAD interaction train data."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "import pickle\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else cwd\n",
                "sys.path.append(str(workspace_dir))\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "\n",
                "from PersonalizedLearningAgent.ml.recommendation.user_item_matrix import build_user_item_matrix\n",
                "from PersonalizedLearningAgent.ml.recommendation.collaborative_filtering import fit_similarity\n",
                "\n",
                "m5_dir = workspace_dir / \"Model5_Recommendation\"\n",
                "\n",
                "# Load train data\n",
                "train_df = pd.read_csv(m5_dir / \"data\" / \"train_interactions.csv\")\n",
                "\n",
                "# Build sparse matrix\n",
                "R, s_to_idx, site_to_idx, idx_to_s, idx_to_site = build_user_item_matrix(train_df)\n",
                "\n",
                "# Fit Similarity matrix\n",
                "S = fit_similarity(R)\n",
                "\n",
                "# Save model package\n",
                "model_package = {\n",
                "    \"S\": S,\n",
                "    \"student_to_idx\": s_to_idx,\n",
                "    \"site_to_idx\": site_to_idx,\n",
                "    \"idx_to_student\": idx_to_s,\n",
                "    \"idx_to_site\": idx_to_site\n",
                "}\n",
                "with open(m5_dir / \"models\" / \"recommendation_model.pkl\", \"wb\") as f:\n",
                "    pickle.dump(model_package, f)\n",
                "\n",
                "print(\"Model packages exported successfully to recommendation_model.pkl.\")"
            ]
        }
    ]
    
    # ----------------------------------------------------
    # 04_Evaluation.ipynb
    # ----------------------------------------------------
    eval_cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 04. Model Evaluation & Generation of Top-K Recommendations\n",
                "\n",
                "This notebook evaluates the collaborative filtering model on the unseen test interaction set using Precision@K, Recall@K, NDCG@K, and Hit Rate@K. It also saves sample recommendations for users."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "import pickle\n",
                "import json\n",
                "from pathlib import Path\n",
                "cwd = Path.cwd()\n",
                "workspace_dir = cwd.parents[1] if cwd.name == 'notebooks' else cwd\n",
                "sys.path.append(str(workspace_dir))\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "import seaborn as sns\n",
                "\n",
                "from PersonalizedLearningAgent.ml.recommendation.user_item_matrix import build_user_item_matrix\n",
                "from PersonalizedLearningAgent.ml.recommendation.evaluate import evaluate_recommender\n",
                "from PersonalizedLearningAgent.ml.recommendation.recommend import recommend_top_k\n",
                "\n",
                "m5_dir = workspace_dir / \"Model5_Recommendation\"\n",
                "\n",
                "# 1. Load splits and model package\n",
                "train_df = pd.read_csv(m5_dir / \"data\" / \"train_interactions.csv\")\n",
                "test_df = pd.read_csv(m5_dir / \"data\" / \"test_interactions.csv\")\n",
                "\n",
                "with open(m5_dir / \"models\" / \"recommendation_model.pkl\", \"rb\") as f:\n",
                "    model_package = pickle.load(f)\n",
                "\n",
                "S = model_package[\"S\"]\n",
                "s_to_idx = model_package[\"student_to_idx\"]\n",
                "site_to_idx = model_package[\"site_to_idx\"]\n",
                "idx_to_s = model_package[\"idx_to_student\"]\n",
                "idx_to_site = model_package[\"idx_to_site\"]\n",
                "\n",
                "# Rebuild train R consistently\n",
                "R_train, _, _, _, _ = build_user_item_matrix(train_df, idx_to_s, idx_to_site)\n",
                "\n",
                "# 2. Run test evaluation\n",
                "summary = evaluate_recommender(R_train, test_df, S, s_to_idx, site_to_idx, idx_to_site, k_list=[5, 10])\n",
                "\n",
                "# Save metrics report to JSON\n",
                "with open(m5_dir / \"reports\" / \"metrics_report.json\", \"w\") as f:\n",
                "    json.dump(summary, f, indent=4)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Plot recommendation metrics"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "metrics_df = pd.DataFrame(summary).T.reset_index().rename(columns={'index': 'K'})\n",
                "melted = pd.melt(metrics_df, id_vars=['K'], var_name='Metric', value_name='Score')\n",
                "\n",
                "plt.figure(figsize=(10, 5))\n",
                "sns.barplot(data=melted, x='Metric', y='Score', hue='K', palette='coolwarm')\n",
                "plt.title('Recommendation Performance Metrics (K=5 vs K=10)')\n",
                "plt.ylim(0, 1.0)\n",
                "plt.ylabel('Metric Score')\n",
                "plt.grid(axis='y', linestyle='--', alpha=0.7)\n",
                "plt.tight_layout()\n",
                "plt.savefig(m5_dir / \"reports\" / \"metrics_chart.png\")\n",
                "plt.show()"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "### Generate and save sample recommendations CSV"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Generate recommendations for the first 100 test students and export\n",
                "sample_test_students = list(test_df['id_student'].unique())[:100]\n",
                "rec_rows = []\n",
                "\n",
                "for sid in sample_test_students:\n",
                "    recs = recommend_top_k(sid, R_train, S, s_to_idx, site_to_idx, idx_to_site, k=5)\n",
                "    for r in recs:\n",
                "        rec_rows.append({\n",
                "            \"id_student\": sid,\n",
                "            \"rank\": r[\"rank\"],\n",
                "            \"id_site\": r[\"id_site\"],\n",
                "            \"score\": r[\"score\"],\n",
                "            \"type\": r[\"type\"]\n",
                "        })\n",
                "        \n",
                "rec_df = pd.DataFrame(rec_rows)\n",
                "rec_df.to_csv(m5_dir / \"outputs\" / \"recommendations.csv\", index=False)\n",
                "print(\"Sample recommendations saved to: outputs/recommendations.csv\")\n",
                "print(rec_df.head(10))"
            ]
        }
    ]
    
    # Write notebooks as JSON structures
    for nb_name, cells in [("01_EDA.ipynb", eda_cells), 
                           ("02_Preprocessing.ipynb", prep_cells), 
                           ("03_Recommendation.ipynb", rec_cells), 
                           ("04_Evaluation.ipynb", eval_cells)]:
        nb = nbformat.v4.new_notebook()
        for cell in cells:
            if cell["cell_type"] == "markdown":
                nb.cells.append(nbformat.v4.new_markdown_cell(source="".join(cell["source"])))
            elif cell["cell_type"] == "code":
                nb.cells.append(nbformat.v4.new_code_cell(source="".join(cell["source"])))
                
        nb_path = notebooks_dir / nb_name
        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"Created notebook template: {nb_name}")

def run_pipeline():
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    m5_dir = workspace_dir / "Model5_Recommendation"
    data_dir = workspace_dir / "data"
    
    m5_dir.mkdir(parents=True, exist_ok=True)
    (m5_dir / "data").mkdir(parents=True, exist_ok=True)
    (m5_dir / "models").mkdir(parents=True, exist_ok=True)
    (m5_dir / "reports").mkdir(parents=True, exist_ok=True)
    (m5_dir / "outputs").mkdir(parents=True, exist_ok=True)
    
    # Step 1: Pre-aggregate the massive raw OULAD click dataset to save memory and time
    print("==================================================")
    print("PRE-AGGREGATING studentVle.csv DESCRIPTORS...")
    print("==================================================")
    t0 = time.time()
    
    # Import locally from preprocess
    from PersonalizedLearningAgent.ml.recommendation.preprocess import load_and_preprocess_data
    grouped, site_info = load_and_preprocess_data(data_dir)
    grouped.to_csv(m5_dir / "data" / "vle_interactions_aggregated.csv", index=False)
    
    print(f"Aggregation completed in {time.time() - t0:.2f} seconds.")
    
    # Step 2: Generate notebook files
    generate_notebook_structures(m5_dir)
    
    # Step 3: Run Jupyter notebooks programmatically
    print("\n==================================================")
    print("EXECUTING NOTEBOOKS PROGRAMMATICALLY...")
    print("==================================================")
    notebooks = [
        "01_EDA.ipynb",
        "02_Preprocessing.ipynb",
        "03_Recommendation.ipynb",
        "04_Evaluation.ipynb"
    ]
    
    ep = ExecutePreprocessor(timeout=1800, kernel_name='python3')
    
    for nb_name in notebooks:
        nb_path = m5_dir / "notebooks" / nb_name
        print(f"Executing {nb_name}...")
        t_nb = time.time()
        try:
            with open(nb_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
            
            # Execute in workspace root context so imports can resolve
            ep.preprocess(nb, {'metadata': {'path': str(workspace_dir)}})
            
            with open(nb_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)
            print(f"Successfully finished executing {nb_name} in {time.time() - t_nb:.2f} seconds.")
        except Exception as e:
            print(f"ERROR executing {nb_name}: {e}")
            raise e

if __name__ == "__main__":
    run_pipeline()
