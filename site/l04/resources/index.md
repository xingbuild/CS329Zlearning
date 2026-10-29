---
title: L04 · 外部资源与视频
---

# L04 · 外部资源与视频

> [← 返回 L04 课文](/l04/) · 2026-10-29 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L04 课文的**外部对照实验室**。先说一句坦诚的话：**工具调用领域的成熟交互可视化是几讲里最少的**——机制活在**协议与代码**里，不在几何空间里；所以本页以"官方文档 + 代码实操 + 榜单"为主，可视化交互件只有 BFCL 一件。按课文五幕对位（含两讲延伸阅读已有的论文链接，此处不重复）。

## 先做这三个动手任务

::: tip 任务 ① · 去 BFCL 亲手考"相关性检测"
打开 [BFCL 在线演示](https://gorilla.cs.berkeley.edu/leaderboard.html)，输入 `What is 2*3?` 只给一个 `add` 函数——看模型是硬调 `add`，还是答 "only add is available"。这是课文思考题 4（"不该调用时拒绝"为什么难）的现实版。
:::

::: tip 任务 ② · 对照 OpenAI 指南与 Lab 01 第 3 站
读 [OpenAI Structured Outputs 指南](https://developers.openai.com/api/docs/guides/structured-outputs) 的 "JSON mode vs Structured Outputs" 一节，再回看你摸过的掩码解码——**"保证"是约束解码给的，不是 prompt 求来的**；官方文档说的和你在实验室做的是同一件事。
:::

::: tip 任务 ③ · 工具投毒 vs 两道闸
看 [Invariant 的 rug pull 案例](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks.html)，回答："Lab 01 的两道闸（语法/类型）挡得住工具描述里藏的注入吗？"（参考：**挡不住**——闸校验的是结构，注入活在语义里；"语法可判定、语义只能逼近"的又一次应验。）
:::

## 第一幕 · 三类缺口与工具的定义

- Anthropic Engineering：[Writing Effective Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) **（图文）**——少而精的工具而非 API 包装器、命名空间、高信号返回（自然语言优于 UUID）、错误信息要指向修复：工具设计的第一手工程哲学，正对"正典定义"，也是第五幕的预防面。
- Hugging Face：[AI Agents Course](https://huggingface.co/learn/agents-course) **（免费课程）**——Unit 1 讲工具与"Python 函数即工具"；Bonus 1《Fine-tuning an LLM for Function-calling》正对第二幕的"改模型"路线。

## 第二幕 · 学会调工具

坦白说明：本幕的权威材料是 **Toolformer / ToolkenGPT / ToolLLM / Gorilla 四篇论文本身**（已在课文延伸阅读），外部讲解类暂无达标交互件；最短的上手路径是上面 HF 课程的 **Bonus 1**——亲手微调一个会 function calling 的模型。

## 第三幕 · 标准接口三代（REST → FC → MCP）· 资源最富的一幕

- Anthropic：[Tool Use 官方文档](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/overview) **（文档）**——tool_use / tool_result 回环、tool_choice 强制调用、`strict: true` 的 schema 一致性保证；get_weather 全流程示例。FC 的官方正典。
- OpenAI：[Structured Outputs 指南](https://developers.openai.com/api/docs/guides/structured-outputs) **（文档）**——"JSON mode 只保证合法 JSON，Structured Outputs 保证 schema"：Lab 01 掩码解码的工业版，动手任务 ② 的场地。
- [Outlines 文档](https://dottxt-ai.github.io/outlines/latest/) **（文档 + 代码）**——正则 / JSON Schema → FSM → logits 掩码的开源约束生成库；Lab 01 第 3 站（GBNF/Outlines）的生产级对应物。
- [Instructor](https://python.useinstructor.com/) **（库）**——Pydantic 模型定义输出 + 自动校验重试 + 15 家 provider；结构化输出工程化的事实标准之一（约 11k★、月下载 300 万+）。
- FastMCP：[Generate MCP servers from OpenAPI specs](https://gofastmcp.com/integrations/openapi) **（文档）**——讲义 p.55 `FastMCP.from_openapi()` 的官方出处；文档还诚实注明"手工设计通常优于自动转换"——这句话本身就是第三代协议边界的教学点。
- freeCodeCamp：[Intro to MCP Servers](https://www.youtube.com/watch?v=DosHnyq78xY) **（视频课程）**——MCP server 实操向长片（官方频道背书）。
- 技术蛋老师：[Function Calling、MCP 和 A2A 的核心原理与区别](https://www.bilibili.com/video/BV1XFhPzoEBx) **（中文视频，B 站）**——三代接口核心区别的通俗中文讲解（32.5 万粉技术区 UP，2025-07）。

## 第四幕 · 评估

- [BFCL V4](https://gorilla.cs.berkeley.edu/leaderboard.html) **（交互榜单 + 在线演示）**——输入 prompt + 函数签名，实时看模型输出；AST / 真实执行 / 多轮状态 / 相关性检测四层。动手任务 ① 的场地。
- [τ-bench 仓库](https://github.com/sierra-research/tau-bench) **（GitHub）**——tool-agent-user 三方交互 + policy 合规；leaderboard 直接列 **Pass^1–Pass^4**——页内 pass^k 计算器与 Lab 03 的现实数据源。README 注明任务已演进到 τ³-bench（银行域、语音、修复版任务）——**这个 benchmark 自己也在迭代**。

## 第五幕 · 失败模式

- Invariant Labs：[MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks.html) **（图文 + 实测截图）**——工具描述里藏恶意指令（模型看得见、用户看不见）、rug pull（审批后偷改描述）、工具影子（覆盖可信工具）；附 Cursor 真实外泄演示与缓解措施（版本锁定、描述透明化、MCP-Scan）。提示注入同族的现场版，动手任务 ③ 的场地。

## 加餐 · 官方动手课程

- Anthropic 官方课程库 [tool_use 章](https://github.com/anthropics/courses) **（GitHub notebooks，22.9k★）**——tool use 从基础到 agentic 循环的官方教程。**注意：仓库 2026-09 起已归档（只读），内容完整可学但不再更新。**
