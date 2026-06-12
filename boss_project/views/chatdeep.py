from fastapi import APIRouter
from fastapi.responses import StreamingResponse

deep_router = APIRouter()

from openai import OpenAI

client = OpenAI(
    api_key="sk-efab2752c9d94425aad9fa90d310c81f",
    base_url="https://api.deepseek.com",
)


messages=[]
def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

def send_messages_stream(messages):
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        tools=tools,
        stream=True
    )

    for chunk in response:
        if chunk.choices:
            content =chunk.choices[0].delta.content
            if content:
                yield f"data: {content}\n\n"

    yield f"data: [DONE]\n\n"
      
    
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "当用户想知道天气的时候调用这个工具",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，例如北京，天津等",
                    }
                },
                "required": ["location"]
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_orders",
            "description": "当你查询订单时，调用这个工具",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "订单ID",
                    }
                },
                "required": ["order_id"]
            },
        }
    },
]

import json

def get_orders(order_id: str):
    args = json.loads(order_id)
    order_id = args["order_id"]
    return "订单状态：已支付，订单金额：100元,订单号：{}".format(order_id)

def get_weather(location: str):
   location = json.loads(location)
   location = location["location"]
   return "{}的天气是：{}".format(location, "晴,30度")

def get_result(result):     
        yield f"data: {result}\n\n"


tool_dict = {
    "get_orders": get_orders,
    "get_weather": get_weather,
}

@deep_router.get("/check_order")
def check_order(message: str):
    messages.append({"role": "user", "content": message})
    result = send_messages([{"role": "user", "content": message}])
    print(result)
    if result.tool_calls:
        name = result.tool_calls[0].function.name
        arguments = result.tool_calls[0].function.arguments
        tool_result = tool_dict[name](arguments)
        print(tool_result)
        # 工具结果加入messages，让模型生成最终回复
        messages.append({"role": "assistant", "content": None, "tool_calls": result.tool_calls})
        messages.append({"role": "tool", "tool_call_id": result.tool_calls[0].id, "content": tool_result})
        final_result = send_messages(messages)
        return StreamingResponse(get_result(final_result.content),media_type="text/event-stream",headers={"Connection": "keep-alive"})
   
    content = result.content
    if content:
        return StreamingResponse(send_messages_stream(messages),media_type="text/event-stream",headers={"Connection": "keep-alive"})
    

