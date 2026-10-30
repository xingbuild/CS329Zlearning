---
title: L05 · 术语与复刻指南
---

# L05 · 术语与复刻指南

> [← 返回课文](/l05/) · 费曼检验："凡是我不能创造的，我就不理解"

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

