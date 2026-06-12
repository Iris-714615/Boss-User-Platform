from fastapi import APIRouter, Request
from apps.models import *
from datetime import datetime
import random,json,time
from tools.myredis import r

chat_router = APIRouter()

import os
from openai import OpenAI
client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为: api_key="sk-xxx",
        api_key="sk-310108a8f49a425087fc65d0d939564e",
        # 以下为华北2（北京）地域的URL，各地域的URL不同。
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

@chat_router.get("/chat_message")
def chat_message(message: str):
    try:
        completion = client.chat.completions.create(
            model="qwen-plus",  # 模型列表: https://help.aliyun.com/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': message}
            ]
        )
        print(completion.choices[0].message.content)
        return {"code": 200, "message": completion.choices[0].message.content}
    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")
        return {"code": 500, "message": str(e)}

def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages
    )
    return completion.choices[0].message.content 

#多轮对话
# 初始化 messages  一定要写在 函数外面
messages = []
@chat_router.get("/chat_many")
def chat_many(message: str):
    messages.append({"role": "user", "content": message})
    print(f"第{len(messages)}轮")
    print(f"用户：{messages[0]['content']}")
    assistant_output = get_response(messages)  
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型：{assistant_output}\n")
    return {"code": 200, "message": assistant_output}


#流式响应
def get_stream(message: str):
    completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ],
    stream=True,
    stream_options={"include_usage": True}
    )
    # 3. 处理流式响应
    # 用列表暂存响应片段，最后 join 比逐次 += 字符串更高效
    content_parts = []
    print("AI: ", end="", flush=True)

    for chunk in completion:
        if chunk.choices:
            content = chunk.choices[0].delta.content or ""
            print(content, end="", flush=True)
            content_parts.append(content)
            yield f"data: {content}\n\n"
        elif chunk.usage:
            print("\n--- 请求用量 ---")
            print(f"输入 Tokens: {chunk.usage.prompt_tokens}")
            print(f"输出 Tokens: {chunk.usage.completion_tokens}")
            print(f"总计 Tokens: {chunk.usage.total_tokens}")
    yield f"data: [DONE]\n\n"
    # full_response = "".join(content_parts)
    # print(f"\n--- 完整回复 ---\n{full_response}")

from fastapi.responses import StreamingResponse
@chat_router.get("/chat_stream")
def chat_stream(message: str):
    return StreamingResponse(get_stream(message), media_type="text/event-stream", headers={"Cache-Control": "no-cache", "Connection": "keep-alive"})

@chat_router.post("/mestype")
async def mestype():
    category = await MessageCategory.create(name="新对话",user_id=1)
    return {"code":200,"typeid":category.id}


# 定义工具列表
tools = [
       {
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "description": "获取当前天气信息",
            "parameters": {
              "type": "object",
              "properties": {"location": {"type": "string"}},
              "required": ["location"]
            }
          }
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "获取当前时间",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },
        {
          "type": "function",
          "function": {
            "name": "get_order_info",
            "description": "获取订单信息",
            "parameters": {
              "type": "object",
              "properties": {"order_id": {"type": "string"}},
              "required": ["order_id"],
            }
          }
        }
      ]

# 模拟天气查询工具
def get_current_time(arguments):
    return f'当前时间是：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

# 模拟订单查询工具
def get_current_weather(arguments):
    weather_conditions = ["晴天", "多云", "雨天"]
    random_weather = random.choice(weather_conditions)
    location = arguments["location"]
    return f"{location}今天是{random_weather}。"

def get_order_info(arguments):
    order_id = arguments["order_id"]
    return f"订单{order_id}的信息如下：订单金额为100元，订单状态为已支付。"

tools_dict = {'get_current_weather': get_current_weather, 'get_order_info': get_order_info, 'get_current_time': get_current_time}

#封装响应函数
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen3.6-plus",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools
    )
    return completion

messages = []
current_typeid = 0

@chat_router.get("/chat_ask222")
async def chat_ask222(message: str,typeid: int,imgurl: str = None):
    global messages
    global current_typeid
    userid = 1
    if current_typeid != typeid:
        messages = []
    messages = [{"role": "user", "content": message}]
    response = get_response(messages)
    assistant_output = response.choices[0].message
    if assistant_output.tool_calls is None:
        print(f'无需调用工具，直接回复：{assistant_output.content}')
        messages.append(assistant_output)
    else:
        #进入工具调用循环
        while assistant_output.tool_calls is not None:
            tool_call = assistant_output.tool_calls[0]
            tool_call_id = tool_call.id
            func_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"工具调用：{func_name}参数：({arguments})")
            #执行工具
            tool_result = tools_dict[func_name](arguments)
            #构造工具返回信息
            tool_message = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": tool_result
            }
            print(f"工具返回：{tool_message['content']}")
            messages.append(tool_message)
            #调用模型
            response = get_response(messages)
            assistant_output = response.choices[0].message
            if assistant_output.content is None:
                assistant_output.content = ""
                messages.append(assistant_output)
            print(f"模型最终回复：{assistant_output.content}")
    
    await Message.create(content=message,message_category_id=typeid,role="user")
    await Message.create(content=assistant_output.content,message_category_id=typeid,role="assistant")
    if current_typeid != typeid:
        category = await MessageCategory.filter(id=typeid).first()
        if category and category.name == "新对话":
            category.name = message
            await category.save()
            value = json.dumps({'cateid':typeid,'name':message,'time':int(time.time())})
            r.zadd('message_history'+str(userid),int(time.time()),value)
            #只保留最近10个历史记录
            # r.zremrangebyrank('message_history'+str(userid),0,-4)
        current_typeid = typeid
    return {"code": 200, "message": assistant_output.content}

