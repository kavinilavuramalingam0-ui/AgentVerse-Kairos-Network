from pydantic import BaseModel, Field
from typing import List

class ScheduledTask(BaseModel):
    task_name: str = Field(description="Name of the task")
    reasoning: str = Field(description="Explain WHY this start time was chosen.")
    is_new_task: bool = Field(description="Set to True ONLY for newly requested tasks. False for existing events or daily meals.")
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

