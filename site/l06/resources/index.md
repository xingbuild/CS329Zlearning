---
title: L06 · 外部资源与视频
---

# L06 · 外部资源与视频

> [← 返回 L06 课文](/l06/) · 2026-10-30 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L06 课文的**外部对照实验室**。先说一句坦诚的话：**L06 是论文密集区**——四模式论文（Reflexion / CodeAct / ReWOO / LLMCompiler）与两篇上下文工程文已密集挂在课文延伸阅读，那是本讲的主战场；本页补的是**模式的工业展开与课程**——六条正选 + 一条站内交叉 + 一条 repo 交叉，条条对位四幕。

## 先做这三个动手任务

::: tip 任务 ① · 在真实系统里认出五个模式
拿着 [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) 的五模式图，去 [STORM](https://github.com/stanford-oval/storm) 的 README 里找出它各用了哪几个（提示链？并行化？编排者-工人？……）——这是讲义 p.22"一次用齐四个模式"的亲手版：**模式是半成品，看别人怎么烤熟的**。
:::

::: tip 任务 ② · 两套分类学对读，找出"对方没有"的那个
做一张对照表：LangChain 的 **Write / Select / Compress / Isolate 四分类** ↔ 课文第三幕的**卸载 / 压缩 / 遮蔽 / 隔离 / 事件日志五模式**——找出两边各有一个对方没有的模式。结论会让你吃一惊：**分类学本身就是设计视角**，两棵树长不一样，因为两家公司疼的地方不一样。
:::

::: tip 任务 ③ · 在课程代码里找到"外部反馈"那一行
看 [AutoGen 短课](https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/) 第 1 课（reflection），然后回答课文思考题 2：**"外部反馈 vs 自评"在课程的示例代码里是哪一行体现的**——找到它，你就找到了 Reflexion 与"LLM 不能自评"这两个知识点的焊点。
:::

## 第一幕 · 工作流五模式

- Anthropic：[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) **（判据文 · 2024-12）**——五模式（提示链 / 路由 / 并行化 / 编排者-工人 / 评估者-优化者）的**出处**，"augmented LLM"分层与"找最简方案"军规。页面现已带"2024 以来工具生态已变"的更新提示——**判据仍在，工具名会旧**，这恰好是课文"模式是半成品"的又一证。（延伸阅读已挂链，此处展开定位；L05 资源页交叉引用本条。）
- [STORM](https://github.com/stanford-oval/storm) **（repo · Stanford Oval）**——写维基级长文的真实系统：一次用齐提示链 + 并行化 + 编排者-工人 + 事实核查循环（讲义 p.22–29 的标本）；**用 DSPy 构建**（连回 L05 的 Optimizer 思想），`pip install knowledge-storm` 可本地复刻；官方在线 demo（storm.genie.stanford.edu）可达但有 ToS 弹窗，建议直接读 repo。

## 第二幕 · 推理与行动四模式

- DeepLearning.AI：[AI Agentic Design Patterns with AutoGen](https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/) **（免费短课 · 1h35m · Chi Wang / Qingyun Wu）**——AutoGen 两位创造者主讲的 **reflection / tool use / planning / multi-agent** 四模式课，正对课文第二幕（multi-agent 章节与 L08 交叉）。
- （站内交叉）[ReAct 论文精读](/l01/readings/react/) **（站内 · 34 段三层精读）**——四模式的老祖宗在站内已有全文精读；学本幕前先回读一遍，"行动之前先推理"会从口号变成机制。

## 第三幕 · 上下文管理五模式

- LangChain：[Context Engineering for Agents](https://www.langchain.com/blog/context-engineering-for-agents) **（图文 · 2025-07）**——**Write / Select / Compress / Isolate 四分类**（注意第四个是"隔离"不是"组合"）+ Claude Code / Cursor / Cognition 等真实系统逐个对号——讲义 p.73"LangChain 分类学"的原文（延伸阅读已挂链，此处展开定位）。
- Anthropic：[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) **（图文 · 2025-09）**——attention budget / compaction / 结构化笔记 / **just-in-time 检索** / sub-agent 架构——上下文五模式的工业级展开（延伸阅读已挂链，此处展开）。

## 第四幕 · 案例 Pi

- （repo 交叉）[Pi](https://github.com/earendil-works/pi)——极简 harness 的完整答案：4 件套工具 / 树状上下文 / 无权限哲学。**主放 L05 资源页**（四 harness 对照处），本页交叉引用——读课文第四幕后直奔它的系统提示与上下文转换代码，看"三板斧"怎么落在不到一百行里。
