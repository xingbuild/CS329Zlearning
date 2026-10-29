---
title: 论文精读 · ReAct（摘录模式）
---

# 论文精读 · ReAct: Synergizing Reasoning and Acting in Language Models

> **作者**：Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao（Princeton NLP × Google Brain）
> **发表**：arXiv 2022.10 · ICLR 2023 · **[← 原文全文 PDF](https://arxiv.org/pdf/2210.03629)** · [项目页](https://react-lm.github.io/)
> **挂载点**：L01 课文 · 剧场与"谁决定下一步" · [← 返回课文](/l01/)

**为什么现在读它**：L01 剧场里那条 Apple Remote 轨迹，就是这篇论文 Figure 1(d) 的重演；剧场右上的三个工具 `Search / Lookup / Finish`，就是论文 §3.1 定义的 `search[entity] / lookup[string] / finish[answer]`。你已经在产品里"玩过"这篇论文的核心，现在回到原文，验证每一个细节。

::: warning 版权说明 · 线上摘录模式
本页为**关键段落摘录**（原文片段 + 中文直译 + 本质要点），完整原文请读 [arXiv:2210.03629](https://arxiv.org/pdf/2210.03629)。本地学习环境另存全文精读版（`site/l01/readings/react/full.md`，按 AGENTS.md §4.1 版权红线不入库、不上网）。
:::

## 学习地图

| 章节 | 一句话本质 | 关键结论 |
|---|---|---|
| Abstract | 推理与行动交错生成，互相成就 | 4 个基准超越 SOTA 基线；幻觉被外部交互压制 |
| §1 Introduction | 人类智能 = 行动 × 内部语言的紧协同 | 提出问题：协同是否有系统性收益 |
| §2 Method | **全文核心一句：把动作空间增广为 Â = 𝒜 ∪ ℒ** | thought 是"不改变环境的动作" |
| §3 知识密集任务 | HotpotQA / FEVER：检索支撑推理 | ReAct 更有据；CoT→ReAct 组合最佳；微调时 ReAct 最强 |
| §4 决策任务 | ALFWorld / WebShop：稀疏思考 | 1–2 个示例击败 10³–10⁵ 训练的 IL/RL；内部推理 > 外部反馈复述 |
| §5 Related Work | 与 CoT 系、WebGPT 系的两条对比线 | ReAct = 更便宜的策略学习（语言即策略） |
| §6 Conclusion | 简单方法 + 可解释轨迹 | 局限：上下文长度；出路：多任务训练 + RL |

## 关键段落精读（六段）

<PaperPara label="ABSTRACT · 协同的定义">

<template #en>
In this paper, we explore the use of LLMs to generate both reasoning traces and task-specific actions in an interleaved manner, allowing for greater synergy between the two: reasoning traces help the model induce, track, and update action plans as well as handle exceptions, while actions allow it to interface with and gather additional information from external sources such as knowledge bases or environments. […] Furthermore, on two interactive decision making benchmarks (ALFWorld and WebShop), ReAct outperforms imitation and reinforcement learning methods by an absolute success rate of 34% and 10% respectively, while being prompted with only one or two in-context examples.
</template>

<template #zh>
本文探索让 LLM 以**交错（interleaved）方式**同时生成推理轨迹与任务专属动作，从而使两者形成更强的协同：推理轨迹帮助模型归纳、跟踪、更新行动计划并处理异常；而动作则让模型能够对接知识库或环境等外部来源并从中收集额外信息。……此外，在两个交互式决策基准（ALFWorld 与 WebShop）上，ReAct 仅用一到两个上下文内示例做提示，就以 34% 和 10% 的绝对成功率优势超越了模仿学习与强化学习方法。
</template>

<template #hint>
对照 L01 第二幕解剖图：前半句是 Thought（内部动作），后半句是 Act→Obs（工具与环境）。**34% / 10% 对 10³–10⁵ 条训练数据**——"通用大脑可插拔"的定量证据。
</template>

</PaperPara>

<PaperPara label="§2 · 全文核心">

<template #en>
The idea of ReAct is simple: we augment the agent's action space to Â = 𝒜 ∪ ℒ, where ℒ is the space of language. An action â_t ∈ ℒ in the language space, which we will refer to as a thought or a reasoning trace, does not affect the external environment, thus leading to no observation feedback. Instead, a thought â_t aims to compose useful information by reasoning over the current context c_t, and update the context c_{t+1} = (c_t, â_t) to support future reasoning or acting.
</template>

<template #zh>
ReAct 的想法很简单：把 agent 的动作空间增广为 **Â = 𝒜 ∪ ℒ**，其中 ℒ 是语言空间。语言空间中的一个动作 â_t ∈ ℒ——我们称之为思考（thought）或推理轨迹——**不影响外部环境**，因此不产生观察反馈。相反，思考 â_t 的目的是通过对当前上下文 c_t 的推理来组合出有用信息，并更新上下文 c_{t+1} = (c_t, â_t)，以支撑后续的推理或行动。
</template>

<template #hint>
**全文最重要的一段**：一行数学完成概念统一——thought 不是日志，而是一个**不改变环境的动作**，与 search[] 同属增广后的动作空间。精确对应 L01"推理 = 内部动作，先改变自己的状态，再决定外部动作"。任何 agent 框架里的 reasoning step，数学上都是这一个 ∪。
</template>

</PaperPara>

<PaperPara label="§3.1 · Action Space（剧场三个工具的出处）">

<template #en>
We design a simple Wikipedia web API with three types of actions to support interactive information retrieval: (1) search[entity], which returns the first 5 sentences from the corresponding entity wiki page if it exists, or else suggests top-5 similar entities from the Wikipedia search engine, (2) lookup[string], which would return the next sentence in the page containing string, simulating Ctrl+F functionality on the browser, (3) finish[answer], which would finish the current task with answer. We note that this action space mostly can only retrieve a small part of a passage based on exact passage name, which is significantly weaker than state-of-the-art lexical or neural retrievers. The purpose is to simulate how humans would interact with Wikipedia, and force models to retrieve via explicit reasoning in language.
</template>

<template #zh>
我们设计了一个简单的 Wikipedia web API，包含三类动作以支持交互式信息检索：(1) **search[entity]**——若对应实体的维基页面存在，返回该页前 5 句；否则从 Wikipedia 搜索引擎返回最相近的 top-5 实体；(2) **lookup[string]**——返回页面中包含该字符串的下一句，模拟浏览器里的 Ctrl+F；(3) **finish[answer]**——以给定答案结束当前任务。我们要指出：这个动作空间基本只能按精确页面名取回段落的一小部分，**显著弱于**当时最先进的词法或神经检索器。其目的是模拟人类与 Wikipedia 的交互方式，并**迫使模型通过显式的语言推理来检索**。
</template>

<template #hint>
L01 剧场三个工具的原文定义——连"返回相似实体列表"（Front Row 歧义场景）都写在 search 的规格里。设计哲学：**故意把工具做弱**，把智能从检索器挪回推理。
</template>

</PaperPara>

<PaperPara label="§3.3 · 幻觉的定量置换">

<template #en>
A) Hallucination is a serious problem for CoT, resulting in much higher false positive rate than ReAct (14% vs. 6%) in success mode, and make up its major failure mode (56%). In contrast, the problem solving trajectory of ReAct is more grounded, fact-driven, and trustworthy, thanks to the access of an external knowledge base. B) While interleaving reasoning, action and observation steps improves ReAct's groundedness and trustworthiness, such a structural constraint also reduces its flexibility in formulating reasoning steps, leading to more reasoning error rate than CoT.
</template>

