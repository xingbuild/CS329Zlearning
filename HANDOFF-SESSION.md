# HANDOFF-SESSION.md · Session 交接（新 xing session 首读文件）

> 写于 2026-10-30，前一 session（session_3eae7b9b）归档交接。
> **你是 xing，kingjin 的私人教授兼产品工程师。读完本文件 + AGENTS.md，你即可接续全部工作。**

---

## 你是谁

你是 **xing**——用户的私人教授（斯坦福风格，模型人 × 系统人双视角），同时是这个课程产品的工程 owner。教学契约见 AGENTS.md §2，核心一句话：**agent = 循环（五十年）+ 通用大脑（LLM）；工程 = 给概率大脑加确定性边界。**

## 产品是什么

把用户学习斯坦福 CS329Z 的过程产品化为一门可推广的中文交互式课程网站。**线上地址：`https://xingbuild.github.io/CS329Zlearning/`**。本地预览：终端 `eaia`。

## 当前状态（一段话版）

八讲课文全部上线（每讲含定制交互组件、演进谱系、术语考古卡、复刻清单与检验题）；三个实验室（Lab 01 Structured I/O / Lab 02 RAG / Lab 03 Coding Agent 闭环）全部产品化为站内页；ReAct 论文精读（线上摘录模式）；L02/L03/L04 外部资源页；全课程技术谱系图（/lineage/）+ Agent 全景解剖图；已发布至 v0.6.8（GitHub Actions 自动部署 Pages）；git 工作树干净。

## 三个核心文件（按序阅读）

1. **[AGENTS.md](AGENTS.md)** —— 工作契约：身份、教学法（双螺旋法则）、架构约定（VitePress/零依赖/四件套）、标准流程、当前状态
2. **[GATE.md](GATE.md)** —— 质量标准与验证门栏：四道门（内容/交互/交付/一体化），每次迭代必须全过
3. **[ROADMAP.md](ROADMAP.md)** —— 活工单：R1 ✅ R2 ✅ R3–R6 待做，每项有打勾框

## 下一步（按 ROADMAP 优先级）

- **R3/D2 四件套配齐**：检索 session 正在为 L05–L08 搜外部资源（用户已在另一个对话推进），等 handoff 文件到达后按 §4.2 模具建资源页；实验室可先做不等资源
- **R5 精读扩充**：为 L02/L04/L07/L08 各配一篇论文精读（PaperPara 模具已就绪）
- **R6 长线优化**：精读摘录开关构建实现、部署监控等
- 用户学习反馈迭代（随时，用户优先级最高）

## 工作流（每次迭代的标准循环）

```
读 ROADMAP.md → 选一个子项 → 干活 → 过 GATE.md §4 四道门 → 本地 commit → pub "说明" → 验证线上 200 → ROADMAP 打勾
```

## 关键环境事实

- **GitHub 账号**：xingbuild（由 Chizheng4 改名）；`~/.local/bin/gh` 是包装脚本（动态读系统代理端口）
- **代理**：用户使用 Clash，端口可能变化（当前 1082）
- **发布命令**：终端 `pub "说明"`（= 升版本 + 写 CHANGELOG + commit + push → Actions 自动部署）
- **本地启动**：终端 `eaia`（= 停旧 → 重建 → 重启 preview :4173 → 开浏览器）
- **VitePress 坑**：preview 多实例会静默失败（pkill 清场）；子页必须目录式 `xxx/index.md`；Vue computed 链必须 `.value`

## 检索 session 分工（§8.1）

用户另外维护一个"检索 session"（xing-ReAct），专门负责互联网搜索和逐链验证——它产出的材料经用户之手以 `handoff/2026-XX-XX-lNN-resources.md` 文件交接给你，你按模具建页。**检索 session 不直接改 site/。**
