---
title: L10 · 评测即事实源：Terminal-Bench
---

# L10 · 评测即事实源：Terminal-Bench

> 对应讲义 lecture10（客座 · Alex Shaw & Ryan Marten，Laude Institute · Terminal-Bench 团队）· 全 64 页 · 约 40 分钟 · 前置：L04 评估幕 · 进阶三部曲之二（Eval 支柱）

1969 年 Hoare 写下程序的经典信条："程序的一切性质，原则上都可以**从程序文本出发、用纯演绎推理**得出。" 七十年后，agent 写的软件永远失去了这个定理——当代码不可读、行为是概率的，你还能把"正确"写在哪里？这一讲的答案：**写进评测里。规范（specification）让位于评测（evaluation）：代码作为事实源 → 评测作为事实源。**

::: info 演进谱系 · 本讲的一条链
演绎式软件（规则即事实源，Hoare）→ 归纳式 ML（数据即事实源）→ **agent：评测即事实源**（Evaluator=?）。问题主线：**当规则不可写，怎么把"正确"钉死**——答案是一个可复现的考场：指令 + 环境 + 隔离的可判定验收。（[全课程谱系图 →](/lineage/)）
:::

<LessonPack mins="40" :units="[{ t: 'Lab 09 · 任务工坊', href: '/l10/lab/' }, { t: '外部资源 · 三个任务', href: '/l10/resources/' }]" />

## 开场：一切数字创造都在归纳化

讲义的史观三跳：1940s 手写机器码 → 1950s 汇编 → 高级语言（**演绎式创造**：Rules + Inputs → Outputs，人写规则）；ML 反转了它（**归纳式创造**：Inputs + Outputs → Rules，人给例子、训练推规则）；现在第三跳——Models（从数据学）、**Agents（从评测进化）**、Software（由 agent 生成）——全部归纳化。specifier 仍是软件工程师，**evaluator 是谁？** 这就是本讲要回答的空格。

## 第一幕：一个 Terminal-Bench 任务长什么样

> **Terminal-Bench**：用 bash 当万能工具的 agent 基准——64 张 model cards、171 位贡献者、700 万+ 次基准运行；首个 commit（2025.1）与 Claude Code 发布（2025.2）同龄。

一个任务 = 一个目录（agent 无关、可移植）：

<div class="widget">
  <h3>任务解剖 · 概率住在哪一段</h3>
  <TaskAnatomyTB />
</div>

看那个真实任务（讲义示例）：给一张 2D 示意图（schematic.png），要求产出 STEP 3D 模型文件——验收是 9 条断言：`watertight()`（水密）、`correct_volume()`、`correct_principal_inertia()`（主惯性矩）……**L04 学的"可判定验收"，在这里是工业级的形态**。

## 第二幕：写任务的纪律

讲义的四问（每一问都是一条防线）：

1. **你在测什么？测得对吗？**——instruction 与 verifier 一一对应（每条断言映射一条需求）；
2. **防 reward hacking**——verifier 环境与 agent 环境隔离（agent 够不着打分处）；参考解（solution/）先跑通再放考（verifier 自证）；solution 不能硬编码答案（要像 agent 会走的路）；
3. **环境要真实**——真软件真服务 > mock；尽量开放世界（但网络依赖要"烤入"镜像防 flaky）；
4. **指令三态选一**——完全指定 / 尽量简洁 / 尽量自然（按你测什么而定），模糊指令 = 给 hacking 留门。

## 第三幕：verifier 设计——对状态的判定

verifier 的定义值得背下来：**对环境最终状态的 outcome 分类器**（不是看过程、不是看文本相似）。设计谱系：程序化断言（确定性，FP 可控）> rubric 检查单 > LLM-as-Judge（泛化但要有校准）> 人类偏好（最泛最贵最模糊）。**每个 verifier 都该报混淆矩阵**（FP/TP/FN/TN）——verifier 自己也是被测对象。

## 第四幕：任务即软件

Terminal-Bench/Harbor 的工程观：**任务就是软件**——软件有 bug，任务也会以微妙的方式坏掉。所以：**Task QA**（静态检查 + agent judge 双检：oracle/judge/frontier/cheat agents 各司其职）；**CI/CD 持续基准**（新模型=新行为，昨日全绿今日假阴性）；**版本三元组** `(x+1,y,z)=rerun / (x,y+1,z)=regrade / (x,y,z+1)=reuse`——改 agent 环境要重跑、改 verifier 要重评分、改文档可复用旧跑；**全收据**：每一行结果都有 per-trial 的轨迹/日志/工件/奖励。

## 术语考古与复刻检验

<TermCard term="Task / Verifier（任务与验收器）" from="Terminal-Bench/Harbor 词表：Task=单测（定输入+成功判据）；Verifier=打分逻辑——评测世界的「测试用例/断言」" replaced="「跑个 demo 看看」——没有固定输入与判据的观察不是测量" is="instruction + environment + tests 三件套：agent 无关、可移植、可复现" isNot="不是「数据集」——数据集只有输入输出，任务还带环境与验收" />

