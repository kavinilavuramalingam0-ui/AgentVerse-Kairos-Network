from pydantic import BaseModel, Field
from typing import List

class ExtractedTask(BaseModel):
    task_name: str = Field(description="A clean, concise name for the extracted task.")
    estimated_duration_mins: int = Field(description="Estimate how long this will take based on context.")
    priority: str = Field(description="High, Medium, or Low based on urgency.")

class EmailAnalysis(BaseModel):
    sender_intent: str = Field(description="A 1-sentence summary of what the sender wants.")
    actionable_tasks: List[ExtractedTask] = Field(description="List of actionable tasks extracted from the message.")