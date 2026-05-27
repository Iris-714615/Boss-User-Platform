import redis

class MYREDIS:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def set(self,key,value):
        self.r.set(key,value)

    def get(self,key):
        return self.r.get(key)
    # 删除缓存数据
    def strdelete(self,key):
        self.r.delete(key)

    def zadd(self,key,score,value):
        self.r.zadd(key,{value:score})
     #根据排序删除，只保留5个
    def zremrangebyrank(self, key, start, end):
        self.r.zremrangebyrank(key, start, end)
    # 升序获取数据
    def zrange(self, key, start, end):
        return self.r.zrange(key, start, end)
    # 降序获取数据
    def zrevrange(self, key, start, end):
        # return self.r.ZREVRANGE (key, start, end)
        return self.r.zrevrange(key, start, end)

r = MYREDIS()
    