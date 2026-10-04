from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
#创建fastapi实例
app = FastAPI(title="汉字谜盒")
#挂载静态文件的存放目录
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def root():
    print("访问项目首页")
    return FileResponse("./static/index.html")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)