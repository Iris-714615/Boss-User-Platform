from fastapi import APIRouter, Request
from apps.models import *
from tools.myredis import r
import json,time
home_router = APIRouter()

from pydantic import BaseModel

# class SearchHistory(BaseModel):
#     jobname: str = None
#     city: str = None

from database import es

#接口 sql数据同步到es
@home_router.post("/sync_job_to_es")
async def sync_job_to_es():
    job = await Job.all()
    if job:
        for i in job:
            city = await i.city
            company = await i.company
            jobdict ={"id":i.id,"job_name":i.job_name,"salary_range":i.salary_range,"city":city.name,"education":i.education,"work_year":i.work_year,"job_desc":i.job_desc,'companyName':company.name,'industry':company.intro,'scale':company.scale}
            await es.index(index="esjob", document=jobdict)
            
#es 搜索
def search_job_city(name=None,city=None):
    slist = []
    if name:
        slist.append({"match":{"job_name":name}})
    if city:
        slist.append({"match":{"city":city}})
    return slist

#依赖注入 分页
from fastapi import Depends
def pagination(page:int=1,page_size:int=5):
    offset = (int(page) - 1) * int(page_size)
    return {"offset":offset,"size":page_size}
@home_router.get("/search")
async def search( request: Request,name:str=None,city:str=None,pag:dict=Depends(pagination)):
    mes = name or city
    print(mes)
    if mes:  
        hot_search = await HotSearch.filter(keyword__contains=mes).all()
        if hot_search:
            for item in hot_search:
                item.search_count += 1
                await item.save()
        else:
            await HotSearch.create(keyword=mes, search_count=1)
        hot_search = await HotSearch.all().order_by("-search_count")[:5]
        searchlist = [item.keyword for item in hot_search]
        r.set("home_hot_search", json.dumps(searchlist))
        userid = request.state.userid
        if userid:
            await UserSearchHistory.create(user_id=userid, keyword=mes)
            key = f"user_search_history"+str(userid)
            r.zadd(key, int(time.time()), mes)
            r.zremrangebyrank(key, 0, -4)
    
    
    slist = search_job_city(name,city)
    body = {
        "query": {"bool": {"must": [], "should": []}},
        "from": pag["offset"],
        "size": pag["size"]
    }
    if len(slist) > 0:
        for i in slist:
            body["query"]["bool"]["must"].append(i)
    else:
        body["query"]["match_all"] = {}
        del body["query"]["bool"]
    data = await es.search(index="esjob", body=body)
    searchlist = []
    count = data["hits"]["total"]["value"]
    if count > 0:
        for item in data["hits"]["hits"]:
            searchlist.append(item["_source"])
    
    return {'code': 200, 'msg': '成功', 'data': searchlist}

@home_router.get("/search_history")
async def user_search_history(request: Request):
    userid = 1
    search_history = []
    if userid:
        key = f"user_search_history"+str(userid)
        search_history = r.zrevrange(key, 0, -1)
        if search_history:
            search_history = [item.decode("utf-8") for item in search_history]
        else:
            search_history = await UserSearchHistory.filter(user_id=userid).all().order_by("-create_time").limit(3)
            if search_history:
                for item in search_history:
                    r.zadd(key, int(time.time()), str(item.keyword))
                    search_history.append(item.keyword)
          
    return {"code": 200, "msg": "成功", "data": search_history}
   
@home_router.get("/hot_search")
async def hot_search():
    hot_search = r.get("home_hot_search")
    if hot_search:
        hot_search = json.loads(hot_search)
    else:
        hot_search = await HotSearch.all().order_by("-search_count")[:5]
        if hot_search:
            searchlist = [item.keyword for item in hot_search]
            r.set("home_hot_search", json.dumps(searchlist))
            hot_search = searchlist
        else:
            hot_search = []

    return {"code": 200, "msg": "成功", "data": hot_search}
   
#获取用户信息
@home_router.get("/user_info")
async def user_info(request: Request):
    userid = 1
    user = await User.filter(id=userid).first()
    if user:
        city_name = ""
        if user.intention_city:
            city = await user.intention_city
            city_name = city.name if city else ""
        salary = ""
        if user.expected_salary_min and user.expected_salary_max:
            salary = f"{user.expected_salary_min}-{user.expected_salary_max}K"
        userinfo = {
            'position': user.intention_position or "",
            'city': city_name,
            'salary': salary,
            'name': user.username or "",
            'avatar': user.avatar or "",
                   }
    else:
        userinfo = {}
    return {"code": 200, "msg": "成功", "data": userinfo}

