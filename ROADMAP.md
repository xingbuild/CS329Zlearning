# ROADMAP.md · 后续迭代规划（活工单）

> 生成于 2026-10-30。本文件是**所有待完成工作的唯一清单**——每项完成后打勾 ✓ 并标注日期；跨 session 回看此文件即知进度；全部清零 = 课程产品按 GATE.md 标准 100% 完成。
> 与 GATE.md 的关系：GATE.md 是"什么算好"（验收标准），本文件是"还差什么"（工单清单）。

---

## 当前状态快照（每次迭代后更新）

- 版本：0.5.22 · 日期：2026-10-30（R3 全部完成：资源页 8/8 讲、实验室 8/8 讲配齐，R4 全销；D2 关闭）
- 四尺达标：8/8 讲 ✅（guide 子页八讲齐全）
- 交付层：D1 ✅ D3 ✅ D5 ✅（16 单元聚合）D4 ✅ D2 ✅（八讲四件套配齐：资源 8/8 + 实验室 8/8）D6 ✅（随实验室）
- 剩余工单：**仅 R6-3 品牌命名（需用户输入，挂起）**——其余全部清零 ✅

---

## 迭代执行序列（2026-10-30 制定 · 自主推进模式）

> 排序原则：R3/R4 实验室优先（每讲一轮，同轮销 R3 实验室 + R4 交互密度两票）→ L01 资源页 → R6-1 摘录开关（R5 的前置依赖：让新精读页一出生就带全文/摘录切换）→ R5 四篇精读 → R6 收尾。每轮固定动作：**GATE §4 四门自检 → 本地 commit → pub → 线上 200 → 本表与工单双处打勾**。

| 轮 | 工单 | 交付物 | 状态 |
|---|---|---|---|
| 1 | R3+R4 · L05 实验室 | `site/l05/lab/`：光谱定档决策器 + Optimizer 浏览器复刻（真计算）+ 持久执行重放机 | ✅ 2026-10-30 |
| 2 | R3+R4 · L06 实验室 | `site/l06/lab/`：模式组装器（七积木三场景）+ 反思对照实验 | ✅ 2026-10-30 |
| 3 | R3+R4 · L07 实验室 | `site/l07/lab/`：三因子记忆检索实验（拨权重看排序 + 写入/淘汰） | 🔲 |
| 4 | R3+R4 · L08 实验室 | `site/l08/lab/`：协调成本计算器（DAG 真执行）+ 交接丢失实验 | ✅ 2026-10-30 |
| 5 | R3 · L01 资源页 | `site/l01/resources/`：8 条框架文/一手出处（自检索验证） | ✅ 2026-10-30 |
| 6 | R6-1 · 精读摘录开关 | `site/scripts/build.sh`：默认摘录 / `FULL=1` 全文，eaia 切全文 | ✅ 2026-10-30 |
| 7 | R5 · L02 精读 | Chain-of-Thought（Wei 2022） | ✅ 2026-10-30 |
| 8 | R5 · L04 精读 | Toolformer（Schick 2023） | ✅ 2026-10-30 |
| 9 | R5 · L07 精读 | MemGPT（Packer 2024） | ✅ 2026-10-30 |
| 10 | R5 · L08 精读 | Why Do Multi-Agent LLM Systems Fail?（Cemri 2025） | ✅ 2026-10-30 |
| 11 | R6-2 · 部署监控 | `.github/workflows/uptime.yml` 每日 7 页 200 检查，失败邮件通知 | ✅ 2026-10-30 |
| 12 | R6-4 · 移动端打磨 | 五张结构图 overflow-x + min-width（390px 实测可横滑） | ✅ 2026-10-30 |
| 13 | R6-5 · hero CTA 文案 | hero 主按钮三态联动（无进度/继续下一讲/复习），实测三态 | ✅ 2026-10-30 |
| — | R6-3 · 品牌命名 | **需用户输入（命名决策），挂起不做** | ⏸ |

## R1 · D4 术语与复刻抽子页（八讲一致操作）

