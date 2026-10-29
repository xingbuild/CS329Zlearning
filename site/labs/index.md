# 实战实验室

实验室与讲次相互独立、**全部在浏览器本地运行**。v2 实验室直接内建在课程站里（产品化页面）；早期实验室（Lab 01）保留独立 HTML 形态，双击即用。

## Lab 02 · RAG 交互实验室 【产品化 · v2】

**教什么**：把 RAG 整条管道亲手跑一遍——三种分块策略真实切分（亲眼看关键证据被切断在边界）、BM25 / 向量 / RRF 混合三种检索器真实计算、上下文组装与成败判定（召回天花板 / 干扰项 / 中间丢失现场复现）。

**配套讲次**：L03 · RAG（四件套之②）

**入口**：<a href="/l03/lab/">进入 Lab 02 · RAG 交互实验室 →</a>

## Lab 01 · Structured I/O 实验室 【独立 HTML · v1 形态】

**教什么**：Structured I/O 的本质——把 LLM 的输出从「对自然语言的概率采样」变成「对形式语言的概率采样」。从裸接口的 8 种失败形态出发，经过两道闸门（语法/语义）与修复回路，直抵核心的**掩码解码**（正则→NFA→token 掩码），再看 function calling 协议与最小 agent 闭环。

**配套讲次**：L04 · 工具使用（深度实战）、L06 · 设计模式（最小 ReAct 闭环）。

**入口**：<a href="/labs/01-structured-io/structured-io-lab.html" target="_blank" rel="noopener">在新标签页打开实验室 →</a>（本地仓库中也可直接打开 `labs/01-structured-io/structured-io-lab.html`，另有 Python 进阶脚本见其 README）
