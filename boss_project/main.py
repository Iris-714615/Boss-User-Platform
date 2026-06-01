from  fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from settings import TORTOISE_ORM
from tortoise.contrib.fastapi import register_tortoise
from apps.models import *
# from views.users import users_router
from views.home import home_router
from views.auth import auth_router
from tools.myjwt import mjwt
from fastapi.responses import JSONResponse
app = FastAPI()
# app.include_router(users_router, prefix="/user")
app.include_router(home_router, prefix="")
app.include_router(auth_router, prefix="/auth")

# 挂载 static 目录
app.mount("/static", StaticFiles(directory="static"), name="static")

#数据库
register_tortoise(
    app,
    config=TORTOISE_ORM,
    # generate_schemas=True,    # 仅开发环境使用，生产环境不要开启
    # add_exception_handlers=True,  # 生产环境不要开启，会泄露调试信息
)

# @app.middleware("http")
async def m2(request: Request, call_next):
    # 请求代码块
    wlist = ["/auth/login", "/auth/register", "/auth/dingding", "/auth/dingcallback"]
    if request.url.path not in wlist:
        try:
            token = request.headers.get("Authorization")
            if token:
                payload = mjwt.decode(token)
                userid = payload["userid"]
                request.state.userid = userid
            else:
                return JSONResponse( content={'code': 401, 'message': "未登录"})
        except Exception as e:
            return JSONResponse( content={'code': 401, 'message': f"登录验证失败: {str(e)}"})
    
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

# from sqlalchemy.ext.asyncio import AsyncSession
# from database import get_db, Base, engine
# from binlog_listener import binlog_listener
# import asyncio


# @app.on_event("startup")
# async def startup():
#     # 创建 MySQL 表
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

#     # 启动异步 binlog 监听（后台常驻）
#     asyncio.create_task(binlog_listener())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)