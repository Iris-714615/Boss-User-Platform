from fastapi import APIRouter, Request, HTTPException
from fastapi.params import Query
from fastapi import Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from apps.models import *
from tortoise.queryset import Q
import json
import time
from tools.myjwt import mjwt
from tools.myredis import r

users_router = APIRouter()


# 定义分页依赖函数
def paginate(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    """
    分页依赖
    Args:
        page: 页码，默认1，必须大于等于1
        limit: 每页数量，默认10，范围1-100
    Returns:
        dict: 包含 page, limit, offset 的分页信息
    """
    return {
        "page": page, 
        "limit": limit, 
        "offset": (page - 1) * limit
    }


# Pydantic 模型定义
class LoginRequest(BaseModel):
    """登录请求模型"""
    name: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class RegisterRequest(BaseModel):
    """注册请求模型"""
    name: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class AddRoleRequest(BaseModel):
    """添加角色请求模型"""
    name: str = Field(..., description="角色名称")

class AddUserRequest(BaseModel):
    """添加用户请求模型"""
    name: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    role: int = Field(..., ge=1, description="角色ID")

class UpdateUserRequest(BaseModel):
    """更新用户请求模型"""
    name: Optional[str] = Field(None, description="用户名")
    password: Optional[str] = Field(None, description="密码")
    role: Optional[int] = Field(None, ge=1, description="角色ID")

class AddResourceRequest(BaseModel):
    """添加资源请求模型"""
    name: str = Field(..., description="资源名称")
    url: Optional[str] = Field(None, description="资源路径")
    pid: Optional[int] = Field(0, ge=0, description="父资源ID")

class AddRoleResourceRequest(BaseModel):
    """添加角色资源关联请求模型"""
    role_id: int = Field(..., ge=1, description="角色ID")
    reslist: List[int] = Field(..., description="资源ID列表")


@users_router.post("/login", summary="登录")
async def login(request: LoginRequest):
    """登录接口"""
    try:
        name = request.name
        password = request.password
        
        # 查询用户
        user = await User.get_or_none(name=name)
        if not user:
            return {"code": 400, "msg": "用户名不存在"}
        
        if user.password != password:
            return {"code": 400, "msg": "密码错误"}
        
        role_id = user.role_id
        reslist = []
        # resids = []
        
        if role_id == 1:
            # 管理员获取所有资源
            parent_resources = await Resource.filter(pid=None).all()
            for item in parent_resources:
                children = await Resource.filter(pid=item.id).all()
                sonlist = []
                for child in children:
                    sonlist.append({
                        "id": child.id,
                        "name": child.name,
                        "url": child.path,
                        "pid": child.pid_id
                    })
                    # resids.append(child.id)
                resdict = {"id": item.id, "name": item.name, "son": sonlist}
                reslist.append(resdict)
        else:
            # 根据角色获取资源
            role = await Role.get(id=role_id)
            print(role)
            resources = await role.resources.all()
            resdict = {}
            for parent_item in resources:
                children = await Resource.filter(pid=parent_item.id).all()
                for child in children:
                    # resids.append(child.id)
                    pid = parent_item.id
                    if pid not in resdict:
                        resdict[pid] = {
                            "id": pid,
                            "name": parent_item.name,
                            "son": [{
                                "id": child.id,
                                "name": child.name,
                                "url": child.path,
                                "pid": child.pid_id
                            }]
                        }
                    else:
                        resdict[pid]["son"].append({
                            "id": child.id,
                            "name": child.name,
                            "url": child.path,
                            "pid": child.pid_id
                        })
            reslist = list(resdict.values())
        
        # 获取接口列表
        # interlist = ["/user/users", "/user/roles", "/user/resources", "/user/role_res"]
        # r.set(str(role_id), json.dumps(interlist))
        
        # 生成token
        token = mjwt.encode({
            "userid": user.id,
            "roleid": role_id,
            "name": user.name,
            "exp": int(time.time() + 3600)
        })
        
        return {
            "code": 200,
            "msg": "登录成功",
            "userid": user.id,
            "token": token,
            "menulist": reslist,
            "name": user.name,
            # "interface": interlist
        }
    except Exception as e:
        print('登录异常:', str(e))
        return {"code": 500, "msg": "服务器内部错误"}


@users_router.post("/register", summary="注册")
async def register(request: RegisterRequest):
    """注册接口"""
    name = request.name
    password = request.password
    
    # 检查用户名是否存在
    existing_user = await User.get_or_none(name=name)
    if existing_user:
        return {"msg": "用户名已存在"}
    
    # 创建用户
    user = await User.create(name=name, password=password, role_id=1)
    return {"msg": "注册成功", "id": user.id}


@users_router.get("/role", summary="获取角色列表")
async def get_roles():
    """获取角色列表"""
    roles = await Role.all()
    role_list = []
    for role in roles:
        role_list.append({
            "id": role.id,
            "name": role.name
        })
    return {"msg": "查询角色列表成功", "code": 200, "data": role_list}


@users_router.post("/role", summary="添加角色")
async def add_role(request: AddRoleRequest):
    """添加角色"""
    name = request.name
    
    # 检查角色名是否存在
    existing_role = await Role.get_or_none(name=name)
    if existing_role:
        return {"msg": "角色已存在", "code": 400}
    
    # 创建角色
    role = await Role.create(name=name)
    return {"msg": "添加角色成功", "code": 200, "name": name, "id": role.id}


@users_router.get("/user", summary="获取用户列表")
async def get_users(pagination:Depends(paginate)):
    """获取用户列表"""
    users = await User.all().prefetch_related("role")
    user_list = []
    for user in users:
        role = await user.role
        user_dict = {
            "id": user.id,
            "name": user.name,
            "role": user.role_id,
            "role_name": role.name if role else "未知"
        }
        user_list.append(user_dict)
    return {"msg": "查询用户列表成功", "code": 200, "data": user_list}


@users_router.post("/user", summary="添加用户")
async def add_user(request: AddUserRequest):
    """添加用户"""
    name = request.name
    password = request.password
    role_id = request.role
    
    # 检查用户名是否存在
    existing_user = await User.get_or_none(name=name)
    if existing_user:
        return {"msg": "用户名已存在", "code": 400}
    
    # 创建用户
    user = await User.create(name=name, password=password, role_id=role_id)
    return {"msg": "添加用户成功", "code": 200, "name": name, "id": user.id}


@users_router.put("/user/{user_id}", summary="更新用户")
async def update_user(user_id: int, request: UpdateUserRequest):
    """更新用户"""
    user = await User.get_or_none(id=user_id)
    
    if not user:
        return {"msg": "用户不存在", "code": 400}
    
    if request.name:
        user.name = request.name
    if request.password:
        user.password = request.password
    if request.role:
        user.role_id = request.role
    
    await user.save()
    return {"msg": "修改成功", "code": 200}


@users_router.delete("/user/{user_id}", summary="删除用户")
async def delete_user(user_id: int):
    """删除用户"""
    user = await User.get_or_none(id=user_id)
    
    if not user:
        return {"msg": "用户不存在", "code": 400}
    
    await user.delete()
    return {"msg": "删除成功", "code": 200}


@users_router.get("/resource", summary="获取资源列表")
async def get_resources():
    """获取资源列表"""
    resources = await Resource.all()
    res_list = []
    for res in resources:
        res_list.append({
            "id": res.id,
            "name": res.name,
            "url": res.path,
            "pid": res.pid_id if res.pid else None
        })
    return {"msg": "查询资源列表成功", "code": 200, "data": res_list}


@users_router.post("/resource", summary="添加资源")
async def add_resource(request: AddResourceRequest):
    """添加资源"""
    name = request.name
    url = request.url
    pid = request.pid
    
    # 检查资源名是否存在
    existing_res = await Resource.get_or_none(name=name)
    if existing_res:
        return {"msg": "资源已存在", "code": 400}
    
    # 创建资源
    resource = await Resource.create(name=name, path=url, pid=pid if pid else None)
    return {"msg": "添加资源成功", "code": 200, "name": name, "url": url, "pid": pid}


@users_router.post("/role_res", summary="添加角色资源")
async def add_role_res(request: AddRoleResourceRequest):
    """添加角色资源关联"""
    role_id = request.role_id
    res_list = request.reslist
    
    # 获取角色
    role = await Role.get_or_none(id=role_id)
    if not role:
        return {"msg": "角色不存在", "code": 400}
    
    # 清空现有资源关联
    await role.resources.clear()
    
    # 添加新资源
    resources = await Resource.filter(id__in=res_list).all()
    await role.resources.add(*resources)
    
    return {"msg": "添加角色资源成功", "code": 200}


@users_router.get("/role_res", summary="获取角色资源列表")
async def get_role_res():
    """获取角色资源关联列表"""
    role_resources = await RoleResource.all()
    res_list = []
    for item in role_resources:
        res_list.append({
            "id": item.id,
            "role_id": item.role_id,
            "resource_id": item.resource_id
        })
    return {"msg": "查询角色资源列表成功", "code": 200, "data": res_list}
