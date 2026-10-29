"""
第 5 步：Function Calling 协议解剖（训练层 + 各层打包）
=======================================================

理论对应：厂商用 SFT/RLHF 专门训练模型输出工具调用格式（特殊 token 分隔），
服务端再用 constrained decoding 兜底 + 解析校验。你从 API 拿到的
tool_calls 已经是解析好的结构——训练层把前四层的机制打包成了协议。

运行：python3 step5_function_calling.py            # 离线：解剖协议载荷
      DEEPSEEK_API_KEY=sk-... python3 step5_function_calling.py --live
                                                     # 在线：真调一次（两轮）
"""

import json
import os
import sys

# ---------------------------------------------------------------
# 载荷 1：请求 —— tools 数组就是"菜单"，parameters 是 JSON Schema
# ---------------------------------------------------------------
REQUEST = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "北京现在多少度？用摄氏度。"}
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询指定城市当前天气",
                # ★ 契约本体：JSON Schema。它同时是 (a) 给模型看的菜单说明
                #   (b) 服务端 constrained decoding 的文法来源（strict 模式）
                #   (c) 客户端二次校验的依据。一份 schema，三处消费。
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string", "description": "城市名"},
                        "unit": {"type": "string",
                                 "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["city", "unit"],
                },
            },
        }
    ],
    "tool_choice": "auto",   # 'auto' 模型自己决定；'required' 必须调用；
                             # {'type':'function',...} 指定必须调哪个
}

# ---------------------------------------------------------------
# 载荷 2：响应 —— 注意 arguments 是【字符串】不是对象！
# ---------------------------------------------------------------
RESPONSE = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": None,          # 调用工具时正文通常为空
                # ★ 模型实际逐 token 生成的是一段 JSON 文本，被特殊 token
                #   包围；服务端解析后放到这里。你拿到的已经是"第4步的产物"
                "tool_calls": [
                    {
                        "id": "call_0_abc123",
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            # ★ 注意：是 str！模型生成它时和生成普通文本
                            #   没有本质区别，只是在文法约束 + 专门训练下
                            #   逐 token 写出来的
                            "arguments": "{\"city\": \"北京\", \"unit\": \"celsius\"}",
                        },
                    }
                ],
            },
            "finish_reason": "tool_calls",   # 停止原因都变成了协议的一部分
        }
    ]
}

# ---------------------------------------------------------------
# 载荷 3：第二轮 —— 工具结果以 role='tool' 回喂，形成闭环
# ---------------------------------------------------------------
SECOND_ROUND_MESSAGES = [
    {"role": "user", "content": "北京现在多少度？用摄氏度。"},
    {"role": "assistant", "content": None,
     "tool_calls": [{"id": "call_0_abc123", "type": "function",
                     "function": {"name": "get_weather",
                                  "arguments": "{\"city\": \"北京\", \"unit\": \"celsius\"}"}}]},
    # ★ 结构化观察：你代码里的 dict，序列化成 JSON 文本回喂。
    #   模型的输入侧同样是"结构化 -> 文本化"。
    {"role": "tool", "tool_call_id": "call_0_abc123",
     "content": "{\"city\": \"北京\", \"unit\": \"celsius\", \"temp\": 18, \"condition\": \"晴\"}"},
]


def anatomy():
    print("=" * 72)
    print("第 5 步：Function Calling 协议解剖")
    print("=" * 72)
    for title, payload, notes in [
        ("载荷 1 · 请求（tools 即菜单，schema 即契约）", REQUEST, None),
        ("载荷 2 · 响应（arguments 是字符串！）", RESPONSE, None),
        ("载荷 3 · 第二轮消息（结构化观察回喂）", SECOND_ROUND_MESSAGES, None),
    ]:
        print(f"\n---- {title} ----")
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    print(
        "\n读载荷的正确姿势：\n"
        "  1) tools[].function.parameters 就是 JSON Schema——和 step2 的 Pydantic、\n"
        "     step3 的正则、step4 的 GBNF 是同一种东西的不同写法：契约。\n"
        "  2) arguments 是 str 不是 dict。它由模型逐 token 生成（训练+服务端\n"
        "     约束保证其形态），客户端仍然要 json.loads——这一步永远存在。\n"
        "  3) role='tool' 的消息是你的确定性代码产出的结构化观察。\n"
        "     于是 agent loop = 结构化决策 -> 确定性执行 -> 结构化观察 -> 循环，\n"
        "     这正是第 6 步要跑起来的东西。\n"
    )


# ---------------------------------------------------------------
# 在线模式：真的调 DeepSeek API 走完两轮
# ---------------------------------------------------------------
def live():
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        sys.exit("需要 DEEPSEEK_API_KEY 环境变量")
    from openai import OpenAI
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

    msgs = REQUEST["messages"]
    resp = client.chat.completions.create(
        model="deepseek-chat", messages=msgs,
        tools=REQUEST["tools"], tool_choice="auto")
    tc = resp.choices[0].message.tool_calls[0]
    print("模型选择:", tc.function.name)
    args = json.loads(tc.function.arguments)     # 永远要走的解析一步
    print("解析后的参数:", args)

    result = {"city": args["city"], "temp": 18, "condition": "晴"}  # 假装执行了
    msgs += [{"role": "assistant", "content": None,
              "tool_calls": [tc.model_dump()]},
             {"role": "tool", "tool_call_id": tc.id,
              "content": json.dumps(result, ensure_ascii=False)}]
    final = client.chat.completions.create(
        model="deepseek-chat", messages=msgs)
    print("最终回答:", final.choices[0].message.content)


if __name__ == "__main__":
    if "--live" in sys.argv:
        live()
    else:
        anatomy()
