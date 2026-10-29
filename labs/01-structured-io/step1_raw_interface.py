"""
第 1 步：裸接口 —— 模型的原生输出是什么，程序需要什么，差距在哪
================================================================

理论对应：LLM 的原生接口是 token 流（本质是一个 str），概率性、开放、无类型、
无语法保证。而 json.loads / 你的业务代码需要【确定性的合法 JSON】。

下面每一条都是真实 LLM 在"请输出 JSON"场景下高频产出的形态（没有加任何
结构化机制时）。我们逐条喂给 json.loads，看它死在哪里。

运行：python3 step1_raw_interface.py
"""

import json

# (编号, 形态描述, 模型原样输出)
RAW_OUTPUTS = [
    (
        "1",
        "markdown 围栏（最常见，聊天训练的产物）",
        '```json\n{"name": "Alice", "age": 30}\n```',
    ),
    (
        "2",
        "客气话开场白",
        '当然可以！以下是您要的 JSON：{"name": "Alice", "age": 30}',
    ),
    (
        "3",
        "尾随逗号（JS 习惯，JSON 不允许）",
        '{"name": "Alice", "age": 30,}',
    ),
    (
        "4",
        "代码注释（模型见多了带注释的配置文件）",
        '{\n  "name": "Alice",  // 姓名\n  "age": 30\n}',
    ),
    (
        "5",
        "中文引号（中文语境高频，肉眼几乎看不出差别）",
        '{"name": “Alice”, "age": 30}',
    ),
    (
        "6",
        "NaN（非标准扩展：Python 的 json 宽容地接受，严格解析器/jq/上游系统不认）",
        '{"name": "Alice", "age": NaN}',
    ),
    (
        "7",
        "裸 key（JS 对象字面量习惯）",
        '{name: "Alice", age: 30}',
    ),
    (
        "8",
        "终于是合法的",
        '{"name": "Alice", "age": 30}',
    ),
]

def main():
    print("=" * 72)
    print("第 1 步：裸接口 —— 直接把模型输出喂给 json.loads")
    print("=" * 72)
    ok = 0
    for no, desc, raw in RAW_OUTPUTS:
        try:
            json.loads(raw)
            ok += 1
            verdict = "✓ 解析成功"
            detail = ""
        except json.JSONDecodeError as e:
            verdict = "✗ 解析失败"
            detail = f"{e.msg}（第 {e.colno} 列附近）"
        print(f"\n案例 {no}：{desc}")
        print(f"  原样输出: {raw!r}")
        print(f"  json.loads -> {verdict} {detail}")

    print()
    print("=" * 72)
    print(f"结果：{ok}/{len(RAW_OUTPUTS)} 条可被 json.loads 接受。")
    print()
    print("三个要点：")
    print("  1) 模型的原生输出是 str，不是对象。str -> 对象 这一跳必然经过一个")
    print("     语法解析器，而解析器是全有或全无的：差一个字符，整条报废。")
    print("  2) 没有任何机制保证时，'输出合法 JSON' 是一个概率事件。")
    print("     案例概率也许高达 95%~99%，但对程序来说 99% != 100%。")
    print("  3) 注意案例 8 与案例 1-7 的差别只是【表面形态】，不是能力差别——")
    print("     模型完全'会'写 JSON，缺的是让它【必须】这么写的机制。")
    print("     这个机制怎么造，就是后面 5 步的内容。")

if __name__ == "__main__":
    main()
