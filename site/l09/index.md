---
title: L09 · 优化：从玄学到搜索
---

# L09 · 优化：从玄学到搜索

> 对应讲义 lecture09Optimization.pdf · 全 125 页 · 约 50 分钟 · 前置：L05（三支柱与 DSPy）· 进阶三部曲之一（System 支柱）

L05 说过：**Optimizer 把三支柱（Data/System/Eval）代码化了**。这一讲把那句话拆开——优化算法的完整族谱：改 prompt（context）、改权重（weight）、让 agent 自己改（agent-as-optimizer），以及什么时候选哪条。先亲手体验一下为什么要学它：

::: info 演进谱系 · 本讲的一条链
手调 prompt（玄学不可复现）→ 数据驱动（fewshot 顺序/熵 → bootstrap 自举：模型自己造数据）→ 反思进化（OPRO/MIPROv2/GEPA：模型看着失败改指令）。问题主线：**"改系统"怎么从手艺变成可度量的搜索**。更大的杠杆（权重、agent 自改）在第四、五幕接棒。（[全课程谱系图 →](/lineage/)）
:::

<LessonPack mins="50" :units="[{ t: 'Lab 08 · 优化决策台', href: '/l09/lab/' }, { t: '外部资源 · 三个任务', href: '/l09/resources/' }]" />

## 开场实验：提示彩票

同一道数学题、同一个模型，只换一句开场白——先押注，再揭示：

<div class="widget">
  <h3>提示彩票机 · 你猜得中吗</h3>
  <PromptLottery />
</div>

押中或押错都不重要——重要的是**这件事本身没有先验**。手工调优是抽样一张巨大彩票（措辞 × 顺序 × 示例的组合空间），且每换一个任务重抽。本讲的答案一句话：**优化 = 用数据表达意图、用评测度量进展、用算法替代猜测**（讲义定调：Optimization enables us to specify intent through data and evals）。

## 演进谱系 · 三时代一条链

先看全图（点任一时代展开五段全文）——本讲前半程（第二、三幕）走的就是这条链，第四、五幕接棒更大的杠杆：

<div class="widget">
  <h3>Prompt 优化三时代演进链</h3>
  <OptimizerEvo />
</div>

## 第一幕：什么时候值得优化

**优化的定位是 last mile 适配**（讲义 Conditions 节）：模型给出优秀的通用解，优化把它适配到你的具体场景。三个前提条件（三支柱缺一不可）：

1. **有贴合领域的数据与评测**——示例与反馈能表达 prompt 写不完的需求（"有时候一份好的 eval 比一份好的 prompt 更能表达意图"）；
2. **系统组件多到难手调**——多级 prompt、多个模块的组合空间爆炸；
3. **通用模型不够、微调不值**——介于两者之间的那一段路。

收益清单（讲义 Benefits）：可靠性↑、领域适配、**更小模型更低成本**（保持质量换便宜部署）、从经验中学习（轨迹变资产）、随模型/工具演进持续再适配。

## 第二幕：上下文优化 · 上——fewshot 与自举

**顺序也有信息量**（Fantastically Ordered Prompts, Lu et al. 2022）：同一组示例换个顺序，效果大幅波动；用探针集测**全局熵**（模型输出的不确定性）可以逼近"试遍所有顺序"的 oracle——注意这个方法的妙处：**不看标签，看置信度**，连 ground truth 都不用。

**Bootstrap：让模型自己造训练数据**。STaR（Zelikman et al. 2022）：拒绝采样（rejection sampling）——让模型对题目生成推理，**只保留到达正确答案的轨迹**，再用它们训练自己。DSPy（你已经认识）把这条路搬到 prompt 层：bootstrap 成功轨迹当 few-shot 示例 + 随机搜索组合——**实验证明可以胜过人写的示例与金标签**（讲义：bootstrapping + random search can be better than providing human reasoning or gold labels）。

代价（引擎）：自举的上限是**模型已有的能力**——它挖得出"会做但说不清"的解法，挖不出"根本不会"的。

