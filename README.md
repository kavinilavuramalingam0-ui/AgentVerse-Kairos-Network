<img width="450" height="450" alt="MiammiamGIF" src="https://github.com/user-attachments/assets/7192a51e-4d3d-4d6e-b06d-75b72c148469" />### The Kairos Network: Autonomous Multi-Agent Orchestrator

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework-LangChain](https://img.shields.io/badge/Framework-LangChain-orange.svg)](https://www.langchain.com/)
[![RAG-LlamaIndex](https://img.shields.io/badge/RAG-LlamaIndex-purple.svg)](https://www.llamaindex.ai/)
[![Inference-Groq_LPU](https://img.shields.io/badge/Inference-Groq_LPU-red.svg)](https://groq.com/)
[![Tools-Google_Workspace](https://img.shields.io/badge/Tools-Calendar_%26_Gmail_API-green.svg)](https://workspace.google.com/)

An autonomous personal AI companion and event-driven multi-agent ecosystem built from first principles for the **AgentVerse Hackathon**. **The Kairos Network** coordinates four specialized reasoning agents inside an interactive, unified terminal workspace to handle real-world spatial-temporal scheduling, inbound email intent extraction, deterministic academic tutoring (RAG), and dynamic physical workout execution.

---

## System Architecture

```text
===================================================================================
                  THE KAIROS NETWORK: MULTI-AGENT ARCHITECTURE
===================================================================================

                        [ USER INTERACTIVE TERMINAL ]
                                     │
                                     ▼
                  +-------------------------------------+
                  |   KAIROS CORE ORCHESTRATOR LOOP     |
                  | (Loads Profile Memory & Coordinates)|
                  +-------------------------------------+
                                     │
        ┌────────────────┬───────────┴────────────┬────────────────┐
        │                │                        │                │
        ▼                ▼                        ▼                ▼
+---------------+ +---------------+      +----------------+ +---------------+
| AGENT 1       | | AGENT 2       |      | AGENT 3        | | AGENT 4       |
| SCHEDULER     | | WORKFLOW      |      | KNOWLEDGE/RAG  | | FITNESS COACH |
| (Time-Aware)  | | (Extractor)   |      | (Deterministic)| | (Dynamic LCEL)|
+---------------+ +---------------+      +----------------+ +---------------+
        │                │                        │                │
        ├────────────────┘                        │                │
        ▼                                         ▼                ▼
[ Google Workspace ]                      [ Local Vector DB ] [ System Tools ]
- Google Calendar API                     - Hugging Face Embed - OS Winsound Beep
- Gmail Inbox API (OAuth2)                - LlamaIndex Store   - Visual Exercises
```
## Directory Structure
<img width="613" height="761" alt="image" src="https://github.com/user-attachments/assets/376c7c68-22bf-458e-ade7-a956e4c0aae8" />

## Installation & Setup
1. Clone the Repository
   ```bash
   git clone https://github.com/kavinilavuramalingam0-ui/AgentVerse-Kairos-Network.git
   cd AgentVerse-Kairos-Network
   ```
2. Install Required Dependencies
   Run the following package installations in your Python environment:
   ```bash
   # Core LLM, schema validation, and environment variables
    pip install groq google-genai python-dotenv pydantic

    # Knowledge Base & Vector Embeddings
    pip install llama-index llama-index-readers-file llama-index-llms-groq llama-index-embeddings-huggingface

    # Agent Orchestration & Google Workspace APIs
    pip install langchain langchain-groq langchain-core google-api-python-client google-auth-httplib2 google-auth-oauthlib

   ```
3. Configure API Credentials (.env)
   Create a .env file in the root folder and add your LLM keys:
   ```bash
   GROQ_API_KEY=gsk_your_groq_api_key_here
   GEMINI_API_KEY=AIza_your_gemini_api_key_here
   ```
4. Configure Google Cloud OAuth2.0 (credentials.json)
   The Scheduling and Workflow agents require permissions to read/write Google Calendar events and poll Gmail.
   1. Go to the Google Cloud Console (https://console.cloud.google.com/)
   2. Create a project named AgentVerse-Hackathon.
   3. Enable both Google Calendar API and Gmail API under APIs & Services > Library.
      <img width="898" height="497" alt="Screenshot 2026-08-24 114757" src="https://github.com/user-attachments/assets/b6e207d1-496a-4ff2-be74-93401347244f" />
   5. Configure the OAuth Consent Screen:
        Set User Type to External
      <img width="627" height="486" alt="Screenshot 2026-08-24 115140" src="https://github.com/user-attachments/assets/d1dfb1d9-1edd-498a-8129-fb3a3460db29" />
        Add your personal Gmail under Test Users.
   7. Navigate to Credentials > Create Credentials > OAuth client ID.
        Application Type: Desktop App
   8. Download the client secrets JSON, rename it to credentails.json, and place it in the project root directory

5. Understanding Google OAuth2 Authentication & token.json
   Because there is no web UI, everything runs directly in your terminal. When launching the project for the first time, token.json will not exist.
  -What is token.json?
  It is locally generated security badge containing temporary access and refresh tokens. It securely allows the Python agents to query Google APIs on your behalf without prompting a browser login on every single execution.
   -The "Google hasn't verified this app" Screen:
   When you trigger Mode 1,2, or 3 for the first time, a browser window will open asking you to authenticate. Because your Google Cloud project is in personal development/testing status, Google presents an unverified app warning. This is completely safe to bypass for your own local code.
     -Click Continue (or Advanced > Go to AgentVerse-Hackathon (unsafe)).
     -On the permissions screen, select all checkboxes granting access to both Google Calendar and Gmail.
     -Click Continue until the browser window displays "The authentication flow has completed. You may close this window."
   <img width="940" height="382" alt="image" src="https://github.com/user-attachments/assets/cd6f302c-1483-483f-9945-36626f86e318" />
   -Revoking or Resetting Tokens:
   Deleting token.json removes the local session key and forces a fresh OAuth login on the next run.

6. Running the Application
   terminal orchestrator (main.py)
   ```bash
   python main.py
   ```
   Startup Notice-Please Be Patient:
   Startup Notice - Please Be Patient:
    Launching main.py takes time to load. During startup, Agent 3 (Knowledge Agent) must load the       Hugging Face embedding model (sentence-transformers/all-MiniLM-L6-v2) locally, parse your study     documents in data/study_materials/, and build the Vector Index in memory. Once initialization finishes, the main terminal menu appears
   <img width="1088" height="792" alt="image" src="https://github.com/user-attachments/assets/0175a5a1-fc8f-4a36-a8d1-80dd759b383e" />
   user.json file tells about the specific user's profile/lifestyle
   <img width="986" height="602" alt="image" src="https://github.com/user-attachments/assets/005e0778-ab9a-400d-a1e4-ec1a3e040832" />


8. Operational Modes & Verification Guide
   -Mode 1: Direct Task Scheduling(Agent 1)
   Directly schedule tasks using natural language. Agent 1 audits existing calendar events and injects the new task into a conflict-free slot while respecting profile constraints (curfews, meal windows).
     -Trigger: Type 1, then enter a task description:
       ```bash
         Complete OS Lab assignment for 2 hours this evening
       ```
     -Terminal Flow: The agent outputs its reasoning, conflict checks, and event creation link.
     -Tool Verification: Open Google Calendar in your browser to verify the block was created at the allocated time.
     -The Goal of this agent: When you have so many tasks in your mind, don't know when and how to schedule them, don't remember your current schedule, you just give it a prompt "It's a college leave day, buy fruits in market and design a poster and get design approval from incharge faculty, wash clothes". The thing is user.json knows about you, what kind of a person you are, what environment you are living and so and so. So the agents sends both your task prompt query along with your user.json. So the LLM sees that the hostel_curfew_time is 05.00PM, outside_movement_allowed_window is 08:30 AM-05:00 PM so i can't schedule buying fruits outside this time window.
   
    -Mode 2: Paste Email/Message Extraction(Agent 2->Agent 1)
   Parse messy, unstructured text. Agent 2 extracts structured intents, task names, and estimated durations, handing them off to Agent 1 for automated calendar placement.
     -Trigger: Type 2, then paste raw communication text:
       ```bash
         > 📢 Opportunity to participate in Pep Sales Stars 2026! Apply Here before weekend...
       ```
     -Terminal Flow: Agent 2 parses the text, extracts the actionable task, and Agent 1 schedules it.
     -Tool Verification: Check your Google Calendar to confirm the registration block is booked.
     -The Goal of this agent: agent 2 simply parses the text and calls agent 1 to schedule the task of "hackathon registration".
   
    -Mode 3: Autonomous Background Monitor (Live Inbox)
   Runs a continuous loop polling your Gmail inbox for unread messages. It filters spam, extracts academic/career tasks, schedules them, and marks the emails as read.
     -Trigger: Type 3. (Press Ctrl+C to stop monitoring)
     -Terminal Flow: Terminal Flow: The agent pings the Gmail API, processes unread messages, extracts tasks, and updates the calendar.
     -Tool Verification:
         -Open Gmail and verify processed emails are marked as read.
         -Open Google Calendar and verify newly detected tasks appear
     -The Goal of this agent: When your email is loaded with Unstop, internshala, devfolio, devpost hackathon register email, you get worried, frustrated to check your inbox, even clicking the email becomes frustrating. Mode 3 runs on a loop, every time taking 5 unread email and parses them each for words like "Register", "apply", "complete" then calls agent 1 in action to schedule that register as a task in calendar.
      -Mode 4: Knowledge Agent/ Study Mode (Agent 3 - RAG)
   A deterministic academic tutor powered by LlamaIndex and local Hugging Face embeddings. It answers technical subject queries grounded strictly in local documents.
     -Trigger: Type 4, then enter your subject question:
       ```bash
        explain kurtosis with an analogy
       ```
     -Terminal Flow: The agent executes semantic search across indexed chunks and synthesizes an answer directly in the terminal. Type back to return to the menu.
     -The Goal of this agent: Your tutor/faculty mailed you that you are having a test on course Data Science's Normal distribution and pandas, Skewness and Kurtosis. Your Mode 3 takes that study email, parses and sends it to agent 1 for scheduling a study task in your calendar. Agent 3 in actions, reads your calendar that there is a study task scheduled, so i should go to google classroom to download those topic's resources(Normal_distribution.txt,Pandas_Describe_Final_With_Skewness_Kurtosis.txt) download them and store it inside data/study_materials. so even before you sit to complete that study task, your agent gets you ready with the necessary documents, you just prompt your question directly in the terminal, agent 3 sends those downloaded resources to the LLM along ith your question for reasoning. This is just like notebookLM, chatgpt when you use it for studying. But when you sit to study, you realise that you haven't downloaded those 10-15 files, that might seems frustrating. Also a LLM's generic answer is not preferred over context-resources supplied answers.
   Current agent 3 does not hooked to google classroom or email, data/study_materials contains static files that are need to be supplied to the LLM for data science related questions.
   -Mode 5: Dynamic Fitness Coach (Agent 4- Tool Calling)
   A contextual workout coach built with pure LangChain Expression Language (LCEL). It recalculates exercise routines based on real-time constraints and triggers physical timers.
     -Trigger: Type 5, then enter constraints:
       ```bash
         1. I'm exhausted. Give me a 45-second timer for a quick stretch using the run_timer tool.
         2. I had tamarind rice for lunch, my stomach feels bloated, but i don't want to skip my workout schedule today.
       ```
     -Terminal Flow: Agent 4 adapts the prescription and executes the OS-level system timer tool.
     -Tool Verification: When the timer reaches 0, the Python winsound engine will emit a physical, audible 1000Hz alert tone through your computer speakers.
     -The Goal of this agent: Let's say your are full on your biriyani you had at 2 pm, now it's 4.30pm, you still feel bloated, but you don't want to skip your workout today. A normal workout schedule app, doesn't capture your perception that you had biriyani, so giving intense running sessions might cause you irritation, vomiting sensation. A static workout schedule app doesn't knows this, also going to an AI and asking for workout according to your perception is possible but involves tool switching(timer, LLM, image generation). sometime you don't understand the words given by AI(Alternating Reverse Lunges, seated incline bicep curls), so you might need an image that clearly shows the exercise preferred by the LLM. so in-order reduce tool switching time this agent 4 works in action with pregenerated_Exercises fed into the LLM along with your current health perception to suggest pregenerated_Exercise and starts up a quick timer.
