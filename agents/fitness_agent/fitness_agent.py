import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Import your local tool 
from tools.timer_tool import start_workout_timer

load_dotenv()

class FitnessAgent:
    def __init__(self, profile_data: dict):
        print("[System] Initializing Agent 4 (Dynamic Fitness Coach via Core LCEL)...")
        
        # 1. Initialize the Core LLM
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.4, 
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # 2. Dynamically load user context 
        self.user_name = profile_data.get("user_name", "Kavinilavu R")
        self.profile_context = json.dumps(profile_data, indent=2)
        
        # 3. Scan the image folder for available visual aids
        image_dir = "data/gym/Pregenerated_Exercises"
        self.available_images = []
        if os.path.exists(image_dir):
            self.available_images = os.listdir(image_dir)
        
        # 4. Define the System Prompt Goal
        self.system_prompt = (
             "You are The Kairos Network's Elite Dynamic Fitness Agent.\n"
             f"User Name: {self.user_name}\n\n"
             "=== USER PROFILE & PHYSICAL CONSTRAINTS ===\n"
             f"{self.profile_context}\n\n"
             "=== AVAILABLE VISUAL AIDS ===\n"
             f"You can use these exact filenames: {self.available_images}\n\n"
             "YOUR DIRECTIVES:\n"
             "1. DYNAMIC ADAPTATION: The user will provide real-time constraints (e.g., 'full stomach', 'treadmill taken'). You MUST instantly recalculate the workout.\n"
             "2. VISUAL MAPPING: You MUST prioritize designing routines using the specific exercises listed in the visual aids.\n"
             "3. GRACEFUL FALLBACK: If you MUST prescribe an exercise NOT in the visual aids list, provide a 2-sentence physical description instead. DO NOT guess image links.\n"
             "4. LINK FORMAT: Output markdown links exactly like this: `![Visual](data/gym/Pregenerated_Exercises/Exact_Filename.png)`.\n"
             "5. AUTONOMOUS TIMING: If the user says 'start workout', you MUST trigger the `run_timer` tool to automate their exercise sequentially."
        )
        
        # 5. FIRST PRINCIPLES TOOL BINDING: Define the tool structure manually
        self.timer_schema = {
            "type": "function",
            "function": {
                "name": "run_timer",
                "description": "Start a live physical countdown timer for the user's workout or rest periods.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "duration_seconds": {
                            "type": "integer", 
                            "description": "The exact duration in seconds (e.g., 45)."
                        },
                        "exercise_name": {
                            "type": "string", 
                            "description": "The name of the exercise."
                        }
                    },
                    "required": ["duration_seconds", "exercise_name"]
                }
            }
        }
        
        # Inject the tool directly into the LLM's capabilities
        self.llm_with_tools = self.llm.bind_tools([self.timer_schema])

    def generate_and_run_workout(self, user_input: str):
        print("\n[System] Fitness Agent reasoning and evaluating tool calls...")
        try:
            # Construct the conversation history
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=user_input)
            ]
            
            # The LLM decides what to do (Perception -> Decision)
            response = self.llm_with_tools.invoke(messages)
            
            # (Action) Check if the LLM decided to trigger a tool
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    if tool_call['name'] == 'run_timer':
                        args = tool_call['args']
                        print(f"\n[AGENT 4] Autonomous Decision: Executing timer for {args['duration_seconds']}s")
                        
                        # Physically run the Python function
                        timer_result = start_workout_timer(
                            duration_seconds=args['duration_seconds'], 
                            exercise_name=args['exercise_name']
                        )
                        return f"[TOOL EXECUTION COMPLETE] {timer_result}"
            
            # If no tools were needed, return the standard text response
            return response.content

        except Exception as e:
            return f"[Error] Fitness Agent encountered an issue: {e}"