from flask import Blueprint,request,jsonify
from models import db
from models.model import *
user_bp = Blueprint('user',__name__)

from tools.myjwt import mjwt
from tools.myredis import r
import time,json
#登录
@user_bp.route('/login',methods=['GET','POST'])
def login():
    try:
        if request.method == 'POST':
            data = json.loads(request.data)
            username = data['username']
            password = data['password']
            #查询数据库，判断用户名是否存在
            user = Users.query.filter_by(username=username).first()
            if not user:
                return jsonify({'code':400,'msg':'用户名不存在'})
            #判断密码是否正确
            if user.password != password:
                return jsonify({'code':400,'msg':'密码错误'})
            roleid = user.role
            reslist = []
            #数据结构[{"id":1,"name":"权限管理","son":[{},{}]}]
            resids = []
            if int(roleid) == 1:
                # 管理员获取所有资源
                res = Resources.query.filter_by(pid=None).all()
                for item in res:
                    sonlist = []
                    # 直接查询子级资源
                    children = Resources.query.filter_by(pid=item.id).all()
                    for child in children:
                        sonlist.append(child.to_dict())
                        resids.append(child.id)
                    resdict = {'id':item.id,'name':item.name,'son':sonlist}
                    reslist.append(resdict)
            else:
                resdict = {}
                role = Roles.query.filter_by(id=roleid).first()
                if role:
                    rlist = role.resources
                    for parent_item in rlist:
                        # 直接查询子级资源
                        children = Resources.query.filter_by(pid=parent_item.id).all()
                        for child in children:
                            resids.append(child.id)
                            pid = parent_item.id
                            if pid not in resdict:
                                resdict[pid] = {'id':pid,'name':parent_item.name,'son':[child.to_dict()]}
                            else:
                                resdict[pid]['son'].append(child.to_dict())
                    reslist = list(resdict.values())

            interface = Interfaces.query.filter(Interfaces.resource.in_(resids)).all() if resids else []
            interlist = []
            for item in interface:
                interlist.append('/user' + item.url)
            r.set(str(roleid),json.dumps(interlist))
            token = mjwt.encode({'userid':user.id,'roleid':roleid,'name':user.username,'exp':int(time.time()+3600)})
            return jsonify({'code':200,'msg':'登录成功','userid':user.id,'token':token,'menulist':reslist,'name':user.username,'interface':interlist})
    except Exception as e:
        print('登录异常:', str(e))
        return jsonify({'code':500,'msg':'服务器内部错误'})
    
#注册
@user_bp.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        #查询数据库，判断用户名是否存在
        user = Users.query.filter_by(username=username).first()
        if user:
            return jsonify({'msg':'用户名已存在'})
        #添加用户
        user = Users(username=username,password=password,role=1)
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg':'注册成功'})
    else:
        #get请求
        name = request.args.get('name')
        return jsonify({'name':name})

#添加角色
@user_bp.route('/roles',methods=['GET','POST'])
def roles():
    if request.method == 'POST':
        data = json.loads(request.data)
        name = data['name']
        #添加角色
        role = Roles(name=name)
        db.session.add(role)
        db.session.commit()
        return jsonify({'msg':'添加角色成功','code':200,'name':name})
    else:
        #get请求，查询角色列表 
        roles = Roles.query.all()
        rolelist = [role.to_dict() for role in roles]
        return jsonify({'msg':'查询角色列表成功','code':200,'data':rolelist})

#添加用户
@user_bp.route('/users',methods=['GET','POST'])
def user():
    if request.method == 'POST':
        data = json.loads(request.data)
        username = data.get("username")
        password = data.get("password")
        role = data.get("role")
        #查询数据库，判断用户名是否存在
        user = Users.query.filter_by(username=username).first()
        if user:
            return jsonify({'msg':'用户名已存在','code':400})
        #添加用户
        user = Users(username=username,password=password,role=int(role))
        db.session.add(user)
        db.session.commit()
        return jsonify({'msg':'添加用户成功','code':200,'username':username,'id':user.id})
    else:
        #get请求，查询用户列表 
        users = Users.query.all()
        userlist = []
        for user in users:
            user_dict = user.to_dict()
            role = Roles.query.get(user.role)
            user_dict['role_name'] = role.name if role else '未知'
            userlist.append(user_dict)
        return jsonify({'msg':'查询用户列表成功','code':200,'data':userlist})

#更新用户
@user_bp.route('/users/<int:user_id>',methods=['PUT'])
def update_user(user_id):
    data = json.loads(request.data)
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'msg':'用户不存在','code':400})
    if 'username' in data:
        user.username = data['username']
    if 'password' in data:
        user.password = data['password']
    if 'role' in data:
        user.role = int(data['role'])
    db.session.commit()
    return jsonify({'msg':'修改成功','code':200})

#删除用户
@user_bp.route('/users/<int:user_id>',methods=['DELETE'])
def delete_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'msg':'用户不存在','code':400})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg':'删除成功','code':200})

#添加资源
@user_bp.route('/resources',methods=['GET','POST'])
def resources():
    if request.method == 'POST':
        name = request.form.get("name")
        url = request.form.get("url")
        pid = request.form.get("pid")
        #添加资源
        resource = Resources(name=name,url=url,pid=int(pid))
        db.session.add(resource)
        db.session.commit()
        return jsonify({'msg':'添加资源成功','code':200,'name':name,'url':url,'pid':pid})
    else:
        #get请求，查询资源列表
      
        resources = Resources.query.all()
        reslist = [resource.to_dict() for resource in resources]
        return jsonify({'msg':'查询资源列表成功','code':200,'data':reslist})

#添加角色资源
@user_bp.route('/role_res',methods=['GET','POST'])
def role_res():
    if request.method == 'POST':
        data = json.loads(request.data)
        role_id = data['role_id']
        reslist = data['reslist']
        #添加角色资源
        role = Roles.query.filter_by(id=int(role_id)).first()
        role.resources = []
        res = Resources.query.filter(Resources.id.in_(reslist)).all()
        role.resources = res
        db.session.commit()
        return jsonify({'msg':'添加角色资源成功','code':200})
    else:
        #get请求，查询角色资源列表
        role_res = TbRoleRes.query.all()
        role_reslist = [role_res.to_dict() for role_res in role_res]
        return jsonify({'msg':'查询角色资源列表成功','code':200,'data':role_reslist})