## 第三幕：上下文优化 · 下——反思式进化

**OPRO**（LLM as Optimizer, Yang et al. 2024）：把"历史指令 + 各自得分"喂给 LLM，让它写一条新指令——开场那张"深呼吸"就是它搜出来的，**不是人想出来的**。

**MIPROv2**（Opsahl-Ong et al. 2024）三步走（本讲最值得复刻的流程）：

1. **Bootstrap 示例**：跑训练集若干次，按 metric 保留成功轨迹（含推理），失败丢弃；
2. **情境化指令提案**（grounded proposal）：把"程序是干什么的（program-aware）+ 数据长什么样（data-aware）+ 成功轨迹样例 + 提示技巧"一起喂给提案 LLM，生成一批候选指令（讲义的 iris 鸢尾花例子：提案 LM 会写出"为了拯救濒危物种，请准确预测鸢尾花品种"这种带场景感的指令）；
3. **贝叶斯代理搜索**：对"指令 × 示例集"的组合维护信念（beliefs），采样→小批量评测→更新信念，每隔几轮全量评测——**在搜索预算内找出最优组合**。

再往前两步：**TextGrad**（把 LLM 的改进建议当"文本梯度"沿系统反向传播回各 prompt）；**GEPA**（遗传式 Pareto 前沿进化， reflective prompt evolution 全面胜出基线）。代价：**prompt 越优化越长**——上下文膨胀与"过拟合评测"的新风险。

## 第四幕：权重优化——把能力烧进参数

**SFT 蒸馏**：teacher 模型在 agent 任务上 rollout → 学生在"老师做完的任务"上微调。FireAct（Chen et al. 2023）：Llama2-13B 微调 GPT-4 轨迹后，**超过了 prompted GPT-3.5**——权重优化把"读提示的能力"换成"长在身上的能力"。OpenThoughts-Agent（Raoof et al. 2026）：强 teacher 轨迹蒸馏全面有效（下一讲 L11 的主角之一）。

**RL：让模型自己练习**。PPO 的账单：**4 个模型驻留显存、每步训 2 个、逐 token 的 KL 计算**——贵。GRPO（DeepSeek-R1 采用）砍掉 value model：**3 个模型、组内相对优势**——同一 prompt 采一组输出，用组内 reward 的 z-score 当优势（"这次比同组平均好多少"）。铁律：**可验证性是关键**（reward 必须可判定——L02 RLVR 的正式展开）。

**On-Policy 蒸馏**（Thinking Machines）：类比妙极——**象棋教练复盘你自己下过的棋，而不是给你看大师对局**；学生按自己的策略走，老师给逐 token logprob 指导。实验：比 RL 更高效、产出的模型更好（学生 logprob − 老师 logprob 的期望，见讲义公式页）。

## 第五幕：让 agent 当优化器

最激进的一层：优化器本身也是 agent。

- **Darwin Gödel Machine**（Zhang et al. 2026）：agent 修改自己的代码，按性能选择父代（且性能越差后代越多——保持探索）；关键发现：**"自己改自己"（而非 meta-agent 代改）与"回访祖先"（而非只沿最新迭代）都至关重要**；
- **Meta-Harness**：meta agent 能看到**全部历史经验**，决定下一步改哪——上下文里积累的"改 harness 史"越来越值钱；
- **Auto-Research**（Karpathy 的 autoresearch）：给 agent 仓库权限——brainstorm → 改代码 → 跑实验 → 指标涨了就保留、跌了就回滚 → 记录发现。**能在软件上跑的东西，agent 都能优化**。

讲义的警告：此时 **evals 成为最要紧的控制点**——agent 优化器会无情地利用评测的每一个漏洞（下一讲 L10 的伏笔）。

## 第六幕：选型判据——context 还是 weight

