---
title: L02 · LLM 作为建筑材料
---

# L02 · LLM 作为建筑材料

> 对应讲义 lecture02.pdf · p.2–176 · 约 45 分钟 · 前置：L01

L01 说清了 agent 是什么；这一讲往下钻一层——**把 LLM 这块"建筑材料"的物理性质弄清楚**。你不需要会训练模型，但你必须知道它的出厂性质从哪来、限制从哪来，否则你在这个材料上做的每一层工程（采样、上下文、成本、选型）都是玄学。

## 开场：三条昂贵的线索

同一个模型，三个真实的翻车现场：

1. **代码 agent 随机崩**：temperature 用默认 1.0，同样的任务时好时坏——因为每一步都在从长尾里抽签；
2. **一句 "Actually…" 让成本翻倍**：有人在对话历史**开头**补了一句修正，账单暴涨——因为 KV Cache 全部失效，整个历史重新计算；
3. **上下文塞满却答不准**：把所有材料都放进 context，模型反而开始丢信息——context rot（上下文腐烂）。

三条线索指向同一层：**把 LLM 当黑盒用，就会在最贵的层面试错**。这一讲把黑盒拆到"builder 够用的深度"。

## 第一幕：语言模型 = 分布机器，不是答案机器

讲义 p.6–23。一个语言模型定义只有一行数学：

$$P(x_1, x_2, \dots, x_n) = \prod_{i=1}^{n} P(x_i \mid x_1, \dots, x_{i-1})$$

序列的概率 = 逐 token 条件概率的连乘。讲义用真实数字演示（p.8）："The class was about agents" 整句概率约 1.2×10⁻¹⁷——实践中取对数求和以保数值稳定。

关键推论一：**这是生成式模型**（建模数据分布），不是判别式（区分类别）——所以你可以**从它采样**。关键推论二：模型每次给你的从来不是"答案"，而是**整个词表上的一个分布**；"答案"是你用解码策略从这个分布里挑出来的。

<div class="widget">
  <h3>采样实验室 · 解码策略如何重塑分布</h3>
  <SamplingLab />
</div>

讲义的原始数字值得玩味（p.16→p.18）：同一个前缀多给一个词 `to`，下一个 token 的分布从"泛泛的虚词"（to/as/the/a）跳到"动词的天下"（be/begin/go/start）——**上下文每多一个 token，分布就重写一次**。这就是 prompt 工程的全部物理基础。

**解码策略速查**（p.18–22）：

| 策略 | 做法 | 适用 |
|---|---|---|
| 贪心 greedy | 永远取 argmax | 可复现、但呆板易重复 |
| 温度 T | logit 除以 T 再 renormalize | T↓ 更确定，T↑ 更多样 |
| Top-k | 只留概率前 k 个再归一 | 砍长尾 |
| Top-p（nucleus） | 留累计概率达 p 的最小集合 | 自适应截断 |
| 束搜索 beam | 同时维护 b 条最优路径 | 质量↑、延迟与内存↑ |

工程经验：**数学/代码用低温度**（答案分布本该尖锐），**创意写作用高多样性**；beam search 贵，按预算选。注意温度与 lab01 的掩码解码是同一族数学——**都是先修改概率质量、再重新归一化**；区别只是掩码是硬约束（合法集外清零），温度是软变换。

## 第二幕：架构——注意力的代价结构

讲义 p.24–91。历史一分钟版（p.25）：n-gram → 神经 LM（2003）→ RNN → LSTM → **Transformer（2017）**。现代 agent 用的都是 decoder-only Transformer，先看它的一张数据流图：

<div class="widget">
  <h3>decoder-only Transformer · 数据流一图</h3>
  <TransformerFlow />
</div>

把它压成一张账单：

```
token → [嵌入 + 位置编码]
      → ×N 层 Transformer Block：
           多头因果自注意力（QKV → Softmax(QKᵀ/√dₖ)V → 投影）
           + 残差连接 + LayerNorm + 前馈网络 FFN
      → LM Head → Softmax → 词表分布
```

其中注意力是唯一"看全局"的机制（p.33–48 的逐步动画值得课后回看）。作为 builder，你要记住的不是矩阵细节，而是**代价结构**（p.61、87）：

