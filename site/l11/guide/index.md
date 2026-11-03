---
title: L11 · 术语与复刻指南
---

# L11 · 术语与复刻指南

> [← 返回课文](/l11/) · 费曼检验："凡是我不能创造的，我就不理解"

## 术语考古与复刻检验

<TermCard term="轨迹与环境（Trajectory / Environment）" from="Karpathy 的「conversations 与 environments」：演示 vs 练习场——SFT 的教材 vs RL 的考场" replaced="「语料」——纯文本既没有行动也没有可判定的成功" is="轨迹=Context+学到的 thought/action；环境=任务+沙箱+verifier" isNot="不是一回事的两种叫法——轨迹教模仿，环境养策略（分布内 vs 分布外的应对）" />

<TermCard term="逆动力学标注（Inverse Dynamics）" from="机械学术语（由运动结果反推力）→ VideoAgentTrek：看视频结果反推每步点了什么键" replaced="人工看视频逐帧标动作——不可扩量" is="模型从「前后两帧」反推动作标签：39K 视频→1.52M 交互步" isNot="不是完美标注——反推有噪声，靠后续验证过滤兜底" />

<TermCard term="Harness 过拟合" from="SWE-bench 训练实践：同一任务可跑在多种 harness 上，但轨迹只来自一种" replaced="「模型学会了写代码」——可能只学会了 mini-swe-agent 的输出格式" is="SFT 把能力与脚手架约定一起模仿且无法区分——换 harness 即掉分" isNot="不是 benchmark 过拟合的别名——那是题目泄漏；这是格式/约定的绑定" />

### 复刻清单 · 造一份 agent 训练数据的五零件

任务定义（目标可判定）→ 环境沙箱（真软件或高保真模拟）→ 轨迹采集（rollout + 验证过滤）→ harness 多样性（多脚手架混采）→ 泄漏与事故审计（held-out 新题 + 事故卡检查单）。**缺验证过滤 = 好坏通吃；缺 harness 多样性 = 换壳就废。**

<details>
  <summary>复刻检验 · 给"内部运维 agent"设计一份数据方案：两类数据各多少、来自哪几种来源、怎么防六事故中的至少三个？</summary>
  <p><b>参考答案（示例）</b>：环境侧——工单系统模拟环境（⑤）+ 注入故障造任务（④）配真实回放 verifier；轨迹侧——SRE 操作录像转轨迹（①）+ 运维 wiki 挖掘（②），全过"工单关闭+回归测试"过滤。防事故：擦工单号防背题、verifier 隔离防改成绩、混用 CLI/API harness 防格式绑定。</p>
</details>
