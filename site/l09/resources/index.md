---
title: L09 · 外部资源与视频
---

# L09 · 外部资源与视频

> [← 返回 L09 课文](/l09/) · 2026-11-03 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L09 课文的**外部对照实验室**。先说一句坦诚的话：**优化域的精华几乎全在论文与一手实现里**——交互可视化件基本不存在（评估回路本身就难可视化），所以本页以**论文原文、官方文档与一手博客**为主（八条，全部 200 验证），按课文六幕对位。

## 先做这三个动手任务

::: tip 任务 ① · 去读 OPRO 的"指令进化轨迹"
打开 [OPRO 论文](https://arxiv.org/abs/2309.03409) 的图 3（指令随轮次的演化）——观察新指令怎么从"历史指令+得分"里长出来。然后回答课文思考题 1 的变体：**这个轨迹和 MIPROv2 的差别在哪**（提示：OPRO 只看指令，MIPROv2 还看程序、数据与成功轨迹）。
:::

::: tip 任务 ② · 对照 MIPROv2 与你写的三步
读 [MIPROv2 论文](https://arxiv.org/abs/2310.03714) 的方法节，对照你在 guide 复刻检验里写的三步——找出你漏掉的那一步细节（多数人漏：贝叶斯信念是**对组合**维护的，不是对单条指令）。
:::

::: tip 任务 ③ · 亲手跑一遍 autoresearch
打开 Karpathy 的 [autoresearch](https://github.com/karpathy/autoresearch) README——读完它的循环设计（brainstorm→改→实验→保留/回滚→记录），对照课文第五幕：**它防"作弊"的机制是什么**？（这正是下一讲 L10 的主题预告：优化器越强，evals 越要紧。）
:::

## 第二、三幕 · 上下文优化（论文群）

- [STaR](https://arxiv.org/abs/2203.14465) **（论文 · NeurIPS 2022）**——bootstrap 的源头：拒绝采样挖推理轨迹、自我训练——"用自己的产出抬高自己"的机制原文。
- [DSPy 官方文档](https://dspy.ai) **（文档 · 动手）**——Signature/Module/Optimizer 的官方指南；课文"50 行复刻 Optimizer"的对照面（Lab 04 站②你已摸过浏览器版）。
- [TextGrad](https://arxiv.org/abs/2406.07496) **（论文 · 2024）**——把 LLM 反馈当"文本梯度"反向传播回每个 prompt——梯度的语言学化。
- [GEPA](https://arxiv.org/abs/2507.19457) **（论文 · 2026）**——遗传式 Pareto 前沿进化；课文"样本效率 ≫ RL"的实验出处。

## 第四幕 · 权重优化（论文与一手博客）

- [FireAct](https://arxiv.org/abs/2310.05915) **（论文 · 2023）**——Llama2-13B 微调 GPT-4 轨迹超 prompted GPT-3.5 的实验原文——"蒸馏换部署成本"的定量证据。
- [DeepSeek-R1 / GRPO](https://arxiv.org/abs/2501.12948) **（论文 · 2025）**——GRPO 的正式出处：PPO 的工程减法（4 模型→3 模型、组内 z-score 优势）。
- [On-Policy Distillation](https://thinkingmachines.ai/blog/on-policy-distillation/) **（博客 · Thinking Machines）**——"复盘你自己下过的棋"：学生策略分布上做逐 token 蒸馏，比 RL 更高效的一手实验记录（含公式与曲线）。

## 第五幕 · agent 当优化器（一手现场）

- [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) **（论文 · 2026）**——自改代码的进化 agent；讲义强调的两个关键（自己改自己 + 回访祖先）在消融实验里。
- [autoresearch](https://github.com/karpathy/autoresearch) **（repo · Karpathy）**——"优化任何能跑在软件上的东西"的最小实现——几十行读懂 agent-as-optimizer 的骨架。