| | 全注意力 Softmax Attention | 线性注意力 Linear Attention |
|---|---|---|
| 每步顺序操作 | **O(1)**（可大规模并行训练） | O(1) |
| 序列复杂度 | O(n²) | **O(n)** |
| 记忆 | KV Cache 随长度线性膨胀 | 压缩状态，常数内存 |
| 长上下文 | 全历史直接可查 | 只见压缩态，长程更弱 |

线性注意力的技巧一句话（p.66–67）："drop softmax"——去掉 softmax 后整个计算变成线性，可以改结合律先算 K·V，把历史折叠进一个小状态。**快了、省了，但历史被有损压缩**（p.84：RULER 上长上下文明显更弱）。所以实践里主流模型**混搭两种注意力**（p.89–90，如 Kimi K3）。还有一个被反复误解的点（p.85）：**上下文长度不是架构的硬限制，而是训练的限制**——位置编码没学过的长度，模型就不会用。

## 第三幕：训练三段论——你手上的模型是管道的产物

讲义 p.92–118。训练目标只有一个：**交叉熵**——让数据的下一个 token 概率最大（p.99 示例：P(how)=0.0124 → loss = −log(0.0124) = 1.907）。但数据管道决定了模型的"体质"：

```
预训练 Pretraining：网页级原始数据 → 抽取/去重/语言识别/质量过滤（p.102）
      ↓
中训练 Midtraining：换数据配比，聚焦目标域（数学/代码）（p.108–111）
      ↓
后训练 Posttraining：指令微调 SFT → 人类偏好 RLHF（p.112–114）
      ↓
可验证奖励 RLVR：奖励可判定的任务（单元测试/Lean 证明/精确匹配）（p.116）
      ↓
Agent 专属训练：如 SWE-Smith 造软件工程数据（p.117–118）
```

两个 builder 必须记住的坑：

- **RLHF 的副作用**（p.115）：人类标注者不可靠、偏好彼此冲突——优化它催生**谄媚（sycophancy）与武断**。你在 L01 第四幕见过的"对齐问题"，根子在这条数据管道里。
- **RLVR 为何先赢在数学/代码**（p.116）：奖励可判定（测试过/不过）。还记得 lab01 的铁律吗——**语法可判定，语义不可判定**。可验证奖励 = 把"语法级"的可判定性搬到了训练目标上；也因此要警惕 verifier 本身被模型钻空（Goodhart）。

## 第四幕：推理的经济学 + agent 工程学

讲义 p.119–173。这是离你钱包最近的一幕。

### 推理两阶段：Prefill 与 Decode

- **Prefill（处理 prompt）**：整段并行计算，**算力瓶颈**（compute-bound）——长 prompt 慢就慢在这；
- **Decode（逐 token 生成）**：每步只算一个 token，**带宽瓶颈**（memory-bound）——生成长输出贵在频繁搬运权重与 KV Cache。

**KV Cache 是推理经济学的核心**（p.124–133）：已算过的 token 把 K/V 存下来，后续步骤直接复用。但它只对**前缀不变**的序列有效：

<div class="widget">
  <h3>KV Cache 剧场 · “Actually, …” 为什么这么贵</h3>
  <KvCacheDemo />
</div>

工程结论一句话：**上下文设计要 append-only（只追加）**——往头部插话、改写历史，都是在付全量重算的钱（这也是为什么 agent 框架都把新观察追加在尾部）。

两个加速手段（p.136–137）：**投机解码**——小模型起草、大模型批量验证，"有些领域比其他领域更可预测"（这句话和 L01 的 ReAct 重复循环错误脚注遥相呼应）；**推理时缩放**——CoT、可控推理预算的 reasoning LLM（GPT-OSS 的 low/medium/high；Kimi K3 多教师蒸馏按任务学预算）、**重复采样**（Large Language Monkeys：SWE-bench 上采样 250 次覆盖率从 15%→56%）以及没有 verifier 时的**自洽性投票**。

### LLM for Agents：两个直接落点

**① Structured I/O（p.151–159）**：复合 AI 系统的组件之间需要**共享契约**（p.152）——手段从约束解码（SGLang 的 FSM）、DSPy 签名、分类头到 System One 模型。**这正是 Lab 01 的主题**：你已经从零手写过掩码解码、解剖过 function calling 载荷，本讲给你的是它的"宇宙观"——它是 LLM 工程的第一层确定性边界。

**② Context Engineering（p.160–173）**：agent 的上下文 = 系统提示 + 消息历史 + 记忆 + 工具返回 + 附件（p.162）。为什么不能全塞？**Context Rot**（p.163–164）：上下文越长，有效注意力越稀。实践准则：

