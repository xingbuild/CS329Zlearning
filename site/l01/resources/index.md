---
title: L01 · 外部资源与视频
---

# L01 · 外部资源与视频

> [← 返回 L01 课文](/l01/) · 2026-10-30 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L01 课文的**外部对照实验室**。先说一句坦诚的话：**L01 的主角是"控制流"这个抽象概念**，交互可视化天然稀少（页内的接线剧场与误差复利计算器就是本域最直观的形态）——所以本页以**框架文章、一手出处与免费课程**为主：开山框架文一篇、判据出处两篇、作者本人一处、评估批评论文一篇、免费课程一门、实践随笔一位，按课文四幕对位。ReAct arXiv / BAIR / HAL / Sutton & Barto 已挂课文延伸阅读，此处只做展开定位。

## 先做这三个动手任务

::: tip 任务 ① · 两张解剖图对读
读 [Lilian Weng 的开山框架文](https://lilianweng.github.io/posts/2023-06-23-agent/)，把她的四件套（Planning / Memory / Tools / Action）与课文第二幕的**五大件**（LLM Core / 推理 / 记忆 / 工具 / 环境）逐项对照——找出两边各有一个对方没有的部件（提示：一边有"环境"，一边把"规划"单列）。分类学差异暴露的是**看问题的切口**，不是对错。
:::

::: tip 任务 ② · 去 HAL 仪表盘找一个"能力-可靠性落差"
打开 [HAL 仪表盘](https://hal.cs.princeton.edu)，任选一个模型，找到它的 consistency（同任务多次运行一致率）显著低于 capability（单点能力）的区间——然后用这个数据回答课文思考题 3 的延伸：**哪类任务上 pⁿ 现象最刺眼**？"能力涨得快、可靠性涨得慢"就是这条缝。
:::

::: tip 任务 ③ · 用"Agents That Matter"的批评清单审一遍 Lab 01
读 [AI Agents That Matter](https://arxiv.org/abs/2407.01502) 的摘要与引言（agent 评估的系统性问题：成本不计、基线不公、过拟合基准……），拿它当 checklist 审 [Lab 01](/l04/lab/)：我们的 pass^k 口径避开了其中哪几条、还有哪几条没躲开？——**评估自己的评估**，是这门课给你的第一件元工具。
:::

## 开场与第三幕 · 控制流与那一刀

- Berkeley BAIR：[The Shift from Models to Compound AI Systems](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/) **（判据文 · 2024-02）**——课文第三幕那一刀（workflow vs agent 皆 compound system）的直接出处（延伸阅读已挂链，此处展开定位）。
- Simon Willison：[Agents 随笔合集](https://simonwillison.net/tags/agents/) **（实践博客 · 持续更新）**——Django 作者、llm 工具作者的 agent 一线手记：从"到底什么算 agent"的较真到工具设计的实战细节——**工程师视角的 L01 长期参考文献**。

## 第一、二幕 · 循环五十年与解剖图

- Lilian Weng：[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) **（开山框架文 · 2023-06）**——"agent = LLM + Planning + Memory + Tools"这个流传最广的解剖框架的出处；配图被无数后续文章转引。读它等于给课文第二幕的五部件找一个平行参照系。
- [ReAct 项目页](https://react-lm.github.io/) **（项目页 · 官方）**——ReAct 原文作者团队的主页：论文、代码、HotpotQA demo——课文轨迹语法 `Thought/Act/Obs` 的一手现场（站内已有[34 段全文精读](/l01/readings/react/)，此处给的是原生物）。
- Shunyu Yao：[个人主页](https://shunyuyao.github.io/) **（作者主页）**——ReAct 一作的 research 页：从 ReAct 到 Tree of Thoughts 到 SWE-agent——**一个人串起这门课的半条主线**，值得知道他是谁、在看什么。

## 第四幕 · 四大挑战的实证现场

- Princeton：[HAL 仪表盘](https://hal.cs.princeton.edu) **（交互榜单）**——Holistic Agent Leaderboard：能力与可靠性并排量——"能力涨得快、可靠性涨得慢"（课文 p.63）的原始数据现场（延伸阅读已挂链，此处展开定位）。
- Kapoor et al.：[AI Agents That Matter](https://arxiv.org/abs/2407.01502) **（论文 · NeurIPS 2024）**——agent 评估方法学的批评之作：不计成本、基线不公、过拟合基准——为什么"跑分高"≠"工程可用"的系统论证。

## 动手课程

- HuggingFace：[Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) **（免费课程 · 交互）**——从 agent 概念到 smolagents 框架的免费体系课（含单元测验与结业项目）；与 Lab 01 对照着上：**它教你怎么用框架，本课程教你看穿框架**——两种视角互为校准。
