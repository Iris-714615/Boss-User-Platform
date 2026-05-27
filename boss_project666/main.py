from  fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from apps.models import *
# from views.users import users_router
from views.home import home_router

app = FastAPI()
# app.include_router(users_router, prefix="/user")
app.include_router(home_router, prefix="")

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
    request.state.userid = 1
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
    "http://localhost:3000",
    "http://localhost:3002",
    "http://localhost:5173",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:3002",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)