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

    
