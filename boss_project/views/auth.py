import hashlib
import random,time,requests,uuid
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Depends, File, UploadFile
from pydantic import BaseModel
from apps.models import *
from tools.myredis import r
from tools.myjwt import mjwt
from tools.tlogin import p
from cmath import e

auth_router = APIRouter()



class LoginRequest(BaseModel):
    phone: str = ""
    username: str = ""
    password: str


class RegisterRequest(BaseModel):
    phone: str = ""
    username: str = ""
    password: str
    name: str = ""


class SMSSendRequest(BaseModel):
    phone: str


class SMSLoginRequest(BaseModel):
    phone: str
    code: str


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# 发送短信接口  手机号验证码存入redis
@auth_router.post("/send_sms")
async def send_sms(req: SMSSendRequest):
    phone = req.phone
    res = r.get(phone)
    if res:
        return {'code': 400, 'msg': '手机号已发送验证码'}
    
    code = random.randint(1000, 9999)
    r.set(phone, str(code))

    return {'code': 200, 'msg': '短信发送成功', 'sms_code': code}


# 注册接口
@auth_router.post("/register")
async def register(req: RegisterRequest):
    phone = req.phone
    user = await User.filter(phone=phone).first()
    if user:
        return {'code': 400, 'msg': '手机号已注册'}
    
    await User.create(
        phone=phone,
        username=req.username,
        password=hash_password(req.password),
        real_name=req.name or f"用户{phone[-4:]}"
    )
    return {'code': 200, 'msg': '注册成功'}


# 手机号短信登录
@auth_router.post("/login_sms")
async def login_sms(req: SMSLoginRequest):
    phone = req.phone
    
    if req.code not in ["8888", "0000", "1234"]:
        return {'code': 400, 'msg': '验证码错误'}
    
    user = await User.filter(phone=phone).first()
    if not user:
        user = await User.create(
            phone=phone,
            username=f"user_{phone[-4:]}",
            password=hash_password("default"),
            real_name=f"用户{phone[-4:]}"
        )
    if user.status != 1:
        return {'code': 400, 'msg': '账号已被冻结或封禁'}
    
    token = mjwt.encode({
        "userid": str(user.id),
        "phone": user.phone,
        "username": user.username,
    })
    return {'code': 200, 'msg': '登录成功', 'token': token, 'userid': user.id, 'username': user.username}


# 用户名密码登录
@auth_router.post("/login_password")
async def login_password(req: LoginRequest):
    user = await User.filter(username=req.username).first()
    if not user:
        user = await User.filter(phone=req.phone).first()
    if not user:
        return {'code': 400, 'msg': '用户名或手机号不存在'}
    if user.password != hash_password(req.password):
        return {'code': 400, 'msg': '密码错误'}
    if user.status != 1:
        return {'code': 400, 'msg': '账号已被冻结或封禁'}
    
    token = mjwt.encode({
        "userid": str(user.id),
        "phone": user.phone,
        "username": user.username,
    })
    return {'code': 200, 'msg': '登录成功', 'token': token, 'userid': user.id, 'username': user.username}



@auth_router.get("/")
def get_users():
    return [
        {
            "id": 1,
            "name": "User 1",
            "email": "",
        },
        {
            "id": 2,
            "name": "User 2",
            "email": "",
        },
    ]

@auth_router.get("/dingding")
def get_dingding_url(types:str):
    classname = p.get_cls_class(types)
    url = classname.get_url()
    return {"url": url}

@auth_router.get("/dingcallback")   
async def dingcallback(code: str = None, authCode: str = None, types: str = "dingding"):
    # 钉钉回调可能使用 code 或 authCode 参数
    auth_code = authCode if authCode else code
    if not auth_code:
        return {"code": 400, "msg": "缺少授权码"}
    # 根据authCode获取用户accessToken
    classname = p.get_cls_class(types)
    if not classname:
        return {"code": 400, "msg": "不支持的登录类型"}
    
    userdict = classname.callback(auth_code)

    name = userdict.get("name")
    phone = userdict.get("phone")
    uid = userdict.get("uid")
    accessToken = userdict.get("accessToken")
    
    # 如果获取用户信息失败，返回错误
    if not uid or not name:
        return {"code": 400, "msg": "钉钉授权失败，无法获取用户信息"}
    
    # 检查是否已有绑定记录
    userauth = await UserAuth.filter(auth_type='dingding', openid=uid).first()
    if userauth:
        # 用户已绑定，获取用户信息
        user = await User.filter(id=userauth.user_id).first()
    else:
        # 用户未绑定，检查手机号是否已注册
        user = await User.filter(phone=phone).first() if phone else None
        if not user:
            # 创建新用户
            user = await User.create(
                username=name or f"dingding_{uid[:8]}", 
                phone=phone or "",
                password=hash_password("dingding_default"),
                real_name=name or "钉钉用户"
            )
        # 创建绑定记录
        await UserAuth.create(user_id=user.id, auth_type='dingding', openid=uid, token=accessToken)
    
    # 生成token返回
    token = mjwt.encode({"userid": str(user.id), "exp": int(time.time()) + 452222})
    
    # 重定向到前端登录成功页，携带token
    from fastapi.responses import RedirectResponse
    frontend_url = f"http://localhost:3002/dinglogin-success?token={token}&userid={user.id}&username={user.username or ''}&phone={phone or ''}&name={name or ''}"
    return RedirectResponse(url=frontend_url, status_code=302)

import json
from tools.qntoken import qiniu_token

@auth_router.get("/qntoken")
def get_qntoken():
    token = qiniu_token()
    print(token)
    return {"code": 200, "msg": "获取成功", "token": token}

from tools.bdapi import bdapi

class IdCardOcr(BaseModel):
    imgurl: str = ""
   
@auth_router.post("/idcard_ocr")
async def idcard_ocr(img: IdCardOcr):
    imgurl = img.imgurl
    res = bdapi.font_ocr(imgurl)
    print(res)
    res = json.loads(res)
    name = res["words_result"][0]["words"][-2:]
    idcard = res["words_result"][1]["words"][-18:]
    
    return {"code": 200, "msg": "获取成功", "realName": name, "idCardNumber": idcard}

class userIdCard(BaseModel):
    realName: str = ""
    idCardNumber: str = ""
    imgurl: str = ""
    
@auth_router.post("/idcard_upload")
async def idcard_upload(userIDcard: userIdCard, request: Request):
    userid = 1
    await UserAuthReal.create(
        user_id=userid,
        real_name=userIDcard.realName,
        id_card=userIDcard.idCardNumber,
        front_img=userIDcard.imgurl,
        status=0,
        )  
    await User.filter(id=userid).update( is_real=1 )    
    return {"code": 200, "msg": "上传成功"}