| 走 Context 优化的三个信号 | 走 Weight 优化的三个信号 |
|---|---|
| **动不了权重**：闭源 API 强模型无微调权限 | **context 已失败**：小模型指令遵循太弱，prompt 雕不出花 |
| **要快跑**：频繁重跑优化，简单基建 | **有强老师要便宜学生**：蒸馏直接换部署成本 |
| **样本金贵**：环境交互贵，context 优化样本效率高一个量级（GEPA 实证） | **上下文在膨胀**：把 prompt 里长出来的知识烧进权重 |

两条实证：**BetterTogether**（prompt→weight→prompt 交替最优）；**GEPA（prompt 优化样本效率 ≫ RL）vs OpenThoughts（weight 优化数据饥渴但千级样本持续涨）**。→ 亲手判六个场景：**[Lab 08 · 优化决策台](/l09/lab/)**。

## 术语考古与复刻检验

<TermCard term="Last Mile Adaptation（最后一公里适配）" from="电信借喻：骨干网已通，最后一段入户线才决定体验——模型是骨干，你的场景是入户" replaced="「等下一代模型」——通用解永远差你场景的最后一段" is="优化的定位：通用模型 × 你的数据与评测 = 你的系统" isNot="不是「调参玄学」——是带度量与搜索空间的工程" />

<TermCard term="Bootstrap（自举）" from="靴襻悖论（pull yourself up by your bootstraps）：用自己的产出抬高自己——STaR/DSPy 的机制名" replaced="人工标注示例——贵、慢、常不带推理过程" is="拒绝采样：模型生成→按可判定指标过滤→保留成功轨迹当教材" isNot="不是无限提升——上限是模型已有能力（挖得出「会而未显」，挖不出「根本不会」）" />

<TermCard term="GRPO（组相对策略优化）" from="DeepSeek-R1（2025）采用而流行：PPO 砍掉 value model，用组内相对比较估计优势" replaced="PPO 的 4 模型显存账单——训练门槛高" is="同 prompt 采一组输出，组内 reward z-score 当优势：这次比同组平均好多少" isNot="不是新 RL 理论——是工程减法：3 模型驻留、序列级优势" />

### 复刻清单 · 最小反思式优化器的零件

评估回路（metric 可判定——缺则"改进"无从谈起）／候选生成（bootstrap 轨迹或 LLM 写新指令——缺则没有搜索空间）／选择机制（贝叶斯信念 / Pareto 前沿 / 简单贪心——缺则搜索退化成抽奖）／预算控制（小批量评测 + 定期全量——缺则算力烧在无效组合上）。**缺评估回路 = OPRO 也只是更贵的抽卡。**

<details>
  <summary>复刻检验 · 不看上文，写出 MIPROv2 三步并说明为什么第二步要"情境化"（grounded）而不是直接让 LLM 写 20 条指令？</summary>
  <p><b>参考答案</b>：①bootstrap 成功轨迹（含推理）→②情境化提案（程序说明+数据摘要+成功样例+技巧 → 生成候选指令）→③贝叶斯代理搜索指令×示例组合（小批量更新信念+定期全量）。情境化的意义：<b>给提案 LLM 提供与任务分布对齐的先验</b>——凭空写指令=在无尽措辞空间均匀采样（彩票）；带着程序/数据/轨迹上下文写=在有依据的邻域采样（搜索）。</p>
</details>

## 带走三句话

1. 优化 = **数据表达意图 + 评测度量进展 + 算法替代猜测**——三支柱是前提，不是可选项。
2. 杠杆从小到大：**措辞 → 示例（自举）→ 指令（反思进化）→ 权重（SFT/RL/蒸馏）→ agent 自改**——每级都有代价与适用信号，别跳级也别停级。
3. 当优化器变成 agent，**evals 就成了主战场**——它优化的是你给的指标，包括指标里的每一个漏洞（→ L10）。

## 思考题

