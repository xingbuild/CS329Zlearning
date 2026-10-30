---
title: L05 · 框架与编排：看穿打包术
---

# L05 · 框架与编排：看穿打包术

> 对应讲义 lecture05Frameworks Orchestration.pdf · p.7–130 · 约 45 分钟 · 前置：L01–L04

前四讲你已经能徒手写出 agent 的每个器官（lab01 的闭环、L03 的检索、L04 的工具协议）。这一讲站在**选型层**：LangChain/DSPy/LangGraph/Temporal 这些框架到底替你做了什么、什么时候该用、什么时候是负债。方法论只有一句（讲义 p.5 的坦白）：**框架抽象掉底层细节，而本课程要求你懂那些细节——所以今天学抽象，是为了看穿它，不是崇拜它。**

::: info 演进谱系 · 本讲的一条链
手写循环（透明但每次重造轮子）→ 重框架（快但抽象税+依赖风险）→ 编排服务化（Temporal：持久执行/重试）。问题主线：**复用与可靠怎么兼得**——框架打包的是你已会的机制，买不买取决于你懂不懂里面是什么。（[全课程谱系图 →](/lineage/)）
:::

<LessonPack mins="45" :units="[{ t: '外部资源 · 三个任务', href: '/l05/resources/' }]" />

## 开场：三个团队的三种命运

- **A 团队**：三天用重框架搭出 demo，三个月后没人敢动——每一层抽象都是别人的决定；
- **B 团队**：手写 while 循环，快而透明，但重试、状态、观测全部手工——每次新需求重新发明轮子；
- **C 团队**：agent 半夜挂了，没有 trace、没有日志，只能复现到天亮。

三个坑对应三种缺失：**不知在光谱哪一档**、**不知框架抽象了什么**、**没有编排与遥测**。本讲按这三问展开。

## 第一幕：工程三支柱与 Agency 光谱

讲义 p.10–16 给出全课程的坐标系统。**AI 系统工程 = 三支柱**：

```
Data（数据：训练数据/轨迹/示范/人类反馈）
System（系统：语言模型/复合系统/工作流/Agentic 系统）
Evaluation + Metric（评测与指标：通过率/EM/LLM 裁判/成本/延迟）
```

后面整个课程的讲次都能挂回这三支柱（p.13 的课程地图）。而框架按 **Agency 光谱**分布：

<div class="widget">
  <h3>Agency 光谱探索器 · 你的系统在哪一档？</h3>
  <AgencySpectrum />
</div>

这就是 L01"谁决定下一步"那一刀的**选型版**：左端是焊死在代码里的确定控制流，右端是交给模型的概率控制流。框架没有高下，只有**你该在哪一档**。

## 第二幕：两大工作流抽象——DSPy 与 LangGraph

**DSPy：把提示工程变成编程**（p.22–51）。三个概念：

| 概念 | 是什么 | 例 |
|---|---|---|
| **Signature 签名** | 严格定义对模型的输入/输出契约（What） | `"text -> sentiment"` |
| **Module 模块** | 把签名组合成可调用函数（How） | `dspy.Predict` / `ChainOfThought` / `BestOfN` |
| **Optimizer 优化器** | 给定数据与指标，自动改进程序的 prompt 或权重 | 靠 metric 驱动的自动调优 |

关键的认知升级：**Optimizer 把三支柱代码化了**——数据 + 指标 + 系统，然后自动搜索更好的程序。

**造一个最小 Optimizer**（费曼级）：你只需要三个零件——
1. **候选生成器**：给定当前 prompt（含 few-shot 示例的选择），产生变体——换示例、改措辞、调格式；
2. **评估回路**：对每个候选，在标注数据上跑完整管道、用指标打分（如精确匹配、LLM 裁判分）；
3. **搜索策略**：贪心（留最好的）、BootstrapCoprompt（从错误中选新示例）、或随机搜索。

