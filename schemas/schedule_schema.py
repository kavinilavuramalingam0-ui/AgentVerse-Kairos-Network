from pydantic import BaseModel, Field
from typing import List

class ScheduledTask(BaseModel):
    task_name: str = Field(description="Name of the task")
    # CoT happens here: The LLM must reason BEFORE assigning the time.
    reasoning: str = Field(description="Explain WHY this start time was chosen. Check prior dependencies (like drying clothes) or curfews.")
    start_time: str = Field(description="Start time in HH:MM AM/PM format")
    end_time: str = Field(description="End time in HH:MM AM/PM format")
    duration_mins: int = Field(description="Duration in minutes")
    location: str = Field(description="Location of the task")
    priority: str = Field(description="High, Medium, or Low")
    notes: str = Field(default="", description="Additional context")

class DailySchedule(BaseModel):
    date_context: str = Field(description="Day context summary")
    total_tasks: int = Field(description="Total count of scheduled entries")
    schedule: List[ScheduledTask] = Field(description="Chronological list of tasks")