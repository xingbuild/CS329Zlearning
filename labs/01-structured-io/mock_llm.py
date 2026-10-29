"""
ScriptedLLM：按剧本出牌的"模型"。

为什么需要它：本教程要演示的是【结构化机制本身】，而不是某个模型当天的发挥。
所以凡是需要"模型"的地方，接口统一为：

    llm(messages: list[dict]) -> str

这与 openai / deepseek SDK 的 chat 接口形状一致。把 ScriptedLLM 换成真实 API
调用（见 step5/step6 的 RealLLM），其余代码一行不改——因为对上层代码而言，
模型就是一个 str -> str 的函数，一切"结构化"都是在这层之上叠加的机制。

剧本里的每条回复都取自真实 LLM 的高频输出形态（markdown 围栏、代码注释、
Python 习惯、单位用中文等），注释里逐条标明。
"""


class ScriptedLLM:
    def __init__(self, script, name="scripted-model"):
        self.script = list(script)
        self.name = name

    def __call__(self, messages):
        if not self.script:
            raise RuntimeError("剧本演完了：真实模型不会，mock 会。")
        reply = self.script.pop(0)
        print(f"    [mock 模型吐出第 {getattr(self, 'turn', 1)} 条回复]")
        self.turn = getattr(self, "turn", 1) + 1
        return reply
