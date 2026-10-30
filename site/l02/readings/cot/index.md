---
title: 论文精读 · Chain-of-Thought（摘录模式）
---

# 论文精读 · Chain-of-Thought Prompting Elicits Reasoning in Large Language Models

> **作者**：Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc V. Le, Denny Zhou（Google Research）
> **发表**：arXiv 2022.01 · NeurIPS 2022 · **[← 原文 PDF](https://arxiv.org/pdf/2201.11903)**
> **挂载点**：L02 课文 · 采样与"模仿推理的文本" · [← 返回课文](/l02/)

**为什么现在读它**：L02 讲"模型是概率的"，那概率的模型怎么突然"会推理"了？答案就在这篇：推理不是训练出来的新器官，是**提示出来的中间步骤**——而且只在足够大的模型上涌现。它是 L06 CoT 模式的源头、Self-Consistency 的地基、也是"reasoning 模型"时代（o1 式 RLVR 训练）的史前史。读懂它的"涌现"与"流利但不合逻辑"，你就拿到了 L02 与 L06 之间那条线。

::: warning 版权说明 · 线上摘录模式
本页为**关键段落摘录**（短引原文 + 中文直译 + 本质要点，引文均控制在一两句内），完整论证与全部实验请读 [arXiv:2201.11903](https://arxiv.org/pdf/2201.11903)。
:::

## 学习地图

| 章节 | 一句话本质 | 关键结论 |
|---|---|---|
| Abstract | 中间推理步骤 × 大模型 = 复杂推理 | 算术/常识/符号三域大涨；8 个示例超微调 verifier |
| §1 引言 | 只堆规模推不动难题 | scaling alone 不够，需要"让人写解题步骤"式的提示 |
| §2 方法 | **CoT = 一串自然语言中间推理步** | 少样本提示三元组 ⟨input, CoT, output⟩ |
| §3 算术 | GSM8K 17.9 → 56.9（PaLM 540B） | 涌现能力：~100B 以下无收益 |
| §3 消融 | 小模型"流利但不合逻辑" | 涌现有阈值——不是渐变是相变 |
| §4 常识/符号 | 同一配方通吃三域 | 方法通用性 |
| §8 结论 | CoT 是模型规模的涌现属性 | 打开"以提示换能力"的时代 |

## 关键段落精读（八段）

<PaperPara label="ABSTRACT · 提示出来的推理">

<template #en>
Chain-of-thought prompting improves performance on "arithmetic, commonsense, and symbolic reasoning tasks."
</template>

<template #zh>
思维链提示在"算术、常识与符号推理任务"上提升表现。
</template>

<template #hint>
摘要的三个域就是后面三张结果表。注意动词是 **elicit**（引出）——论文标题不用 "learn/improve reasoning"，措辞本身就在暗示：能力已在权重里，提示只是把它**引出来**。这个措辞分寸在 2022 年是洞察，在 RLVR 时代回看更是预言。
</template>

</PaperPara>

<PaperPara label="图 1 · 一个示例看懂整篇">

<template #en>
"Chain-of-thought prompting enables large language models to tackle complex arithmetic, commonsense, and symbolic reasoning tasks."（图 1：同一道 GSM8K 题，标准提示直接给答案算错；CoT 提示先写解题步骤再给答案算对）
</template>

<template #zh>
"思维链提示使大语言模型能够处理复杂的算术、常识与符号推理任务。"（图 1 对比：标准提示 = 输入→输出；CoT 提示 = 输入→**一串中间步骤**→输出）
</template>

<template #hint>
整篇论文的机制就在这张图：**把"答案"变成"过程 + 答案"**。对应 L02 的一句话——采样自回归的本质没变，变的是中间 token 在为最终答案**积累上下文**（每一步都重写下一 token 分布）。你在 L02 采样实验室见过的"分布跳变"，在这里被工程化为解题步骤。
</template>

</PaperPara>

<PaperPara label="§1 · 规模单腿走不动">

<template #en>
"scaling up model size alone has not proved sufficient for achieving high performance on challenging tasks."
</template>

<template #zh>
"仅仅扩大模型规模，尚未被证明足以在具有挑战性的任务上取得高性能。"
</template>

<template #hint>
2022 年的痛点：GSM8K 这类多步推理题，模型从 8B 堆到 540B，标准提示下的分数几乎是**平的**。这句话是整篇的动机——也是后来所有"推理时间计算"工作（Self-Consistency、搜索、RLVR）的共同起点：**买算力不如买步数**。
</template>

</PaperPara>

<PaperPara label="§2 · 定义：一串中间步骤">

<template #en>
"A chain of thought is a series of intermediate natural language reasoning steps that lead to the final output."
</template>

<template #zh>
"思维链是一系列导向最终输出的**自然语言中间推理步骤**。"
</template>

<template #hint>
全文最核心的定义句。三个关键词：**series**（有顺序依赖）、**natural language**（不是符号系统）、**intermediate**（不直接产生答案，为答案铺路）。少样本实现 = 提示里放 8 个 ⟨问题, 步骤, 答案⟩ 三元组——对比 L05 DSPy：那 8 个示例要人工写，BootstrapFewShot 把这一步自动化了。
</template>

</PaperPara>

<PaperPara label="§3 · 涌现：规模的相变">

<template #en>
"chain-of-thought prompting is an emergent ability of model scale."
</template>

<template #zh>
"思维链提示是模型规模的一种**涌现能力**。"
</template>

<template #hint">
**全文最重要的定性结论**：CoT 不是对所有模型都有效的通用技巧——它在小模型上**无效甚至有害**，越过某个规模阈值（约 10²B 参数级）突然生效。涌现 = 不连续。这是 L02"模型是建筑材料"的一个物理属性：同一份提示，不同规模的砖，盖出来的房子不一样。
</template>

</PaperPara>

<PaperPara label="§3 · GSM8K 的数字">

<template #en>
PaLM 540B：标准提示 solve rate 17.9%，CoT 提示 56.9%（外接计算器 58.1%）；仅用 8 个 CoT 示例即超越带 verifier 的微调 GPT-3（55%）。
</template>

<template #zh>
PaLM 540B 上：标准提示 17.9%，CoT 提示 56.9%（允许最终答案调用计算器为 58.1%）；只用 8 个上下文示例，就超过了用 verifier 微调过的 GPT-3（55%）。
</template>

<template #hint>
三个数字三件事：**17.9→56.9**（同一权重、同一采样器，只改提示——能力差全在"中间步骤"里）；**8 个示例 > 整个微调管线**（in-context learning 的效率宣言，L01"大脑可插拔"的定量版）；**58.1 vs 56.9**（外接计算器只 +1.2——说明瓶颈不是算术而是**分解**，这正是 L04"工具该补什么"的反面教材）。
</template>

</PaperPara>

<PaperPara label="§3 消融 · 流利但不合逻辑">

<template #en>
"chain-of-thought prompting does not positively impact performance for small models"，小模型会产生"fluent but not logical"的推理链。
</template>

<template #zh>
"思维链提示对小型模型的性能没有正向影响"——小模型生成的推理链**流利但不合逻辑**。
</template>

<template #hint>
**"流利但不合逻辑"六个字值一门课**：语言流畅性（下一 token 预测练出来的）与逻辑有效性（推理）是两种能力。小模型模仿了 CoT 的**文体**，没掌握 CoT 的**推理**——这正是 L06 术语卡 CoT"不是真推理，是模仿推理的文本"的实验证据。两年后 RLVR 做的事，就是把"真推理"从文体里区分出来练进权重（L02 RLVR 节）。
</template>

</PaperPara>

<PaperPara label="§8 · 结论：规模的涌现属性">

<template #en>
结论（转述）：CoT 提示是增强推理的简单通用方法；"chain-of-thought reasoning is an emergent property of model scale"，使大模型能完成 scaling 曲线原本平坦的任务。
</template>

<template #zh>
结论：CoT 提示是增强推理的简单而通用的方法；思维链推理是**模型规模的涌现属性**，它让大模型得以完成那些只靠 scaling 分数不动了的任务。
</template>

<template #hint>
读结论别只读"通用方法"——要读**涌现属性**这四个字的工程含义：能力不随规模线性涨，而是一档一档解锁。它直接催生了两个方向：往上（更大的模型解锁更多）与往侧（同规模下用采样/投票/搜索换能力——Self-Consistency、ToT、ReAct 全在这一侧）。
</template>

</PaperPara>

## 结果速览 · 三域与规模消融（PaLM 家族）

| 基准 | Standard | CoT | 备注 |
|---|---|---|---|
| GSM8K（算术） | 17.9 | **56.9** | PaLM 540B，8 示例 |
| StrategyQA（常识） | 63.6 | **70.7** | MC 校准后 |
| 末位词拼接（符号） | 26.4 | **56.5** | 2 跳任务 |

| 模型规模 | CoT 是否有效 |
|---|---|
| ~8B / ~62B | 无效甚至有害（流利但不合逻辑） |
| ~540B | 大幅增益（涌现阈值在此之上） |

## 精读思考题

<details>
  <summary>1 · "涌现"对工程选型意味着什么？如果你的模型是 7B，CoT 提示该不该用？</summary>
  <p><b>参考答案</b>：涌现 = 能力不连续，不能线性外推。7B 模型上 CoT 大概率无效甚至掉分（流利但不合逻辑），工程上应：a) 换用该规模有效的手段（分解为多次调用 / 检索接地 / 微调）；b) 若坚持 CoT，必须配验证闸（L01 契约闸）防"文体正确、结论错误"。这也是评估小模型的纪律：别用为大模型设计的提示去考小模型。</p>
