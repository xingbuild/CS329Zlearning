"""
第 4 步（阅读件）：三个生产级工具的对照
========================================

step3 你手写了"正则 -> NFA -> 掩码"全链路。这个文件对照三件真实武器，
它们做的是同一件事，只是工程化程度不同：

  1) llama.cpp GBNF        —— 见同目录 person.gbnf（文法文件 + 推理时编译）
  2) Outlines（2023 论文） —— 把正则/JSON Schema 编译成生成自动机，
                              拦截模型的 logits_to_tokens 钩子做掩码
  3) JSON Schema strict    —— OpenAI/DeepSeek 结构化输出：厂商在服务端
                              替你做 constrained decoding + 解析校验

Outlines 用法（需要 pip install outlines，且要有本地小模型才能跑，这里作为
精确可抄的阅读件）：

    import outlines

    model = outlines.from_transformers(...)   # 或 from_llama_cpp(...)

    # 正则引导：等价于 step3 的 GRAMMAR，Outlines 内部编译成 FSM
    @outlines.generate(model, regex=r'\{"name": *"[a-z]+", *"age": *[0-9]+\}')
    def make_person(topic: str): ...

    # JSON Schema 引导：schema 即契约（和 function calling 用的是同一种 schema）
    from pydantic import BaseModel

    class Person(BaseModel):
        name: str
        age: int

    generator = outlines.generate.json(model, Person)
    person = generator("描述一个人物")     # 返回的就是 Person 实例

要点：outlines.generate(regex=...) 返回的不是普通函数，而是一个【被文法
劫持了的采样器】——每次采样前，当前 FSM 状态算出合法 token 集，把其余
logit 置 -inf。你在 step3 已经手写过这行代码的迷你版。
"""

print(__doc__)
