---
title: L05 · 外部资源与视频
---

# L05 · 外部资源与视频

> [← 返回 L05 课文](/l05/) · 2026-10-30 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L05 课文的**外部对照实验室**。先说一句坦诚的话：**L05 是选型层的讲次，这个领域几乎没有成熟的可视化交互件**——学问不在几何空间里，在**别人的代码与判据文章**里。所以本页的主角是**课程、演讲与一手 repo 实物**（演讲 1 + 课程 2 + repo 4 + 文档展开 1 + 交叉引用 1，共 9 条）；DSPy/LangGraph/Temporal/LangFuse/LangSmith 官方文档已挂课文延伸阅读，此处不重复。

## 先做这三个动手任务

::: tip 任务 ① · 在别人的 100 行里找出五个零件
打开 [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) 的源码，读它的 agent 主类（约 100 行）：把课文复刻清单的五个零件——**状态对象 / 工具注册表 / 循环壳 / 错误回喂 / 重试预算**——各对应到哪几行。找齐之后，"看穿框架"这四个字对你就不再是口号——这是复刻检验题的现实版。
:::

::: tip 任务 ② · 用一张表判"什么时候你会选它"
对照 [Pi](https://github.com/earendil-works/pi) 与 [OpenClaw](https://github.com/openclaw/openclaw) 的工具清单：一个 4 件套极简 vs 一个 Gateway + 20+ 消息通道全都要——给两边各写一行"换来什么 / 付出什么 / 什么时候你会选它"。这是课文思考题 3 的扩展：**两种哲学背后是两种完全不同的用户**，判据永远比立场有用。
:::

::: tip 任务 ③ · 把整门课装进一个隐喻
看 Karpathy 演讲里的 **LLMOS 隐喻（LLM = CPU、context = RAM、工具 = 外设）**，然后把本课程八讲各映射到 CPU / RAM / 外设 / 进程的哪个位置——放得进去，说明你手里已经有了整门课的一张图（可对照站内[技术谱系图](/lineage/)自检）。
:::

## 第一幕 · 工程三支柱与 Agency 光谱

- Karpathy：[Software Is Changing (Again)](https://www.ycombinator.com/library/MW-andrej-karpathy-software-is-changing-again) **（演讲 · YC AI Startup School 2025-06）**——Software 1.0/2.0/3.0 三范式与 LLMOS 隐喻：整讲的宇宙观级开胃菜，harness 与编排为什么存在的全景解释（YC Library 页内嵌视频与文字稿）。

## 第二幕 · 两大工作流抽象——DSPy 与 LangGraph

- [DSPy 官方文档](https://dspy.ai) **（文档 · 动手）**——"Program, don't prompt"的出处：Signatures / Modules / Optimizers（BootstrapFewShot / MIPROv2 / GEPA）指南——课文"50 行复刻 Optimizer"的官方对照（延伸阅读已挂此链，此处展开定位）。
- DeepLearning.AI：[AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) **（免费短课 · 1h42m · Harrison Chase）**——先**手写**一个 agent、再用 LangGraph 重建一遍——课程结构与课文论点完全同构：**框架没有发明新机制，只是给手写循环加了语法与配套**。
- [挑战 19 分钟搞定：LangGraph 快速入门与原理剖析](https://www.bilibili.com/video/BV1HVFLzfEeS) **（中文视频 · B 站 · 敲代码的码农）**——State / Node / Edge 四原语的中文速览；先自己写完 lab01 闭环再看，"语法糖"三个字会自己浮出来。

## 第三幕 · Agent Harness——四个一手 repo

- [mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent) **（repo · 约 9k★）**——约 100 行核心、bash 唯一工具、SWE-bench Verified >74%——"极简 → 评测变量最少"哲学的实物；动手任务 ① 的场地。
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) **（repo · 约 92k★）**——事件溯源架构的编码 agent 平台——课文"可回放调试"的出处、事件溯源的工业级形态（L05 手写版在第四幕，对照食用）。
- [Pi](https://github.com/earendil-works/pi) **（repo · 约 119k★）**——Mario Zechner 的极简 harness：4 件套工具、树状历史、无权限系统——"最小骨架 + 好的系统提示就能打"的证明。（repo 已从 badlogic/pi-mono 迁移至 earendil-works，旧链仍自动重定向；官方文档 pi.dev 已挂延伸阅读。）
- [OpenClaw](https://github.com/openclaw/openclaw) **（repo · 约 393k★）**——常驻型个人助理：Gateway + 20+ 消息通道 + 本地数据 + 夜间记忆整理——"跨会话人格"的实物样本；它的 AGENTS.md 注入与本站连续性机制同构（课文第三幕已点破）。

## 第四、五幕 · 编排、遥测与判据

- （交叉引用）Anthropic：[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) **（判据文 · 2024-12）**——其"workflow vs agent"判据正对 L05 第一幕的光谱定档问题。**主放 [L06 资源页](/l06/resources/)**（五模式出处），此处一行交叉引用；一句话提醒：**判据仍在，工具名会旧**——这本身就是"爬你自己的山"的又一证。
