---
title: L10 · 外部资源与视频
---

# L10 · 外部资源与视频

> [← 返回 L10 课文](/l10/) · 2026-11-03 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L10 课文的**外部对照实验室**。先说一句坦诚的话：**评测工程的最好教材就是真实考场本身**——本页以一手基准与框架为主（四条全部 200 验证），按课文四幕对位。

## 先做这三个动手任务

::: tip 任务 ① · 去 Terminal-Bench 挑一个任务，读它的三件套
打开 [Terminal-Bench](https://www.tbench.ai) 的任务浏览——任选一个任务，找到它的 instruction.md、environment/Dockerfile、tests/ 三件套，对照课文第一幕的解剖图：**它的验收是 outcome 断言还是过程检查？有没有参考解？**
:::

::: tip 任务 ② · 用 Harbor 的词表给自己出题
打开 [Harbor](https://harborframework.com) 文档的词表节（Task/Trial/Verifier/Trajectory/Harness）——用这五个词写一段话描述你项目里最近一次"看看效果行不行"，找出它缺了哪几件（多数人缺 Verifier 与 Trial 记录）。
:::

::: tip 任务 ③ · 读 Anthropic 的写任务纪律
读 [Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) 的任务写作节——对照课文第二幕四问，找出一条讲义没写但它强调的纪律（提示：注意它关于 flaky 与依赖钉住的段落）。
:::

## 一手基准与框架

- [Terminal-Bench](https://www.tbench.ai) **（基准 · 官网）**——bash 万能工具的世界观、64 model cards、700 万+ 次运行的任务库；[GitHub 源](https://github.com/laude-institute/terminal-bench) 可看任务的完整目录结构。
- [Harbor](https://harborframework.com) **（框架 · 客座方开源）**——eval-driven development 工具链：任务即软件的版本学/CI/全收据的工程实现。
- [Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) **（指南 · Anthropic）**——讲义词表与"写任务纪律"的主要出处；LLM-as-Judge 校准与混淆矩阵的实践版。
