import asyncio
import sys
# 把之前装过 mysql-replication 的 site-packages 目录加进去
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent
from database import es

# ===================== 【可配置】多表 + 多索引映射 =====================
MYSQL_SETTINGS = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "root",
}
DB_NAME = "boss_project"

# 关键：多张表 + 对应 ES 索引（自己加表就行）
TABLE_INDEX_MAP = {
    "company": "esjob",          # 表名: ES索引名
    "industry": "esjob",          # 第二张表
    "job": "esjob",        # 第三张表
}

# 要监听的表名列表（自动从上面取）
ONLY_TABLES = list(TABLE_INDEX_MAP.keys())

# ===================== 异步 binlog 监听 =====================
async def binlog_listener():
    await asyncio.sleep(2)
    print(f"[INFO] 启动监听表：{ONLY_TABLES}")

    while True:
        try:
            stream = BinLogStreamReader(
                connection_settings=MYSQL_SETTINGS,
                server_id=3,
                blocking=True,
                only_schemas=[DB_NAME],
                only_tables=ONLY_TABLES,  # 多张表！
                only_events=[WriteRowsEvent, UpdateRowsEvent, DeleteRowsEvent]
            )

            print("[INFO] Binlog 监听运行中...")

            for event in stream:
                await process_event(event)
                
        except Exception as e:
            print("异常重连:", e)
            await asyncio.sleep(3)
        finally:
            stream.close()
            print("[INFO] 已关闭 binlog 连接")

# ===================== 多表通用：自动匹配 ES 索引 =====================
async def process_event(event):
    table = event.table  # 自动获取当前是哪张表
    es_index = TABLE_INDEX_MAP[table]  # 自动找对应ES索引

    # 新增
    if isinstance(event, WriteRowsEvent):
        for row in event.rows:
            print("新增:", row)
            doc = row["values"]
            _id = doc.get("id") or doc.get("UNKNOWN_COL0")
            # if es_index == "company":

            # sql = "select  from company  inner join job on company.id = job.company_id inner join industry on job.industry_id = industry.id where company.id = %s"
            # result = db.cursor.execute(sql, _id)
            # doc = {"id":result[0],name:result[1],industry:result[2]}
            await es.index(index=es_index, id=_id, document=doc)
            print(f"【{table}】新增 → ES：{_id}")

    # 修改
    elif isinstance(event, UpdateRowsEvent):
        for row in event.rows:
            print("修改:", row)
            doc = row["after_values"]

            _id = doc.get("id") or doc.get("UNKNOWN_COL0")
            await es.update(index=es_index, id=_id, doc=doc)
            print(f"【{table}】更新 → ES：{_id}")

    # 删除
    elif isinstance(event, DeleteRowsEvent):
        for row in event.rows:
            print("删除:", row)

            _id = row["values"].get("id") or row["values"].get("UNKNOWN_COL0")
            await es.delete(index=es_index, id=_id)
            print(f"【{table}】删除 → ES：{_id}")