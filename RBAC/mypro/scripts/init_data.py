import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, db
from models.model import Roles, Users, Resources, Interfaces

# 创建应用上下文
with app.app_context():
    # 添加角色数据
    roles_data = [
        {'name': '管理员'},
        {'name': '运营官'},
        {'name': '普通用户'}
    ]
    
    print("正在添加角色数据...")
    for role_data in roles_data:
        role = Roles.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Roles(name=role_data['name'])
            db.session.add(role)
            print(f"  添加角色: {role_data['name']}")
    
    # 添加资源数据
    resources_data = [
        {'name': '用户管理', 'url': '/user', 'pid': None},
        {'name': '角色管理', 'url': '/role', 'pid': None},
        {'name': '资源管理', 'url': '/resource', 'pid': None},
        {'name': '接口管理', 'url': '/interface', 'pid': None},
        {'name': '系统设置', 'url': '/settings', 'pid': None}
    ]
    
    print("\n正在添加资源数据...")
    for resource_data in resources_data:
        resource = Resources.query.filter_by(name=resource_data['name']).first()
        if not resource:
            resource = Resources(
                name=resource_data['name'],
                url=resource_data['url'],
                pid=resource_data['pid']
            )
            db.session.add(resource)
            print(f"  添加资源: {resource_data['name']}")
    
    # 添加用户数据
    users_data = [
        {'username': 'admin', 'password': 'admin123', 'role': 1},
        {'username': 'operator', 'password': 'operator123', 'role': 2},
        {'username': 'user', 'password': 'user123', 'role': 3}
    ]
    
    print("\n正在添加用户数据...")
    for user_data in users_data:
        user = Users.query.filter_by(username=user_data['username']).first()
        if not user:
            user = Users(
                username=user_data['username'],
                password=user_data['password'],
                role=user_data['role']
            )
            db.session.add(user)
            print(f"  添加用户: {user_data['username']}")
    
    # 添加接口数据
    interfaces_data = [
        {'url': '/user/login', 'resource': 1},
        {'url': '/user/register', 'resource': 1},
        {'url': '/user/add_user', 'resource': 1},
        {'url': '/user/add_role', 'resource': 2},
        {'url': '/user/add_resource', 'resource': 3}
    ]
    
    print("\n正在添加接口数据...")
    for interface_data in interfaces_data:
        interface = Interfaces.query.filter_by(url=interface_data['url']).first()
        if not interface:
            interface = Interfaces(
                url=interface_data['url'],
                resource=interface_data['resource']
            )
            db.session.add(interface)
            print(f"  添加接口: {interface_data['url']}")
    
    # 提交事务
    db.session.commit()
    print("\n✅ 数据初始化完成！")
    
    # 打印统计信息
    print("\n📊 当前数据库数据统计:")
    print(f"  角色数量: {Roles.query.count()}")
    print(f"  用户数量: {Users.query.count()}")
    print(f"  资源数量: {Resources.query.count()}")
    print(f"  接口数量: {Interfaces.query.count()}")
