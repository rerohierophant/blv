from openai import OpenAI
import os


def result(order, img_url, desc):
    # desc = "What’s in this image?"
    client = OpenAI(
        api_key="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",
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": order},
                    {"type": "text", "text": desc},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_url,
                        },
                    },
                ],
            }
        ],
        model="gpt-4-vision-preview",
        max_tokens=50,
    )
    return chat_completion.choices[0].message.content

