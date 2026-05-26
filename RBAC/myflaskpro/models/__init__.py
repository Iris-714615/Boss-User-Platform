from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy（不直接绑定 app，避免循环导入）
db = SQLAlchemy()

from .model import *