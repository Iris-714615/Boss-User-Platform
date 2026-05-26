from tortoise import Tortoise

TORTOISE_ORM = {
    'connections': {
        'default': {
            # 数据库引擎选择
            'engine': 'tortoise.backends.mysql',  # MySQL
            # 'engine': 'tortoise.backends.asyncpg',  # PostgreSQL
            # 'engine': 'tortoise.backends.sqlite',  # SQLite
            
            # 数据库连接配置
            'credentials': {
                'host': '127.0.0.1',      # 数据库地址
                'port': '3306',           # 端口
                'user': 'root',           # 用户名
                'password': 'root',       # 密码
                'database': 'boss_project',    # 数据库名
                'minsize': 1,             # 最小连接数
                'maxsize': 5,             # 最大连接数
                'charset': 'utf8mb4',     # 字符集
                'echo': True              # 是否打印 SQL（开发环境）
            }
        },
    },
    'apps': {
        'models': {
            # 注册模型所在的模块
            'models': ['apps.models', 'aerich.models'],
            'default_connection': 'default',
        }
    },
    'use_tz': False,               # 是否使用 UTC 时间
    'timezone': 'Asia/Shanghai'    # 时区设置
}