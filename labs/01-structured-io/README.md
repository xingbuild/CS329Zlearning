# Structured I/O 实战教程：从裸接口到用 LLM 编程

> 配套理论：Structured I/O 的本质 = **把 LLM 的输出从"对自然语言的概率采样"
> 变成"对一个形式语言的概率采样"** —— 在概率空间（模型）与符号空间（程序）
> 之间架设类型契约。关键分工：**语法可判定（可 100% 保证），语义不可判定
> （只能逼近）**。

## 学习地图：四层机制 × 六个步骤

| 机制层 | 文件 | 演示什么 | 怎么跑 |
|---|---|---|---|
| 裸接口（问题） | `step1_raw_interface.py` | 模型原生输出是 str，8 个真实失败形态过 json.loads | `python3 step1_raw_interface.py` |
| 提示层+校验层 | `step2_prompt_and_validation.py` | 软约束的局限；json.loads（语法闸）× Pydantic（语义闸）；报错回喂修复回路 | `python3 step2_prompt_and_validation.py` |
| **解码层（核心）** | `step3_constrained_decoding.py` | 从零实现 constrained decoding：正则→Thompson NFA→ε-闭包→token 级掩码→贪心解码，三组对照实验 | `python3 step3_constrained_decoding.py` |
| 真实工具对照 | `step4_real_tools/` | llama.cpp GBNF 文法、Outlines 用法、与手写版的对应 | 读 `person.gbnf`、`outlines_demo.py` |
| 训练层（协议） | `step5_function_calling.py` | function calling 三个载荷逐字段解剖；arguments 为什么是字符串 | `python3 step5_function_calling.py`（`--live` 需 key） |
| 架构层（闭环） | `step6_mini_agent.py` | 类型化工具注册表；决策→校验→执行→观察循环；无契约对照实验 | `python3 step6_mini_agent.py`（有 `DEEPSEEK_API_KEY` 自动切真模型） |

依赖：`pydantic`（已装）。step5/step6 联网模式另需 `openai` SDK + `DEEPSEEK_API_KEY`。

## 每一步观察什么

1. **step1**：7/8 失败。模型"会"写 JSON，缺的是让它"必须"写的机制。
2. **step2**：注意第 2 次生成——语法全对、语义仍错（age=-5），说明必须有
   Pydantic 第二道闸；修复回路把失败率从 e 降到 e^k，但永远到不了零。
3. **step3**（最重要，建议精读代码）：
   - 掩码解剖：`'ice":'` 在第 5 个字符处越界 → 整个 token 作废退回单字符，
     这就是 XGrammar 解决的"token×字符粒度求交"问题的缩影；
   - 实验 B：模型想写 Python 的 `True`，掩码逼它写 `3`——保证由构造而来；
   - 实验 C：`Ada Lovelace` → `adalovelace`。语法被拯救，语义被改写；
     同时注意无掩码那次"侥幸"合法——离开文法后全靠概率，没有任何保证。
4. **step4**：GBNF/Outlines/strict 模式与你手写的是同一个机制的不同包装。
5. **step5**：`arguments` 是字符串不是对象；schema 一份三吃（菜单/文法/校验）。
6. **step6**：`validate=False` 的对照运行——`摄氏度` 直接击穿确定性代码。
   契约是"模型生成数据，代码解释执行"得以成立的前提。

## 一个值得记住的演进逻辑

```
prompt 里求它（软，概率保证）          → step1~2
解码时逼它（硬，构造保证）              → step3~4
训练它+服务端打包成协议（产品化）       → step5
在协议上盖架构（agent = 契约化边界）    → step6
```

## 延伸阅读

- Outlines 论文：Willard & Louf, *Efficient Guided Generation for Large Language Models* (2023) —— 正则→FSM→logit 掩码的原始表述
- XGrammar（2024）：token 级掩码的高效实现（自适应掩码、词表×文法求交）
- OpenAI *Introducing Structured Outputs in the API*（2024）：context-free grammar 编译成 FSM 的工程叙述
- llama.cpp `grammars/README.md`：GBNF 语法
- DeepSeek / OpenAI Function Calling 文档：协议细节
- 进阶练习：把 step3 的贪心解码改成带 temperature 的采样，观察"分布在合法
  集上重归一化"；或把 Pydantic 模型自动编译成 step3 的正则（schema→grammar），
  你就复刻了 outlines 的核心。

## 交互实验室（推荐先玩这个）

`structured-io-lab.html` —— 双击用浏览器打开即可，无需任何环境：
六个章节，问题先行：第 0 章先讲根本问题（含 P(合法) 成本计算器），随后裸接口失败动物园 / 两道闸门修复回路剧场 / **掩码解码实验室**：逐 token
步进看 FSM 掩蔽 / 工具协议解剖 / Agent 闭环剧场：开关契约闸门看崩溃分支）。
全部逻辑在浏览器本地运行，其中掩码解码引擎与 `step3` 的 Python 实现逐行对应。
