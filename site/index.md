---
layout: home

hero:
  name: Engineering AI Agents
  text: 把「会用 AI」变成「会工程化 AI」
  tagline: 以斯坦福 CS329Z 讲义为底本的交互式课程——每一讲都从一个真实场景的失败开始，逼出机制，再用可交互的演示拆到本质：概率大脑 × 确定性边界。
  actions:
    - theme: brand
      text: 从 L01 开始 →
      link: /l01/
    - theme: alt
      text: 先看课程地图
      link: #课程地图

features:
  - icon: 🧭
    title: L01 · Agent 是什么：一个循环的五十年
    details: 同一道题、三种接线：控制流的归属如何决定成败；解剖图与四大挑战。
    link: /l01/
  - icon: 🧱
    title: L02 · LLM 作为建筑材料
    details: 概率采样机、上下文窗口、成本结构：动手前必须懂的物理性质。
    link: /l02/
  - icon: 🔎
    title: L03 · RAG：外挂知识器官
    details: 检索 → 增强 → 生成，以及它如何天然成为 agent 的第一个工具。
    link: /l03/
  - icon: 🔧
    title: L04 · 工具使用：从会说到会做
    details: 结构化输出与函数调用协议——配套 Lab 01 已可先玩。
    link: /l04/
  - icon: 🏗️
    title: L05 · 框架与编排：看穿打包术
    details: 框架到底替你做了什么；用不用框架，是一道架构决策题。
    link: /l05/
  - icon: 🧩
    title: L06 · 设计模式与脚手架
    details: ReAct、Reflexion、规划-执行：被实践验证过的循环形状。
    link: /l06/
  - icon: 🧠
    title: L07 · 记忆架构
    details: 上下文窗口 ≠ 记忆：存什么、怎么压缩、何时取回的工程系统。
    link: /l07/
  - icon: 🌐
    title: L08 · 多智能体系统
    details: 分工、通信与失控成本：本质是组织设计问题。
    link: /l08/
---

<HomeProgress :ids="['l01', 'l02', 'l03', 'l04', 'l05', 'l06', 'l07', 'l08']" />

## 一张图看懂这门课

<AgentPanorama />

## 课程地图

四个阶段、八讲，从「单个 agent 的器官」到「agent 社会」。已上线讲次点卡片进入；学习进度自动保存在本机浏览器。

## 实战实验室

实验室与讲次相互独立、双击即用、零依赖——全部逻辑在浏览器本地运行。

- **[Lab 01 · Structured I/O 实验室](/labs/)** —— 从裸接口失败动物园，到正则→NFA→掩码解码，再到函数调用协议与最小 agent 闭环。（配套 L04 / L06）

## 如何使用本课程

1. **读** —— 每讲按「场景 → 本质 → 机制 → 思考题」推进，先见问题，后见方法。
2. **玩** —— 交互组件是课程的一部分：逐步播放、拨动参数、看因果，玩过才算学过。
3. **答** —— 每讲末尾的思考题先自己答，再展开参考答案；答不上来回上一幕。

::: tip 这条线贯穿全课程
Agent = **循环（五十年历史）** + **通用大脑（LLM）**。全课只做一件事：给概率大脑加确定性边界——结构化输出、校验闸、工具协议、记忆系统、评测与安全，并在误差复利 p<sup>n</sup> 的现实里，把工程做可靠。
:::
