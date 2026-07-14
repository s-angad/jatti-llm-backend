import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEYgsk_94xdTV1pcNXcmevkeFlQWGdyb3FYYdRP4k9Azc83KwqU1Gw0b1uI"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Say hello!"
        }
    ]
)

print(response.choices[0].message.content)