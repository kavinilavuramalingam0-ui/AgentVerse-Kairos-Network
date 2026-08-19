Markdown# The Kairos Network: Autonomous Multi-Agent Orchestrator

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
Directory StructureWhen cloning this repository from GitHub, secret configuration files (.env, credentials.json, token.json) are excluded via .gitignore for security. Your local folder will look like this:PlaintextAgentVerse_Project/
├── agents/
│   ├── fitness_agent/        # Agent 4: Dynamic Fitness Coach & LCEL tool bindings
│   ├── knowledge_agent/      # Agent 3: LlamaIndex RAG Knowledge Agent
│   ├── scheduling_agent/     # Agent 1: Time-Aware Spatial-Temporal Scheduler
│   └── workflow_agent/       # Agent 2: Unstructured Communication & Intent Extractor
├── core/
│   └── llm_client.py         # Resilient multi-provider client (Groq / Google GenAI)
├── data/
│   ├── gym/                  # Visual aids for dynamic physical routines
│   ├── study_materials/      # Source documents (.txt/.pdf) for RAG indexing
│   └── user_profile.json     # Persistent stateful memory (curfews, meal windows)
├── tools/
│   ├── calendar_tool.py      # Google Calendar API read/write bindings
│   ├── gmail_tool.py         # Gmail API inbox monitor & query tools
│   └── timer_tool.py         # OS-level hardware beep countdown timer
├── .env                      # [USER CREATED] API keys
├── credentials.json          # [USER PROVIDED] Google Cloud OAuth 2.0 Desktop Client
├── token.json                # [AUTO GENERATED] Cached OAuth2 session badge
├── requirements.txt          # Python dependencies
└── main.py                   # Main CLI Entry Point & Multi-Agent Loop
Installation & Setup1. Clone the RepositoryBashgit clone [https://github.com/your-username/AgentVerse_Project.git](https://github.com/your-username/AgentVerse_Project.git)
cd AgentVerse_Project
2. Install Required DependenciesRun the following package installations in your Python environment:Bash# Core LLM, schema validation, and environment variables
pip install groq google-genai python-dotenv pydantic

# Knowledge Base & Vector Embeddings
pip install llama-index llama-index-readers-file llama-index-llms-groq llama-index-embeddings-huggingface

# Agent Orchestration & Google Workspace APIs
pip install langchain langchain-groq langchain-core google-api-python-client google-auth-httplib2 google-auth-oauthlib
3. Configure API Credentials (.env)Create a .env file in the root folder and add your LLM keys:Ini, TOMLGROQ_API_KEY=gsk_your_groq_api_key_here
GEMINI_API_KEY=AIza_your_gemini_api_key_here
4. Configure Google Cloud OAuth 2.0 (credentials.json)The Scheduling and Workflow agents require permissions to read/write Google Calendar events and poll Gmail.Go to the Google Cloud Console.Create a project named AgentVerse-Hackathon.Enable both Google Calendar API and Gmail API under APIs & Services > Library.Configure the OAuth Consent Screen:Set User Type to External.Add scopes: .../auth/calendar.events and .../auth/gmail.modify.Add your personal Gmail under Test Users.Navigate to Credentials > Create Credentials > OAuth client ID.Application Type: Desktop App.Download the client secrets JSON, rename it to credentials.json, and place it in the project root directory.Understanding Google OAuth2 Authentication & token.jsonBecause there is no web UI, everything runs directly in your terminal. When launching the project for the first time, token.json will not exist.What is token.json?It is a locally generated security badge containing temporary access and refresh tokens. It securely allows your Python agents to query Google APIs on your behalf without prompting a browser login on every single execution.The "Google hasn't verified this app" Screen:When you trigger Mode 1, 2, or 3 for the first time, a browser window will open asking you to authenticate. Because your Google Cloud project is in personal development/testing status, Google presents an unverified app warning. This is completely safe to bypass for your own local code.Click Continue (or Advanced > Go to AgentVerse-Hackathon (unsafe)).On the permissions screen, select all checkboxes granting access to both Google Calendar and Gmail.Click Continue until the browser window displays "The authentication flow has completed. You may close this window."Revoking or Resetting Tokens:Deleting token.json removes the local session key and forces a fresh OAuth login on the next run.Running the ApplicationExecute the terminal orchestrator:Bashpython main.py
Startup Notice - Please Be Patient:Launching main.py takes time to load. During startup, Agent 3 (Knowledge Agent) must load the Hugging Face embedding model (sentence-transformers/all-MiniLM-L6-v2) locally, parse your study documents in data/study_materials/, and build the Vector Index in memory. Once initialization finishes, the main terminal menu appears.Plaintext===================================================
  The Kairos Network: MULTI-AGENT ORCHESTRATOR     
===================================================
Enter User Name: Kavinilavu
[System] Initializing Agent 3 (Knowledge & RAG)...
[System] Reading raw study materials into memory...
[System] Successfully loaded 2 document chunks. Building Vector Index...
[System] Knowledge Agent is ready to answer questions.
[System] Initializing Agent 4 (Dynamic Fitness Coach via Core LCEL)...

---------------------------------------------------
Choose Mode:
1. Direct Task
2. Paste Email (Manual Extract)
3. AUTONOMOUS BACKGROUND MONITOR (Live Inbox)
4. ASK KNOWLEDGE AGENT (Study Mode)
5. FITNESS COACH (Dynamic Workout)
Type 'exit' to quit.
>
Operational Modes & Verification GuideMode 1: Direct Task Scheduling (Agent 1)Directly schedule tasks using natural language. Agent 1 audits existing calendar events and injects the new task into a conflict-free slot while respecting profile constraints (curfews, meal windows).Trigger: Type 1, then enter a task description:Plaintext> Complete OS Lab assignment for 2 hours this evening
Terminal Flow: The agent outputs its reasoning, conflict checks, and event creation link.Tool Verification: Open Google Calendar in your browser to verify the block was created at the allocated time.Mode 2: Paste Email / Message Extraction (Agent 2 $\rightarrow$ Agent 1)Parse messy, unstructured text. Agent 2 extracts structured intents, task names, and estimated durations, handing them off to Agent 1 for automated calendar placement.Trigger: Type 2, then paste raw communication text:Plaintext> 📢 Opportunity to participate in Pep Sales Stars 2026! Apply Here before weekend...
Terminal Flow: Agent 2 parses the text, extracts the actionable task, and Agent 1 schedules it.Tool Verification: Check your Google Calendar to confirm the registration block is booked.Mode 3: Autonomous Background Monitor (Live Inbox)Runs a continuous loop polling your Gmail inbox for unread messages. It filters spam, extracts academic/career tasks, schedules them, and marks the emails as read.Trigger: Type 3. (Press Ctrl + C to stop monitoring).Terminal Flow: The agent pings the Gmail API, processes unread messages, extracts tasks, and updates the calendar.Tool Verification:Open Gmail and verify processed emails are marked as read.Open Google Calendar and verify newly detected tasks appear.Mode 4: Knowledge Agent / Study Mode (Agent 3 - RAG)A deterministic academic tutor powered by LlamaIndex and local Hugging Face embeddings. It answers technical subject queries grounded strictly in local documents.Trigger: Type 4, then enter your subject question:Plaintext> explain kurtosis with an analogy
Terminal Flow: The agent executes semantic search across indexed chunks and synthesizes an answer directly in the terminal. Type back to return to the menu.Mode 5: Dynamic Fitness Coach (Agent 4 - Tool Calling)A contextual workout coach built with pure LangChain Expression Language (LCEL). It recalculates exercise routines based on real-time constraints and triggers physical timers.Trigger: Type 5, then enter constraints:Plaintext> I'm exhausted. Give me a 45-second timer for a quick stretch using the run_timer tool.
Terminal Flow: Agent 4 adapts the prescription and executes the OS-level system timer tool.Tool Verification: When the timer reaches 0, the Python winsound engine will emit a physical, audible 1000Hz alert tone through your computer speakers.
