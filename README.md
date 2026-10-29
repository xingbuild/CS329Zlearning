# Engineering AI Agents · 学习仓库

AI Agent 工程的系统学习仓库：**讲义**（lecture PDF）+ **交互式课程站**（site/ · VitePress v2）+ **实战实验室**（labs/）。
学习即产品：边学边把每一讲沉淀为课程页面，目标部署上网开放给更多学习者。

> Agent（助手）必读：[AGENTS.md](AGENTS.md) —— 身份、教学法、v2 架构约定与项目当前状态。

## 快速开始

```bash
eaia        # ← 随时启动课程站（任意终端；= 构建最新内容 + 本地服务 + 自动开浏览器）
            #   别名指向仓库根目录的 start.sh；停止：终端 Ctrl+C

# 逐条等价写法
cd site && npm install && npm run dev      # 迭代模式（热更，localhost:5173）
cd site && npm run build                   # 构建 → site/.vitepress/dist
cd site && npx vitepress preview           # 预览构建产物（localhost:4173）

# 实验室：双击 labs/01-structured-io/structured-io-lab.html，无需任何环境
```

- **v1（冻结版）**：双击 [index.html](index.html) 进入——历史版本，仅作参考，不再迭代。
- 部署：`npm run build` 后把 `dist` 交给任意静态托管（GitHub Pages / Netlify / Cloudflare Pages 皆可）。

## 目录结构

```
engineeringaiagents/
├── AGENTS.md                # Agent 工作契约（连续性事实源）
├── index.html               # → v1 冻结版入口
├── lecture01–08 *.pdf       # 课程讲义（ground truth，勿部署）
├── v1/                      # v1 冻结版静态站
├── site/                    # ★ v2 课程站（VitePress：markdown 课文 + Vue 交互组件）
│   ├── index.md / l01/ / labs/
│   └── .vitepress/          # 配置 + 主题 + 组件
└── labs/                    # 实战实验室（独立项目，互不依赖）
```

## 讲次一览（site/）

| # | 讲次 | 状态 | 特色交互 | 配套讲义 |
|---|------|------|----------|----------|
| L01 | Agent 是什么：一个循环的五十年 | ✅ | 控制流剧场 + pⁿ 计算器 + ReAct 论文精读（34 段三层） | lecture01 |
| L02 | LLM 作为建筑材料 | ✅ | 采样实验室 + KV Cache 剧场 | lecture02 |
| L03 | RAG：外挂知识器官 | ✅ | 分块实验室 + RAG 失败动物园 | lecture03 |
| L04 | 工具使用：从会说到会做 | ✅ | 接口三代剧场 + pass^k 计算器（配套 Lab 01） | lecture04 |
| L05 | 框架与编排：看穿打包术 | ✅ | Agency 光谱 + Harness 对比 | lecture05 |
| L06 | 设计模式与脚手架 | ✅ | 工作流/上下文模式图鉴 | lecture06 |
| L07 | 记忆架构 | ✅ | 记忆类型图谱 + 设计盘 | lecture07 |
| L08 | 多智能体系统 | ✅ | 编排拓扑选择器 + MAS 失败动物园 | lecture08 |

## labs 索引

| # | 项目 | 教什么 | 入口 | 形态 |
|---|------|--------|------|------|
| 02 | [RAG 交互实验室](site/l03/lab/) | 整条 RAG 管道浏览器内真跑：分块切散证据 / BM25·向量·RRF 真实检索 / 召回天花板与中间丢失现场复现 | 课程站内页面 | **v2 产品化** |
| 01 | [structured-io](labs/01-structured-io/) | Structured I/O 本质：概率文本→形式语言的条件化；校验回路 vs 掩码解码；Function Calling 协议；agent 闭环 | 双击 [structured-io-lab.html](labs/01-structured-io/structured-io-lab.html)；进阶脚本见其 [README](labs/01-structured-io/README.md) | 遗留（独立 HTML） |

## 约定（详见 AGENTS.md）

- 新增讲次：`site/lNN/index.md` + 交互组件（.vue）+ 三处清单登记（config 侧栏 / index.md features / HomeProgress ids）。
- 新增实验室：`labs/NN-项目名/`（零依赖、双击即用）；发布时复制 HTML 进 `site/public/labs/`。
- 每次变更后更新 AGENTS.md「当前状态」。

> 教学法：问题先行——先场景与根本问题，再方法与机制；交互产品"控件位置固定、指引随进度更新、内容不无限增长"。
