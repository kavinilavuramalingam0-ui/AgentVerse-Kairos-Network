import os
import json
import datetime
import time
from tools.calendar_tool import add_to_calendar, get_todays_events
from tools.gmail_tool import fetch_unread_emails

# Import all four agents
from agents.scheduling_agent.scheduling_agent import SchedulingAgent
from agents.workflow_agent.workflow_agent import WorkflowAgent
from agents.knowledge_agent.knowledge_agent import KnowledgeAgent
from agents.fitness_agent.fitness_agent import FitnessAgent

def load_or_create_profile(user_name: str) -> dict:
    profile_path = f"data/{user_name}_profile.json"
    if os.path.exists(profile_path):
        print(f"[MEMORY] Welcome back, {user_name}! Loading constraints.")
        with open(profile_path, "r") as f:
            return json.load(f)
    else:
        return {"user_name": user_name}

def process_and_schedule_input(raw_text: str, scheduling_agent, workflow_agent):
    analysis = workflow_agent.analyze_message(raw_text)
    
    if not analysis or not analysis.actionable_tasks:
        print("[INFO] No actionable tasks found in this text.")
        return
        
    print(f"\n[AGENT 2] Extracted Intent: {analysis.sender_intent}")
    user_input = "Please schedule these extracted tasks:\n"
    for t in analysis.actionable_tasks:
        user_input += f"- {t.task_name} (Priority: {t.priority}, Est: {t.estimated_duration_mins} mins)\n"
        print(f" -> Found Task: {t.task_name} ({t.estimated_duration_mins} mins)")

    print("\n[AGENT 1] Reasoning & Planning your optimal schedule...")
    current_schedule = get_todays_events()
    current_time_str = datetime.datetime.now().astimezone().strftime('%A, %B %d, %Y %I:%M %p %Z')
    
    schedule_data = scheduling_agent.schedule_day(user_input, current_schedule, current_time_str)
    
    if schedule_data:
        print(f"\n[AUDIT LOG]\n{schedule_data.calendar_audit_log}\n")
        print("[AGENT 1] Executing real-world actions...")
        
        for task in schedule_data.schedule:
            if hasattr(task, 'is_new_task') and not task.is_new_task:
                continue
            if current_schedule != "No events scheduled for the upcoming window." and task.task_name.strip().lower() in current_schedule.lower():
                print(f"[SHIELD] Blocked duplicate event: {task.task_name}")
                continue
                
            add_to_calendar(task.task_name, task.start_time, task.end_time, task.location)
            
        print("\n[SUCCESS] Tasks pushed to Google Calendar!")

def main():
    print("===================================================")
    print("  The Kairos Network: MULTI-AGENT ORCHESTRATOR     ")
    print("===================================================")
    
    user_name = input("Enter User Name: ").strip()
    profile_data = load_or_create_profile(user_name)
    
    # Initialize all 4 agents
    scheduling_agent = SchedulingAgent(profile_data=profile_data)
    workflow_agent = WorkflowAgent()
    knowledge_agent = KnowledgeAgent()
    fitness_agent = FitnessAgent(profile_data=profile_data)
    
    while True:
        print("\n---------------------------------------------------")
        print("Choose Mode:")
        print("1. Direct Task")
        print("2. Paste Email (Manual Extract)")
        print("3. AUTONOMOUS BACKGROUND MONITOR (Live Inbox)")
        print("4. ASK KNOWLEDGE AGENT (Study Mode)")
        print("5. FITNESS COACH (Dynamic Workout)  <-- NEW")
        print("Type 'exit' to quit.")
        
        mode = input("> ").strip()
        
        if mode.lower() in ['exit', 'quit']:
            break
            
        if mode == "1":
            # DIRECT TASK MODE: Bypasses Agent 2 entirely and talks directly to Agent 1
            user_input = input("\nEnter your tasks directly for scheduling:\n> ")
            print("\n[AGENT 1] Reasoning & Planning your optimal schedule...")
            
            current_schedule = get_todays_events()
            current_time_str = datetime.datetime.now().astimezone().strftime('%A, %B %d, %Y %I:%M %p %Z')
            
            # Agent 1 handles the raw natural language directly
            schedule_data = scheduling_agent.schedule_day(user_input, current_schedule, current_time_str)
            
            if schedule_data:
                print(f"\n[AUDIT LOG]\n{schedule_data.calendar_audit_log}\n")
                print("[AGENT 1] Executing real-world actions...")
                
                for task in schedule_data.schedule:
                    if hasattr(task, 'is_new_task') and not task.is_new_task:
                        continue
                    if current_schedule != "No events scheduled for the upcoming window." and task.task_name.strip().lower() in current_schedule.lower():
                        print(f"[SHIELD] Blocked duplicate event: {task.task_name}")
                        continue
                        
                    add_to_calendar(task.task_name, task.start_time, task.end_time, task.location)
                    
                print("\n[SUCCESS] Tasks pushed to Google Calendar!")   
        elif mode == "2":
            raw_email = input("\nPaste the email/message here:\n> ")
            process_and_schedule_input(raw_email, scheduling_agent, workflow_agent)
            
        elif mode == "3":
            print("\n[SYSTEM] Entering Autonomous Mode. Press CTRL+C to stop.")
            while True:
                try:
                    unread_emails = fetch_unread_emails()
                    for email_text in unread_emails:
                        print(f"\n[SYSTEM] Processing new inbound email...")
                        process_and_schedule_input(email_text, scheduling_agent, workflow_agent)
                        print("-" * 40)
                    time.sleep(60) 
                except KeyboardInterrupt:
                    print("\n[SYSTEM] Exited Autonomous Mode.")
                    break
                except Exception as e:
                    print(f"\n[ERROR] Autonomous Monitor Interrupted: {e}")
                    print("[SYSTEM] Safely retrying in 60 seconds...")
                    time.sleep(60)
                
        elif mode == "4":
            print("\n[SYSTEM] Entering Study Mode. Type 'back' to return.")
            while True:
                user_question = input("\nAsk your Data Science question:\n> ").strip()
                if user_question.lower() == 'back':
                    break
                if user_question:
                    answer = knowledge_agent.query(user_question)
                    print(f"\n[AGENT 3 - KNOWLEDGE]\n{answer}")
                    
        elif mode == "5":
            print("\n[SYSTEM] Entering Gym Mode. Type 'back' to return.")
            while True:
                user_question = input("\nWhat are your current constraints (e.g., 'treadmill taken, full stomach') or type 'start workout':\n> ").strip()
                if user_question.lower() == 'back':
                    break
                if user_question:
                    answer = fitness_agent.generate_and_run_workout(user_question)
                    print(f"\n[AGENT 4 - FITNESS]\n{answer}")
        else:
            continue

if __name__ == "__main__":
    main()