from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class StudentBase(BaseModel):
    gender: str = Field(..., description="Gender of the student (M or F)", examples=["M"])
    region: str = Field(..., description="Region where the student resides", examples=["East Anglian Region"])
    highest_education: str = Field(..., description="Highest education level", examples=["A Level or Equivalent"])
    imd_band: str = Field(..., description="Index of Multiple Deprivation band", examples=["80-90%"])
    age_band: str = Field(..., description="Age band of the student", examples=["0-35"])
    num_of_prev_attempts: int = Field(0, description="Number of previous attempts at this course", ge=0, examples=[0])
    disability: str = Field(..., description="Disability status (Y or N)", examples=["N"])
    
    # Study plan settings
    available_hours_per_day: float = Field(3.0, description="Hours available for study per day", gt=0.0, examples=[3.0])
    learning_goal: str = Field("General Study", description="Student learning goal", examples=["Prepare for exams"])
    current_course: str = Field("General Course", description="Current course name", examples=["Mathematics"])
    target_exam_days_away: int = Field(7, description="Number of days until the target exam", ge=1, examples=[7])

class StudentCreate(StudentBase):
    id_student: int = Field(..., description="Unique OULAD student ID", examples=[1001])

class StudentResponse(StudentBase):
    id_student: int = Field(..., description="Unique OULAD student ID", examples=[1001])
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time of record creation")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Time of record update")

    model_config = {
        "from_attributes": True
    }
