import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas.schedule_schema import DailySchedule

load_dotenv()

class SchedulingAgent:
    def __init__(self, profile_data: dict):
        self.user_profile = profile_data
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=2048
        )
        
        self.structured_llm = self.llm.with_structured_output(DailySchedule)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are AuraOS, an Autonomous Life Companion & Scheduling Agent.\n"
             "Analyze user tasks and create a realistic schedule. You MUST read the Existing Schedule and NEVER overlap new tasks with existing events.\n\n"
             "=== USER PROFILE & HARD CONSTRAINTS ===\n"
             "{profile_data}\n\n"
             "=== EXISTING CALENDAR EVENTS ===\n"
             "{existing_schedule}\n\n"
             "=== STRICT SCHEDULING RULES ===\n"
             "1. CLASSIFICATION RULE: For every task in the JSON output, you MUST set 'is_new_task' to false if it is an existing calendar event, meal, or sleep. Set to true ONLY for the brand new tasks requested by the user.\n"
             "2. INVISIBLE CONSTRAINTS: Respect sleep schedules, college hours, and meal windows implicitly. Do not push them to the calendar if they aren't explicitly requested.\n"
             "3. CONFLICT AVOIDANCE: Find empty gaps in the EXISTING CALENDAR EVENTS to place the new tasks.\n"
             "4. LAUNDRY PHYSICS: Insert a passive 'Drying Clothes' gap of at least 3 hours between washing and folding.\n"
             "5. TIME MATH: Ensure end_time strictly follows start_time + duration_mins."
            ),
            ("human", "Here are my tasks to add for today:\n{tasks}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def schedule_day(self, raw_input_text: str, existing_schedule_text: str) -> DailySchedule:
        print("[System] AuraOS LangChain Pipeline Initiated (Context-Aware)...")
        try:
            return self.chain.invoke({
                "profile_data": json.dumps(self.user_profile, indent=2),
                "existing_schedule": existing_schedule_text,
                "tasks": raw_input_text
            })
        except Exception as e:
            print(f"[Execution Error] LangChain failed to process: {e}")
            return None