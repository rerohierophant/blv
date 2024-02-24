import openai

# 设置你的OpenAI API密钥
openai.api_key = '你的API密钥'

# 初始化对话历史变量，用于存储对话历史
conversation_history = []

while True:
    # 获取用户输入
    user_input = input("You: ")

    # 将用户输入添加到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 调用ChatGPT API，发送对话历史，包括最新的用户输入
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 确保使用正确的模型名称
        messages=conversation_history
    )

    # 获取模型的回复，并打印
    model_reply = response.choices[0].message['content']
    print("ChatGPT:", model_reply)

    # 将模型的回复也添加到对话历史中，以便下次请求时使用
    conversation_history.append({"role": "assistant", "content": model_reply})

    # 可选：在这里添加终止循环的条件，例如特定的用户输入
    if user_input.lower() == "quit":
        break