**内容**：把每讲 `lNN/index.md` 中的"术语考古与复刻检验"节（3 张 TermCard + 复刻清单 + 复刻检验题）抽出为 `lNN/guide/index.md` 子页，侧栏讲次组新增"术语与复刻指南"。课文页保留一行链接入口。

- [x] L01 抽出 → `/l01/guide/` ✓ 2026-10-30
- [x] L02 抽出 → `/l02/guide/` ✓ 2026-10-30
- [x] L03 抽出 → `/l03/guide/` ✓ 2026-10-30
- [x] L04 抽出 → `/l04/guide/` ✓ 2026-10-30（最重：已有双份术语卡 + 复刻清单 + FC 五零件，抽出后课文从 12 节→约 10 节）
- [x] L05 抽出 → `/l05/guide/` ✓ 2026-10-30
- [x] L06 抽出 → `/l06/guide/` ✓ 2026-10-30
- [x] L07 抽出 → `/l07/guide/` ✓ 2026-10-30
- [x] L08 抽出 → `/l08/guide/` ✓ 2026-10-30
- [x] 八讲侧栏统一登记（config.mts） ✓ 2026-10-30
- [x] 课文页留一行入口链接 ✓ 2026-10-30
- [x] 交互级验证 ✓ 2026-10-30

## R2 · W1-深度：知道级机制补到"能造"层

**内容**：GATE.md §1 记分表"深度点名"列列出的机制，逐讲补写从"知道是什么"到"能从零造"的正文段落。

**优先序**（从最薄开始）：

- [x] **L05**：DSPy Optimizer ✓ 2026-10-30（三支柱如何代码化为 Sig+Mod+Opt）、Temporal（Activity/Workflow/重试策略的零件图——已有复刻清单，正文需展开机制）、Harness 详解（四案例的设计决策逐维拆解）
- [x] **L02**：RLVR ✓ 2026-10-30（奖励设计 vs Goodhart 风险的机制级）、midtraining（域聚焦数据配比的实际操作）
- [x] **L06**：CodeAct ✓ 2026-10-30（代码作为动作空间的形式化、与 FC 的递进关系）、ReWOO（规划如何把 agent 变回 workflow 的具体操作步骤）、LLMCompiler（并行执行 + 动态重规划的调度机制）
- [x] **L03**：RAPTOR ✓ 2026-10-30（聚类→摘要→再嵌入的递归树构造步骤）、GraphRAG（LLM 抽实体→建图→社区发现的管线零件）、Late Chunking（长上下文编码器→块边界池化的实现路径）
- [x] **L07**：MemGPT ✓ 2026-10-30（LLM 管理内存的 write/replace/search 工具集操作流）、G-Memory（洞察图/查询图/交互图三图的构造与检索路径）、Sleep-time Compute（闲时后台 agent 的触发/整理/写入策略）
- [x] **L08**：DyLAN ✓ 2026-10-30（前向评分→互相打分→信用回传→选队的完整流程）
- [x] 每讲补完后跑 GATE §6 取证脚本更新记分 ✓ 2026-10-30

**R2 全部完成** ✓ 2026-10-30

## R3 · D2 四件套配齐（等检索 session 材料）

**内容**：L05–L08 逐讲补齐资源页（需检索 session 出 handoff 材料，§8.1 分工）+ 实验室设计。