- **避膨胀**（p.166）：工具不是越多越好——Pi 只有 read/write/edit/bash 四件；用检索取回相关的少数（L03 的主题）；
- **只追加**（p.168–169）：见 KV Cache 剧场；
- **实证评估**（p.170）：上下文方案的好壊要靠 eval，不靠直觉；
- **压缩 Compaction**（p.171）：留多了很快又要压缩，丢多了丢掉关键信息——这个两难将在 L07 记忆架构里正式解决（递归语言模型 RLM 是新思路，p.172–173）。

## 带走三句话

1. LLM 是**分布机器**：它输出的是词表上的分布，你的解码策略（温度/截断/贪心）才决定"答案"——采样参数是工程旋钮，不是玄学。
2. 成本由架构决定：**O(n²) 注意力、prefill/decode 两阶段、KV Cache 只认不变前缀**——append-only 是上下文设计的铁律。
3. 模型是训练管道的产物：谄媚来自 RLHF、可验证奖励先赢在可判定任务、上下文长度是训练边界——选型和排障都要对着管道想。

## 思考题

<details>
  <summary>1 · temperature=0 的 agent 就是确定、可靠的吗？</summary>
  <p><b>参考答案</b>：T→0 时每步取 argmax，模型侧确实逐步确定；但端到端仍不确定——环境（检索结果、API 返回）会变，而 agent 的每一步依赖观察（L01）。可靠性要靠确定性边界（校验/重试/契约）而不是靠"关温度"；另外贪心会放大重复循环错误（ReAct 论文 §3.3 的 B 观察）。</p>
</details>

<details>
  <summary>2 · 为什么"在对话开头补一句修正"比"在结尾追加同样的话"贵得多？</summary>
  <p><b>参考答案</b>：KV Cache 以前缀为键：尾部追加只算新 token；头部插入改变其后所有 token 的位置编码，全部注意力结果失效，整段历史重新 prefill（本讲 KV Cache 剧场②）。所以 agent 的消息流要设计成 append-only，-prefix cache 命中率就是成本。</p>
</details>

<details>
  <summary>3 · RLVR 为什么先在数学与代码上成功？它和 Lab 01 的"语法可判定"是什么关系？</summary>
  <p><b>参考答案</b>：因为这两个域的奖励可判定（单元测试/精确匹配），优化目标无歧义。这正是 lab01"语法可判定、语义不可判定"的训练版：可判定性搬到哪里，确定性工程就能做到哪里。代价是 verifier 设计要防 Goodhart（模型学会钻验证器空子）。</p>
</details>

<details>
  <summary>4 · 采样实验室里，把"采样 ×100"跑几轮，频率列与概率列的关系说明了什么？</summary>
  <p><b>参考答案</b>：大数定律——频率依概率收敛。工程含义：单次采样的结果不可预期，但分布是可预期的；你能工程化的是分布（温度、截断、掩码），不是单次结果。这也是 Self-Consistency 投票有效的原因。</p>
</details>

## 延伸阅读

- HuggingFace：[Decoding Strategies in LLMs](https://huggingface.co/blog/mlabonne/decoding-strategies) · [Tokenizers](https://huggingface.co/learn/llm-course/en/chapter2/4)
- Vaswani et al., *Attention Is All You Need*（2017）
- *Large Language Monkeys: Scaling Inference Compute with Repeated Sampling*（arXiv:2407.21787）
- Wang et al., *Self-Consistency Improves CoT Reasoning*（arXiv:2203.11171）
- Anthropic：[Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- 动手：[Lab 01 · Structured I/O 实验室](/labs/)——把本讲的"约束解码"亲手写一遍

### 外部资源 · 交互与视频

**[→ 精选外部资源与视频页](/l02/resources/)**：14 条逐链验证可达的交互与视频（Transformer Explainer、3b1b 双语 Ch5–6、李沐精读、Karpathy Deep Dive、KV Cache 系列、Anthropic 归因图……），按本讲四幕对位。

先带走两个动手任务（详见资源页顶部）：

1. 在 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) 输入 `The class was about` 再加 `to`——**亲手复现讲义 p.16→p.18 的分布跳变**；
2. 在 [LLM Sampling Visualizer](https://artefact2.github.io/llm-sampling/index.xhtml) 把温度拨到 0.2 与 1.5 对照——**用它回答思考题 1**。

<LessonDone id="l02" />