DSPy 的 `BootstrapFewShot` 本质就是：用当前程序跑一遍 → 收集正确答案的轨迹 → 把它们作为新 few-shot 示例注入 → 重跑 → 留分高的。**你能用 50 行 Python 复刻这个机制。**（你在 L02 见过的 DSPy 签名提示内部结构，就是它编译出来的。）DSPy 还内置 agent 模块（`dspy.ReAct`、`dspy.RLM`）——签名背后还是你已认识的循环。

**LangGraph：把工作流变成图**（p.53–76）。四个原语：

- **State**：共享工作区，一个被图不断修改的对象；
- **Node**：读写 State 的函数；
- **Edge**：节点间的控制流；**条件边**实现分支；
- 每个 Graph 必有 Start/End。

用 LangGraph 写 agent 就是画那张你早已熟悉的图（p.58）：**State（消息历史）+ LLM 节点 + Tools 节点构成的环**——lab01 step6 手写的 `decide → execute → observe` 循环，在这里变成两个节点加一条回边。看穿了吗？**框架没有发明任何新机制，只是给你的手写循环加了语法与配套**（持久化、流式、条件边的管理）。

## 第三幕：Agent Harness——围绕模型的手艺

讲义 p.80–89。**Harness（挽具）** = 包在模型外的全部脚手架：工具、记忆、上下文管理、执行方式。四个开源案例，四种哲学：

<div class="widget">
  <h3>Harness 取舍对比 · 同一个模型，四种人生</h3>
  <HarnessCompare />
</div>

三个要害观察：

1. **Harness tax 是真的**（p.86）：同一模型换个 harness，成绩差一大截——"模型能力"里有一大块其实是 harness 贡献的；
2. **每个维度都是取舍**：工具越少越可控（Pi 的 4 件套）vs 终端越真越好用（OpenHands 的 tmux）；历史线性可预测（Mini）vs 树可回溯分叉（Pi）；
3. **讲义的原话鼓励**（p.89）："也许你能造出下一个流行的 agent harness"——因为这门课已经把每个部件都拆给你看过。

**四案例的设计决策拆解**（费曼级——你会怎么选？）：

| 决策点 | Mini SWE-Agent | OpenHands | Pi | Open Claw |
|---|---|---|---|---|
| 为什么这么选 | 极简→评测变量最少 | 事件溯源→可回放 | 刻意简单→社区扩展 | 常驻→跨会话人格 |
| 换来什么 | 受控实验的可信度 | 调试与审计能力 | 用户可控、上手快 | 连续性与主动性 |
| 付出什么 | 功能弱 | 复杂度高 | 天花板低 | 资源占用大 |
| 什么时候你会选它 | 做研究/评测 | 做生产/团队 | 个人使用/原型 | 长期助理 |

**你自己造 harness 的最短路径**（< 100 行）：一个 while 循环 + 一个工具注册表 + 一个消息列表 + bash 一个工具——你已经在 Lab 01 闭环剧场摸过这个最小骨架。Pi 证明这个骨架加好的系统提示就能打。顺带一提：Open Claw 的 AGENTS.md 注入与夜间记忆整理，与本课程站点的 AGENTS.md 连续性机制同构——**用文件承载身份与记忆**是正在成形的工程惯例。

## 第四幕：编排与遥测——把软件工程的教训搬过来

讲义 p.92–122。动机（p.92–93）：**agent 的运行时长正在跨越"人类时间"量级**（METR 的时间视界研究）——跑得越久，基础设施的可靠性越要紧；日志与可观测性是调试的生命线。

**Temporal 的执行模型**（p.95–118）给你一套"agent 版的数据库事务"：

**从零理解持久执行**（费曼级）：Temporal 的核心机制是**事件溯源**（event sourcing）——
- Workflow 代码不是直接执行，而是被 Temporal Runtime **记录为一系列事件**（"调了 Activity A → 成功 → 调了 B → 超时 → 重试 B → 成功 → …"）
- 这些事件**追加写入数据库**（append-only，就像 Lab 01 的 agent 事件日志）
- 崩溃后恢复 = **从数据库重放事件流**，跳过已成功的 Activity，只重执行未完成的
- **你要造的最小版**：一个 JSON 事件列表 + 一个 `execute(workflow_fn, history)` 函数——重放 history 里已有的步骤，遇到未完成的调真实执行并追加记录

