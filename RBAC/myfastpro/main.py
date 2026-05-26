from  fastapi import FastAPI,Request
from views.tusers import users_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from apps.models import *

app = FastAPI()
app.include_router(users_router, prefix="/user")

# 挂载 static 目录
app.mount("/static", StaticFiles(directory="static"), name="static")

#数据库
register_tortoise(
    app,
    config=TORTOISE_ORM,
    # generate_schemas=True,    # 仅开发环境使用，生产环境不要开启
    # add_exception_handlers=True,  # 生产环境不要开启，会泄露调试信息
)

@app.middleware("http")
async def m2(request: Request, call_next):
    # 请求代码块
    # print("m2 request")
    response = await call_next(request)
    # 响应代码块
    # response.headers["author"] = "moluo"
    # interlist = ["/user/user", "/user/role", "/user/resource", "/user/role_res"]
    # if request.url.path in interlist:
    #     response.headers["author"] = "moluo"
    # print("m2 response")
    return response


# 定义允许跨域请求的来源列表
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1:5500",  # VS Code Live Server
    # 可以添加更多允许的域名，如生产环境域名
    "https://yourproductiondomain.com"
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # 允许的来源列表
    allow_credentials=True,     # 允许携带凭证（如 cookies）
    allow_methods=["*"],        # 允许的 HTTP 方法，* 表示允许所有方法
    allow_headers=["*"],        # 允许的 HTTP 请求头，* 表示允许所有头
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)