#热门行业
@home_router.get("/hot_industry")
async def hot_industry():
    hot_industry = r.get("home_hot_industry")
    if hot_industry:
        industrylist = json.loads(hot_industry)
    else:
        industry = await Industry.filter(is_recommend=1).all().order_by("-total_jobs")[:6]
        industrylist = [{'id':item.id,'name':item.name,'icon':item.icon,'count':item.total_jobs} for item in industry]
        r.set("home_hot_industry", json.dumps(industrylist))      
      
    return {"code": 200, "msg": "成功", "data": industrylist}

#热门岗位
@home_router.get("/hot_job")
async def hot_job():
    hot_job = r.get("home_hot_job")
    if hot_job:
        joblist = json.loads(hot_job)
    else:
        job = await Job.filter(is_recommend=1).all()[:3]
        joblist = []
        if job:
            for i in job:
                city = await i.city
                company = await i.company
                jobdict ={"id":i.id,"job_name":i.job_name,"salary_range":i.salary_range,"city":city.name,"education":i.education,"work_year":i.work_year,"job_desc":i.job_desc,'companyName':company.name,'industry':company.intro,'scale':company.scale}
                joblist.append(jobdict)

        r.set("home_hot_job", json.dumps(joblist))       
    return {"code": 200, "msg": "成功", "data": joblist}

#热门城市
@home_router.get("/hot_city")
async def hot_city():
    hot_city = r.get("home_hot_city")
    if hot_city:
        citylist = json.loads(hot_city)
    else:
        city = await City.filter(is_recommend=1).order_by("id")[:6]
        citylist = [item.name for item in city]
        r.set("home_hot_city", json.dumps(citylist))
    return {"code": 200, "msg": "成功", "data": citylist}



@home_router.get("/search_job")
async def search_job(jobname, city, pagination: dict = Depends(pagination)):
    slist = search_job_city(jobname,city)
    body = {
        "query": {"bool": {"must": [], "should": []}},
        "from": pagination["offset"],
        "size": pagination["size"]
    }
    if len(slist) > 0:
        for i in slist:
            body["query"]["bool"]["must"].append(i)
    else:
        body["query"]["match_all"] = {}
        del body["query"]["bool"]
    data = await es.search(index="esjob", body=body)
    searchlist = []
    count = data["hits"]["total"]["value"]
    if count > 0:
        for item in data["hits"]["hits"]:
            searchlist.append(item["_source"])
    
    return {'code': 200, 'msg': '成功', 'data': searchlist}

    
#职位详情
@home_router.get("/jobdetail/{id}")
async def job_detail(id: int):
    #获取参数、职位id
    key = "jobdetail"+str(id)
    #查询redis中是否存在该职位，存在则直接返回，不存在则查询数据库并缓存到redis中
    value = r.get(key)
    if value:
        value = json.loads(value)
        return {"code": 200, "msg": "成功", "data": value}
    else:
        #并发访问同时1万人，分布式锁，确保只查询一次
        jobdict = {}
        # r.delete(key+"_lock")
        if r.setnx(key+"_lock", 1):     
            #查询数据库
            job = await Job.filter(id=id).first()
            if job:
                city = await job.city
                companymes = await job.company
                company = {'id':companymes.id,'name':companymes.name,'intro':companymes.intro,'scale':companymes.scale,'address':companymes.address}
                publishermes = await job.publisher
                dept = await publishermes.dept
                publisher = {'id':publishermes.id,'name':publishermes.real_name,'company':companymes.name,'dept':dept.dept_name}
                
                jobdict ={"id":job.id,"job_name":job.job_name,
                "salary_range":job.salary_range,"city":city.name,
                "education":job.education,"work_year":job.work_year,
                "job_desc":job.job_desc,'company':company,'publisher':publisher}
                r.set(key, json.dumps(jobdict))
            r.delete(key+"_lock")
        else:
            time.sleep(1)
            value = r.get(key)
            if value:
                value = json.loads(value)
                return {"code": 200, "msg": "成功", "data": value}
        return {'code':200,'msg':'成功','data':jobdict}
    #存入redis
    #返回职位详情
# 临时禁用：当前做大模型对话模块，MongoDB 暂不需要
# from tools.mymongodb import mongo_db
# db = mongo_db.createdbs("comment")
# collection = mongo_db.createcoll(db, 'hrcomment')
collection = None  # 占位
from datetime import datetime

#评价请求体
class HrComment(BaseModel):
    hrid: int = None
    rating: int = 5
    content: str = None

