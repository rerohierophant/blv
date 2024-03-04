from openai import OpenAI
import os

api_key = "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"
max_tokens = 800

client = OpenAI(
    api_key=api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "你好"},
            ],
        },
    ],
    model="gpt-4-vision-preview",
    max_tokens=max_tokens,
    stream=True
)
print(chat_completion)
