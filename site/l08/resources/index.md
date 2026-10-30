---
title: L08 · 外部资源与视频
---

# L08 · 外部资源与视频

> [← 返回 L08 课文](/l08/) · 2026-10-30 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L08 课文的**外部对照实验室**。先说一句坦诚的话：**MAS 域的可视化交互件几乎不存在**（编排拓扑已由页内 `MasTopology` 组件承载）——但这个域有一份别的域没有的黄金组合：**同一周发布的两篇正反判据文章**、**官方框架文档**与**失败研究的原始出处**。MAST / CooperBench / AutoGen / Magentic-One / 蜂群编译器 / A2A 论文已挂课文延伸阅读，本页补展开与实物。

## 先做这三个动手任务

::: tip 任务 ① · 同周对读，找出"无争议区"
先读 [Cognition 的反方檄文](https://cognition.com/blog/dont-build-multi-agents)（2025-06-12）再读 [Anthropic 的正方战报](https://www.anthropic.com/engineering/built-multi-agent-research-system)（2025-06-13）——两文发布只差一天。各用一句话写出两文的"何时拆"判据，然后对照课文 p.14 原表，指出**三个判据的交集**：那是业界无争议的地带，也是你做决策时的安全区。
:::

::: tip 任务 ② · 去正典文档里找控制权的定义
打开 [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/) 的 Handoff 章节，找出**"交接之后，原 agent 还能不能说话"**的官方回答——这是课文思考题 2（Handoff vs Agent-as-Tool 谁保留控制权）的权威版本；找到它，L01 那把"谁决定下一步"的刀就在多智能体世界里有了官方刻度。
:::

::: tip 任务 ③ · 把双账本抄成两列
读 [Magentic-One 出版页](https://www.microsoft.com/en-us/research/publication/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)并翻到论文相应章节，把**任务计划账本 / 进度账本**两本各自记什么抄成两列——这是课文 Task Ledger 的官方颗粒度，也是你复刻最小 MAS 时"共享账本"零件的参考图纸。
:::

## 开场 · 收益与代价的账本（同周对撞的两篇判据文）

- Anthropic：[How we built our multi-agent research system](https://www.anthropic.com/engineering/built-multi-agent-research-system) **（工程博客 · 2025-06-13）**——编排者-子代理架构 + 并行工具调用的实战复盘；一手数据：**多 agent 比单 agent 提升 90.2%，代价是约 15× token**——收益与代价账本的最诚实样本。
- Cognition：[Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) **（判据文 · 2025-06-12 · Walden Yan）**——反方判据：上下文碎片化、"Actions carry implicit decisions"、推荐单线程线性 agent。（域名已从 cognition.ai 迁至 **cognition.com**。）两文发布仅差一天——同一个 2025 年 6 月，业界站在同一场争论的两侧，课文开场"带着怀疑进入正题"的最佳现场。

## 第二幕 · 通信——对话、交接与协议

- [OpenAI Agents SDK 文档](https://openai.github.io/openai-agents-python/) **（正典文档）**——**Handoff（控制权转移）概念的正典出处**（vs agent-as-tool）；guardrails、sessions、tracing 一并覆盖——动手任务 ② 的场地。
- [AutoGen](https://microsoft.github.io/autogen/) **（官方框架文档 · 微软）**——"多 agent 通信 = 对话"世界观的实物：群聊 / 嵌套对话 / 层级编排，课文 p.32–35 对应框架的官方形态。

## 第三幕 · 协调——基础设施与涌现

- Microsoft Research：[Magentic-One 出版页](https://www.microsoft.com/en-us/research/publication/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/) **（出版页）**——Orchestrator + **双账本**（任务计划账本 / 进度账本）设计的官方出处；GAIA / WebArena 成绩与开源发布（aka.ms/magentic-one）。
- （课程交叉）[AI Agentic Design Patterns with AutoGen](/l06/resources/) **（站内交叉）**——其 multi-agent 章节正对本讲编排与角色分工，**主放 L06 资源页**，此处一行交叉引用。

## 第四、五幕 · 失败动物园与蜂群

- MAST（*Why Do Multi-Agent LLM Systems Fail?*）已在延伸阅读（arXiv:2503.13657）。**注意**：论文配套站 mast.systems 域名已失效（落入无关公司）——**只可用 arXiv 版**。
- Anthropic 蜂群编译器（[Building a C Compiler with an Agent Swarm](https://www.anthropic.com/engineering/building-c-compiler)）与 [A2A 协议](https://a2a-protocol.org) 均已在延伸阅读——课文第五幕六条经验即出自蜂群原文，读课文后直取原文对读效果最佳。

---

> 🏁 **八讲外部资源页至此全部集齐**（L01 · L02 · L03 · L04 · L05 · L06 · L07 · L08）——从 L02 的采样可视化到 L08 的判据对撞，每一讲都有了"学完之后去哪里动手"的去处。课程本身的闭环，见课文末"八讲之旅到此闭环"。
