import os
from pathlib import Path
import nbformat as nbf

def create_notebooks():
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    kt_dir = workspace_dir / "Model3_KnowledgeTracing"
    notebooks_dir = kt_dir / "notebooks"
    notebooks_dir.mkdir(parents=True, exist_ok=True)
    
    # =========================================================================
    # 1. CREATE 01_Preprocessing.ipynb
    # =========================================================================
    print("Creating 01_Preprocessing.ipynb...")
    nb1 = nbf.v4.new_notebook()
    nb1.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 3 — Knowledge Tracing (EdNet)\n"
            "## 01: Preprocessing Pipeline\n\n"
            "This notebook cleans and prepares raw student interaction data from the EdNet dataset. "
            "It removes duplicates, missing values, sorts interactions chronologically per student, "
            "and label encodes question IDs so they can be fed into our embedding layers."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import pandas as pd\n"
            "import numpy as np\n"
            "from pathlib import Path\n"
            "import pickle\n"
            "from sklearn.preprocessing import LabelEncoder"
        ),
        nbf.v4.new_code_cell(
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "kt_dir = workspace_dir / 'Model3_KnowledgeTracing'\n"
            "data_path = kt_dir / 'data' / 'ednet_data.csv'\n"
            "models_dir = kt_dir / 'models'\n"
            "models_dir.mkdir(parents=True, exist_ok=True)\n\n"
            "print(f'Loading data from {data_path}...')\n"
            "df = pd.read_csv(data_path)\n"
            "print(f'Original dataset shape: {df.shape}')\n"
            "display(df.head())"
        ),
        nbf.v4.new_markdown_cell(
            "### 1. Cleaning Missing Values and Duplicates"
        ),
        nbf.v4.new_code_cell(
            "# Drop rows with missing essential fields\n"
            "df.dropna(subset=['user_id', 'question_id', 'correct', 'timestamp'], inplace=True)\n"
            "# Drop duplicates\n"
            "df.drop_duplicates(subset=['user_id', 'timestamp', 'question_id'], inplace=True)\n"
            "print(f'Dataset shape after cleaning: {df.shape}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 2. Chronological Sorting\n"
            "DKT is a sequence learning problem, so student responses must be sorted by user and timestamp."
        ),
        nbf.v4.new_code_cell(
            "df.sort_values(by=['user_id', 'timestamp'], ascending=[True, True], inplace=True)\n"
            "print('Dataset sorted chronologically.')\n"
            "display(df.head(10))"
        ),
        nbf.v4.new_markdown_cell(
            "### 3. Encoding Question IDs"
        ),
        nbf.v4.new_code_cell(
            "le = LabelEncoder()\n"
            "df['question_id_encoded'] = le.fit_transform(df['question_id'].astype(str))\n\n"
            "encoder_path = models_dir / 'question_encoder.pkl'\n"
            "with open(encoder_path, 'wb') as f:\n"
            "    pickle.dump(le, f)\n\n"
            "print(f'Saved Question Encoder to: {encoder_path}')\n"
            "print(f'Total Unique Questions: {len(le.classes_)}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 4. Save Preprocessed Data"
        ),
        nbf.v4.new_code_cell(
            "preprocessed_path = kt_dir / 'data' / 'ednet_preprocessed.csv'\n"
            "df.to_csv(preprocessed_path, index=False)\n"
            "print(f'Saved preprocessed data to {preprocessed_path}')"
        )
    ]
    with open(notebooks_dir / "01_Preprocessing.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb1, f)
        
    # =========================================================================
    # 2. CREATE 02_SequenceGeneration.ipynb
    # =========================================================================
    print("Creating 02_SequenceGeneration.ipynb...")
    nb2 = nbf.v4.new_notebook()
    nb2.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 3 — Knowledge Tracing (EdNet)\n"
            "## 02: Sequence Generation and Datasets\n\n"
            "In sequence learning, we group interactions per student and slice them into windows. "
            "This notebook loads the preprocessed data, slices them into sliding windows of size $W=50$, "
            "pads sequences shorter than 50, and splits the data into Train, Val, and Test PyTorch DataLoaders."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import torch\n"
            "import numpy as np\n"
            "import pandas as pd\n"
            "from pathlib import Path\n"
            "from Model3_KnowledgeTracing.src.dataset import prepare_sequences, get_dataloaders"
        ),
        nbf.v4.new_code_cell(
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "kt_dir = workspace_dir / 'Model3_KnowledgeTracing'\n"
            "preprocessed_path = kt_dir / 'data' / 'ednet_preprocessed.csv'\n\n"
            "# Test preparing sequences\n"
            "questions, prev_correctness, targets = prepare_sequences(\n"
            "    preprocessed_path, \n"
            "    window_size=50, \n"
            "    step_size=20, \n"
            "    num_questions=500\n"
            ")\n"
            "print('Sequence Shapes:')\n"
            "print(f'  Questions:        {questions.shape}')\n"
            "print(f'  Prev Correctness: {prev_correctness.shape}')\n"
            "print(f'  Targets:          {targets.shape}')"
        ),
        nbf.v4.new_markdown_cell(
            "### 1. Slicing and Padding Logic\n"
            "Let's look at one generated sequence. "
            "The question array contains encoded question IDs (value 500 represents padding). "
            "The previous correctness contains a shifted sequence starting with 0.0."
        ),
        nbf.v4.new_code_cell(
            "print('Sample Question Sequence:\\n', questions[0])\n"
            "print('\\nSample Previous Correctness Sequence:\\n', prev_correctness[0])\n"
            "print('\\nSample Target Sequence:\\n', targets[0])"
        ),
        nbf.v4.new_markdown_cell(
            "### 2. PyTorch DataLoaders\n"
            "We construct and verify train, val, and test loaders."
        ),
        nbf.v4.new_code_cell(
            "train_loader, val_loader, test_loader = get_dataloaders(\n"
            "    preprocessed_path,\n"
            "    window_size=50,\n"
            "    step_size=20,\n"
            "    batch_size=64,\n"
            "    num_questions=500\n"
            ")\n\n"
            "batch = next(iter(train_loader))\n"
            "print('Batch Shapes:')\n"
            "print('  Questions batch:', batch['questions'].shape)\n"
            "print('  Prev Correctness batch:', batch['prev_correctness'].shape)\n"
            "print('  Targets batch:', batch['targets'].shape)"
        )
    ]
    with open(notebooks_dir / "02_SequenceGeneration.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb2, f)

    # =========================================================================
    # 3. CREATE 03_Training.ipynb
    # =========================================================================
    print("Creating 03_Training.ipynb...")
    nb3 = nbf.v4.new_notebook()
    nb3.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 3 — Knowledge Tracing (EdNet)\n"
            "## 03: Model Training\n\n"
            "This notebook builds the Deep Knowledge Tracing (DKT) PyTorch LSTM, defines the optimizer "
            "and loss functions with padding masks, and runs the training loop with early stopping."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import json\n"
            "import torch\n"
            "from pathlib import Path\n"
            "from Model3_KnowledgeTracing.src.train import train_dkt"
        ),
        nbf.v4.new_code_cell(
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "kt_dir = workspace_dir / 'Model3_KnowledgeTracing'\n"
            "preprocessed_path = kt_dir / 'data' / 'ednet_preprocessed.csv'\n"
            "models_dir = kt_dir / 'models'\n\n"
            "# Run DKT training\n"
            "train_dkt(\n"
            "    preprocessed_csv_path=preprocessed_path,\n"
            "    output_dir=models_dir,\n"
            "    num_questions=500,\n"
            "    seq_len=50,\n"
            "    epochs=25,\n"
            "    batch_size=64,\n"
            "    lr=0.001,\n"
            "    patience=5\n"
            ")"
        )
    ]
    with open(notebooks_dir / "03_Training.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb3, f)

    # =========================================================================
    # 4. CREATE 04_Evaluation.ipynb
    # =========================================================================
    print("Creating 04_Evaluation.ipynb...")
    nb4 = nbf.v4.new_notebook()
    nb4.cells = [
        nbf.v4.new_markdown_cell(
            "# Model 3 — Knowledge Tracing (EdNet)\n"
            "## 04: Evaluation\n\n"
            "This notebook loads the trained DKT LSTM weights, evaluates the model performance "
            "on the unseen test set (ignoring padding elements), and plots the ROC curve."
        ),
        nbf.v4.new_code_cell(
            "import os\n"
            "import json\n"
            "import torch\n"
            "from pathlib import Path\n"
            "from Model3_KnowledgeTracing.src.evaluate import evaluate_dkt"
        ),
        nbf.v4.new_code_cell(
            "workspace_dir = Path('c:/Users/shiva/OneDrive/Desktop/StudentPlanner')\n"
            "kt_dir = workspace_dir / 'Model3_KnowledgeTracing'\n"
            "preprocessed_path = kt_dir / 'data' / 'ednet_preprocessed.csv'\n"
            "models_dir = kt_dir / 'models'\n\n"
            "# Evaluate the model\n"
            "metrics = evaluate_dkt(\n"
            "    preprocessed_csv_path=preprocessed_path,\n"
            "    models_dir=models_dir,\n"
            "    num_questions=500,\n"
            "    seq_len=50,\n"
            "    batch_size=64\n"
            ")"
        )
    ]
    with open(notebooks_dir / "04_Evaluation.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb4, f)
        
    print("All Model 3 notebooks created successfully.")

if __name__ == "__main__":
    create_notebooks()
