"""
第 2 步：软约束（prompt 里给 schema）+ 校验层（Pydantic + 修复回路）
====================================================================

理论对应：
  - 提示层（软约束）：把 schema 写进 prompt，靠模型的形式语言先验。
    成功率高但非 100%——约束只存在于"模型的注意力"里，不存在于解码过程里。
  - 校验层（回路）：语法用 json.loads 兜，语义用 Pydantic 兜（范围/枚举/必填），
    失败把【报错原文】回喂给模型重试。这就是语义层的"编译器报错 -> 改代码"循环。

关键分工再演示一次：
  json.loads  只能管【语法】     —— 这是可判定问题，机器可 100% 保证
  Pydantic    还能管【语义】     —— age>=0、枚举值、字段必填，这些 schema
                                    约束能表达的部分；再往上的"答案对不对"
                                    机器永远无法保证，只能逼近

运行：python3 step2_prompt_and_validation.py
"""

import json
from typing import Literal

from pydantic import Field, ValidationError
from mock_llm import ScriptedLLM

# ---------------------------------------------------------------
# 契约：一个 Pydantic 模型 = 一份同时给人和给机器看的 schema
# ---------------------------------------------------------------
from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int = Field(ge=0, le=150)          # 语义约束：0 <= age <= 150
    mood: Literal["happy", "neutral", "sad"]  # 语义约束：封闭枚举


SYSTEM_PROMPT = """你是结构化输出助手。必须只输出一个 JSON 对象，不要任何其他文字。
格式：{"name": <字符串>, "age": <整数>, "mood": "happy"|"neutral"|"sad"}"""


# ---------------------------------------------------------------
# 第一部分：失败动物园（语法失败 vs 语义失败）
# ---------------------------------------------------------------
def failure_zoo():
    print("=" * 72)
    print("第 2 步 · 第一部分：两类失败 —— 语法 vs 语义")
    print("=" * 72)
    cases = [
        ("围栏包裹", '```json\n{"name":"Alice","age":30,"mood":"happy"}\n```'),
        ("类型错：age 是字符串", '{"name":"Alice","age":"thirty","mood":"happy"}'),
        ("语义错：age 为负", '{"name":"Alice","age":-5,"mood":"happy"}'),
        ("语义错：枚举外取值", '{"name":"Alice","age":30,"mood":"ecstatic"}'),
        ("缺字段", '{"name":"Alice","age":30}'),
    ]
    for desc, raw in cases:
        try:
            data = json.loads(raw)          # 第一道闸：语法
            stage = "json.loads 通过"
        except json.JSONDecodeError as e:
            print(f"\n[{desc}] -> 死在【语法闸】json.loads：{e.msg}")
            continue
        try:
            Person.model_validate(data)     # 第二道闸：语义
            print(f"\n[{desc}] -> 两道闸都通过")
        except ValidationError as e:
            first = e.errors()[0]
            print(f"\n[{desc}] -> 语法 OK，死在【语义闸】Pydantic："
                  f"字段 {first['loc']} {first['msg']}")


# ---------------------------------------------------------------
# 第二部分：修复回路 —— 把报错当对话喂回去
# ---------------------------------------------------------------
def structured_generate(llm, task: str, model_cls, max_retries: int = 3):
    """通用的'带校验的生成'回路。生产代码就是这个形状（换掉 llm 即可）。"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]
    for attempt in range(1, max_retries + 1):
        print(f"\n---- 第 {attempt} 次生成 ----")
        raw = llm(messages)
        print(f"  模型输出: {raw!r}")
        try:
            data = json.loads(raw)                       # 语法闸
            obj = model_cls.model_validate(data)         # 语义闸
            print(f"  两道闸通过 -> {obj!r}")
            return obj
        except json.JSONDecodeError as e:
            err = f"输出不是合法 JSON（{e.msg}），只输出 JSON 本体，不要围栏/注释/多余文字。"
        except ValidationError as e:
            err = f"JSON 合法但违反约束：{e}。请修正后重新只输出 JSON。"
        print(f"  校验失败 -> 回喂报错：{err[:80]}...")
        messages += [
            {"role": "assistant", "content": raw},
            {"role": "user", "content": err},            # 报错原文回喂
        ]
    raise RuntimeError("修复回路超过重试上限")


def repair_loop_demo():
    print()
    print("=" * 72)
    print("第 2 步 · 第二部分：修复回路（报错 -> 回喂 -> 重试）")
    print("=" * 72)

    # 剧本：真实模型在此场景的典型三连
    #   第1次：围栏+注释（聊天本能）
    #   第2次：形式修好了，但 age=-5 还在（模型修语法不修语义，非常真实）
    #   第3次：报错点名 age 后才修对
    llm = ScriptedLLM([
        '```json\n{"name": "Alice", // 姓名\n "age": -5, "mood": "happy"}\n```',
        '{"name": "Alice", "age": -5, "mood": "happy"}',
        '{"name": "Alice", "age": 30, "mood": "happy"}',
    ])

    person = structured_generate(llm, "描述 Alice，30 岁，心情不错", Person)
    print()
    print(f"最终产物（类型化对象，不再是 str）：{person}")
    print(f"可以直接当 Python 对象用：name={person.name!r}, age+1={person.age + 1}")
    print()
    print("要点：")
    print("  1) 回路把'一次性的概率事件'变成'带反馈的收敛过程'——失败率从 e")
    print("     降到 e^k（k 次重试），但永远到不了零：这是校验层的天花板。")
    print("  2) 注意第 2 次生成：语法全对、语义仍错。json.loads 管不了这个，")
    print("     这就是必须有 Pydantic 这第二道闸的原因。")
    print("  3) 每次重试都要再付一次推理的钱和延迟——这正是第 3 步")
    print("     '把保证移进解码过程'的动机：与其事后返工，不如事前不可能出错。")


if __name__ == "__main__":
    failure_zoo()
    repair_loop_demo()
