
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)

model = "gemini-3.5-flash-lite"

# Conversation history
messages = []

# General instruction
instruction = "You are a helpful chatbot. Answer clearly and naturally."

while True:
    prompt = input("You: ")

    if prompt.lower() in ["exit", "quit"]:
        break

    # Add the user's message
    messages.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    # Start streaming
    stream = client.models.generate_content_stream(
        model=model,
        contents=messages,
        config={
            "system_instruction": instruction
        }
    )

    # Print chunks as they arrive and collect the full answer
    print("Bot: ", end="", flush=True)
    answer_parts = []

    for chunk in stream:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            answer_parts.append(chunk.text)

    print()

    # Save the complete response for the next turn
    answer = "".join(answer_parts)
    messages.append({
        "role": "model",
        "parts": [{"text": answer}]
    })