#提交评价接口
@home_router.post("/hrcomment")
async def hrcomment(hrcomment: HrComment, request: Request):
    userid = 1
    user = await User.filter(id=userid).first()
    comment = {
        "userid": userid,
        "hrid": hrcomment.hrid or 1,
        "rating": hrcomment.rating or 5,
        "content": hrcomment.content,
        "time": datetime.now(),
        "username": user.real_name if user else "匿名",
        "avatar": user.avatar if user else "",
        "hrname": ""
    }
    collection.insert_one(comment)
    return {"code": 200, "msg": "添加成功"}

#获取评价列表接口（按 hrid 过滤 + 分页）
@home_router.get("/hrcomment")
async def get_hrcomment(hrid: int = 1, page: int = 1, page_size: int = 5):
    skip = (int(page) - 1) * int(page_size)
    query = {"hrid": int(hrid)}
    cursor = collection.find(query).sort("time", -1).skip(skip).limit(int(page_size))
    hrcomment = list(cursor)
    # ObjectId 转为字符串，方便前端使用
    for item in hrcomment:
        if "_id" in item:
            item["_id"] = str(item["_id"])
        if "time" in item and item["time"]:
            item["time"] = str(item["time"])
    total = collection.count_documents(query)
    return {"code": 200, "msg": "成功", "data": hrcomment, "total": total}

# 初始化测试数据（只在模块加载时执行一次，避免每次请求都重复插入）
def _init_chatrecord_testdata():
    db = mongo_db.createdbs("boss")
    collection = mongo_db.createcoll(db, 'rebotmessage')
    # 如果已经有数据就不再插入
    if collection.count_documents({}) > 0:
        return
    orders = [
        {"sendid": 1, "recvid": "1001", "room": "11001", "content": "你好", "date": "2024-01-01", "comment_type": 1},
        {"sendid": "1001", "recvid": 1, "room": "11001", "content": "你好324234234", "date": "2024-01-02"},
        {"sendid": 2, "recvid": "1001", "room": "21001", "content": "你好324234234", "date": "2024-01-01"},
        {"sendid": "1001", "recvid": 2, "room": "21001", "content": "你好324234234", "date": "2024-01-03"},
        {"sendid": 2, "recvid": "1002", "room": "21002", "content": "你好324234234", "date": "2024-01-01"},
        {"sendid": "1002", "recvid": 2, "room": "21002", "content": "你好324234234", "date": "2024-01-03"},
    ]
    collection.insert_many(orders)

# 临时禁用：MongoDB 未连接
# _init_chatrecord_testdata()

# 获取聊天记录接口（临时禁用：依赖 MongoDB）
# @home_router.get("/chatrecord")
async def get_chatrecord(room: str = None, page: int = 1, page_size: int = 5):
    """
    获取聊天记录
    :param room: 房间号（可选）。如果传入则只返回该房间；否则返回所有房间聚合
    :param page: 页码
    :param page_size: 每页条数
    """
    db = mongo_db.createdbs("boss")
    collection = mongo_db.createcoll(db, 'rebotmessage')

    # 如果指定了 room，按房间查询并分页
    if room:
        skip = (int(page) - 1) * int(page_size)
        cursor = collection.find({"room": room}).sort("date", -1).skip(skip).limit(int(page_size))
        messages = []
        for item in cursor:
            item["_id"] = str(item["_id"])
            messages.append(item)
        total = collection.count_documents({"room": room})
        return {"code": 200, "msg": "成功", "data": messages, "total": total}

    # 否则按用户聚合（这里默认用户 id=2 的所有房间）
    # 兼容 sendid/recvid 可能是 int 或 str：分别查一次然后合并
    target_id_str = "2"
    # 用两次 find 替代 aggregate，避免 $match+$group 组合的 $expr 求值坑
    cursor = collection.find({
        "$or": [
            {"sendid": int(target_id_str)},   # 匹配 int
            {"sendid": target_id_str},        # 匹配 str
            {"recvid": int(target_id_str)},
            {"recvid": target_id_str}
        ]
    }).sort("date", -1)

    # Python 里手工 group
    grouped = {}
    for doc in cursor:
        room = doc.get("room")
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        if room not in grouped:
            grouped[room] = []
        grouped[room].append(doc)

    result = [{"_id": room, "messages": msgs} for room, msgs in grouped.items()]
    for item in result:
        # 修复：group 后的字段是 messages（数组），不是 content
        msg_list = item.get('messages', [])
        print('房间号', item['_id'])
        print('消息数', len(msg_list))
        for m in msg_list:
            # 把 ObjectId 转字符串，避免 JSON 序列化失败
            if '_id' in m:
                m['_id'] = str(m['_id'])
            print('  ', m.get('content'))
        print("-----------------")
    return {"code": 200, "msg": "成功", "data": result}
