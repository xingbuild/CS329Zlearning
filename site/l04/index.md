<LessonPack mins="50" :units="[{ t: 'Lab 01 · Structured I/O', href: '/l04/lab/' }, { t: 'Lab 03 · Coding 闭环', href: '/l04/lab2/' }, { t: '外部资源', href: '/l04/resources/' }]" />

---
title: L04 · 工具使用：从会说到会做
---

# L04 · 工具使用：从会说到会做

> 对应讲义 lecture04Tool Use.pdf · p.3–68 · 约 50 分钟 · 前置：L01–L03 · **配套实验：[Lab 01 · Structured I/O 实验室](/l04/lab/)（本讲的四件套之②）**

L01 让模型"会做"，靠的就是工具；这一讲把"工具"本身拆开：**模型怎么学会调用工具、工具怎么暴露给模型、工具用得好不好怎么量化**。你在 Lab 01 已经从工程侧打穿了一遍（结构化输出 → 掩码解码 → function calling 协议 → 最小闭环），这一讲补齐算法侧与生态侧的完整图景。

## 开场：RAG 的天花板，逼出工具

讲义用三页给 RAG 收尾（p.4–13），也顺手给出了"为什么需要工具"的动机：

- **Lost in the middle**（p.6–7）：闭卷最好 ~56%，只喂相关文档的"oracle" ~88.5%——中间那 30 个点被上下文吃掉了；且 RAG 曲线在 **10–20 篇文档后就饱和**——检索器再好，模型也用不动更多文档；
- **引用本身也会幻觉**（p.8–9，Liu et al. 2023）：RAG 的独特卖点是可引用，但引文是模型生成的——读起来可信，精确率/召回率都低；
- **大海捞针**（p.12）：针在，不代表每次都捞得着。

一句话：**"把资料塞进上下文"这条路有物理上限**。真正的大厦要走另一条路——让模型伸手去操作世界。

## 演进谱系 · 三个时代一条链

本讲全部技术挂在一条链上（背景 → 根本问题 → 技术应答 → 代价 → 新问题），先看全图再进细节：

<div class="widget">
  <h3>工具使用的三时代演进链（点击任一时代展开全文）</h3>
  <EvoChain />
</div>

## 第一幕：三类缺口与工具的定义

<TermCard term="Tool（工具）" from="2024 年综述的正典定义——比口语的插件/API 更窄：函数接口 + 外部确定性程序" replaced="人工写死的调用胶水代码（前 LLM 时代 workflow 的固定分支）" is="一份契约（签名/Schema）+ 模型外部的确定性执行" isNot="不是 prompt 的一部分，也不是模型的一部分——模型只生成调用意图" />

讲义 p.15–19 的分类值得整表背下：

| 缺口类型 | 具体内容 | 工具对应物 |
|---|---|---|
| **算不了** | 大数算术、多步逻辑演绎、精确可验证操作 | 计算器、代码解释器、符号求解器/验证器 |
| **没见过** | 长尾事实、训练截止后事件、私有数据 | 网络搜索、实时 API、内部语料 RAG |
| **够不着** | 非语言接口（API/数据库）、物理世界、实时状态 | function calling/MCP、浏览器/机器人、时钟/传感器/行情 |

而"工具"的正典定义（Wang et al. 2024 综述，p.18）：**LM 使用的工具 = 一个运行在模型之外的计算机程序的函数接口；模型生成函数调用与入参来使用它。** 注意两个关键词：**函数接口**（签名即契约）与**运行在外部**（执行是确定性的，不属于概率世界）。这正是 lab01 的中心命题——"模型生成数据，代码解释执行"。

最简例子（p.20）：`What is 17,423 × 892?` → 模型输出 `calculate(17423 × 892)` → 计算器返回 `15,541,316`。模型贡献了**意图**，工具贡献了**正确性**。

## 第二幕：模型怎么学会调工具——从自监督到规模化

**Toolformer（Schick et al., 2023，p.22–31）**：让 6B 的 GPT-J **教自己**用工具，三步：