三个关键原语：
- **Activity**：可失败的功能单元（一次工具调用、一次 LLM 调用），每个有独立的重试策略与超时；
- **Workflow**：把 Activity 串起来的编排逻辑——写成普通代码，由 Temporal Runtime 沙箱执行并记录；
- **Worker**：从任务队列拉 Activity 执行的进程——worker 可以崩、可以扩缩容，因为状态在 Temporal 服务端。

**服务端计时**：`sleep(30天)` 不是进程内阻塞——Temporal 在历史里记一个 Timer 事件，到期后唤醒 Workflow 续跑。这就是为什么 agent 可以放心"等用户回复再继续"而不用保活进程。

**遥测三件套**（p.118–121）：**MLFlow**（实验追踪）、**LangSmith**（LangChain 系的 trace/评测）、**LangFuse**（开源可观测）——trace 每一次模型调用、工具调用、状态变更。讲义的结论（p.122）值得裱起来：**"搭建 agent"与"工程化 agent"的分界线，就是有没有编排、评测与监控。**

## 第五幕：最佳实践与陷阱

讲义 p.123–130，四条军规 + 三个陷阱：

**军规**：

1. **保持简单**（p.124）：你可能根本不需要 agent——workflow 就够了；真要 agent 时，工具要一个一个论证；
2. **让失败可观察、可恢复**（p.125）：trace 一切；设超时、重试上限、执行预算；错误**回喂给 agent** 让它自己换路（lab01 的修复回路）；
3. **评测驱动决策**（p.127）：设计选择要落在 eval 上，不落在直觉上；
4. **爬你自己的山**（p.128）：除非你在造通用编码 agent，**标准编码基准不是你该爬的**——评测要代表你的任务分布。

**陷阱**（p.129）：

- **抽象让你远离底层**——先懂原理（本课程前四讲），再上框架；
- **复杂系统里定位失败很难**——去看 traces，别猜；
- **框架 = 依赖 = 别人的维护节奏**——升级会突然砸到你。

## 术语考古与复刻检验

<TermCard term="Signature（签名）" from="DSPy（2023）从编程语言类型签名借喻：输入→输出的类型化声明" replaced="手写 prompt 模板——签名由编译器自动编译成 prompt" is="声明式契约：定义 What，编译器负责 How" isNot="不是 prompt——签名是 prompt 的源代码" />

<TermCard term="Harness（挽具）" from="马具隐喻：模型是马、挽具是不改变马而引导其力量的结构——比「框架」更精确：不换模型，只加边界" replaced="「框架」一词的模糊性——挽具暗示了包裹与不侵入" is="模型外的全部脚手架：工具、记忆、上下文管理、执行" isNot="不是模型能力的一部分——同一模型换挽具成绩差一大截（harness tax）" />

<TermCard term="Durable Execution（持久执行）" from="Temporal（2020）核心概念：执行历史落盘、崩溃可恢复" replaced="进程内重试——worker 一死全部重来" is="每步落盘的状态机：崩溃后从历史续跑" isNot="不是消息队列——队列管传递，持久执行管恢复" />

### 复刻清单 · 手写最小 agent 循环的骨架零件

状态对象（消息历史/共享字典）→ 工具注册表 → 循环壳（终止条件/步数上限）→ 错误回喂（失败变信息）→ 重试预算（Temporal 的 Activity 等价物）。**缺重试预算 = 无限循环烧钱；缺状态 = 每轮失忆。**

