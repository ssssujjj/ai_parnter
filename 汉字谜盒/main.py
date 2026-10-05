from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
import json
from typing import Any
from pydantic import BaseModel

#创建fastapi实例
app = FastAPI(title="汉字谜盒")

#挂载静态文件的存放目录,/static是静态文件的访问路径,dir后边是目录名
app.mount("/static", StaticFiles(directory="static"), name="static")

#创建会话存放的目录
if not os.path.exists("./session"):
    os.mkdir("./session")

#定义会话标识
def generate_session_id():
    return "session_" + datetime.now().strftime("%Y%m%d%H%M%S")

#数据模型,定义返回的数据类型
class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any

#定义路径操作函数，处理根路径的GET请求
@app.get("/")
def root():
    print("访问项目首页")
    return FileResponse("./static/index.html")

#创建会话
@app.post("/api/sessions")
def create_session() -> ApiResponse:
    print("创建会话")
    #1.生成会话标识(名字)
    session_id = generate_session_id()
    #2.组装会话数据,保存到文件
    session_data = {
        "current_session" : session_id,
        "messages" : []
    }
    with open(f"./session/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)
    #3.返回数据
    # return {"code":200, "message":"创建会话成功", "data":session_id}
    return ApiResponse(code=200, message="创建会话成功", data=session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)