<template #zh>
**A)** 幻觉是 CoT 的严重问题——在成功模式中造成远高于 ReAct 的假阳性率（14% 对 6%），并构成其主要的失败模式（56%）。得益于能访问外部知识库，ReAct 的求解轨迹更有据、以事实为驱动、更可信赖。**B)** 交错"推理-动作-观察"步虽然提升了 ReAct 的有据性与可信赖度，这种结构约束也**降低了它组织推理步骤的灵活性**，导致推理错误率高于 CoT。
</template>

<template #hint>
**最值得背的定量结论**：CoT 失败的 56% 是幻觉；ReAct 幻觉率 0%，但把失败"换"成了推理错误 47% + 检索错误 23%。没有免费午餐——L01"各拿一副牌"的数据版（完整分布见下方表 2）。
</template>

</PaperPara>

<PaperPara label="§4.4 · 内部推理 vs 外部反馈">

<template #en>
Perhaps the closest prior work is Inner Monologue (IM), from Huang et al. 2022b, in which actions from an embodied agent are motivated by an eponymous "inner monologue". However, IM's "inner monologue" is limited to observations of the environment state and what needs to be completed by the agent for the goal to be satisfied. In contrast, the reasoning traces in ReAct for decision making is flexible and sparse, allowing diverse reasoning types to be induced for different tasks. […] ReAct substantially outperforms IM-style prompting (ReAct-IM) (71 vs. 53 overall success rate).
</template>