</details>

<details>
  <summary>2 · 8 个示例超过微调 + verifier——用 L01 的语言解释为什么"这么便宜"。</summary>
  <p><b>参考答案</b>：in-context learning 不动权重：知识已在预训练权重里，示例只指定"用什么格式调用它"。微调 GPT-3 + verifier 做的是把格式与判别练进参数（贵、慢、僵化）；CoT 提示是"运行时换说明书"——L01"大脑可插拔、控制流可用自然语言编写"的定量注脚。</p>
</details>

<details>
  <summary>3 · 外接计算器只带来 +1.2（56.9→58.1），说明 GSM8K 的瓶颈是什么？这对 L04 工具设计是正面还是反面教材？</summary>
  <p><b>参考答案</b>：瓶颈在<b>分解</b>不在算术——多数错误是列错式子而非算错数。对 L04 是个校准器：工具该补的是模型<b>结构性缺</b>的能力（精确检索、实时状态、并行执行），而不是已有能力的锦上添花；加工具前先问"失败分布里哪一块是工具能吃掉的"。</p>
</details>

<details>
  <summary>4 · "流利但不合逻辑"与 L06 的"LLM 不能自评"（Huang 2023）合成什么结论？RLVR 解决了哪一半？</summary>
  <p><b>参考答案</b>：合成——生成侧：模仿文体 ≠ 掌握推理；校验侧：模型自评也分不出两者（自评同样只是文本）。RLVR 解决"判定"一半：用可验证奖励（测试/答案比对）当外部裁判，让"真推理"被区分并强化进权重；剩下的一半是部署侧的关键决策仍需外挂可判定信号（L06 思考题 2 的延伸）。</p>