- [x] L05 资源页 ✓ 2026-10-30（9 条：Karpathy LLMOS 演讲 / DL.AI LangGraph 短课 / B 站中文视频 / 四 harness repo / DSPy 展开 / Anthropic 判据交叉）
- [x] L06 资源页 ✓ 2026-10-30（6 条：Anthropic 五模式出处主放 / STORM repo / AutoGen 短课 / 站内 ReAct 精读交叉 / 上下文工程两篇展开 / Pi repo 交叉）
- [x] L07 资源页 ✓ 2026-10-30（8 条：MemGPT 作者亲授短课 / Generative Agents / Mem0 / Zep Graphiti repo / Voyager 项目页 / Letta 官网与 sleep-time 博文 / LangChain 工程实录展开）
- [x] L08 资源页 ✓ 2026-10-30（6 条：Anthropic vs Cognition 同周判据对撞 / OpenAI Agents SDK / AutoGen 官方文档 / Magentic-One 出版页 / DL.AI 交叉；含"八讲资源页集齐"闭环提示）
- [x] L05 实验室设计 ✓ 2026-10-30（Lab 04 · Agent 选型工作台：六卡定档决策台 / Optimizer 评估回路蒙特卡洛真算 + Bootstrap 注入 / Temporal 事件溯源崩溃恢复重放，IAB 实测三站全绿）
- [x] L06 实验室设计 ✓ 2026-10-30（Lab 05 · 模式组装台：七积木拼三场景逐槽判定 + 自评 vs 外反馈蒙特卡洛对照）
- [x] L07 实验室设计 ✓ 2026-10-30（Lab 06 · 记忆系统模拟器：三因子检索真算 + RAM FIFO 淘汰 × core_memory_write 对照）
- [x] L08 实验室设计 ✓ 2026-10-30（Lab 07 · MAS 成本账本：四拓扑 DAG 真执行成本对比 + Handoff/挑上下文超几何实验，判据翻转实测）
- [x] L01 资源页 ✓ 2026-10-30（主 session 自检索：Lilian Weng 框架文 / BAIR / ReAct 项目页 / Shunyu Yao / HAL / Agents That Matter / HF 课程 / Simon Willison，8 条全 200）

## R4 · D6 L05–L08 交互密度补齐（随 R3 同步）

**内容**：L05–L08 各配 1–2 个定制交互组件（当前仅文字+表格，交互密度低于 L01–L04 水准）。

- [x] L05 交互密度 ✓ 2026-10-30（Lab 04 三组件：TaskSizingDesk / MiniOptimizer / DurableReplay）
- [x] L06 交互密度 ✓ 2026-10-30（PatternAssembler / ReflectionLab）
- [x] L07 交互密度 ✓ 2026-10-30（MemoryRetrievalLab / MemoryLossTheater）
- [x] L08 交互密度 ✓ 2026-10-30（MasCostCalc / HandoffLossLab）

## R5 · 精读扩充

**内容**：为后续讲次配论文精读页（PaperPara 模具已就绪，`site/lNN/readings/<paper>/`）。

- [x] L02 精读 ✓ 2026-10-30（Chain-of-Thought：涌现阈值/GSM8K 17.9→56.9/流利但不合逻辑——短引+直译+要点式摘录精读）
- [x] L04 精读 ✓ 2026-10-30（Toolformer：采样→执行→困惑度过滤三步/五工具/6.7B 胜 175B）
- [x] L07 精读 ✓ 2026-10-30（MemGPT：虚拟上下文管理/memory pressure/嵌套 KV 唯一通关）
- [x] L08 精读 ✓ 2026-10-30（MAST：14 失败模式全谱/78.7% 组织层/+9.4%/+15.6% 干预）

## R6 · 长线优化

- [x] 精读摘录开关 ✓ 2026-10-30（scripts/build.sh：默认摘录=安全侧、FULL=1 全文临时替换构建后还原；eaia → build:full；实测摘录 47.5KB / 全文 111KB、git 零残留）
- [x] 部署监控 ✓ 2026-10-30（uptime.yml：每日 05:30 北京时间查 7 个关键页，失败即 Actions 邮件）
- [ ] 课程品牌命名（当前用课程名，用户可自定义）
- [x] 移动端打磨 ✓ 2026-10-30（Panorama/TransformerFlow/RagPipeline/ToolCallAnatomy/LineageMap 五图横滑查看，桌面不受影响）
- [x] hero CTA 文案 ✓ 2026-10-30（HomeProgress.syncHeroCta：三态改写，静态按钮兜底）

---

## 迭代纪律

1. 每轮迭代**只做一个 R 编号下的一个子项**，做完打勾 + 标注日期
2. 每轮迭代后跑 GATE.md §6 取证脚本，更新 GATE.md §1/§2 记分
3. 每轮迭代后 `pub` 发布 + 线上验证 200
4. 每完成一个 R 编号的全部子项，在 GATE.md 记分表标注该维度 ✅
5. 全部 R1–R6 清零 = 课程产品按 GATE.md 标准 100% 完成
