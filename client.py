'''from openai import OpenAI

client = OpenAI(
    api_key = "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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a virtual assistant named siri skilled in general tasks like Alexa and Google Cloud"},
    {"role": "user", "content": "what is coding"}
  ]
)

print(completion.choices[0].message.content)
'''

import g4f
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()

def speak(text):
    print("AI:", text)   # show on screen
    engine.say(text)     # speak aloud
    engine.runAndWait()

def ask_ai(prompt: str) -> str:
    """Send a prompt to free g4f AI and return response."""
    try:
        response = g4f.ChatCompletion.create(
            model="gpt-4o-mini",  
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    question = input("Ask your question: ")
    answer = ask_ai(question)
    speak(answer)


