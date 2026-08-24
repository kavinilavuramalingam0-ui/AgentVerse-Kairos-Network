### The Kairos Network: Autonomous Multi-Agent Orchestrator

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Framework-LangChain](https://img.shields.io/badge/Framework-LangChain-orange.svg)](https://www.langchain.com/)
[![RAG-LlamaIndex](https://img.shields.io/badge/RAG-LlamaIndex-purple.svg)](https://www.llamaindex.ai/)
[![Inference-Groq_LPU](https://img.shields.io/badge/Inference-Groq_LPU-red.svg)](https://groq.com/)
[![Tools-Google_Workspace](https://img.shields.io/badge/Tools-Calendar_%26_Gmail_API-green.svg)](https://workspace.google.com/)

An autonomous personal AI companion and event-driven multi-agent ecosystem built from first principles for the **AgentVerse Hackathon**. **The Kairos Network** coordinates four specialized reasoning agents inside an interactive, unified terminal workspace to handle real-world spatial-temporal scheduling, inbound email intent extraction, deterministic academic tutoring (RAG), and dynamic physical workout execution.

---

### System Architecture

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
### Directory Structure<br>
<img width="613" height="761" alt="image" src="https://github.com/user-attachments/assets/376c7c68-22bf-458e-ade7-a956e4c0aae8" />

### Installation & Setup<br>
## 1. Clone the Repository
   ```bash
   git clone https://github.com/kavinilavuramalingam0-ui/AgentVerse-Kairos-Network.git
   cd AgentVerse-Kairos-Network
   ```
   <br>
   
## 2. Install Required Dependencies<br>
   Run the following package installations in your Python environment:
   
   ```bash
    #Core LLM, schema validation, and environment variables
    pip install groq google-genai python-dotenv pydantic

    # Knowledge Base & Vector Embeddings
    pip install llama-index llama-index-readers-file llama-index-llms-groq llama-index-embeddings-huggingface

    # Agent Orchestration & Google Workspace APIs
    pip install langchain langchain-groq langchain-core google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
<br>

## 3. Configure API Credentials (.env)<br>
   Create a .env file in the root folder and add your LLM keys:
   
   ```bash
   GROQ_API_KEY=gsk_your_groq_api_key_here
   GEMINI_API_KEY=AIza_your_gemini_api_key_here
   ```
<br>

## 4. Configure Google Cloud OAuth 2.0 (`credentials.json`)

The Scheduling and Workflow agents require permissions to read/write Google Calendar events and poll Gmail.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project named `AgentVerse-Hackathon`.
3. Enable both the **Google Calendar API** and **Gmail API**:
   - Go to **APIs & Services → Library**.
   - Search for **Google Calendar API** and enable it.
   - Search for **Gmail API** and enable it.
4. Configure the OAuth consent screen:
   - Go to **APIs & Services → OAuth consent screen**.
   - Configure the required application details.
   - Add the required Google Calendar and Gmail scopes.
5. Create OAuth credentials:
   - Go to **APIs & Services → Credentials**.
   - Click **Create Credentials → OAuth client ID**.
   - Select the appropriate application type.
   - Download the generated `credentials.json`.
   - Place `credentials.json` in the required project folder.

## 5. First-Time Authentication

On the first run of the project, `token.json` will not exist.

- **What is `token.json`?**  
  It is a locally generated security badge containing temporary access and refresh tokens. It securely allows your Python agents to query Google APIs on your behalf without prompting a browser login on every single execution.

- **The "Google hasn't verified this app" Screen**  
  When you trigger the Scheduling or Workflow agents for the first time, a browser window will open asking you to authenticate. Because your Google Cloud project is in personal development/testing status, Google may present an unverified app warning. This is expected for local development.

  1. Click **Continue** (or **Advanced → Go to AgentVerse-Hackathon (unsafe)**).
  2. On the permissions screen, select all checkboxes granting access to both **Google Calendar** and **Gmail**.
  3. Click **Continue** until the browser window displays **"The authentication flow has completed."**
  4. You may close the browser window.

## 6. Revoking or Resetting Tokens

Deleting `token.json` removes the local session key and forces a fresh OAuth login on the next run.

## 7. Running the Application<br>

   terminal orchestrator (main.py)<br>
   ```bash
   python main.py
   ```
<br>
        Startup Notice-Please Be Patient:<br>
                Launching main.py takes time to load. During startup, Agent 3 (Knowledge Agent) must load the Hugging Face embedding model (sentence-transformers/all-MiniLM-L6-v2) locally, parse your study documents in data/study_materials/, and build the Vector Index in memory. Once initialization finishes, the main terminal menu appears.<br>
   <img width="1088" height="792" alt="image" src="https://github.com/user-attachments/assets/0175a5a1-fc8f-4a36-a8d1-80dd759b383e" /><br>
         user.json file tells about the specific user's profile/lifestyle<br>
   <img width="986" height="602" alt="image" src="https://github.com/user-attachments/assets/005e0778-ab9a-400d-a1e4-ec1a3e040832" /><br>


8. Operational Modes & Verification Guide<br>
        Mode 1: Direct Task Scheduling(Agent 1)<br>
               Directly schedule tasks using natural language. Agent 1 audits existing calendar events and injects the new task into a conflict-free slot while respecting profile constraints (curfews, meal windows).<br>
               Trigger: Type 1, then enter a task description:<br>
               ```bash
                 Complete OS Lab assignment for 2 hours this evening
               ```
               <br>
             Terminal Flow: The agent outputs its reasoning, conflict checks, and event creation link.<br>
             Tool Verification: Open Google Calendar in your browser to verify the block was created at the allocated time.<br>
             The Goal of this agent: When you have so many tasks in your mind, don't know when and how to schedule them, don't remember your current schedule, you just give it a prompt "It's a college leave day, buy fruits in market and design a poster and get design approval from incharge faculty, wash clothes". The thing is user.json knows about you, what kind of a person you are, what environment you are living and so and so. So the agents sends both your task prompt query along with your user.json. So the LLM sees that the hostel_curfew_time is 05.00PM, outside_movement_allowed_window is 08:30 AM-05:00 PM so i can't schedule buying fruits outside this time window.<br>
     <img width="1917" height="886" alt="image" src="https://github.com/user-attachments/assets/947ba9e8-7b23-4c1c-8fa8-72271ab567b3" />
   <br><br>
        Mode 2: Paste Email/Message Extraction(Agent 2->Agent 1)<br>
               Parse messy, unstructured text. Agent 2 extracts structured intents, task names, and estimated durations, handing them off to Agent 1 for automated calendar placement.<br>
               Trigger: Type 2, then paste raw communication text:<br>
               ```bash
                 > 📢 Opportunity to participate in Pep Sales Stars 2026! Apply Here before weekend...
               ```
               <br>
               Terminal Flow: Agent 2 parses the text, extracts the actionable task, and Agent 1 schedules it.<br>
               Tool Verification: Check your Google Calendar to confirm the registration block is booked.<br>
               The Goal of this agent: agent 2 simply parses the text and calls agent 1 to schedule the task of "hackathon registration".<br>
     <img width="1917" height="911" alt="image" src="https://github.com/user-attachments/assets/c29c8212-bb23-4bf0-b1aa-aa257da5643c" /><br>
     <img width="1917" height="922" alt="image" src="https://github.com/user-attachments/assets/c721fcea-5315-452a-855b-9d807f782ae4" /><br>
     <img width="1917" height="916" alt="image" src="https://github.com/user-attachments/assets/f6a2476b-9635-402b-b321-3c67ab25f0d0" /><br>
     <img width="1917" height="918" alt="image" src="https://github.com/user-attachments/assets/50087072-b111-4099-afd1-4b6cb85bb4a4" /><br>
   <br><br>
        Mode 3: Autonomous Background Monitor (Live Inbox)<br>
               Runs a continuous loop polling your Gmail inbox for unread messages. It filters spam, extracts academic/career tasks, schedules them, and marks the emails as read.<br>
               Trigger: Type 3. (Press Ctrl+C to stop monitoring)<br>
               Terminal Flow: Terminal Flow: The agent pings the Gmail API, processes unread messages, extracts tasks, and updates the calendar.<br>
               Tool Verification:<br>
                       Open Gmail and verify processed emails are marked as read.<br>
                       Open Google Calendar and verify newly detected tasks appear.<br>
               The Goal of this agent: When your email is loaded with Unstop, internshala, devfolio, devpost hackathon register email, you get worried, frustrated to check your inbox, even clicking the email becomes frustrating. Mode 3 runs on a loop, every time taking 5 unread email and parses them each for words like "Register", "apply", "complete" then calls agent 1 in action to schedule that register as a task in calendar.<br>
     <img width="1917" height="912" alt="image" src="https://github.com/user-attachments/assets/00c0083a-8dfa-4045-9fa7-71e7c711609a" /><br>
     <img width="1917" height="907" alt="image" src="https://github.com/user-attachments/assets/89408df9-7e01-4559-b325-d6266b9d6f1b" /><br>
     <img width="967" height="1010" alt="image" src="https://github.com/user-attachments/assets/229f1a4d-478c-4c6c-bd5f-cfd18c055bc8" /><br>
     <br><br>
        Mode 4: Knowledge Agent/ Study Mode (Agent 3 - RAG)<br>
               A deterministic academic tutor powered by LlamaIndex and local Hugging Face embeddings. It answers technical subject queries grounded strictly in local documents.<br>
               Trigger: Type 4, then enter your subject question:<br>
               ```bash
                explain kurtosis with an analogy
               ```
               <br>
               Terminal Flow: The agent executes semantic search across indexed chunks and synthesizes an answer directly in the terminal. Type back to return to the menu.<br>
               The Goal of this agent: Your tutor/faculty mailed you that you are having a test on course Data Science's Normal distribution and pandas, Skewness and Kurtosis. Your Mode 3 takes that study email, parses and sends it to agent 1 for scheduling a study task in your calendar. Agent 3 in actions, reads your calendar that there is a study task scheduled, so i should go to google classroom to download those topic's resources(Normal_distribution.txt,Pandas_Describe_Final_With_Skewness_Kurtosis.txt) download them and store it inside data/study_materials. so even before you sit to complete that study task, your agent gets you ready with the necessary documents, you just prompt your question directly in the terminal, agent 3 sends those downloaded resources to the LLM along ith your question for reasoning. This is just like notebookLM, chatgpt when you use it for studying. But when you sit to study, you realise that you haven't downloaded those 10-15 files, that might seems frustrating. Also a LLM's generic answer is not preferred over context-resources supplied answers.<br>
               Current agent 3 does not hooked to google classroom or email, data/study_materials contains static files that are need to be supplied to the LLM for data science related questions.<br>
   <img width="1887" height="927" alt="image" src="https://github.com/user-attachments/assets/560f39c8-f642-46a0-831b-187e92449498" /><br>
   <br><br>
       Mode 5: Dynamic Fitness Coach (Agent 4- Tool Calling)<br>
               A contextual workout coach built with pure LangChain Expression Language (LCEL). It recalculates exercise routines based on real-time constraints and triggers physical timers.<br>
               Trigger: Type 5, then enter constraints:<br>
               ```bash
                 1. I'm exhausted. Give me a 45-second timer for a quick stretch using the run_timer tool.
                 2. I had tamarind rice for lunch, my stomach feels bloated, but i don't want to skip my workout schedule today.
               ```
               <br>
               Terminal Flow: Agent 4 adapts the prescription and executes the OS-level system timer tool.<br>
               Tool Verification: When the timer reaches 0, the Python winsound engine will emit a physical, audible 1000Hz alert tone through your computer speakers.<br>
               The Goal of this agent: Let's say your are full on your biriyani you had at 2 pm, now it's 4.30pm, you still feel bloated, but you don't want to skip your workout today. A normal workout schedule app, doesn't capture your perception that you had biriyani, so giving intense running sessions might cause you irritation, vomiting sensation. A static workout schedule app doesn't knows this, also going to an AI and asking for workout according to your perception is possible but involves tool switching(timer, LLM, image generation). sometime you don't understand the words given by AI(Alternating Reverse Lunges, seated incline bicep curls), so you might need an image that clearly shows the exercise preferred by the LLM. so in-order reduce tool switching time this agent 4 works in action with pregenerated_Exercises fed into the LLM along with your current health perception to suggest pregenerated_Exercise and starts up a quick timer.<br>
     <img width="1881" height="903" alt="image" src="https://github.com/user-attachments/assets/cd339d51-a213-449d-8c55-e218e69a204f" /><br>
     <img width="1486" height="957" alt="image" src="https://github.com/user-attachments/assets/9fec4523-f24c-42f9-aae0-9e98e9e61ae4" /><br>
     <img width="942" height="1000" alt="image" src="https://github.com/user-attachments/assets/aef65d2d-2d1a-43f0-813c-6019b71f49c6" /><br>
     <img width="958" height="1003" alt="image" src="https://github.com/user-attachments/assets/59897df1-f177-4aa5-b63b-fe83842842e5" /><br>
     <img width="961" height="813" alt="image" src="https://github.com/user-attachments/assets/04cb486c-8f33-4e44-9170-2231acf31d6c" /><br>
     <img width="971" height="997" alt="image" src="https://github.com/user-attachments/assets/3d61744a-dd34-417d-8a92-457d5d99799b" /><br>
     <br>
