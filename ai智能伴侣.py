import os
from openai import OpenAI
import streamlit as st
#创建与ai大模型进行交互的客户端对象
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")
#与ai大模型进行交互
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)
#打印ai大模型的回复
print(response.choices[0].message.content)