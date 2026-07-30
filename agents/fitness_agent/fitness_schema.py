from pydantic import BaseModel, Field

class TimerToolSchema(BaseModel):
    duration_seconds: int = Field(
        description="The strict duration of the exercise or rest period in seconds (integers only)."
    )
    exercise_name: str = Field(
        description="The name of the exercise or rest period."
    )