1. **采样候选**：在"模型已经很有把握"的位置（loss 低于阈值 τ_s）采样可能的 API 调用——`Pittsburgh is known as [QA("What other name is Pittsburgh known by?")] the Steel City`；
2. **执行**：真跑一遍 API，拿到结果插回文本；
3. **过滤**（精髓）：用加权交叉熵比较"有调用+有结果"是否比"不调用"**更能降低后续 token 的 loss**，只留增益超过 τ_f 的调用。

用过滤后的数据微调 GPT-J——结果（p.30）：Toolformer(6B) 在事实补全、时间题等任务上超过原模型，多任务逼近 GPT-3(175B)。**loss filter 的本质**：把"这个调用有没有用"变成一个**可计算的量**——不需要人工标注"何时该调用"。

**三条规模化路线**（p.32–45）：

- **ToolkenGPT**：把每个工具变成一个 token（"toolken"），为它学一个 embedding——工具一旦被预测，模型切进"工具模式"补参数。**工具入了词表**；
- **ToolLLM**：16k+ 真实 API，配一个**神经 API 检索器**按指令推荐工具——API 多到要检索（L03 又回来了）；
- **Gorilla**：1.6k API（TorchHub/TFHub/HF Hub），GPT-4 自举指令数据；两个工程亮点：**检索感知训练 RAT**（训练时混入错误检索，教模型"该信时信、该忽略时忽略"）与 **AST 子树匹配**评估（不比字符串，比语法树——调用幻觉率显著下降）。

| | Toolformer | ToolkenGPT | ToolLLM | Gorilla |
|---|---|---|---|---|
| 调用形式 | 文本内嵌调用 | 一个新 token | ReAct 式轨迹 | API 调用代码 |
| 训练什么 | GPT-J 6B | toolken embeddings | LLaMA 7B | LLaMA 7B |
| 标签从哪来 | 自监督（loss 过滤） | 真值/合成调用 | ChatGPT 轨迹 | GPT-4 self-instruct |
| 何时调用 | loss filter 学出 | embedding 触发 | 微调 | 微调 |
| 规模 | 5 个工具 | 234 | 16k API | 1.6k API |

## 第三幕：标准接口三代——从"改模型"到"改协议"

讲义 p.47 的一张对仗给全讲定了调：**上面这些方法都在"改模型来适应工具"（每个新 API 再训练一次）；标准接口走反方向——"改工具的描述方式，让任何模型都能用"（运行时给 schema，不为每个 API 微调）。**

<div class="widget">
  <h3>接口三代剧场 · 同一个"查天气"的三种接法</h3>
  <InterfaceEvo />
</div>

<TermCard term="Function Calling（函数调用）" from="OpenAI 2023-06 命名；直系祖先是 Toolformer 的 API calls——从论文机制变成产品协议" replaced="前 GPT-4 时代的做法：从模型文本里用正则抠参数（开场实验里它碎给你看过）" is="schema 一份三吃：菜单（进上下文）/ 文法（约束解码）/ 校验（执行前闸门）" isNot="不是模型替你执行函数——执行永远发生在你的代码里" />

三代的本质差异一句话（p.48）：**REST 面向人**（读文档、手写请求、无机器契约）→ **Function Calling 面向模型**（JSON Schema 即契约，harness 校验分发，但 schema 困在各家代码库）→ **MCP 面向生态**（一个协议任意客户端，`tools/list` 运行时发现、`tools/call` 执行、入站/出站双 auth）。

<TermCard term="MCP（Model Context Protocol）" from="Anthropic 2024-11 发布；类比：agent 世界的 USB-C——一次实现、任意客户端" replaced="每个工具 × 每个宿主的 N×M 份重复适配代码" is="一个网络协议：tools/list 运行时发现 + tools/call 执行 + 入站/出站双 auth" isNot="不是模型能力，也不是插件商店——只是协议；工具可信仍是你自己的责任" />

两个工程甜点（p.55–56）：FastMCP 可以**直接从 OpenAPI 规范一键生成 MCP 服务器**（`FastMCP.from_openapi(...)` → 自动得到 `list_assignments`/`post_grade` 等工具）；**入站/出站认证分离**（agent→MCP 服务器一个 token，MCP 服务器→真正的 API 另一个 token）。

## 第四幕：评估——工具用得好不好，怎么算数

讲义 p.58–66。

