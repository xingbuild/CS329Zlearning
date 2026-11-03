---
title: L11 · Agent 数据：喂什么，教出什么
---

# L11 · Agent 数据：喂什么，教出什么

> 对应讲义 lecture11 · 全 75 页 · 约 45 分钟 · 前置：L09（优化）· 进阶三部曲之三（Data 支柱）

L09 优化的是模型外的系统；这一讲"优化模型本身"——而**数据是那根主杠杆**。讲义 tl;dr：过去两年 agent 能力的大涨，几乎全靠大规模"agentic 数据"的涌入。先看一个反直觉的开场事实：

> **最好的模型 ≠ 最好的老师**（OpenThoughts-Agent 实验）：用 GPT-5.3-Codex 的轨迹训练的学生，反而不如用旧一代 GLM-4.7 轨迹训练的——数据贵在质与适配，不在老师的名气。**你以为在买模型能力，其实在买数据的分布。**

::: info 演进谱系 · 本讲的一条链
网络文本（只有对话、没有环境）→ 人类演示（真但贵）→ 网络挖掘（issue/教程/视频转轨迹）→ 合成（模型写步骤、造任务）→ 模拟用户与环境（无限练习，但学会模拟器的错）。问题主线：**agent 的"教材"从哪来、又偷偷教了什么**。（[全课程谱系图 →](/lineage/)）
:::

<LessonPack mins="45" :units="[{ t: 'Lab 10 · 数据工坊', href: '/l11/lab/' }, { t: '外部资源 · 三个任务', href: '/l11/resources/' }]" />

## 第一幕：两类数据与奖励谱系

**轨迹（trajectory）**= 演示：一段 agent 解题的完整记录（Context 只含系统提示/任务/工具输出；**要学的是 thought 与 action**——格式由 harness 决定）→ 拿来 **SFT**（模仿）。**环境（environment）**= 练习场：任务 + 沙箱 + 成功判据 → 拿来 **RL**（练习）。Karpathy 的一句话版：conversations 与 environments。

奖励谱系（可靠窄 ↔ 泛模糊）：**代码测试**（确定性）→ rubric 检查单 → LLM-as-Judge → 人类偏好。量级感（DeepSeek v3 系）：预训练 14.8T tokens、SFT 1.5M 例、RL 85K 任务——且一年后 post-train 预算已超预训练 10%。

## 第二幕：五来源全景

<div class="widget">
  <h3>五来源 × 成本/真实/规模/事故</h3>
  <DataSourceMap />
</div>

三个对照案例值得记住：**Mind2Web vs OpenCUA**（众包记录 vs 自己电脑上录屏+无障碍树+事后合成推理）；**Synatra vs AgentTrek**（离线写步骤 $0.031/条 vs 真浏览器重放 $0.55/条——前者便宜但无真实截图，后者贵但保真）；**SWE-smith**（注入 bug 自动造 50K 任务只花 20 人工时——任务也可以是造出来的）。

## 第三幕：数据的事故教学——它偷偷教什么

"有了一堆轨迹和环境，训练就万事大吉？"——不。六张事故卡（全部真实案例，点开看"以为 vs 实际"）：

<div class="widget">
  <h3>事故卡动物园 · 你以为它在学 vs 它实际在学</h3>
  <DataGotcha />
</div>

三类结构性 gotcha（讲义归纳）：**Reward Hacking**（环境奖励有漏洞）、**过拟合 Harness**（轨迹只教一种脚手架的格式——SFT 分不清能力与脚手架，模型把 harness 约定当能力学了；解法：训练时换着 harness 用）、**训练趋势**（SFT 会过拟合——SWE-RL 同种子数据上 SFT 拉低五个域外任务而 RL 提升它们；RL 会过冲——OpenThoughts 最佳 checkpoint 之后过探索崩塌，他们发布的是崩塌前快照）。

## 第四幕：六条 takeaway（讲义原话的直译）

1. Agent 需要的不只是文本——任务、环境、轨迹；2. 人类演示真实但贵、难上量；3. 挖掘轨迹便宜——代码/教程/视频都能转；4. 合成可以极便宜地扩量；5. 模拟器给无限练习——**但它的错误也会被学进去**；6. **数据总在偷偷教**——reward hack 与 harness 过拟合是常态而非例外。

## 术语考古与复刻检验

<TermCard term="轨迹与环境（Trajectory / Environment）" from="Karpathy 的「conversations 与 environments」：演示 vs 练习场——SFT 的教材 vs RL 的考场" replaced="「语料」——纯文本既没有行动也没有可判定的成功" is="轨迹=Context+学到的 thought/action；环境=任务+沙箱+verifier" isNot="不是一回事的两种叫法——轨迹教模仿，环境养策略（分布内 vs 分布外的应对）" />

<TermCard term="逆动力学标注（Inverse Dynamics）" from="机械学术语（由运动结果反推力）→ VideoAgentTrek：看视频结果反推每步点了什么键" replaced="人工看视频逐帧标动作——不可扩量" is="模型从「前后两帧」反推动作标签：39K 视频→1.52M 交互步" isNot="不是完美标注——反推有噪声，靠后续验证过滤兜底" />

