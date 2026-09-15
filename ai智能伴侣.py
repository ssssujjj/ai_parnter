import streamlit as st
import os
from openai import OpenAI
#设置页面的配置项
st.set_page_config(
    page_title="ai智能伴侣",
    page_icon="🧊",
    #布局
    layout="wide",
    #侧边栏
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
#设置页面标题和图标
st.title("ai智能伴侣")
st.logo(".venv/资源/screen.png")

#初始化聊天信息（把聊天信息保存起来，令旧会话不会被新会话覆盖）
if "messages" not in st.session_state:
    st.session_state.messages = []

#展示聊天信息
for message in st.session_state.messages:  #{'role': 'user', 'content': 'prompt'}
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # elif message["role"] == "assistant":
    #     st.chat_message("assistant").write(message["content"])

#设置系统提示词
system_prompt = "你是一名历史老师，性格和蔼可亲"

#创建与ai大模型进行交互的一个客户端对象
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#创建一个输入框（用户输入问题的地方）
prompt = st.chat_input('请输入您的问题')
if prompt:   #字符串会自动转换为布尔值，非空字符串为True，空字符串为False
    st.chat_message('user').write(prompt)
    print('------>调用ai大模型,提示词:',prompt)
    #保存用户输入的提示词
    st.session_state.messages.append({"role": "user", "content": prompt})

#调用大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
           {"role": "system", "content": system_prompt},
           {"role": "user", "content":prompt},
    ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    #输出大模型的回复
    print('------>ai大模型的回复:',response.choices[0].message.content)
    st.chat_message('assistant').write(response.choices[0].message.content)
    #保存大模型的回复
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
print('my second commit')
