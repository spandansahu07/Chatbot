import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

print("🔁 Loading environment variables...")
api_key = os.getenv("GROQ_API_KEY")
print("🔑 Loaded API Key:", api_key)




if not api_key:
    print("❌ Error: GROQ_API_KEY not found in .env file!")
    exit()

print("✅ API Key loaded successfully.")
print("🤖 Groq AI Terminal Chatbot (type 'exit' to quit)")

# Groq API config (using free model)
url = "https://api.groq.com/openai/v1/chat/completions"
model = "llama3-8b-8192"  # Free model
messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("👋 Goodbye!")
        break

    messages.append({"role": "user", "content": user_input})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        ai_message = response.json()["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ai_message})
        print("AI:", ai_message)
    except Exception as e:
        print("❌ API call failed:", e)
