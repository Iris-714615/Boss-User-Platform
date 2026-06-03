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

from typing import List,Dict
from fastapi import WebSocket,WebSocketDisconnect
active_connections: List[WebSocket] = []
client_connections: Dict[str, WebSocket] = {}

async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)

@app.websocket("/ws/{userid}")
async def websocket_endpoint(websocket: WebSocket, userid: str):
    client_connections[userid] = websocket
    await websocket.accept()
    client_connections[str(userid)] = websocket
    print(f"客户端 {userid} 已连接，当前连接数：{len(active_connections)}")
    try:
       while True:
           data = await websocket.receive_text()
           print(f"收到消息: {data}")
           await websocket.send_text(f"服务器已收到消息: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        client_connections.pop(userid,None)
        await broadcast(f"userid {userid} disconnected")
        print(f"客户端 {userid} 已断开，当前连接数：{len(active_connections)}")

from tools.myredis import r
from tools.bdapi import bdapi
import json

def idcardtask():
    len = r.llen('idcardocr')
    if len > 0:           
        idlist=r.lrange('idcardocr',0,-1)
        for id in idlist:
            imgurl=id.decode('utf-8')
            mes = bdapi.font_ocr(imgurl)
            mes = json.loads(mes)
            name = mes["words_result"][0]["words"][-2:]
            idcard = mes["words_result"][1]["words"][-18:]
            # r.set(imgurl,json.dumps({'name':name,'idcard':idcard}))
            # r.lrem('idcardocr',1,id)
            # userAuth = UserAuthReal.filter(font_img=imgurl).first()
            # userid = userAuth.user
            userid = 1
            client_connections[str(userid)].send_text(json.dumps({'realName':name,'idCardNumber':idcard}))
    else:
        print("无数据处理等待中")
from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()

def add_jobs():
    scheduler.add_job(
        func=idcardtask, 
        trigger='interval', 
        seconds=2,
        id='time_printer'
        )

# @app.on_event("startup")
def startup_event():
    add_jobs()
    scheduler.start()
    print("调度器启动")

# @app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    print("调度器关闭")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)