---
title: L02 · 外部资源与视频
---

# L02 · 外部资源与视频

> [← 返回 L02 课文](/l02/) · 2026-10-26 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L02 课文的**外部对照实验室**：本站页内的采样实验室与 KV Cache 剧场是"机制模拟"，这里的交互与视频是"真实机器"——同一批概念，换成浏览器里真跑的 GPT-2、真实的注意力热图与真实的推理算术。按课文四幕对位，选你缺的那块补。

## 先做这两个动手任务

::: tip 任务 ① · 亲手复现讲义的分布跳变
打开 [Transformer Explainer](https://poloclub.github.io/transformer-explainer/)，输入 `The class was about`，看下一 token 分布（泛虚词的天下）；再补一个 `to`——分布瞬间跳到动词的世界。**这就是讲义 p.16 → p.18 的那两页，也是"上下文每多一个 token，分布就重写一次"的实证。**
:::

::: tip 任务 ② · 用温度回答思考题 1
打开 [LLM Sampling Visualizer](https://artefact2.github.io/llm-sampling/index.xhtml)，把温度拨到 **0.2** 看分布坍缩、再拨到 **1.5** 看长尾抬起——然后用这个观察回答课文思考题 1（temperature=0 真的等于可靠吗？）。
:::

## 第一幕 · 分布机器与解码

- [Transformer Explainer](https://poloclub.github.io/transformer-explainer/) **（交互）**——浏览器里跑真 GPT-2（124M）：输入任意文本看下一 token 分布，拨 temperature / top-k / top-p 看分布实时重塑，悬停 token 还能看注意力热图。一页打通第一、二幕；动手任务 ① 的场地。
- [LLM Sampling Visualizer](https://artefact2.github.io/llm-sampling/index.xhtml) **（交互）**——在真实分布上逐项对照温度、top-k、top-p、min-p 等 8 种采样参数；本站采样实验室的"外部对照版"，动手任务 ② 的场地。
- [Tiktokenizer](https://tiktokenizer.vercel.app/) **（交互）**——Karpathy 视频里现场用的分词器 playground，直观感受"token 不是词"。

## 第二幕 · 架构与注意力

- 3Blue1Brown 官方双语：[GPT 是什么？直观解释 Transformer（第 5 章）](https://www.bilibili.com/video/BV13z421U7cs) · [直观解释注意力机制（第 6 章）](https://www.bilibili.com/video/BV1TZ421j7Ke) **（视频，各约 25 分钟**；YouTube 原版：[Ch5](https://www.youtube.com/watch?v=wjZofJX0v4M) / [Ch6](https://www.youtube.com/watch?v=eMlx5fFNoYc)**）**——QKV 为什么存在、softmax 之后发生了什么，动画层面最清晰的两支。
- [LLM Visualization](https://bbycroft.net/llm) **（交互 3D）**——把 GPT 架构拆成可旋转、可逐层放大的 3D 零件图，张量流动全着色；课文那页"decoder-only 结构图"的立体版。
- 李沐：[Transformer 论文逐段精读](https://www.bilibili.com/video/BV1pu411o7BE) **（视频，约 1.5 小时）**——中文世界最经典的架构精读，与本站论文精读同一套方法论。

## 第三幕 · 训练管道

- Karpathy：[Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI) **（视频，约 3.5 小时）**——预训练 → 后训练 → RLHF 一路讲穿，幻觉与谄媚从哪来；第三幕的最佳视频版。

## 第四幕 · 推理经济学

- [The KV Cache: Memory Usage in Transformers](https://www.youtube.com/watch?v=80bIUggRJf4) **（短视频）**——KV Cache 到底省了什么、吃掉多少显存；看完再玩一遍课文里的 KV Cache 剧场。
- Jay Alammar：[The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/) **（图文动画）**——"GPT-2 保留已算过的 K/V 向量"概念的出处，逐步动画拆解自注意力。
- HuggingFace：[KV Caching Explained](https://huggingface.co/blog/not-lain/kv-caching) **（文 + 代码）**——T4 上 `use_cache` 带来约 5× 加速实测。
- kipply：[Transformer Inference Arithmetic](https://kipp.ly/transformer-inference-arithmetic/) **（深度文）**——prefill/decode 两阶段、算力瓶颈 vs 带宽瓶颈的一手算术，第四幕的硬核版。
- HuggingFace：[Assisted Generation（投机解码）](https://huggingface.co/blog/assisted-generation) **（文 + 动图）**——小模型起草、大模型批量验证的动画演示。

## 加餐 · 打开黑盒

- Anthropic：[On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) **（可交互论文）**——Claude 内部的归因图：多步推理怎么走线、写诗前先选韵脚、幻觉的电路长什么样。学完 L02 再看它，"概率大脑"四个字第一次有了显微镜。