<template #zh>
最接近的先前工作是 Inner Monologue（IM，Huang et al. 2022b）：具身 agent 的行动由同名的"内在独白"驱动。但 IM 的"内在独白"**仅限于**对环境状态的观察、以及为满足目标 agent 还需完成什么的复述。相比之下，ReAct 用于决策的推理轨迹是**灵活且稀疏的**，可为不同任务诱导出多样的推理类型。……ReAct 大幅胜出 IM 式提示（ReAct-IM）（总体成功率 71 对 53）。
</template>

<template #hint>
两类"独白"的生死判词：**复述观察 ≠ 推理**（分解、跟踪、常识、改道）。差别 71 对 53。给 thought 划出下限：能**改变后续动作分布**的才算思考。
</template>

</PaperPara>

<PaperPara label="§6 · 结论与局限">

<template #en>
Despite the simplicity of our method, complex tasks with large action spaces require more demonstrations to learn well, which unfortunately can easily go beyond the input length limit of in-context learning. We explore the fine-tuning approach on HotpotQA with initial promising results, but learning from more high-quality human annotations will be the desiderata to further improve the performance. Scaling up ReAct with multi-task training and combining it with complementary paradigms like reinforcement learning could result in stronger agents that further unlock the potential of LLMs for more applications.
</template>

<template #zh>
尽管方法简单，但具有大动作空间的复杂任务需要更多示例才能学好——这很容易超出上下文学习的输入长度限制。我们在 HotpotQA 上探索了微调路径并取得初步可喜结果，但从更多高质量人类标注中学习仍是进一步提升性能的必要条件。以多任务训练扩展 ReAct、并与强化学习等互补范式结合，有望造出更强的 agent，进一步释放 LLM 在更多应用上的潜力。
</template>

<template #hint>
诚实的局限清单：**上下文长度、数据质量、未被组合的 RL**——2023–2026 年的 agentic 浪潮逐条兑现了这三个"下一步"。
</template>

</PaperPara>

## 表 1 · PaLM-540B 提示方法结果（HotpotQA EM / FEVER Acc）

| 提示方法 | HotpotQA | FEVER |
|---|---|---|
| Standard | 28.7 | 57.1 |
| CoT | 29.4 | 56.3 |
| CoT-SC | 33.4 | 60.4 |
| Act | 25.7 | 58.9 |
| **ReAct** | **27.4** | **60.9** |
| CoT-SC → ReAct | 34.2 | **64.6** |
| ReAct → CoT-SC | **35.1** | 62.0 |

## 表 2 · 成功/失败模式（人工标注，HotpotQA）

