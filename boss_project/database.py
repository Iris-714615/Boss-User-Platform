from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from elasticsearch import AsyncElasticsearch

# ===================== 异步 MySQL =====================
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:root@localhost:3306/boss_project"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# ===================== 异步 ES =====================
es = AsyncElasticsearch("http://localhost:9200")

# 异步 DB 依赖
async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()