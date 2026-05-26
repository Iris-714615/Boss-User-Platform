from flask import Flask, request, jsonify, Blueprint
from flask_migrate import Migrate
from views.user import user_bp
from config import Config
from flask_cors import CORS
from models import db
from tools.myjwt import mjwt
from tools.myredis import r
import time
import json
from flask import g

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

app.config['JSON_AS_ASCII'] = False  # 允许JSON输出中文
app.json.ensure_ascii = False
CORS(app)  # 允许所有跨域请求

app.register_blueprint(user_bp, url_prefix='/users')

@app.route('/')
def index():
    return 'hello world'

# 每次请求前执行（请求校验）
@app.before_request
def before_request():
    whitelist = ['/users/login', '/users/register', '/']
    if request.path not in whitelist:
        token = request.headers.get('Authorization')
        if token is None:     
            return jsonify({'code':400,'msg':'token不存在'})
        payload = mjwt.decode(token)
        if payload:
            userid = payload['userid']
            roleid = payload['roleid']
            interlist = r.get(str(roleid))
            if interlist:
                interlist = json.loads(interlist)
                if request.path not in interlist:
                    return jsonify({'code':403,'msg':'没有权限'})
            
            g.userid = userid
            g.roleid = roleid
        else:
            return jsonify({'code':403,'msg':'token验证失败'})
    


if __name__ == '__main__':
    app.run(debug=True)