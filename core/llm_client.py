import os
from dotenv import load_dotenv
from groq import Groq
from google import genai

# Load credentials from .env file
load_dotenv()

class ResilientLLMClient:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        
        self.groq_client = Groq(api_key=self.groq_key) if self.groq_key else None
        self.gemini_client = genai.Client(api_key=self.gemini_key) if self.gemini_key else None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        # Primary Engine: Groq LPU
        if self.groq_client:
            try:
                response = self.groq_client.chat.completions.create(
                    model= "qwen/qwen3.6-27b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2
                )
                return f"[Source: Groq LPU]\n{response.choices[0].message.content}"
            except Exception as e:
                print(f"[Fallback Warning] Groq API unavailable ({e}). Switching to Gemini...")

        # Fallback Engine: Google Gemini 2.5 Flash
        if self.gemini_client:
            try:
                full_prompt = f"System: {system_prompt}\nUser Input: {user_prompt}"
                response = self.gemini_client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=full_prompt
                )
                return f"[Source: Google Gemini]\n{response.text}"
            except Exception as e:
                return f"[Execution Error] Both APIs failed. Details: {e}"

        return "[Error] No valid API keys found in environment variables."

# Execution Block (Tells Python to actually run and print)
if __name__ == "__main__":
    client = ResilientLLMClient()
    print("--- Sending Test Request to Cloud LLM ---")
    output = client.generate(
        system_prompt="You are an expert Hackathon Mentor Agent.",
        user_prompt="Confirm if the multi-provider LLM connection is active."
    )
    print("--- Response Received ---")
    print(output)