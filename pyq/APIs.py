from openai import OpenAI
import os

api_key = "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"
max_tokens = 50


def img_result(order, img_url, desc):
    client = OpenAI(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": order},
            {
                "role": "user",
                "content": [
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
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content


def pyq_result(order, img_urls, desc):
    client = OpenAI(
        api_key=api_key,
    )

    img_template = [
        {"type": "text", "text": desc},
    ]
    for img_url in img_urls:
        img_message = {
            "type": "image_url",
            "image_url": {"url": img_url},
        }
        img_template.append(img_message)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": order},
            {
                "role": "user",
                "content": img_template
            }
        ],
        model="gpt-4-vision-preview",
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content


def free_query(order, img_urls, desc, conversation_history):
    client = OpenAI(
        api_key=api_key,
    )

    img_template = [
        {"type": "text", "text": desc},
    ]
    for img_url in img_urls:
        img_message = {
            "type": "image_url",
            "image_url": {"url": img_url},
        }
        img_template.append(img_message)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": order},
            {
                "role": "user",
                "content": img_template
            },
            {
                "role": "user",
                "content": conversation_history
            }

        ],
        model="gpt-4-vision-preview",
        max_tokens=max_tokens,
    )
    return chat_completion.choices[0].message.content