@chat_router.get("/get_message_history")
async def get_message_history():
    userid = 1
    history = r.zrevrange('message_history'+str(userid),0,-1)
    hislist = []
    for item in history:
        item = json.loads(item.decode('utf-8'))
        value = int(int(time.time())-int(item['time'])/60)
        item['time'] = value
        hislist.append(item)
    return {"code": 200, "hislist": hislist}

@chat_router.get("/get_message_bycate")
async def get_message_bycate(typeid: int):
    messages = await Message.filter(message_category_id=typeid).all()
    return {"code": 200, "messages": messages}



# 流式响应
@chat_router.get("/chat_ask_stream")
async def chat_ask_stream(message: str,typeid: int):
    global messages
    global current_typeid
    userid = 1
    if current_typeid != typeid:
        messages = []
        # 从数据库加载历史消息
        history = await Message.filter(message_category_id=typeid).order_by("create_time").all()
        for h in history:
            messages.append({"role": h.role, "content": h.content})
    messages.append({"role": "user", "content": message})
    assistant_output = ""

    while True:
        stream = client.chat.completions.create(
            model="qwen3.6-plus",
            extra_body={"enable_thinking": False},
            messages=messages,
            tools=tools,
            stream=True
        )
        tool_calls = None
        for chunk in stream:
            if not chunk.choices:
                if chunk.usage:
                    print('token用量',chunk.usage)
                continue
            delta = chunk.choices[0].delta
            #正常文本直接流式返回
            if delta.content:
                assistant_output += delta.content
                yield  f"{delta.content}\n\n"
            #收集工具调用信息
            if delta.tool_calls:
                if tool_calls is None:
                    tool_calls = []
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx >= len(tool_calls):
                        tool_calls.append({"id":"", "function":{"name":"","arguments":""}})
                    curr = tool_calls[idx]
                    curr["id"] = tc.id or curr["id"]
                    curr["function"]["name"] = tc.function.name or curr["function"]["name"]
                    curr["function"]["arguments"] += tc.function.arguments or ""
        #如果没有工具调用，直接返回
        if not tool_calls:
            break

        #执行工具
        for tc in tool_calls:
            func_name = tc["function"]["name"]
            arguments = json.loads(tc["function"]["arguments"] or "{}")
            if func_name == "get_current_time":
                res = tools_dict[func_name]()
            else:
                res = tools_dict[func_name](arguments)

    yield "data: [DONE]\n\n"
    messages.append({"role": "assistant", "content": assistant_output})
    await Message.create(content=message,message_category_id=typeid,role="user")
    await Message.create(content=assistant_output,message_category_id=typeid,role="assistant")
    if current_typeid != typeid:
        category = await MessageCategory.filter(id=typeid).first()
        if category and category.name == "新对话":
            category.name = message
            await category.save()
            value = json.dumps({'cateid':typeid,'name':message,'time':int(time.time())})
            r.zadd('message_history'+str(userid),int(time.time()),value)
            #只保留最近10个历史记录
            # r.zremrangebyrank('message_history'+str(userid),0,-4)
        current_typeid = typeid


def pic_stream_chat(message: str,pic: str = None):
    completion = client.chat.completions.create(
        model="qwen3.7-plus", # 此处以qwen3.7-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": pic}
                    },
                    {"type": "text", "text": message},
                ],
            },
        ],
        stream=True,
    )
    print(completion.choices[0].message.content)
    for chunk in completion:
        if chunk.choices:
            content = chunk.choices[0].delta.content or ""
            print("#####")
            print(content, end="", flush=True)

            # content_parts.append(content)
            yield f"data: {content}\n\n"
        elif chunk.usage:
            print("\n--- 请求用量 ---")
            print(f"输入 Tokens: {chunk.usage.prompt_tokens}")
            print(f"输出 Tokens: {chunk.usage.completion_tokens}")
            print(f"总计 Tokens: {chunk.usage.total_tokens}")

    yield f"data: [DONE]\n\n"


@chat_router.get("/chat_ask")
async def chat_ask(message: str,typeid: int,pic: str = None,video: str = None):
    # if pic:
    #     return StreamingResponse(
    #         pic_stream_chat(message,pic),
    #         media_type="text/event-stream",
    #         headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    #     )
    return StreamingResponse(
        chat_ask_stream(message,typeid),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )


#单轮文本过多
#多轮的轮数过多

#关键字提取
#字符串截取[]
#提示词

def limit_message(ask):
    history = r.get("message_history1")
    if history:
        history = json.loads(history)
        history.append({"role":"user","content":ask})
        #优化,只保留最后三轮，前所有轮对话字符串截取
        usermessage = ""
        rolemessage = ""
        now_history = history[0:-7]
        for i in now_history:
            if i['role'] == 'user':
                usermessage += i['content'][0:50]
            else:
                rolemessage += i['content'][0:50]
        input_history = history[-7:]
        input_history.append({"role":"user","content":usermessage})
        input_history.append({"role":"assistant","content":rolemessage})
        ai = get_response(input_history)
        history.append({"role":"assistant","content":ai})
    else:
        history = [{"role":"user","content":ask}]

    r.set("message_history1",json.dumps(history))