**BFCL**（Berkeley Function-Calling Leaderboard，p.58–60）：三层评估——**AST 语法比对**（离线、快）、**真实执行**（跑起来看结果）、**状态跟踪**（多步多轮后世界状态对不对）；语言覆盖 Python/C++/Java/SQL；还有**相关性检测**（给一堆不相关的函数，正确答案是"拒绝调用"——`What is 2*3?` + 只有 `add` 可用时，答 `Error: only add is available` 才算对）。

**ToolBench**（p.61–62）：16k 真实 API × 人类指令，考规模。

**τ-bench**（p.63–66）：引入了**用户**——tool-agent-user 三方交互，模型还要会按政策办事、会问用户。它带来的最重要的数学是 **pass^k**：

<div class="widget">
  <h3>pass^k 计算器 · "至少一次成功" vs "每次都成功"</h3>
  <PassKCalc />
</div>

pass@k（抽 k 次至少一次成功）是研究口径的乐观指标；pass^k（k 次全部成功）才是**部署口径**——客户不会接受"十分之七的概率给你重试"。你认出它了：**pass^k 就是 L01 的 pⁿ 换了件衣服**。

## 第五幕：工具使用的失败模式

讲义 p.67，三族九种（与 L03 失败动物园同款结构）：

| 层 | 失败 | 一句话 |
|---|---|---|
| **单次调用** | 选错工具 / 该不调时调了 | 选择问题 |
| | 参数编造字段、类型/单位错 | lab01 语义闸的靶子 |
| | 幻觉出不存在的 API | Gorilla 用 AST 度量的那种 |
| **多步链** | 跳过前置调用、顺序错 | sequencing |
| | 失败后原地重试、不退避不换路 | recovery——ReAct 的改道能力考的就是这 |
| **对话** | 违反政策强行办事 | τ-bench 的 policy 维度 |
| | 该问用户时自作主张 | interaction |
| | 这次过了下次挂 | 非确定性——pass^k 来收你 |

## 复刻清单 · 最小 Function Calling 的五个零件（费曼检验）

不看任何材料，你能从零重建吗？五个零件，缺一件坏一处（对照第五幕失败模式）：

1. **schema 注册表**——JSON Schema 定义工具（缺 → 模型不知道有什么可调）；
2. **菜单注入**——schema 序列化进上下文（缺 → 有工具而无从选择）；
3. **保证层**——约束解码或校验闸让 arguments 合法（缺 → 参数幻觉直击产线，Lab 01 第 2/3 站）；
4. **分发器**——按 name 路由、沙箱执行（缺 → 意图永远只是意图）；
5. **结果回喂**——带 tool_call_id 配对写回上下文（缺 → 闭环断裂成两次孤立调用）。

**检验句**：让你现在从零复刻，最先卡住的是哪个零件？——那就是你要回去重学的地方。

## 与 Lab 01 的连接（本讲四件套之②）

先看一次工具调用的完整解剖——**Select → Arguments → Validate → Execute → Result**，正是讲义 p.58 的那张图：

<div class="widget">
  <h3>一次工具调用的解剖 · 确定性边界在哪几步</h3>
  <ToolCallAnatomy />
</div>

这一讲的每条主线，Lab 01 都给你留了亲手入口：

- **结构化输出与校验闸** → lab01 step2（两道闸）；
- **约束解码**（function calling 的"保证"从哪来）→ lab01 step3/4（正则→NFA→掩码，GBNF/Outlines）；
- **function calling 协议载荷**（schema 一份三吃：菜单/文法/校验）→ lab01 step5；
- **工具选择与最小闭环**（Select → Arguments → Validate → Execute）→ lab01 step6——`validate=False` 的对照运行就是"失败模式表"的现场演示。

## 带走三句话

1. 工具 = **函数接口 + 外部确定性执行**；模型贡献意图（概率），工具贡献正确性（确定）——结构化输出是两者之间的契约。
2. 学会调用的两条历史路线：**改模型**（Toolformer 自监督 → Gorilla 规模化）输给了**改协议**（REST → function calling → MCP）——运行时 schema 打败了逐 API 微调。
3. 工具评估的三层深处是**可靠性文化**：AST → 执行 → 状态；单次 → 链 → 对话；pass@k → **pass^k**（= pⁿ）。

## 思考题