<TermCard term="Reward Hacking（奖励作弊）" from="RL 术语进入评测工程：优化器无情利用奖励函数的每个漏洞——你的断言就是它的奖励函数" replaced="「agent 不听话」——它非常听话，只是听的是断言不是意图" is="agent 满足可测量的部分、牺牲不可测量的意图（空文件骗存在性检查）" isNot="不是对抗性攻击——是度量与目标错位的必然（Goodhart 在考场重演）" />

<TermCard term="版本三元组（rerun/regrade/reuse）" from="Harbor 的任务版本学：改 agent 环境升 x（要重跑）、改 verifier 升 y（可重评分旧轨迹）、改文档升 z（复用）" replaced="「基准就是基准」——静态基准会静默腐烂（新模型新行为、依赖漂移）" is="评测资产的 semver：结果的可比性靠版本纪律维持" isNot="不是官僚流程——是「全收据」可比性的前提" />

### 复刻清单 · 可判定任务的五零件

明确指令（每句话可对应断言——缺=hacking 留门）／真实环境（Docker 真软件——缺=考的不是部署态）／outcome 验收（对最终状态断言——缺=过程分无法复现）／隔离与自证（verifier 隔离 + 参考解先全绿——缺=agent 能改成绩单）／收据（轨迹+工件落盘——缺=无法归因与重评分）。**缺隔离 = Open score；缺自证 = 你在考 agent 还是在考自己的 bug。**

<details>
  <summary>复刻检验 · 你要测"agent 会修 CSV 报表的图"，写出三件套草案，并指出弱验收（只查文件存在）会怎么被 hack。</summary>
  <p><b>参考答案</b>：instruction=读 /app/data.csv 画月度柱状图存 chart.png（指定列与标题）；environment=装好 python+matplotlib 的镜像、烤入 CSV；tests=断言文件存在+PNG 文件头+柱数=月份数+标题文本+量程≈max(源数据)。弱验收的 hack：agent 交 1×1 像素 PNG 或空文件——绿灯放行（Lab 09 站内亲手复现）。</p>
</details>

## 带走三句话

1. 规则不可写时，**评测就是规范**——你写下什么断言，就得到什么 agent；断言的漏洞就是 agent 的捷径。
2. 一个任务 = **可复现的考场**：指令+镜像+隔离验收+参考解自证——同一条指令同一个镜像同一套断言，分数才可比。
3. **任务即软件**：会坏、要 QA、要 CI、要版本——静态基准静默腐烂，全收据是唯一的防腐剂。

## 思考题

<details>
  <summary>1 · 为什么 verifier 要与 agent 环境隔离、且参考解必须先跑通？分别防的是哪类事故？</summary>
  <p><b>参考答案</b>：隔离防<b>篡改</b>（agent 够得着打分处就能改成绩单——sys.exit(0) 式假通过的物理前提）；参考解先全绿防<b>考官出错</b>（verifier 自身有 bug 时，你在测自己的 bug 不是 agent 的能力——两道防线分别保证"成绩单不可改"与"考卷本身有效"）。</p>
</details>

<details>
  <summary>2 · 你的基准三个月没更新，某天分数集体涨了 5 个点。给出至少三种"任务即软件"的解释。</summary>
  <p><b>参考答案</b>：①新模型新行为——旧断言的边界被新风格踩中（假阳性）；②依赖漂移——镜像内未钉住的包升级，环境变了；③数据泄漏——任务被新模型预训练吃进去（背题，见 L11）；④flaky 测试偶发转绿。处置按版本三元组：改 verifier 走 regrade 重评旧轨迹，先确认是模型变了还是考场变了。</p>
</details>

<details>
  <summary>3 · LLM-as-Judge 什么时候比程序化断言好？讲义为什么仍把程序化检查排在前面？</summary>
  <p><b>参考答案</b>：judge 好——需求难以形式化（文风、帮助性、多步合理性）、开放域产出无法枚举断言。程序化优先——<b>确定性、可复现、便宜、无漂移</b>；judge 是概率组件（自身有 FP/FN、随模型版本漂移），能形式化的就别交给概率——又是"确定性边界优先"的取舍。</p>
</details>

<details>
  <summary>4 · 版本三元组里，为什么"改 verifier 升 y 可以只重评分（regrade）旧轨迹"，而"改环境必须重跑（rerun）"？</summary>
  <p><b>参考答案</b>：verifier 是<b>对轨迹/最终状态的事后判定</b>——旧轨迹+新判据=新分数，无需重跑（全收据的价值正在此）；环境变了则轨迹的前提（世界）变了——旧轨迹记录的是旧世界的行为，新环境下行为本身会不同，只能重跑。</p>
</details>

## 延伸阅读

- [Terminal-Bench 官网](https://www.tbench.ai)（基准、64 model cards、任务浏览）· [GitHub laude-institute/terminal-bench](https://github.com/laude-institute/terminal-bench)
- [Harbor](https://harborframework.com)——eval-driven development 工具链（讲义客座方的开源框架）
- Anthropic：[Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)（讲义词表与"写任务纪律"的主要出处）

**[→ 精选外部资源页](/l10/resources/)**：Terminal-Bench/Harbor 一手现场 + Anthropic 评测指南，配三个动手任务。

<LessonDone id="l10" />