</details>

<details>
  <summary>5 · 用 pⁿ 视角算一笔账：CoT 把一道题从 1 步变成 k 步，为什么端到端可靠性反而升了？</summary>
  <p><b>参考答案</b>：朴素 pⁿ 预言步数越多越不可靠，但 CoT 的每"步"不是独立采样——中间步骤是<b>条件生成</b>（前步写入上下文，重写后步分布），等效于把一道高熵问题分解为若干低熵子问题：p<sub>1</sub>·p<sub>2</sub>···p<sub>k</sub>（各 p 高）> p<sub>单步</sub>（极低）。L02 的采样实验室看过这个机制的微观形态：每多一个 token，分布就更尖。pⁿ 公式没变，变的是每一步的 p。</p>
</details>

## 与课程的连接

- **图 1 ↔ L02 采样实验室**：中间步骤 = 为答案积累上下文的 token 序列；"分布跳变"是 CoT 的微观机制。
- **§3 涌现 ↔ L02"模型是建筑材料"**：能力按规模解锁——选型时先看手里的砖是什么规格。
- **"流利但不合逻辑" ↔ L06 CoT 术语卡**："模仿推理的文本"的实验出处。
- **§1 scaling 瓶颈 ↔ L05 DSPy / Self-Consistency**：买算力 vs 买步数两条路线的分叉点。
- **8 示例 > 微调 ↔ L01 大脑可插拔**：in-context learning 效率的定量宣言。

<LessonDone id="l02-r-cot" />
