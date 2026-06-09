from fastapi import APIRouter, Request

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



from datetime import datetime
import random,json

# 模拟用户问题
USER_QUESTION = "北京天气咋样"
# 定义工具列表
tools = [
     {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
]
def bgcx(arguments):
    data = {
        "code": 200,
        "msg": "请求成功",
        -"data": {
        "姓名": "张三",
        "性别": "男",
        "出生日期": "2005年10月16日",
        "民族": "汉族",
        "学校名称": "南京工业职业技术大学",
        "层次": "本科",
        "专业": "智能制造技术",
        "学制": "4年",
        "学历类别": "普通高等教育",
        "学习形式": "普通全日制",
        "分院": "航空工程学院",
        "系所": "",
        "入学日期": "2024年09月05日",
        "学籍状态": "在籍（注册学籍）",
        "预计毕业日期": "2028年06月30日",
        "更新日期": "2025年03月30日",
        "照片信息": "https://xxx.jpg",
        "pdf": "https://xxx",
        "zxyz_code": "data:image/png;base64",
        "毕业状态": 2,
        "毕业时间": "2028年06月30日"
        },
        "exec_time": 0.076179,
        "ip": "123.123.123.123"
    }

# 模拟天气查询工具
def get_current_weather(arguments):
    weather_conditions = ["晴天", "多云", "雨天"]
    random_weather = random.choice(weather_conditions)
    location = arguments["location"]
    return f"{location}今天是{random_weather}。"

def get_current_time():
    print("获取时间")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 封装模型响应函数
def get_tool_response(messages):
    completion = client.chat.completions.create(
        model="qwen3.6-plus",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
    )
    return completion

tool_dict = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time
}

@chat_router.get("/functioncall_chat")
def functioncall_chat(message: str):
    messages = [{"role": "user", "content": message}]
    response = get_tool_response(messages)
    assistant_output = response.choices[0].message
    if assistant_output.content is None:
        assistant_output.content = ""
    messages.append(assistant_output)
    # 如果不需要调用工具，直接输出内容
    if assistant_output.tool_calls is None:
        print(f"无需调用天气查询工具，直接回复：{assistant_output.content}")
        return {"code": 200, "message": assistant_output.content}
    else:
        # 进入工具调用循环
        while assistant_output.tool_calls is not None:
            tool_call = assistant_output.tool_calls[0]
            tool_call_id = tool_call.id
            func_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"正在调用工具 [{func_name}]，参数：{arguments}")
            # 执行工具
            # tool_result = get_current_weather(arguments)
            if func_name == "get_current_time":
                tool_result = tool_dict[func_name]()
            else:
                tool_result = tool_dict[func_name](arguments)
            # 构造工具返回信息
            tool_message = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": tool_result,  # 保持原始工具输出
            }
            print(f"工具返回：{tool_message['content']}")
            messages.append(tool_message)
            # 再次调用模型，获取总结后的自然语言回复
            response = get_tool_response(messages)
            assistant_output = response.choices[0].message
            if assistant_output.content is None:
                assistant_output.content = ""
            messages.append(assistant_output)
        print(f"助手最终回复：{assistant_output.content}")
        return {"code": 200, "message": assistant_output.content}