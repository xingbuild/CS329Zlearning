# 总交接 · L05–L08 外部资源页工程化（给 xing 主 session）

> 交付方：检索 session（xing-ReAct）· 2026-10-30
> 接收方：xing 主 session（session_3eae7b9b758a4dacdb68d2194c55c8ee）
> 用户指令：按 L02/L03/L04 既有逻辑，把 L05–L08 四讲的外部资源页逐讲工程化。检索 session 本次未改动 `site/` 与 AGENTS.md。

## 1 · 分讲交接文件（按此顺序逐个执行）

| 顺序 | 文件 | 建议产物 |
|---|---|---|
| 1 | [handoff/2026-10-30-l05-resources.md](./2026-10-30-l05-resources.md) | `site/l05/resources/index.md`（9 条正选） |
| 2 | [handoff/2026-10-30-l06-resources.md](./2026-10-30-l06-resources.md) | `site/l06/resources/index.md`（6 条正选） |
| 3 | [handoff/2026-10-30-l07-resources.md](./2026-10-30-l07-resources.md) | `site/l07/resources/index.md`（8 条正选） |
| 4 | [handoff/2026-10-30-l08-resources.md](./2026-10-30-l08-resources.md) | `site/l08/resources/index.md`（6 条正选） |

四个文件内含：材料清单（按各讲幕结构对位、每条带验证日期 2026-10-30 与一句话定位）、未核实候选（未验证不入库，处理意见在文件内）、动手任务建议（L03 模具：tip 块置顶）、融入建议。

## 2 · 统一约定（与 L02–L04 保持一致）

- **模具**：§4.2 外部资源页——`site/lNN/resources/index.md`，页首"← 返回课文" + 验证日期 + 坦诚的话；三个动手任务 tip 置顶；按幕分组；每条"名称（类型）— 一句话定位"。
- **登记三处**：讲次侧栏组、课文延伸阅读入口行、（如适用）labs 交叉。
- **红线**：未验证候选不入库（各分文件 §2）；论文 arXiv 已在延伸阅读的不重复搬运，资源页只做"展开定位"或"交叉引用一行"。
- **每讲完成过 GATE.md 四道门**（内容/交互/交付/一体化），四讲全部完成后收尾：AGENTS.md 当前状态 + CHANGELOG + 版本号。

## 3 · 跨讲资源分配（避免重复，主放页 + 交叉引用页）

| 资源 | 主放 | 交叉引用 |
|---|---|---|
| Anthropic《Building Effective Agents》 | L06（五模式出处） | L05（判据） |
| DL.AI《AI Agentic Design Patterns with AutoGen》 | L06（四模式） | L08（multi-agent 章） |
| Pi repo（earendil-works/pi） | L05（Harness 案例） | L06（Pi 案例幕） |
| LangChain《How we built agent memory》 | L07 | —（延伸阅读已挂，只展开） |
| DSPy 官方文档 | L05 | L06（STORM 用 dspy 构建，一行带过） |

## 4 · 本批验证中发现的全网变动（入库请用新址）

- **cognition.ai → cognition.com**（Don't Build Multi-Agents）
- **badlogic/pi-mono → earendil-works/pi**（GitHub org 迁移，旧链自动重定向，两者皆可用，建议新址）
- **www.mast.systems 已失效**（域名落入医疗公司）——MAST 只可用 arXiv:2503.13657
- docs.anthropic.com → platform.claude.com（L04 批次已发现，如 L05–L08 页面用到 Anthropic 文档链接一并按此处理）
- Mem0 repo 算法已从论文四操作演进为 ADD-only（教学点：论文→工程漂移，L07 文件 §1.5 有展开）
- DeepLearning.AI crewAI 短课疑似下架（500）、LangChain Academy 课程页 404、Anthropic memory tool 文档路径未定位——均列候选未入库

## 5 · 逐讲条数与类型盘点（供页首"坦诚的话"）

- L05：9 条 = 课程 2 + repo 4 + 演讲 1 + 文档展开 1 + 交叉 1（选型层：学问在别人的代码与判据里）
- L06：6 条 = 判据文 2 + 课程 1 + repo 1 + 交叉 2（论文密集区：延伸阅读是主战场，本页补工业展开）
- L07：8 条 = 课程 1 + repo 3 + 官网/博客 3 + 展开 1（无成熟可视化，但一手实物阵容最豪华）
- L08：6 条 = 判据文对撞 2 + 正典文档 3 + 交叉 1（核心价值在"同周正反判据对读"）

## 6 · 收尾建议（四讲全部完成后）

1. 全站资源页 L02–L08 集齐（八讲完）——可在 L08 资源页页尾加闭环提示（L08 文件 §3 有建议措辞）。
2. AGENTS.md「当前状态」加一条 2026-10-30 记录；§4.2 的资源页类型从"四讲齐备"更新为"全站齐备"。
3. pub 发布（版本号 + CHANGELOG 一条）。
4. `handoff/2026-10-30-l0{5,6,7,8}-*.md` 与本文件处理完毕后去留由你与用户商定。
