import os
import json
from agents.scheduling_agent import SchedulingAgent
from tools.calendar_tool import add_to_calendar, get_todays_events

def load_or_create_profile(user_name: str) -> dict:
    profile_path = f"data/{user_name}_profile.json"
    if os.path.exists(profile_path):
        print(f"[MEMORY] Welcome back, {user_name}! Loading your constraints.")
        with open(profile_path, "r") as f:
            return json.load(f)
    else:
        print(f"[MEMORY] New user detected. Creating default profile for {user_name}...")
        default_profile = {
            "user_type": "Hackathon Developer",
            "campus_rules": {
                "hostel_curfew_time": "09:00 PM",
                "college_hours": "08:40 AM - 04:10 PM",
                "outside_movement_allowed_window": "08:30 AM - 05:00 PM"
            },
            "physiological_baselines": {
                "breakfast_window": "08:00 AM - 09:00 AM",
                "lunch_window": "01:00 PM - 02:00 PM",
                "dinner_window": "07:30 PM - 08:30 PM",
                "sleep_schedule_standard": "12:00 AM - 07:15 AM",
                "sleep_schedule_heavy_work": "01:30 AM - 07:45 AM"
            },
            "physical_reality_rules": {
                "laundry_drying_gap_hours": 3,
                "travel_buffer_mins_between_campus_and_market": 20,
                "evening_hackathon_grind_window": "05:00 PM - 11:30 PM"
            }
        }
        os.makedirs("data", exist_ok=True)
        with open(profile_path, "w") as f:
            json.dump(default_profile, f, indent=2)
        return default_profile

def main():
    print("===================================================")
    print("          Kairos: AUTONOMOUS LIFE COMPANION        ")
    print("===================================================")
    
    user_name = input("Enter User/Judge Name (e.g., Kavinilavu): ").strip()
    profile_data = load_or_create_profile(user_name)
    agent = SchedulingAgent(profile_data=profile_data)
    
    while True:
        print("\n---------------------------------------------------")
        user_input = input("Enter your tasks for today (or type 'exit' to quit):\n> ")
        
        if user_input.lower() in ['exit', 'quit']:
            print("Shutting down AuraOS...")
            break
        if not user_input.strip(): continue

        print("\n[AGENT] Reasoning & Planning your optimal schedule...")
        current_schedule = get_todays_events()
        print("\n" + current_schedule) 
        
        schedule_data = agent.schedule_day(user_input, current_schedule)
        
        if schedule_data:
            print("\n[AGENT] Schedule Generated! Executing real-world actions...")
            for task in schedule_data.schedule:
                
                # --- THE DETERMINISTIC SHIELD ---
                # 1. Check if the LLM flagged it as an old task
                if hasattr(task, 'is_new_task') and not task.is_new_task:
                    print(f"[INFO] Skipping flagged baseline/existing task: {task.task_name}")
                    continue
                
                # 2. Check if the task name matches ANY text in the current schedule (Foolproof)
                # We use lower() and strip() to ensure a tight text match.
                # E.g., if "Codestreet" is in the calendar string, drop it immediately.
                if current_schedule != "No events scheduled for today." and task.task_name.strip().lower() in current_schedule.lower():
                    print(f"[SHIELD] Blocked duplicate event: {task.task_name}")
                    continue
                # ---------------------------------
                
                if "drying" in task.task_name.lower():
                    print(f"[INFO] Skipping passive task: {task.task_name}")
                    continue
                    
                add_to_calendar(task.task_name, task.start_time, task.end_time, task.location)
                
            print("\n[SUCCESS] Tasks pushed to Google Calendar!")

if __name__ == "__main__":
    main()