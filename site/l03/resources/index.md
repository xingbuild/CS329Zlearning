---
title: L03 · 外部资源与视频
---

# L03 · 外部资源与视频

> [← 返回 L03 课文](/l03/) · 2026-10-27 逐条验证可达 · 外链随时间可能失效，发现打不开请反馈

这一页是 L03 课文的**外部对照实验室**：页内的分块实验室与失败动物园是"机制模拟"，这里的工具、视频与文章是真实世界的 RAG 工程生态。先说一句坦诚的话：**RAG 领域天然缺交互可视化工具**（成熟的只有分块与向量空间两类），所以本页比 L02 偏图文——交互 4 件、视频 4 件、图文/论文 10 件，按课文五幕对位。

## 先做这三个动手任务

::: tip 任务 ① · 亲手看见"证据被切断在边界上"
打开 [ChunkViz](https://chunkviz.com/)，贴入一段含"周四 9 点平均 3 人排队"的日志文本，把 chunk size 从 100 拨到 500、overlap 从 0 调到 20%——观察这条关键证据**何时被切断在块边界上**。这就是课文思考题 1 的"再看分块"环节，也是页内分块实验室的现实版。
:::

::: tip 任务 ② · 亲眼看看"语义邻近"长什么样
打开 [Embedding Projector](https://projector.tensorflow.org/)，加载默认 Word2Vec 10K 数据，分别搜一个报错码风格的稀有词与一个常见词，各看最近邻——体会 **DPR 式语义邻近与 BM25 式字面匹配的失效面为何互补**（思考题 2 的直觉来源）。
:::

::: tip 任务 ③ · 手算一个 Hit@5 = 0
配合 Pinecone 的[评估指标手算例](https://www.pinecone.io/learn/offline-evaluation/)与页内失败动物园，构造一个"top-5 里根本没有相关段"的例子——**先测检索，再怪模型**，这是本讲最重要的排查纪律。
:::

## 第一幕 · Retriever–Reader 框架与 RAG 的两副面孔

- IBM Technology：[What is Retrieval-Augmented Generation (RAG)?](https://www.youtube.com/watch?v=T-D1OfcDW1M) **（视频，约 6 分钟）**——参数记忆 vs 即时证据的最清晰入门短片（可开自动中文字幕）。
- Jay Alammar：[The Illustrated Retrieval Transformer](https://jalammar.github.io/illustrated-retrieval-transformer/) **（图文）**——RETRO：以 GPT-3 约 4% 参数量靠查库匹配其表现；文末综述 REALM / DPR / FiD / RAG。正对课文"术语考古"：论文里的 RAG 是端到端联合训练模型。

## 第二幕 · 索引侧：分块、上下文注入、向量物理层

- [ChunkViz](https://chunkviz.com/) **（交互）**——粘贴文本、选切分器、拨 chunk size / overlap，块边界实时高亮；页内分块实验室的外部对照版，动手任务 ① 的场地。
- Greg Kamradt：[The 5 Levels Of Text Splitting For Retrieval](https://www.youtube.com/watch?v=8OJC21T2SL4) **（视频，约 1 小时）**——字符 → 递归 → 文档结构 → 语义 → Agentic 五级切分，正对讲义 p.24 的四代策略。
- Jina AI：[Late Chunking in Long-Context Embedding Models](https://jina.ai/news/late-chunking-in-long-context-embedding-models/) **（图文）**——Late Chunking 概念出处（讲义 p.30–31），含朴素分块 vs 晚分块示意与 BeIR 基准。
- Microsoft：[GraphRAG 文档](https://microsoft.github.io/graphrag/) **（文档）**——LLM 抽实体关系建图、Leiden 聚类、社区摘要；Global / Local / DRIFT 三种搜索（讲义 p.34–35 的官方实现）。
- [TensorFlow Embedding Projector](https://projector.tensorflow.org/) **（交互）**——PCA / t-SNE / UMAP 投影高维向量，点选任一点看最近邻；动手任务 ② 的场地。
- [WizMap](https://poloclub.github.io/wizmap/) **（交互）**——浏览器内探索百万级 embedding 地图（Georgia Tech Polo Club）。
- Pinecone：[Hierarchical Navigable Small Worlds (HNSW)](https://www.pinecone.io/learn/series/faiss/hnsw/) **（图文）**——跳表 → NSW → 分层图的推导；M / efConstruction / efSearch 参数与召回–速度–内存基准（讲义 p.36–38）。

## 第三幕 · 检索侧：三代检索器、漏斗与评估

- Elastic：[Practical BM25 — Part 2: The BM25 Algorithm and its Variables](https://www.elastic.co/blog/practical-bm25-part-2-the-bm25-algorithm-and-its-variables) **（图文）**——IDF × 词频饱和（k1）× 长度归一（b），三套索引实证对比（讲义 p.41 的公式逐项展开）。
- Pinecone：[Rerankers and Two-Stage Retrieval](https://www.pinecone.io/learn/series/rag/rerankers/) **（图文）**——bi-encoder 粗筛 → cross-encoder 精排漏斗；"4000 万文档 BERT 重排需 50+ 小时 vs 向量检索 <100ms"的量级对比（讲义 p.50）。
- Pinecone：[Evaluation Measures in Information Retrieval](https://www.pinecone.io/learn/offline-evaluation/) **（图文 + 代码）**——Recall@K / MRR / MAP / nDCG 逐步手算例；动手任务 ③ 的场地。
- [MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) **（交互榜单）**——嵌入模型按检索等任务排名，选型用。

## 第四幕 · Agentic RAG：把检索变成动作

- LangChain：[RAG From Scratch](https://youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x)（[配套代码](https://github.com/langchain-ai/rag-from-scratch)，约 9.5k★）**（视频 18 集 + notebooks）**——索引/检索 → 查询改写、路由、RAG-Fusion、HyDE → CRAG、Self-RAG、Adaptive RAG；**横跨第二、三、四幕**的最佳实操系列。
- [Self-RAG 项目页](https://selfrag.github.io/) **（项目页）**——反思 token 框架图解，论文 / 代码 / 7B·13B 模型（讲义 p.57 的官方出处）。
- DeepLearning.AI：[Building Agentic RAG with LlamaIndex](https://www.deeplearning.ai/short-courses/building-agentic-rag-with-llamaindex/) **（免费短课，约 54 分钟 6 课）**——路由查询引擎 → 工具调用 → agent 推理循环 → 多文档 agent。

## 第五幕 · 失败动物园

- Barnett et al.：[Seven Failure Points When Engineering a RAG System](https://arxiv.org/abs/2401.05856) **（论文）**——三个真实案例的七失败点经验报告；核心论断与页内动物园同气连枝：**"RAG 的健壮性是演化出来的，不是一开始设计出来的。"**
- Liu et al.：[Lost in the Middle](https://arxiv.org/abs/2307.03172)（TACL 2023）**（论文）**——U 形曲线：证据放中间就被丢——阅读侧失效的实证根源，也是 L02 context rot 的原始证据。
