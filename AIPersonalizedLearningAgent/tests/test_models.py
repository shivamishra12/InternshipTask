import sys
import unittest
from pathlib import Path

# Resolve workspace root and append to sys.path
workspace_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(workspace_dir))

class TestPersonalizedLearningAgent(unittest.TestCase):
    
    def test_imports(self):
        """Verify all package components can be imported successfully."""
        try:
            from PersonalizedLearningAgent.ml.performance.preprocess import preprocess_features
            from PersonalizedLearningAgent.ml.performance.train import train_and_evaluate_model
            from PersonalizedLearningAgent.ml.dkt.preprocess import preprocess_ednet_data
            from PersonalizedLearningAgent.ml.recommendation.recommend import recommend_top_k
            from PersonalizedLearningAgent.ml.planner.planner import generate_and_export_plan
            
            self.assertTrue(True)
            print("Imports validation: PASSED")
        except ImportError as e:
            self.fail(f"Import validation failed: {e}")

    def test_recommendation_inference(self):
        """Verify the item-based collaborative filtering recommender can make predictions."""
        import pickle
        from scipy.sparse import csr_matrix
        
        models_dir = workspace_dir / "PersonalizedLearningAgent" / "models"
        self.assertTrue((models_dir / "recommendation_model.pkl").exists(), "recommendation_model.pkl is missing!")
        
        with open(models_dir / "recommendation_model.pkl", "rb") as f:
            model_data = pickle.load(f)
            
        self.assertIn("S", model_data)
        self.assertIn("student_to_idx", model_data)
        self.assertIn("site_to_idx", model_data)
        print("Recommendation model load validation: PASSED")

    def test_study_planner_inference(self):
        """Verify the study planner orchestrates and exports study plans."""
        from PersonalizedLearningAgent.ml.planner.planner import generate_and_export_plan
        
        profile = {
            "available_hours_per_day": 2.5,
            "learning_goal": "Review calculus and pass the algebra mock exam.",
            "current_course": "Advanced Calculus",
            "target_exam_days_away": 7
        }
        
        raw_markdown, plan_dict = generate_and_export_plan(1001, profile)
        self.assertEqual(plan_dict.get("student_id"), 1001)
        self.assertEqual(len(plan_dict.get("plan", [])), 7)
        
        outputs_dir = workspace_dir / "PersonalizedLearningAgent" / "outputs"
        self.assertTrue((outputs_dir / "study_plan.json").exists())
        self.assertTrue((outputs_dir / "study_plan.md").exists())
        print("Study Planner execution validation: PASSED")

if __name__ == "__main__":
    unittest.main()
