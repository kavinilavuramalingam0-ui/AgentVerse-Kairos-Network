import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .workflow_schema import EmailAnalysis

load_dotenv()

class WorkflowAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1, 
            max_tokens=1024
        )
        
        self.structured_llm = self.llm.with_structured_output(EmailAnalysis)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are the Workflow Automation Agent for AuraOS.\n"
             "Your job is to read messy, unstructured inbound communications (emails, client Slack messages) and extract concrete tasks.\n"
             "1. Ignore pleasantries and filler text.\n"
             "2. Estimate realistic durations (e.g., UI mockups take ~120 mins, OS study prep takes ~90 mins).\n"
             "3. If a message contains no actionable tasks, return an empty list."
            ),
            ("human", "Analyze this inbound message:\n\n{message}")
        ])
        
        self.chain = self.prompt | self.structured_llm

    def analyze_message(self, raw_message: str) -> EmailAnalysis:
        print("[System] Workflow Agent analyzing inbound communication...")
        try:
            return self.chain.invoke({"message": raw_message})
        except Exception as e:
            print(f"[Execution Error] Workflow Agent failed: {e}")
            return None