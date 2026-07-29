import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from schemas.schedule_schema import DailySchedule

# Load API Keys
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
             "You are an expert Autonomous Life Companion & Scheduling Agent.\n"
             "Analyze user tasks and create a realistic schedule. You MUST read the Existing Schedule and never overlap new tasks with existing events.\n\n"
             "=== USER PROFILE & HARD CONSTRAINTS ===\n"
             "{profile_data}\n\n"
             "{existing_schedule}\n\n"
             "=== STRICT SCHEDULING RULES ===\n"
             "1. CONFLICT AVOIDANCE: Do NOT schedule any tasks during the times listed in the EXISTING CALENDAR EVENTS.\n"
             "2. PHYSIOLOGY: Inject meals if they are not already in the existing schedule. Respect sleep boundaries strictly.\n"
             "3. LAUNDRY PHYSICS: Insert a passive 'Drying Clothes' gap of at least 3 hours between washing and folding.\n"
             "4. SPATIAL BOUNDARIES: Obey the curfew and campus times strictly based on the user profile.\n"
             "5. TIME MATH: Ensure end_time strictly follows start_time + duration_mins."
            ),
            ("human", "Here are my tasks to add for today:\n{tasks}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def schedule_day(self, raw_input_text: str, existing_schedule_text: str) -> DailySchedule:
        print("[System] LangChain Pipeline Initiated (Context-Aware)...")
        try:
            result: DailySchedule = self.chain.invoke({
                "profile_data": json.dumps(self.user_profile, indent=2),
                "existing_schedule": existing_schedule_text,
                "tasks": raw_input_text
            })
            return result
        except Exception as e:
            print(f"[Execution Error] LangChain failed to process: {e}")
            return None

    def _load_profile(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        return {}
