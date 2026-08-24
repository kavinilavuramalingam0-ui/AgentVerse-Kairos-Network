import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .workflow_schema import EmailAnalysis

load_dotenv()

class WorkflowAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="qwen/qwen3.6-27b",
            temperature=0.1, 
            max_tokens=2048,
            reasoning_effort="none"
        )
        
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are the Workflow Automation Agent for AuraOS.\n"
             "Your job is to read inbound communications (emails, newsletters, messages) and extract concrete, actionable tasks.\n\n"
             "TASK DEFINITION RULES:\n"
             "1. OPPORTUNITIES ARE TASKS: If the message contains invitations to register for hackathons, apply for internships, placement drives, or freelance gigs, you MUST extract it as a task (e.g., 'Register for Pep Sales Stars 2026').\n"
             "2. ACTION VERBS: Look for explicit calls to action like 'Apply Here', 'Register Now', or 'Submit'.\n"
             "3. IGNORE TRUE SPAM: Ignore generic marketing fluff, but NEVER ignore career or academic opportunities.\n"
             "4. ESTIMATIONS: Estimate realistic durations (e.g., 'Apply for Internship' ~30 mins, 'OS study prep' ~90 mins).\n"
             "5. TASK IDENTITY: Extract the task name consistently so equivalent tasks produce the same task identity.\n"
             "6. CRITICAL SCHEMA RULE: When calling the tool, the 'estimated_duration_mins' parameter MUST be a raw integer (e.g., 30). DO NOT wrap it in quotes (e.g., '30').\n\n"
             "If the message contains absolutely no academic, professional, or actionable items, return an empty list."
            ),
            ("human", "Analyze this inbound message:\n\n{message}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    # Inside agents/workflow_agent/agent.py

    def analyze_message(self, raw_text: str):
        print("[System] Workflow Agent analyzing inbound communication...")
        try:
            # Invoking the LLM to extract structured data
            result = self.chain.invoke({"message": raw_text})
            return result
            
        except Exception as e:
            # Safely catch Groq API 400 errors, JSON parsing errors, or hallucinations
            print(f"[Execution Error] Workflow Agent failed to parse tool call: {e}")
            print("[INFO] Skipping this message due to extraction failure.")
            return None