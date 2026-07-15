import sys
from pathlib import Path
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError

# Append the app directory's parent to path so app can be imported
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.predict import PerformanceResponse, RiskResponse, HistoryItem, KnowledgeRequest
from app.schemas.dashboard import DashboardResponse, WeakTopicResponse

def test_student_schemas():
    # 1. Test Valid StudentCreate
    valid_student_data = {
        "id_student": 1001,
        "gender": "M",
        "region": "South Region",
        "highest_education": "HE Qualification",
        "imd_band": "50-60%",
        "age_band": "0-35",
        "num_of_prev_attempts": 0,
        "disability": "N",
        "available_hours_per_day": 3.5,
        "learning_goal": "Pass assessment",
        "current_course": "Maths",
        "target_exam_days_away": 10
    }
    
    student = StudentCreate(**valid_student_data)
    assert student.id_student == 1001
    assert student.gender == "M"
    assert student.available_hours_per_day == 3.5
    
    # 2. Test Invalid StudentCreate (missing required field region)
    invalid_data = valid_student_data.copy()
    del invalid_data["region"]
    
    with pytest.raises(ValidationError):
        StudentCreate(**invalid_data)
        
    # 3. Test Invalid StudentCreate (invalid available_hours_per_day value - must be gt 0)
    invalid_hours = valid_student_data.copy()
    invalid_hours["available_hours_per_day"] = -1.0
    
    with pytest.raises(ValidationError):
        StudentCreate(**invalid_hours)

def test_prediction_schemas():
    # Test valid HistoryItem validation
    item = HistoryItem(question_id="q1", correctness=1)
    assert item.question_id == "q1"
    assert item.correctness == 1

    # Test invalid HistoryItem correctness constraint
    with pytest.raises(ValidationError):
        HistoryItem(question_id="q1", correctness=5)

    # Test KnowledgeRequest with history list
    req = KnowledgeRequest(
        student_id=1001,
        history=[
            {"question_id": "q1", "correctness": 1},
            {"question_id": "q2", "correctness": 0}
        ]
    )
    assert len(req.history) == 2
    assert req.history[0].question_id == "q1"

def test_dashboard_schema():
    # Construct complete DashboardResponse
    student_res = {
        "id_student": 1001,
        "gender": "M",
        "region": "South Region",
        "highest_education": "HE Qualification",
        "imd_band": "50-60%",
        "age_band": "0-35",
        "num_of_prev_attempts": 0,
        "disability": "N",
        "available_hours_per_day": 3.5,
        "learning_goal": "Pass assessment",
        "current_course": "Maths",
        "target_exam_days_away": 10,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    
    perf_res = {
        "student_id": 1001,
        "predicted_performance": "Pass",
        "success_probability": 0.82
    }
    
    risk_res = {
        "student_id": 1001,
        "risk_score": 0.18,
        "is_at_risk": False
    }
    
    knowledge_res = {
        "student_id": 1001,
        "question_mastery": {"q1": 0.95, "q2": 0.33}
    }
    
    weak_topics = [
        {"topic": "Geometry", "mastery": 0.33}
    ]
    
    recommendations = [
        {"rank": 1, "id_site": 541221, "score": 0.95, "type": "Collaborative Filtering"}
    ]
    
    study_plan = {
        "student_id": 1001,
        "plan": [
            {
                "day": 1,
                "tasks": [{"topic": "Geometry Basics", "duration": "60 min"}]
            }
        ],
        "markdown_plan": "# Day 1: Geometry Basics"
    }

    dash = DashboardResponse(
        student=student_res,
        performance=perf_res,
        risk=risk_res,
        knowledge=knowledge_res,
        weak_topics=weak_topics,
        recommendations=recommendations,
        study_plan=study_plan
    )
    
    assert dash.student.id_student == 1001
    assert dash.performance.predicted_performance == "Pass"
    assert dash.weak_topics[0].topic == "Geometry"
    assert len(dash.recommendations) == 1
    assert dash.study_plan.plan[0].day == 1

    print("All Pydantic v2 Schema assertions passed successfully!")

if __name__ == "__main__":
    test_student_schemas()
    test_prediction_schemas()
    test_dashboard_schema()
