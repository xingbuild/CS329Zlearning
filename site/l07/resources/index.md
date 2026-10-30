---
title: L07 · 外部资源与视频
---

# L07 · 外部资源与视频

> [← 返回 L07 课文](/l07/) · 2026-10-30 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L07 课文的**外部对照实验室**。先说一句坦诚的话：**记忆域没有成熟的"可视化交互件"**——但换来的是全课程**最豪华的一手实物阵容**：MemGPT 论文作者亲授的免费课、三个 20k★+ 的官方 repo、两条研究前沿的公司博客。CoALA / MemGPT / Voyager / Generative Agents / Sleep-time / Mem0 / LoCoMo 论文已在课文延伸阅读，本页补的是**能上课、能读代码、能上手**的入口。

## 先做这三个动手任务

::: tip 任务 ① · 官方课上完，回来挑它的"粒度"
看 [DL.AI 记忆短课](https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory/) 第 1–2 课，跟着实现 core memory block 的 **self-editing**——回来对照课文 MemGPT 的**五个记忆工具**，指出课程里少了哪两个（提示：archival 侧的粒度差异）。找齐五个，你就有了"最小记忆系统 50 行"的全部零件。
:::

::: tip 任务 ② · 在源码里找三因子打分函数
打开 [Generative Agents 官方 repo](https://github.com/joonspk-research/generative_agents) 的 memory_stream 模块，找出**时近 × 重要性 × 相关性**三因子检索的打分函数——这是课文复刻检验题的现实版：三个因子怎么加权、缺了哪个会得什么病，源码会给你最诚实的答案。
:::

::: tip 任务 ③ · 见证一次"论文 → 工程"的漂移
读 [Mem0](https://github.com/mem0ai/mem0) 的 README，找出算法从论文的 **ADD / UPDATE / DELETE / NOOP 四操作**演进为 **single-pass ADD-only（只增不覆盖）**给出的理由——然后回答课文第五幕开放问题 1："记什么、忘什么"在这个工程取舍里是怎么被回答的？（讲义是 ground truth，工程如实标注演进——两者都要看。）
:::

## 第一、二幕 · 类型学与三种底座

- [Letta 官网](https://www.letta.com) **（公司站）**——MemGPT 团队的公司：研究线（MemGPT、context repositories、**sleep-time compute**）与 Letta Agent 产品一页看全——"记忆既是一门生意，也是一条研究前沿"的最佳全景入口。
- [Zep Graphiti](https://github.com/getzep/graphiti) **（repo · 约 32k★）**——**bi-temporal 时序知识图谱**：每个事实带生效/失效时间、失效不删除——课文第二幕"知识图谱底座"与"多跳关联"的最新工业实现。

## 第三幕 · 四大架构模式（一手实物）

- DeepLearning.AI：[LLMs as Operating Systems: Agent Memory](https://www.deeplearning.ai/short-courses/llms-as-operating-systems-agent-memory/) **（免费短课 · 约 1.5h · Charles Packer / Sarah Wooders 亲授）**——**MemGPT 论文作者本人讲 MemGPT**：自编辑记忆、两层架构、core / archival blocks、agentic RAG——课文 MemGPT 费曼级的官方课程版，本讲主打。
- [Generative Agents 官方代码库](https://github.com/joonspk-research/generative_agents) **（repo · 约 22k★）**——25 人小镇的完整实现：记忆流、反思、规划全在——第三幕"反思式固化"的原版实物（项目官网 generativeagents.io 不稳，以 GitHub 为准）。
- [Voyager 项目页](https://voyager.minedojo.org) **（项目页）**——技能库三大组件（自动课程 / 可执行代码技能 / 迭代提示 + 自验证）的原版图示；"102 次迭代造出钻石工具"的官方出处。
- [Mem0](https://github.com/mem0ai/mem0) **（repo · 约 68k★）**——记忆层基础设施：后台工作流检测冲突 + 可观测面板。**工程注记**：README 算法已从论文四操作演进为 ADD-only——动手任务 ③ 的场地。
- Letta：[Sleep-time Compute](https://www.letta.com/blog/sleep-time-compute) **（博文 · 2025-04）**——"learned context"概念、闲时整理的 Pareto 改进、主 agent + 后台 sleep-time agent **双体架构**（MemGPT 2.0 / Letta 0.7.0）——课文"睡眠维护"模式的一手出处。

## 第四、五幕 · 评估与开放问题

- LangChain：[How we built agent memory](https://www.langchain.com/blog/how-we-built-agent-builders-memory-system) **（工程实录）**——"文件系统底座 + grep / ls 即记忆工具"的工业实录（延伸阅读已挂链，此处展开定位）——它同时是第二幕"文件底座"与 LongMemEval 实证"文件记忆打败向量检索"的活注脚。
