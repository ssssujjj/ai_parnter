import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json

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

#保存会话信息
def save_session():
    # 1.保存当前会话信息
    if st.session_state.session_id:
        # 构建新的会话对象
        session = {
            "session_id": st.session_state.session_id,
            "name": st.session_state.name,
            "character": st.session_state.character,
            "messages": st.session_state.messages
        }
        with open(f".venv/资源/{st.session_state.session_id}.json", "w", encoding="utf-8") as f:
            json.dump(session, f, ensure_ascii=False, indent=4)

#加载所有的会话列表信息
def load_sessions():
    session_list = []
    #加载资源目录下的json文件
    file_list = os.listdir(".venv/资源")
    for file_name in file_list:
        if file_name.endswith(".json"):
            session_list.append(file_name[:-5])  # 去掉.json后缀
    return session_list

#加载指定的历史会话信息
def load_session(session_id):
    try:
        if os.path.exists(f".venv/资源/{session_id}.json"):
            #读取会话数据
            with open(f".venv/资源/{session_id}.json", "r", encoding="utf-8") as f:
                session = json.load(f)
                st.session_state.session_id = session["session_id"]
                st.session_state.name = session["name"]
                st.session_state.character = session["character"]
                st.session_state.messages = session["messages"]
    except Exception as e:
        st.error(f"加载会话出错：{e}")

#初始化聊天信息（把聊天信息保存起来，令旧会话不会被新会话覆盖）
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "name" not in st.session_state:
    st.session_state.name = "小曦"
#性格
if "character" not in st.session_state:
    st.session_state.character = "温柔可爱的南方姑娘"
#会话标识(获取当前时间作为会话的标识)
if "session_id" not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#展示聊天信息
for message in st.session_state.messages:  #{'role': 'user', 'content': 'prompt'}
    st.chat_message(message["role"]).write(message["content"])
    # if message["role"] == "user":
    #     st.chat_message("user").write(message["content"])
    # elif message["role"] == "assistant":
    #     st.chat_message("assistant").write(message["content"])

#设置系统提示词
system_prompt = """
      你叫%s，是用户的智能伴侣，请完全代入该角色
      规则:
      1.每次只回一条消息
      2.匹配用户的语言
      3.回复简短，像微信聊天一样
      4.用符合伴侣性格的方式回复
      5.回复方式，要充分体现伴侣的性格特征
      性格:
         %s
      你必须严格按照上述规则来回复
  """

#创建左侧边栏  with:streamlit中上下文管理器
with st.sidebar:
    #会话信息
    st.subheader('ai智能伴侣')
    #新建会话按钮
    if st.button('新建会话',width='stretch'):
        save_session()

        #2.创建新会话
        if st.session_state.messages:  #如果聊天信息非空为True;反之为False
          st.session_state.session_id = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
          st.session_state.messages = []
          save_session()
          st.rerun()    #重新运行当前页面

    #历史会话
    st.text('历史会话')
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            #加载会话信息
            if st.button(session,width='stretch',key=f'load_{session}'):
                load_session(session)
                st.rerun()
        with col2:
            #删除会话信息
            if st.button('',width='stretch',key=f'delete_{session}'):
                pass

    st.subheader('伴侣信息')
    #创建一个输入框，让用户输入伴侣的名字和性格特征
    name = st.text_input('名字',placeholder='请输入伴侣的名字',value = st.session_state.name)  #placeholder:输入框为空时,显示的提示文字  value是输入定义的默认值
    if name:
        st.session_state.name = name
    #创建一个输入框，让用户输入伴侣的性格特征
    character = st.text_area('性格',placeholder='请输入伴侣的性格特征',value = st.session_state.character)
    if character:
        st.session_state.character = character

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
           {"role": "system", "content": system_prompt % (st.session_state.name, st.session_state.character)},
           #把保存的聊天信息逐条读取出来(解包，解决会话记忆功能)
           *st.session_state.messages
    ],
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    #输出大模型的回复(非流式输出的解析方式）
    # print('------>ai大模型的回复:',response.choices[0].message.content)
    # st.chat_message('assistant').write(response.choices[0].message.content)

    #保存大模型的回复
    # st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    #输出大模型的回复(流式输出的解析方式）
    response_message = st.empty() # 创建一个空的元素来显示大模型的回复，每次都记录了ai生成的东西，新东西生成就会覆盖旧东西
    full_message = ""  # 初始化一个空字符串来保存完整的回复
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_message += content
            response_message.chat_message('assistant').write(full_message)

    #保存大模型的回复
    st.session_state.messages.append({"role": "assistant", "content": full_message})

    # 保存会话信息
    save_session()

