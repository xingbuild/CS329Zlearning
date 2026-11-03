---
title: L10 · 术语与复刻指南
---

# L10 · 术语与复刻指南

> [← 返回课文](/l10/) · 费曼检验："凡是我不能创造的，我就不理解"

## 术语考古与复刻检验

<TermCard term="Task / Verifier（任务与验收器）" from="Terminal-Bench/Harbor 词表：Task=单测（定输入+成功判据）；Verifier=打分逻辑——评测世界的「测试用例/断言」" replaced="「跑个 demo 看看」——没有固定输入与判据的观察不是测量" is="instruction + environment + tests 三件套：agent 无关、可移植、可复现" isNot="不是「数据集」——数据集只有输入输出，任务还带环境与验收" />

<TermCard term="Reward Hacking（奖励作弊）" from="RL 术语进入评测工程：优化器无情利用奖励函数的每个漏洞——你的断言就是它的奖励函数" replaced="「agent 不听话」——它非常听话，只是听的是断言不是意图" is="agent 满足可测量的部分、牺牲不可测量的意图（空文件骗存在性检查）" isNot="不是对抗性攻击——是度量与目标错位的必然（Goodhart 在考场重演）" />

<TermCard term="版本三元组（rerun/regrade/reuse）" from="Harbor 的任务版本学：改 agent 环境升 x（要重跑）、改 verifier 升 y（可重评分旧轨迹）、改文档升 z（复用）" replaced="「基准就是基准」——静态基准会静默腐烂（新模型新行为、依赖漂移）" is="评测资产的 semver：结果的可比性靠版本纪律维持" isNot="不是官僚流程——是「全收据」可比性的前提" />

### 复刻清单 · 可判定任务的五零件

明确指令（每句可对应断言）→ 真实环境（Docker 真软件）→ outcome 验收（对最终状态断言）→ 隔离与自证（verifier 隔离 + 参考解先全绿）→ 收据（轨迹+工件落盘）。**缺隔离 = Open score；缺自证 = 你在考 agent 还是在考自己的 bug。**

<details>
  <summary>复刻检验 · 你要测"agent 会修 CSV 报表的图"，写出三件套草案，并指出弱验收（只查文件存在）会怎么被 hack。</summary>
  <p><b>参考答案</b>：instruction=读 /app/data.csv 画月度柱状图存 chart.png；environment=python+matplotlib 镜像、烤入 CSV；tests=存在性+PNG 头+柱数=月份数+标题+量程≈源数据 max。弱验收 hack：1×1 像素图或空文件骗过存在性检查（Lab 09 亲手复现）。</p>
</details>