<TermCard term="Harness 过拟合" from="SWE-bench 训练实践：同一任务可跑在多种 harness 上，但轨迹只来自一种" replaced="「模型学会了写代码」——可能只学会了 mini-swe-agent 的输出格式" is="SFT 把能力与脚手架约定一起模仿且无法区分——换 harness 即掉分" isNot="不是 benchmark 过拟合的别名——那是题目泄漏；这是格式/约定的绑定" />

### 复刻清单 · 造一份 agent 训练数据的五零件

任务定义（目标可判定——缺=无法过滤成功）／环境沙箱（真软件或高保真模拟——缺=学到 mock 的世界观）／轨迹采集（人或模型 rollout + **验证过滤**——缺=好坏一起学）／harness 多样性（多脚手架混采——缺=格式绑定）／泄漏与事故审计（held-out 新题 + 事故卡检查单——缺=上线才发现在背题/hack）。**缺验证过滤 = 好坏通吃；缺 harness 多样性 = 换壳就废。**

<details>
  <summary>复刻检验 · 给"内部运维 agent"设计一份数据方案：两类数据各多少、来自哪几种来源、怎么防六事故中的至少三个？</summary>
  <p><b>参考答案（示例）</b>：环境侧——把内部工单系统做成模拟环境（⑤），注入故障造任务（④）配真实回放脚本当 verifier；轨迹侧——SRE 的操作录像+审计日志转轨迹（①），运维 wiki 教程挖掘（②）补量，全部过"工单关闭+回归测试"过滤。防事故：擦除工单号防背题（memo）、verifier 环境隔离防改成绩（exit/git）、混用 CLI 与 API 两种 harness 防 harness 过拟合。</p>
</details>

## 带走三句话

1. 数据是 agent 的主杠杆：**轨迹教模仿、环境养策略**——语料、演示、挖掘、合成、模拟，五来源各背一身债（贵/偏/假/漏/模拟器误差）。
2. **配比胜过单品**：人类演示锚定真实、合成拉开规模、验证器把守质量——数据采购买的是"真实 × 规模"的乘积。
3. 数据总在偷偷教：**reward hack 与 harness 过拟合是常态**——held-out 新题与事故审计不是可选项（接 L10：任务即软件）。

## 思考题

<details>
  <summary>1 · 为什么"最好的模型"可能教出更差的学生？给出至少两个机制。</summary>
  <p><b>参考答案</b>：①<b>分布不匹配</b>——强老师的解法可能跳步/依赖自身能力（学生够不着），弱老师更贴近学生可达的行为分布（zone of proximal development 的数据版）；②<b>轨迹质量≠教学质量</b>——老师答案对但推理路径对学生不可模仿。启示：选 teacher 看学生能学多少，不是看老师多强。</p>
</details>

<details>
  <summary>2 · Synatra（$0.031，离线写步骤）与 AgentTrek（$0.55，真浏览器重放）差 17 倍价格，各适合什么场景？</summary>
  <p><b>参考答案</b>：Synatra 适合<b>格式与指令跟随的预训练级铺垫</b>（量大管饱、分布广、不要求像素级真实）；AgentTrek 适合<b>视觉/交互敏感的精调</b>（真实截图与可访问性树——观测分布必须真实）。组合拳：便宜的打底 + 贵的收口（配比思想的又一例）。</p>
</details>

<details>
  <summary>3 · 你的 RL agent 在模拟环境里练到 95 分，上线 60 分。列出三个模拟器假设并给出诊断顺序。</summary>
  <p><b>参考答案</b>：假设一<b>状态转移</b>与真实一致（DreamGym 的经验模型有系统性偏差）；假设二<b>奖励</b>与真实成功对齐（模拟 verifier 弱→练出 hacking）；假设三<b>任务分布</b>覆盖真实（模拟任务模板窄）。诊断顺序：先拿真实环境轨迹离线评估（分辨能力 vs 适应）、再查奖励对齐（用真实 verifier 重打分）、最后看分布覆盖。</p>
</details>

<details>
  <summary>4 · 六事故卡里哪三张的防线在 L10 的"任务即软件"里？各自对应哪条纪律？</summary>
  <p><b>参考答案</b>：sys.exit(0)→verifier 环境隔离；eval 感知/背题→held-out 与持续新任务（基准会腐烂）；.git 漏洞→solution 自证与评分前清理。数据侧的事故最终都靠<b>评测侧的纪律</b>兜底——三部曲在这里闭环。</p>
</details>

## 延伸阅读

- Mind2Web（[arXiv:2306.06070](https://arxiv.org/abs/2306.06070)）· OpenCUA（[arXiv:2506.23476](https://arxiv.org/abs/2506.23476)）· SWE-rebench（[arXiv:2410.03713](https://arxiv.org/abs/2410.03713)）
- AgentTrek（[arXiv:2412.09605](https://arxiv.org/abs/2412.09605)）· Synatra（[arXiv:2410.07541](https://arxiv.org/abs/2410.07541)）· SWE-smith（[arXiv:2504.21798](https://arxiv.org/abs/2504.21798)）· R2E-Gym（[arXiv:2406.12045](https://arxiv.org/abs/2406.12045)）

**[→ 精选外部资源页](/l11/resources/)**：五来源论文群一手现场，配三个动手任务。

<LessonDone id="l11" />
