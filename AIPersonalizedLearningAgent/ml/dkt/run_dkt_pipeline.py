import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path
import time

def run_pipeline():
    workspace_dir = Path("c:/Users/shiva/OneDrive/Desktop/StudentPlanner")
    notebooks_dir = workspace_dir / "Model3_KnowledgeTracing" / "notebooks"
    
    # Initialize the Executer
    ep = ExecutePreprocessor(timeout=1800, kernel_name='python3')
    
    notebooks = [
        "01_Preprocessing.ipynb",
        "02_SequenceGeneration.ipynb",
        "03_Training.ipynb",
        "04_Evaluation.ipynb"
    ]
    
    for nb_name in notebooks:
        nb_path = notebooks_dir / nb_name
        print(f"\n==================================================")
        print(f"Executing {nb_name}...")
        print(f"==================================================")
        
        t0 = time.time()
        try:
            with open(nb_path, "r", encoding="utf-8") as f:
                nb = nbformat.read(f, as_version=4)
            
            # Execute the notebook in the context of the workspace root to resolve imports
            ep.preprocess(nb, {'metadata': {'path': str(workspace_dir)}})
            
            with open(nb_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)
                
            print(f"Successfully finished executing {nb_name} in {time.time() - t0:.2f} seconds.")
        except Exception as e:
            print(f"Error executing {nb_name}: {e}")
            raise e

if __name__ == "__main__":
    run_pipeline()
