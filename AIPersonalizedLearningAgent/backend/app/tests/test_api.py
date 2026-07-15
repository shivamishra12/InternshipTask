import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Append the app directory's parent to path so app can be imported
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.main import app
from app.services.model_loader import ModelLoader

# Initialize TestClient
client = TestClient(app)

# Load models once for all tests
workspace_dir = Path(__file__).resolve().parents[3]
try:
    ModelLoader.load_all_models(workspace_dir)
    MODELS_LOADED = True
except Exception as e:
    MODELS_LOADED = False
    print(f"Warning: Models could not be loaded: {e}")

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_get_dashboard_valid_student():
    student_id = 11391
    
    # We test the actual endpoint which pulls together all services
    response = client.get(f"/api/v1/dashboard/{student_id}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "student" in data
    assert data["student"]["id_student"] == student_id
    
    assert "performance" in data
    assert "predicted_performance" in data["performance"]
    
    assert "risk" in data
    assert "risk_score" in data["risk"]
    
    assert "knowledge" in data
    assert "question_mastery" in data["knowledge"]
    
    assert "weak_topics" in data
    assert isinstance(data["weak_topics"], list)
    
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    
    assert "study_plan" in data
    assert "markdown_plan" in data["study_plan"]
    
def test_get_dashboard_invalid_student():
    # Attempting to fetch a student that definitely doesn't exist in CSV
    student_id = 999999999
    
    response = client.get(f"/api/v1/dashboard/{student_id}")
    
    # It should return 404 because student is not found
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_predict_performance():
    response = client.post("/api/v1/predict/performance", json={"student_id": 11391})
    assert response.status_code == 200
    assert "predicted_performance" in response.json()

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_predict_risk():
    response = client.post("/api/v1/predict/risk", json={"student_id": 11391})
    assert response.status_code == 200
    assert "risk_score" in response.json()

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_knowledge():
    response = client.post("/api/v1/knowledge", json={"student_id": 11391})
    assert response.status_code == 200
    assert "question_mastery" in response.json()

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_weak_topics():
    # Needs mastery dictionary
    dummy_mastery = {"q1": 0.2, "q2": 0.8}
    response = client.post("/api/v1/weak-topics", json={"student_id": 11391, "question_mastery": dummy_mastery})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_recommendations():
    response = client.post("/api/v1/recommendations", json={"student_id": 11391, "k": 3})
    assert response.status_code == 200
    assert "recommendations" in response.json()

@pytest.mark.skipif(not MODELS_LOADED, reason="Models not found")
def test_study_plan():
    response = client.post("/api/v1/study-plan", json={"student_id": 11391})
    assert response.status_code == 200
    assert "markdown_plan" in response.json()

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_frontend_index_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Personalized Learning Agent" in response.text
    assert "./app.js" in response.text

if __name__ == "__main__":
    test_health_check()
    test_get_dashboard_valid_student()
    test_get_dashboard_invalid_student()
    test_predict_performance()
    test_predict_risk()
    test_knowledge()
    test_weak_topics()
    test_recommendations()
    test_study_plan()
    print("All API tests passed successfully!")
