"""
第 6 步：Mini Agent —— "模型生成数据，代码解释执行"的完整闭环
==============================================================

理论对应：用 LLM 编程的根本架构模式。
  Agent = 概率核心（LLM）+ 确定性脚手架（代码）+ 边界上的类型契约。

本文件实现一个最小但五脏俱全的 agent：
  - 工具注册表：每个工具 = (名字, Pydantic 参数模型, 确定性执行函数)。
    schema 同时是【给模型的菜单】和【运行时的校验器】——一份契约两处消费。
  - 决策协议：模型输出 {"action": "call_tool"|"final", ...} 的 JSON。
  - 循环：结构化决策 -> 校验 -> 确定性执行 -> 结构化观察回喂 -> ... -> final。

默认用 ScriptedLLM 离线跑（剧本取自真实模型行为）；设置 DEEPSEEK_API_KEY
则自动切真模型。

对照实验：validate=False 时跳过 Pydantic 闸门，看一个非法参数如何击穿
确定性代码——这就是"没有契约的 agent"的日常。
"""

import json
import os
from types import SimpleNamespace
from typing import Literal, Optional

from pydantic import BaseModel, Field

from mock_llm import ScriptedLLM


# =====================================================================
# 一、工具层：类型化的注册表（schema 即契约）
# =====================================================================
class WeatherArgs(BaseModel):
    city: str
    unit: Literal["celsius", "fahrenheit"]   # 封闭枚举


def get_weather(a: WeatherArgs) -> dict:
    label = {"celsius": "°C", "fahrenheit": "°F"}[a.unit]   # 确定性代码，
    return {"city": a.city, "temp": f"18{label}",          # 只认契约内的输入
            "condition": "晴"}


class ReportArgs(BaseModel):
    to: str = Field(description="收件人")
    summary: str


def send_report(a: ReportArgs) -> dict:
    return {"sent": True, "to": a.to, "bytes": len(a.summary)}


REGISTRY = {"get_weather": (WeatherArgs, get_weather),
            "send_report": (ReportArgs, send_report)}


class FinalAnswer(BaseModel):
    answer: str
    used_tools: list[str]


# =====================================================================
# 二、决策协议与循环
# =====================================================================
SYSTEM = """你是天气助手。每轮只输出一个 JSON 对象，两种形态之一：
调用工具: {"action": "call_tool", "tool": <名字>, "arguments": {<参数>}}
最终回答: {"action": "final", "answer": <字符串>, "used_tools": [<工具名>]}
可用工具及其参数 schema：""" + json.dumps(
    {n: m.model_json_schema()["properties"] for n, (m, _) in REGISTRY.items()},
    ensure_ascii=False)


def run_agent(llm, task: str, validate: bool = True, max_turns: int = 8):
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": task}]
    for turn in range(1, max_turns + 1):
        print(f"\n======== 第 {turn} 轮 ========")
        raw = llm(messages)
        print(f"[决策·原文] {raw}")
        try:
            data = json.loads(raw)                                # 语法闸
        except json.JSONDecodeError as e:
            messages += [{"role": "assistant", "content": raw},
                         {"role": "user", "content": f"不是合法 JSON：{e}。重输出。"}]
            continue
        if data.get("action") == "final":
            ans = FinalAnswer.model_validate(data)
            print(f"[最终] {ans.answer}（used_tools={ans.used_tools}）")
            return ans
        tool_name = data.get("tool")
        if tool_name not in REGISTRY:
            messages += [{"role": "assistant", "content": raw},
                         {"role": "user", "content": f"没有工具 {tool_name!r}，可选：{list(REGISTRY)}"}]
            continue
        args_model, fn = REGISTRY[tool_name]
        try:
            # validate=False 时用 SimpleNamespace 直通——不校验，脏数据
            # 原样流进确定性代码，等下看它死在哪里
            args = (args_model.model_validate(data["arguments"]) if validate
                    else SimpleNamespace(**data["arguments"]))
        except Exception as e:  # noqa: BLE001 —— 演示用：校验失败统一走修复
            print(f"[校验] ✗ {type(e).__name__}: {str(e).splitlines()[0]}")
            messages += [{"role": "assistant", "content": raw},
                         {"role": "user", "content": f"参数违反 schema：{e}。修正后重发。"}]
            continue
        print(f"[{'校验 ✓ 参数合法' if validate else '闸门关闭·直通'}] {args}")
        try:
            result = fn(args)                                     # 确定性执行
        except Exception as e:  # noqa: BLE001
            print(f"[执行] 💥 确定性代码被非法输入击穿：{type(e).__name__}: {e}")
            return None
        print(f"[执行] {tool_name} -> {result}")
        messages += [{"role": "assistant", "content": raw},
                     {"role": "user", "content":
                      f"工具结果：{json.dumps(result, ensure_ascii=False)}。继续。"}]
    return None


# =====================================================================
# 三、真实 LLM 适配（有 key 就用）
# =====================================================================
def make_llm():
    key = os.environ.get("DEEPSEEK_API_KEY")
    if not key:
        return None
    from openai import OpenAI
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com")

    def llm(messages):
        resp = client.chat.completions.create(
            model="deepseek-chat", messages=messages,
            response_format={"type": "json_object"})   # 厂商侧约束（软→硬之间）
        return resp.choices[0].message.content

    return llm


def main():
    print("=" * 72)
    print("第 6 步：Mini Agent —— 结构化决策 -> 确定性执行 -> 结构化观察")
    print("=" * 72)

    real = make_llm()
    if real:
        print("检测到 DEEPSEEK_API_KEY，使用真实模型")
        run_agent(real, "北京天气如何？把结果发给 boss")
        return

    # 剧本：真实模型的典型轨迹 —— 第一次单位用中文（枚举外），被校验打回
    good_llm = ScriptedLLM([
        '{"action": "call_tool", "tool": "get_weather", "arguments": {"city": "北京", "unit": "摄氏度"}}',
        '{"action": "call_tool", "tool": "get_weather", "arguments": {"city": "北京", "unit": "celsius"}}',
        '{"action": "call_tool", "tool": "send_report", "arguments": {"to": "boss", "summary": "北京 18°C 晴"}}',
        '{"action": "final", "answer": "北京今天 18°C，晴。报告已发给 boss。", "used_tools": ["get_weather", "send_report"]}',
    ])
    print("\n【运行一】带契约（Pydantic 闸门开启）")
    result = run_agent(good_llm, "北京天气如何？把结果发给 boss")
    assert result is not None

    print("\n" + "=" * 72)
    bad_llm = ScriptedLLM([
        '{"action": "call_tool", "tool": "get_weather", "arguments": {"city": "北京", "unit": "摄氏度"}}',
    ])
    print("【运行二】无契约对照（validate=False，同样的第一条决策）")
    print("           —— 没有闸门会怎样？")
    crashed = run_agent(bad_llm, "北京天气如何？", validate=False) is None
    print()
    if crashed:
        print("结论：校验层不是官僚主义——它是确定性代码的护栏。契约（schema）")
        print("在边界上把概率世界的脏数据挡在外面，工具实现才可以假设输入总是对的。")
        print("这就是'模型生成数据，代码解释执行'能成立的前提：解释器信任输入，")
        print("因为契约在前面挡过一道。")


if __name__ == "__main__":
    main()
