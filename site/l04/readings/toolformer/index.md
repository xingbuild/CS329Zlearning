---
title: 论文精读 · Toolformer（摘录模式）
---

# 论文精读 · Toolformer: Language Models Can Teach Themselves to Use Tools

> **作者**：Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicholas Cancedda, Thomas Scialom（Meta AI Research）
> **发表**：arXiv 2023.02 · **[← 原文 PDF](https://arxiv.org/pdf/2302.04761)**
> **挂载点**：L04 课文 · 第二幕"模型怎么学会调工具" · [← 返回课文](/l04/)

**为什么现在读它**：L04 第二幕讲工具使用的自监督规模化，这篇就是那条谱系的源头之作——**模型自己给自己造训练数据**：在语料里采样 API 调用、真执行、用"损失有没有降"当过滤器。它比 Function Calling 早三个月，比 MCP 早一年半，用 6.7B 参数打赢了 175B 的 zero-shot。读它你会看到 L04 复刻清单里"校验闸"的另一个化身：**困惑度过滤器**。

::: warning 版权说明 · 线上摘录模式
本页为**关键段落摘录**（短引原文 + 中文直译 + 本质要点），完整方法与全部实验请读 [arXiv:2302.04761](https://arxiv.org/pdf/2302.04761)。
:::

## 学习地图

| 章节 | 一句话本质 | 关键结论 |
|---|---|---|
| Abstract | 自监督学会用 API，两全其美 | 少量示例/API；零样本大涨且语言能力不掉 |
| §2 方法 | **采样→执行→过滤三步造数据** | 过滤判据 = 损失下降量 ≥ 阈值 |
| §2 工具箱 | 五个 API：计算器/QA/搜索/日历/翻译 | 每个都补模型的结构性短板 |
| §4 知识 | LAMA 三子集全面超 GPT-3 175B | 6.7B + 工具 > 175B zero-shot |
| §4 数学 | 计算器使用率 97.9%，ASDiv 40.4 vs 14.0 | 工具吃掉结构性失败 |
| §4 时间 | Dateset 27.3 vs 0.8 | 日历 54.8% 使用率——权重里没有"今天" |
| §6 局限 | 不能链式、不能交互、样本效率低 | 下一代（FC/ReAct）逐条兑现 |

## 关键段落精读（八段）

<PaperPara label="ABSTRACT · 两全其美">

<template #en>
"LMs can teach themselves to use external tools via simple APIs and achieve the best of both worlds."
</template>

<template #zh>
"语言模型可以**教会自己**通过简单的 API 使用外部工具，从而两全其美。"
</template>

<template #hint>
标题里的 "teach themselves" 不是修辞——训练数据是模型**自己采样、自己执行、自己过滤**出来的，全程无人工标注调用对。对照 L04 演进链：ReAct（提示词里教）→ Toolformer（语料里自教）→ Function Calling（产品化协议）——"谁写教材"三级跳。
</template>

</PaperPara>

<PaperPara label="§2.1 · 第一步：让模型在语料里采样调用">

<template #en>
方法：给每个 API 少量示例，让模型在大规模语料（CCNet 子集）上为文本标注潜在 API 调用——即采样调用位置与参数。
</template>

<template #zh>
对每个 API 提供少量示例，提示模型在数百万文档的语料上"给文本标注可能的 API 调用"——在哪些位置、以什么参数、调用什么工具。
</template>

<template #hint">
对照 Lab 01 的掩码思想：模型对 `[QA(...)` 的**分布**就是对"哪里值得调工具"的判断。这一步产出的是**候选**——噪声极大，所以必须有下一步的执行与过滤。**生成器-验证器分离**：采样便宜、把关交给确定性判据（L04 两道闸的微缩版）。
</template>

</PaperPara>

<PaperPara label="§2.2 · 第二步：真执行，结果必须是文本">

<template #en>
"The response for each API call c_i needs to be a single text sequence r_i."
</template>

<template #zh>
"每个 API 调用 c_i 的响应必须是**单一文本序列** r_i。"
</template>

<template #hint>
一句被忽视的架构约束：工具结果**回喂的条件**是它长得像语言——观察必须能进入上下文窗口。这是 L04 第一幕"三类缺口"的接口面：结构化世界 → 文本化观察。后来的 FC 协议、MCP 响应格式，都活在这个约束里。
</template>

</PaperPara>

<PaperPara label="§2.4 · 第三步：过滤——损失就是裁判">

<template #en>
保留满足 "L_i⁻ − L_i⁺ ≥ τ_f" 的调用——只有当"带调用的版本预测后续 token 的损失"比"不带"低出阈值时才保留。
</template>

<template #zh>
对每个候选调用比较两种上下文：含调用结果的（损失 L_i⁺）与不含的（损失 L_i⁻）；只有损失下降量超过阈值 τ_f 的调用才进入增广数据集，随后用于微调。
</template>

<template #hint>
**全文最锋利的一招**：验证器不是人工规则，是**模型自己的困惑度**——"这个调用让我更容易预测未来吗？"这是可判定信号（L06 Reflexion 判据）在数据清洗上的应用。也是 pass^k 思想的孪生：用可计算的指标当裁判，不请人也不信模型自评。
</template>

</PaperPara>

<PaperPara label="§2 · 工具箱：五件各补一块结构性短板">

<template #en>
五个 API：Calculator（四则运算）、QA（Atlas 问答）、WikiSearch（BM25 检索）、Calendar（返回当前日期）、MT（NLLB 机器翻译）。
</template>

<template #zh>
计算器（精确算术）、问答系统（Atlas，Natural Questions 微调）、维基搜索（BM25 + KILT 索引）、日历（返回今天日期）、机器翻译（600M 参数 NLLB，200 种语言）。
</template>

<template #hint>
注意工具选型的味道：**每个工具都对应模型权重里结构性缺失的能力**（浮点精度、实时日期、跨语言小模型）——不是"越多越好"，是"缺什么补什么"。对照 L05 Pi 的 4 件套哲学：工具少而准。
</template>

</PaperPara>

<PaperPara label="§4.1 · LAMA：6.7B 打赢 175B">

<template #en>
LAMA：Toolformer（GPT-J 6.7B）SQuAD 33.8 / Google-RE 11.5 / T-REx 53.5；GPT-3 175B zero-shot 为 26.8 / 7.0 / 39.8。
</template>

<template #zh>
知识探针 LAMA 上，基于 GPT-J 6.7B 的 Toolformer 在三个子集全部超过 GPT-3 175B 的 zero-shot（分别 +7.0 / +4.5 / +13.7）。
</template>

<template #hint">
**26 倍参数差被五个 API 翻盘**——L04 开场"能力没变，结局全变"的定量版。而且 QA 工具 98.1% 的使用率说明模型**学会了何时自己知识不够**——元认知被练进了权重。这就是 L04 第二幕"规模化"的含义：不是更多工具，是更多"知道自己缺什么"的判断。
</template>

</PaperPara>

<PaperPara label="§4.2/§4.5 · 数学与时间：结构性失败的清零">

<template #en>
数学：ASDiv 40.4 vs GPT-3 的 14.0（计算器使用率 97.9%）；Dateset：27.3 vs 0.8（日历使用率 54.8%）；禁用 API 时语言建模困惑度与基线完全持平（WikiText 10.3）。
</template>

<template #zh>
数学基准 ASDiv 上 40.4 对 GPT-3 175B 的 14.0；时间基准 Dateset 上 27.3 对 0.8；且在全部 API 被禁用时，模型的困惑度与原 GPT-J 完全相同——通用语言能力零退化。
</template>

<template #hint>
三个数字三个教训：**40.4 vs 14.0**——浮点错误被计算器结构性消灭（对照 CoT 精读题 3：工具要吃失败分布里的结构性块）；**27.3 vs 0.8**——权重里没有"今天"，0.8 分是纯猜；**零退化**——工具能力是"外挂"不是"置换"，这是两全其美的真正含义。
</template>

</PaperPara>

<PaperPara label="§6 · 局限：下一代的三张图纸">

<template #en>
局限：无法链式调用（一个工具的输出不能做另一个的输入）、不能交互式使用（无法浏览多个结果或改进查询）、样本效率低（百万文档只洗出几千个有用调用）。
</template>

<template #zh>
API 调用独立生成，不能链式组合；不能交互式地浏览多个搜索结果或改进查询；样本效率低——如计算器 API 处理超百万文档仅得到几千个有用调用示例。
</template>

<template #hint">
把局限清单当**预言**读：不能链式 → ReAct 循环接上（L01）；不能交互 → Agentic RAG 三决策（L03）；效率低 → BootstrapFewShot 式自举迭代（L05）。一篇论文的局限就是下一代的立项书——这也是 L04 演进链"代价引擎"的原文现场。
</template>

</PaperPara>

## 结果速览（GPT-J 6.7B 基座）

| 基准 | Toolformer | GPT-3 175B zero-shot | 工具使用率 |
|---|---|---|---|
| LAMA · SQuAD | **33.8** | 26.8 | QA 98.1% |
| LAMA · T-REx | **53.5** | 39.8 | — |
| ASDiv（数学） | **40.4** | 14.0 | 计算器 97.9% |
| Dateset（时间） | **27.3** | 0.8 | 日历 54.8% |
| WebQS（问答） | 26.3 | 29.0 | —（仍落后） |
| WikiText 困惑度（禁 API） | 10.3 | — | 零退化 |

## 精读思考题

<details>
  <summary>1 · 过滤器用"困惑度下降"当判据，与 Lab 01 的校验闸、L06 的"外部反馈"有什么共同结构？</summary>
  <p><b>参考答案</b>：三者都是<b>可判定信号当裁判</b>——校验闸判 schema 合法性、困惑度判信息增益、外部反馈判测试通过。共同结构 = 生成器（概率、便宜、多样）+ 验证器（确定性、可靠、把关）。这是全课程的主旋律在数据清洗、输出契约、反思三个场景的同一份图纸。</p>
</details>

<details>
  <summary>2 · 为什么"结果必须是单一文本序列"是深层架构约束？它如何塑造了后来的 FC 与 MCP？</summary>
  <p><b>参考答案</b>：LLM 唯一的输入接口是上下文里的 token——一切观察必须文本化。FC 的 JSON 结果、MCP 的 content 块，本质都在定义"外部世界如何翻译成模型能读的序列"。反过来说：图像/音频工具之所以特殊，正因为文本化有损（多模态接口是对这条约束的突破尝试）。</p>
</details>

<details>
  <summary>3 · 26 倍参数被五个 API 翻盘——什么时候"堆参数"仍会赢？给出判据。</summary>
  <p><b>参考答案</b>：工具赢在<b>结构性失败面</b>（精确计算、实时事实、长尾知识——检索/执行可解）；参数赢在<b>语义综合面</b>（复杂指令遵循、跨段推理、文体控制——难以外挂）。WebQS 上 Toolformer 输给 175B 就是后者：多跳问题的<b>分解</b>仍靠大脑。判据：失败是"模型不知道"（工具赢）还是"模型想不通"（参数赢）——L03/L04 反复出现的二分。</p>
</details>

<details>
  <summary>4 · 训练后的模型"何时调工具"的决策从哪来？这与 L01"控制流的归属"如何对接？</summary>
  <p><b>参考答案</b>：决策被练进权重（微调后模型自主决定调用与否，零样本下 98% 任务正确路由）。对接 L01：控制流仍在模型里，但<b>触发条件被数据蒸馏过</b>——相当于把"何时调工具"的 workflow 判断内化。后来的 FC 是把"怎么调"标准化（协议层），Toolformer 是把"何时调"内化（权重层）——两层互补，今天的 agent 两者都要。</p>
</details>

<details>
  <summary>5 · "百万文档只洗出几千个有用调用"——这个样本效率问题，L05 的哪个机制是它的解？</summary>
  <p><b>参考答案</b>：DSPy 的 BootstrapFewShot：用当前程序跑出轨迹 → 只保留评估通过的 → 回注为示例 → 迭代。同是"自举"，差别在 Toolformer 单轮清洗语料、Bootstrap 迭代式从<b>任务分布</b>里长示例——样本跟着需求走而不是跟着语料走。论文作者自己开出的药方（"迭代式应用该方法"）正是这个方向。</p>
</details>

## 与课程的连接

- **§2 三步 ↔ L04 第二幕自监督**：采样→执行→过滤 = 工具使用规模化的原始配方。
- **困惑度过滤 ↔ Lab 01 两道闸**：验证器思想的两种化身（输出契约 vs 数据清洗）。
- **五工具 ↔ L05 Pi 哲学**：缺什么补什么，不是越多越好。
- **局限清单 ↔ L01/L03/L05**：不能链式 → 循环；不能交互 → Agentic RAG；低效 → 自举迭代。
- **6.7B 胜 175B ↔ L04 开场实验**：能力没变（同基座），结局全变（接了工具）。

<LessonDone id="l04-r-toolformer" />
