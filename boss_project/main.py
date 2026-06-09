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
# 临时禁用：当前做大模型对话模块，MongoDB 暂不需要
# from tools.mymongodb import mongo_db
import time
from views.chatai import chat_router
app = FastAPI()
# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.include_router(users_router, prefix="/user")
# app.include_router(home_router, prefix="")
app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chatai")

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

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    client_connections[str(client_id)] = websocket
    print(f"客户端 {client_id} 已连接，当前连接数：{len(active_connections)}")
    #判断是用户还是hr,如果是用户，把用户信息推送给hr
    if client_id.startswith("user"):
        id = client_id.split("hr")[0].replace("user","")
        userdict = {"id":id,"name":str(id)+"号用户"}
        hrid =str(client_id.split("hr")[1])
        #判断hr是否在线
        if hrid not in client_connections:
            key = 'userlist'+str(hrid)
            value = r.get(key)
            if value:
                userlist = json.loads(value)
                flag = True
                for item in userlist:
                    if item['id'] == userdict['id']:
                        flag = False
                        break
                if(flag):
                    userlist.append(userdict)
                    r.set(key,json.dumps(userlist))
            else:
                userlist = []
                userlist.append(userdict)
                r.set(key,json.dumps(userlist))
        else:
            userlist = []
            userlist.append(userdict)
            await client_connections[hrid].send_text(json.dumps(userlist))
    if client_id.find('hr') < 0:
        value = r.get('userlist'+str(client_id))
        if value:
            userlist = json.loads(value)
            await websocket.send_text(json.dumps(userlist))
    
    try:
       while True:
            data = await websocket.receive_text()
            print(f"收到消息: {data}")
            data = json.loads(data)
            # 当用户给hr发消息 key  "hr"+String(route.params.hrId)+"user"+String(userid.value)
            # 当hr给用户发消息 key  "user"+String(userid.value)+"hr"+String(route.params.hrId)
            room = data['room']
            content = data['content']
            nowtime = int(time.time())
            # # 所有消息存入redis，在公司中存入到mysql 创建一张消息表 id 房间号（key） 消息内容 时间
            # #发送给hr
            if room.startswith("hr"):
                userid = room.split("user")[1]
                hrid = room.split("user")[0].replace("hr","")
            #发送给用户
            else:
                userid = room.split("hr")[0].replace("user","")
                hrid = room.split("hr")[1]
            key = "user" + str(userid) + "hr"+str(hrid)
            # r.zadd(key,nowtime,content['content'])
            # 所有聊天消息存入 mongodb 
            # db = mongo_db.createdbs("boss")
            # collection = mongo_db.createcoll(db,'rebotmessage')
            mesdict = {
                "sendid":userid if room.startswith("hr") else hrid,
                "recvid":hrid if room.startswith("hr") else userid,
                "room": key,
                "content":content['content'],
                "time":nowtime
            }
            # collection.insert_one(mesdict)
            #接收者是否上线，如果没上线把新的消息存入redis，等上线后再发送
            if str(room) not in client_connections:
                # key =  "newuser" + str(userid) + "hr"+str(hrid)
                r.zadd(room,nowtime,content['content'])
                
            else:
                await client_connections[str(room)].send_text(json.dumps(content))
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        client_connections.pop(client_id,None)       
        print(f"客户端 {client_id} 已断开，当前连接数：{len(active_connections)}")

from tools.myredis import r
from tools.bdapi import bdapi
import json

async def idcardtask():
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
            userAuth = await UserAuthReal.filter(font_img=imgurl).first()
            userid = userAuth.user_id
            await client_connections[str(userid)].send_text(json.dumps({'realName':name,'idCardNumber':idcard}))
    else:
        print("无数据处理等待中")
from apscheduler.schedulers.asyncio import AsyncIOScheduler
scheduler = AsyncIOScheduler()

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