<details>
  <summary>1 · 你的任务上 bootstrap 出的示例效果很差，最可能缺了三支柱中的哪根？为什么 bootstrap 救不了"模型根本不会"的任务？</summary>
  <p><b>参考答案</b>：缺的往往不是 Data 是<b>能力上限</b>——bootstrap 是拒绝采样，过滤的依据是模型偶尔做对；若单次成功率≈0，采样永远为空，无轨迹可留（对应"挖不出根本不会"）。出路：换强模型当 teacher 走 SFT 蒸馏（把能力引进来再优化），或改任务分解降低单步难度。</p>
</details>

<details>
  <summary>2 · GRPO 用"组内 z-score"当优势，为什么不需要 value model？这个设计把什么成本换成了什么成本？</summary>
  <p><b>参考答案</b>：z-score 用<b>同组真实回报的相对比较</b>替代了 value model 对"期望回报"的估计——省掉一个驻留模型与它的训练。换来的是<b>采样成本</b>：每个 prompt 要跑一组（k 个）输出才能算组内统计。本质：用"多采样几次"换"少养一个模型"——对可验证 reward 的场景（代码/数学）极其划算。</p>
</details>

<details>
  <summary>3 · On-policy 蒸馏为什么比"在老师轨迹上 SFT"更适合做 agent？象棋类比里藏着什么机制？</summary>
  <p><b>参考答案</b>：SFT 学的是<b>老师策略下的状态分布</b>，学生部署时走的是自己的分布——分布错配（covariate shift）；on-policy 蒸馏在<b>学生自己的轨迹上</b>给老师的逐 token 指导，学的每一步都发生在学生真实会遇到的状态上。象棋类比：复盘<b>你下过的棋</b>（你的状态分布）比背大师对局（老师分布）更能提高<b>你的</b>胜率。</p>
</details>

<details>
  <summary>4 · Darwin Gödel Machine 里"回访祖先"（不总沿最新版迭代）为什么关键？这与你见过的哪个机制同构？</summary>
  <p><b>参考答案</b>：贪心沿最新版=单臂老虎机式的局部爬山，容易锁死在局部最优；回访祖先=保留<b>探索分支</b>（进化算法的种群多样性）。同构：GEPA 的 Pareto 前沿保留多个非支配解（不只保最优）、DSPy/Lab 04 站②的蒙特卡洛多次采样——都是"用分布对抗贪心"。</p>
</details>

<details>
  <summary>5 · 给"客服退款 agent + 闭源模型 + 每周政策变化"选优化路线，并写出你不会选的两条路的代价。</summary>
  <p><b>参考答案</b>：Context 优化（OPRO/MIPROv2 级）——权重动不了（闭源）+ 分布周级漂移（要快跑）。不选 weight：无训练权限且管线追不上周级变化；不选 agent 自改：退款域的高风险动作不适合"改了就上线"的自动循环（需要人在环），且该场景的搜索空间（指令措辞）不需要仓库级优化器。</p>
</details>

## 延伸阅读

- OPRO: Yang et al.（[arXiv:2309.03409](https://arxiv.org/abs/2309.03409)）· MIPROv2: Opsahl-Ong et al.（[arXiv:2310.03714](https://arxiv.org/abs/2310.03714)）· GEPA（[arXiv:2507.19457](https://arxiv.org/abs/2507.19457)）· TextGrad（[arXiv:2406.07496](https://arxiv.org/abs/2406.07496)）
- STaR（[arXiv:2203.14465](https://arxiv.org/abs/2203.14465)）· FireAct（[arXiv:2310.05915](https://arxiv.org/abs/2310.05915)）· DeepSeek-R1/GRPO（[arXiv:2501.12948](https://arxiv.org/abs/2501.12948)）· Darwin Gödel Machine（[arXiv:2505.22954](https://arxiv.org/abs/2505.22954)）
- On-Policy Distillation：[Thinking Machines 博客](https://thinkingmachines.ai/blog/on-policy-distillation/) · Karpathy [autoresearch](https://github.com/karpathy/autoresearch)

**[→ 精选外部资源与视频页](/l09/resources/)**：DSPy/MIPROv2 文档与论文、on-policy 蒸馏博客、DGM/autoresearch 一手现场，配三个动手任务。

<LessonDone id="l09" />