<details>
  <summary>1 · Toolformer 的 loss filter 为什么巧妙？它与 RLVR 共享什么思想？</summary>
  <p><b>参考答案</b>：它把"这个 API 调用有没有用"变成可计算量（是否降低后续 token 的 loss），从而免掉人工标注——自监督造标签。与 RLVR 共享的内核：<b>把模糊的目标变成可判定的信号</b>（loss 下降 / 测试通过），再让优化去追这个信号。</p>
</details>

<details>
  <summary>2 · 为什么说"改协议"路线战胜了"改模型"路线？MCP 比 function calling 多解决了什么？</summary>
  <p><b>参考答案</b>：逐 API 微调不可扩展（每来一个新工具就训练一次），运行时 schema 把适配成本从"训练"降到"描述"。MCP 在 FC 之上多解决<b>生态问题</b>：schema 从各家代码库走到网络协议层——运行时发现（tools/list）、跨宿主复用、统一的三类资源（tools/resources/prompts）与双 auth。类比：FC 是 USB 接口，MCP 是 USB 标准 + 设备目录。</p>
</details>

<details>
  <summary>3 · 你的 agent 通过率 90%，客户要求"连跑 5 次全过"——过不了关怎么办？</summary>
  <p><b>参考答案</b>：pass^5 = 0.9⁵ ≈ 59%。两条路：抬 p（校验闸+重试把单次成功率推高——失败变成可恢复的）或降 k（缓存确定性结果、幂等设计让"重跑"变成"不跑"）。注意这是 L01 pⁿ 与修复回路（e → e^k）的工程重现。</p>
</details>

<details>
  <summary>5 · 复刻检验：合上材料，写出最小 function calling 的五个零件，并说出缺第 ③ 件与第 ⑤ 件分别会发生什么。</summary>
  <p><b>参考答案</b>：五零件见"复刻清单"。缺③：arguments 是概率文本直通代码——TypeError/注入击穿产线（Lab 01 闭环剧场关闸版）；缺⑤：工具执行了但观察进不了上下文，模型不知结果，循环断裂。</p>
</details>

<details>
  <summary>4 · BFCL 的"相关性检测"考的是什么能力？为什么它比"会调用"更难？</summary>
  <p><b>参考答案</b>：考"不该调用时拒绝"——工具选择的另一半。难在模型天然倾向于"给出动作"（训练分布里满是调用示例），拒绝需要模型理解<b>任务与工具的不匹配</b>，这比匹配更抽象；也是幻觉调用（调不存在的 API）的镜像问题。</p>
</details>

## 延伸阅读

- Schick et al., *Toolformer: Language Models Can Teach Themselves to Use Tools*（arXiv:2302.04761）
- Patil et al., *Gorilla: Large Language Model Connected with Massive APIs*（arXiv:2305.15334）
- Wang et al., *What Are Tools Anyway? A Survey from the LM Perspective*（arXiv:2403.15452）
- Yao et al., *τ-bench: Tool-Agent-User Interaction*（arXiv:2406.12045）· [BFCL 排行榜](https://gorilla.cs.berkeley.edu/leaderboard.html) · [MCP 文档](https://modelcontextprotocol.io)
- 动手：**[Lab 01 · Structured I/O 实验室](/labs/)**——本讲全部主线的亲手版

### 外部资源 · 交互与视频

**[→ 精选外部资源与视频页](/l04/resources/)**：14 条逐链验证可达的文档、课程与榜单（Anthropic 工具设计哲学、Outlines/Instructor、FastMCP、BFCL 在线演示、τ-bench Pass^1–4、工具投毒实测……），按本讲五幕对位。

先带走三个动手任务（详见资源页顶部）：

1. [BFCL 在线演示](https://gorilla.cs.berkeley.edu/leaderboard.html)里输入 `What is 2*3?` 只给 `add`——**亲手考相关性检测**（思考题 4）；
2. 对照 [OpenAI Structured Outputs 指南](https://developers.openai.com/api/docs/guides/structured-outputs)与 [Lab 01 第 3 站](/l04/lab/)——**"保证"从哪来**；
3. 看 [Invariant 工具投毒](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks.html)——**两道闸为什么挡不住语义注入**。

<LessonDone id="l04" />
