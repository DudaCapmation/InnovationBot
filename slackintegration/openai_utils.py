import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_openai_response (message: str, system_prompt: str) -> str:
    # Gets a response from OpenAI

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.2,
        max_tokens=512
    )

    return response.choices[0].message.content