<details>
  <summary>复刻检验 · 不用任何框架，写出最小 agent 循环的伪代码骨架（< 20 行），并指出 Temporal 分别替换了其中哪些零件。</summary>
  <p><b>参考答案</b>：while not done: decision=llm(ctx); call=validate(decision); result=execute(call); ctx.append(obs)。Temporal 替换：execute→Activity（可重试）、while 循环→Workflow（持久化恢复）、重试预算→RetryPolicy。</p>
</details>

## 带走三句话

1. 先定档再选框：**Agency 光谱（Model → Workflow → Agent）按"控制流归谁"划档**——框架只是每档的语法糖，不是能力来源。
2. 框架的两大真实价值：**抽象**（DSPy 签名/优化器、LangGraph 图）与**基础设施**（Temporal 持久执行、重试、trace）——前者可替代，后者买了不亏。
3. "搭 agent"到"工程化 agent"的分界 = **编排 + 评测 + 监控**；以及一条终身军规：**爬你自己的山（自建域内评测）**。

## 思考题

<details>
  <summary>1 · 用光谱判据给三个任务定档：发票字段抽取、客服退款处理、新闻摘要。</summary>
  <p><b>参考答案</b>：发票抽取 = <b>Model 档</b>（单点转换，结构化输出契约 + 校验闸即可）；新闻摘要 = <b>Model/Workflow 档</b>（若需"检索最新再摘"则是两节点 workflow）；客服退款 = <b>Agent 档</b>（下一步查订单/查政策/问用户/升级人工，取决于对话与查询结果——观察决定行动）。</p>
</details>

<details>
  <summary>2 · DSPy 的 Optimizer、Gorilla 的检索感知训练、RLVR，三者的共同骨架是什么？</summary>
  <p><b>参考答案</b>：都是"数据 + 可计算指标 → 自动改进"：DSPy 改 prompt、Gorilla/RLVR 改权重、RLVR 用可验证奖励。差别只在被优化的对象与信号来源。这正是工程三支柱（Data/System/Eval）的自动化形态——评测不再只是测量，而是优化的燃料。</p>
</details>

<details>
  <summary>3 · 为什么 Pi 敢用"无权限系统 + 树状历史"？这两个决定各自换来什么？</summary>
  <p><b>参考答案</b>：无权限系统换来零摩擦与透明（信任模型与用户，不做拦路虎），代价是安全边界外置给运行环境；树状历史换来"回头路"能力——失败后可回到更早节点分叉重试，而不是线性重放全部。两个决定共同服务它的"刻意简单"哲学：把复杂性赶出核心，交给使用者。</p>
</details>

<details>
  <summary>4 · 你的 agent 要跑 8 小时的数据管道，用 Temporal 的哪些件？为什么 sleep() 是反模式？</summary>
  <p><b>参考答案</b>：每个外部动作（API 调用、LLM 调用）包成 Activity（可重试），流程写成 Workflow（持久化、崩溃可恢复），长等待用服务端计时而不是进程内 sleep——因为 worker 会崩、会扩缩容，只有执行历史里的时间事件能在重启后正确恢复。这就是把"可靠性"从概率世界搬进确定性世界的标准操作。</p>
</details>

## 延伸阅读

- [DSPy 文档](https://dspy.ai) · [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Temporal 文档](https://docs.temporal.io) · [LangFuse](https://langfuse.com) · [LangSmith](https://smith.langchain.com)
- [Harness Tax：arena.ai 博客](https://arena.ai/blog/coding-agents-harness-tax)（同模型换 harness 的成绩差）
- Hamel Husain：[怎样看 prompt 失败](https://hamel.dev/blog/posts/prompt/)（看 traces 的方法论）
- metr.org：[Time Horizons](https://metr.org/time-horizons/)（任务时长指数增长的研究）

**[→ 精选外部资源与视频页](/l05/resources/)**：9 条逐链验证可达的课程、演讲与一手 repo（Karpathy LLMOS 演讲、DL.AI LangGraph 短课、mini-swe-agent / OpenHands / Pi / OpenClaw 四 harness 实物……），按本讲五幕对位，配三个动手任务。

<LessonDone id="l05" />
