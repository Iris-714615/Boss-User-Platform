# 数据库配置
class Config:
    # 数据库连接 URI（以 MySQL 为例，使用 pymysql 驱动）
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/boss_db?charset=utf8mb4"
    # 禁用 SQLAlchemy 跟踪修改（减少内存占用）
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 调试模式（开发环境用）
    DEBUG = True