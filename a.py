import os
from openai import OpenAI

client = OpenAI(

    api_key=os.getenv("GROQ_API_KEY"),

    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(

    model="llama-3.1-8b-instant",

    messages=[

        {
            "role": "user",
            "content": "hello"
        }
    ]
)

print(
    response.choices[0].message.content
)
