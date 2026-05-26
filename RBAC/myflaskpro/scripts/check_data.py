import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, db
from models.model import Roles, Users, Resources, Interfaces

with app.app_context():
    print('数据库数据统计:')
    print('  角色数量:', Roles.query.count())
    print('  用户数量:', Users.query.count())
    print('  资源数量:', Resources.query.count())
    print('  接口数量:', Interfaces.query.count())
    
    print('\n用户列表:')
    for user in Users.query.all():
        role = Roles.query.get(user.role)
        print('  -', user.username, '(角色:', role.name if role else '未知', ')')
