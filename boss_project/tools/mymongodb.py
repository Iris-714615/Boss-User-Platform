import pymongo
from urllib.parse import quote_plus

class Mymongo():
    def __init__(self):
        # 方法1：不使用认证
        # client = pymongo.MongoClient("mongodb://localhost:27017/")

        # 方法2：使用认证
        self.username = quote_plus('admin')   # 对用户名进行编码
        self.password = quote_plus('123456')  # 对密码进行编码
        self.host = "localhost"
        self.port = "27017"
        self.database = "admin"

        self.client = pymongo.MongoClient(
            f'mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        )

    def createdbs(self,dbname):
        # 创建数据库
        my_db = self.client[dbname]
        return my_db

    def createcoll(self,my_db,collname):
        # 创建集合
        my_collection = my_db[collname]
        return my_collection
    
    def insertone(self,collname,data):
        result = collname.insert_one(data)
        return result.inserted_id
    def insertdata(self,collname,data):
        # 2. 插入多个文档
        result = collname.insert_many(data)
        print(f"插入的文档IDs: {result.inserted_ids}")

    def findall(self,collname):
        return  collname.find()
    
    def find(self,collname,query,page,pageSize):
        skip = (int(page)-1)*int(pageSize)
        return collname.find(query).skip(skip).limit(int(pageSize))
    
    def count(self,collname,query):
        return collname.count_documents(query)

mongo_db = Mymongo()
# print(mongo_db)
# db = mongo_db.createdbs("test")
# collection = mongo_db.createcoll(db,'usermessage')
# from datetime import datetime
# user = {
#     "name": "张三",
#     "age": 25,
#     "email": "zhangsan@example.com",
#     "tags": ["程序员", "Python"],
#     "created_at": datetime.now()
# }
# mongo_db.insertone(collection,user)
# users = [
#             {"name": "李四", "age": 30, "email": "lisi@example.com"},
#             {"name": "王五", "age": 28, "email": "wangwu@example.com"},
#             {"name": "赵六", "age": 35, "email": "zhaoliu@example.com","is_checked":1}
#         ]

# mongo_db.insertdata(collection,users)
# datames = mongo_db.findall(collection)
# for i in datames:
    #  print(i)