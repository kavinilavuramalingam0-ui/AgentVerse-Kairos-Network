import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .schedule_schema import DailySchedule

load_dotenv()

class SchedulingAgent:
    def __init__(self, profile_data: dict):
        self.user_profile = profile_data
        
        self.llm = ChatGroq(
            model="qwen/qwen3.6-27b",
            temperature=0.1,
            max_tokens=2048,
            reasoning_effort="none"
        )
        
        self.structured_llm = self.llm.with_structured_output(DailySchedule, method="json_mode")

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are The Kairos Network's Core Scheduling Agent.\n"
             "Your supreme directive is to NEVER double-book events.\n\n"
             "=== LIVE CLOCK ===\n"
             "Current Date & Time: {current_datetime}\n\n"
             "=== USER PROFILE & HARD CONSTRAINTS ===\n"
             "{profile_data}\n\n"
             "=== EXISTING CALENDAR EVENTS ===\n"
             "{existing_schedule}\n\n"
             "=== REASONING & SCHEDULING RULES ===\n"
             "1. THE AUDIT: You must first fill out the 'calendar_audit_log' by analyzing the EXISTING CALENDAR EVENTS compared to the LIVE CLOCK.\n"
             "2. CROSS-MIDNIGHT SCHEDULING: The biological working day does not end at 11:59 PM. You are permitted to schedule tasks past midnight up until the defined sleep bounds.\n"
             "3. STRICT AVOIDANCE: If an event spans 5:00 PM to 10:00 PM, that 5-hour block is a DEAD ZONE. Find an earlier or later gap.\n"
             "4. CLASSIFICATION: Set 'is_new_task' to false for existing calendar events. Set to true ONLY for the brand new extracted tasks.\n"
             "5. TIME MATH: Ensure end_time strictly follows start_time + duration_mins.\n"
             "6. PASSIVE TASKS (CRITICAL): Ignore tasks that do not require active human effort. Do NOT output these into the schedule array.\n"
             "7. OUTPUT FORMAT (MANDATORY): Return exactly one JSON object using these exact top-level keys: "
                "calendar_audit_log (string), date_context (string), total_tasks (integer), and schedule (array). "
                "Do NOT use 'scheduled_tasks'. 'calendar_audit_log' MUST be a plain string, NOT an object. "
                "Each object inside 'schedule' MUST contain exactly these fields: task_name, reasoning, "
                "is_new_task, start_time, end_time, duration_mins, location, priority, and notes. "
                "Do not rename fields, add extra top-level fields, or output markdown/code fences.\n"
            "8. DUPLICATE PREVENTION: Never schedule a task if an equivalent task already exists in the existing calendar.\n"
            "9. TIME CONFLICT: Never schedule a new task over an existing calendar event. Existing events are hard blocked time.\n"
            "10. CROSS-MIDNIGHT: Treat times after midnight as belonging to the following calendar day when calculating duration and conflicts.\n"
            "11. TASK ID: Generate a stable lowercase task_id from the task name, using words separated by underscores.\n"),
            ("human", "Here are the tasks to analyze and schedule:\n{tasks}")
        ])
        self.chain = self.prompt | self.structured_llm

    def schedule_day(self, raw_input_text: str, existing_schedule_text: str, current_time_str: str):
        print("[System] Kairos Network Pipeline Initiated (Time-Aware)...")
        try:
            return self.chain.invoke({
                "current_datetime": current_time_str,
                "profile_data": json.dumps(self.user_profile, indent=2),
                "existing_schedule": existing_schedule_text,
                "tasks": raw_input_text
            })
        except Exception as e:
            print(f"[Execution Error] LangChain failed to process: {e}")
            return None