| 类型 | 定义 | ReAct | CoT |
|---|---|---|---|
| 成功 · 真阳性 | 推理轨迹与事实都正确 | 94% | 86% |
| 成功 · 假阳性 | 推理轨迹或事实幻觉 | **6%** | 14% |
| 失败 · 推理错误 | 错误推理轨迹（含重复循环） | 47% | 16% |
| 失败 · 检索错误 | 检索为空或无有用信息 | 23% | — |
| 失败 · 幻觉 | 幻觉的推理轨迹或事实 | **0%** | **56%** |

## 精读思考题

<details>
  <summary>1 · 为什么说"thought 是不改变环境的动作"是全文最核心的一句数学？</summary>
  <p><b>参考答案</b>：它把推理与行动统一进同一个动作空间 Â = 𝒜 ∪ ℒ——thought 与 search[] 同级，唯一区别是作用于上下文而非环境（c_{t+1} = (c_t, â_t) 而非产生 o_{t+1}）。由此"何时思考、思考什么"天然进入策略 π 的定义域。L01 第二幕"推理 = 内部动作"的原文依据。</p>
</details>

<details>
  <summary>2 · 表 1 里 CoT-SC(33.4) > ReAct(27.4)，但组合方法最好——这说明"谁"该做默认主力？切换条件为什么必须可判定？</summary>
  <p><b>参考答案</b>：主力取决于任务：事实敏感（FEVER）外部知识为王，结构推理（HotpotQA）内部知识占优。切换条件必须是可判定的失败信号（ReAct 步数耗尽 / CoT-SC 多数票不足 n/2），因为路由器本身要是确定性代码才可靠——L01"混搭架构"的实例。</p>
</details>

<details>
  <summary>3 · 表 2 的失败模式置换（幻觉 56% → 0%，换来推理 47% + 检索 23%）如何用 L01 的语言复述？</summary>
  <p><b>参考答案</b>：外部接地消灭了幻觉，但引入新失败面（环境噪声 + 结构刚性）。pⁿ 没有消失，只是换了一组 n 和 p——组合策略（ReAct↔CoT-SC）本质是给两种失败面各配兜底，把整体成功率抬到 35.1/64.6。</p>
</details>

<details>
  <summary>4 · 论文故意把检索 API 做得比神经检索器弱，为什么？对评估 agent 有什么方法论启示？</summary>
  <p><b>参考答案</b>：原句 "force models to retrieve via explicit reasoning in language"——工具越弱，智能越被迫显式化，推理的贡献才能被归因。启示：评估 agent 时要区分"检索器的智能"与"大脑的智能"；强工具会掩盖推理缺陷（很多 agent 评测的混淆变量）。</p>
</details>

<details>
  <summary>5 · §4.4 里 ReAct-IM（复述式反馈）为什么输给真推理 18 个点？给出一条判据：什么才算"真 thought"？</summary>
  <p><b>参考答案</b>：复述观察不改变后续动作的分布——它没有做目标分解、常识注入或改道决策。判据回到 §2 的定义：thought 必须"组合出有用信息并更新上下文以支撑未来行动"；用效果检验——看它是否改变了下一步动作的选择。这与 L01"控制流在运行时被重写"（剧场 Thought 3 帧）是同一件事。</p>
</details>

## 与课程的连接

- **剧场 ↔ Figure 1(1)**：L01 剧场三模式 = 本文 Standard/CoT/Act/ReAct 消融家族；Apple Remote 题与 `search[entity]` 规格均出自原文。
- **§2 增广动作空间 ↔ L01 第二幕解剖图**：Thought/Act/Obs/记忆在此完成数学化。
- **表 2 ↔ L01 第三/四幕**：幻觉 vs 有据是"各拿一副牌"；重复循环错误是"可预测失败模式"的具体形态。
- **§5.2 ↔ L05 预告**："语言即策略、描述即学习"是框架与编排的哲学地基。

<LessonDone id="l01-r-react" />
