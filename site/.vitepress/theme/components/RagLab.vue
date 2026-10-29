<script setup lang="ts">
import { ref, computed } from 'vue'

/* ============ 语料库（内置；d5 为可开关的干扰文档） ============ */
interface Doc { id: string; name: string; lines: string[]; gold?: number; distract?: boolean }
const DOCS: Doc[] = [
  { id: 'd1', name: '答疑时间.md', lines: ['答疑时间安排。', '周二16:00-17:00平均14人排队。', '周四09:00-10:00平均3人排队，推荐。', '周五不安排答疑。'], gold: 2 },
  { id: 'd2', name: '错误代码表.md', lines: ['常见错误代码说明。', 'ERR_4021表示配额耗尽，需要升级套餐。', 'ERR_5002表示网络超时，直接重试即可。'], gold: 1 },
  { id: 'd3', name: '作业政策.md', lines: ['作业迟交每天扣除10%。', '里程碑不可使用迟交额度。', '期末报告第10周周四截止。'], gold: 2 },
  { id: 'd4', name: '评分标准.md', lines: ['项目占40%，作业占15%。', '论文视频占10%，同伴互评占20%。', '期末报告与演示占10%。'] },
  { id: 'd5', name: '校园生活.md', lines: ['食堂中午排队平均20人。', '图书馆占座要在周四早上抢。', '校园卡充值请到服务大厅。'], distract: true },
]

const QUESTIONS = [
  { id: 'qA', label: 'A · 精确词', text: '错误码 ERR_4021 是什么意思？', gold: 'd2' },
  { id: 'qB', label: 'B · 释义（有干扰）', text: '哪个答疑时段人最少？', gold: 'd1' },
  { id: 'qC', label: 'C · 跨文档竞争', text: '期末报告什么时候截止？', gold: 'd3' },
]

type Chunking = 'fixed' | 'overlap' | 'structure'
type Retriever = 'bm25' | 'vec' | 'hybrid'

/* ============ 状态 ============ */
const stage = ref(0)
const STAGES = ['① 语料', '② 分块', '③ 提问', '④ 检索', '⑤ 生成']
const chunking = ref<Chunking>('fixed')
const retriever = ref<Retriever>('bm25')
const qid = ref('qB')
const distractOn = ref(true)
const k = 3

const q = computed(() => QUESTIONS.find((x) => x.id === qid.value)!)
const goldDoc = computed(() => DOCS.find((d) => d.id === q.value.gold)!)
const corpus = computed(() => DOCS.filter((d) => !d.distract || distractOn.value))

/* ============ 分块 ============ */
interface Chunk { docId: string; docName: string; text: string; goldFull: boolean; goldCut: boolean }
function chunkDoc(d: Doc): Chunk[] {
  // 金标准只对"当前问题的目标文档"生效（问题换了，判定跟着换）
  const goldLine = d.id === q.value.gold && d.gold !== undefined ? d.lines[d.gold] : ''
  const mk = (text: string): Chunk => ({
    docId: d.id, docName: d.name, text,
    goldFull: !!goldLine && text.includes(goldLine),
    goldCut: !!goldLine && !text.includes(goldLine) && sharesGoldFrag(text, goldLine),
  })
  const full = d.lines.join('')
  if (chunking.value === 'structure') return [mk(full)]
  const size = 45
  const step = chunking.value === 'overlap' ? Math.floor(size * 0.66) : size
  const out: Chunk[] = []
  for (let i = 0; i < full.length; i += step) out.push(mk(full.slice(i, i + size)))
  return out
}
function sharesGoldFrag(text: string, gold: string): boolean {
  for (let i = 0; i + 4 <= gold.length; i++) if (text.includes(gold.slice(i, i + 4))) return true
  return false
}
const chunks = computed<Chunk[]>(() => corpus.value.flatMap(chunkDoc))

/* ============ 检索（BM25 + TF-IDF 向量 + RRF） ============ */
function norm(s: string): string {
  return s.toLowerCase().replace(/[\s，。？?！!，、:：;；()（）%％\-]/g, '')
}
function ngrams(s: string, n: number): string[] {
  const t = norm(s)
  const out: string[] = []
  for (let i = 0; i + n <= t.length; i++) out.push(t.slice(i, i + n))
  return out
}
function tf(list: string[]): Map<string, number> {
  const m = new Map<string, number>()
  for (const t of list) m.set(t, (m.get(t) || 0) + 1)
  return m
}

const qTermsBi = computed(() => tf(ngrams(q.value.text, 2)))
const qTri = computed(() => tf(ngrams(q.value.text, 3)))

function bm25Scores(): { c: Chunk; score: number; hits: string[] }[] {
  const docsTf = chunks.value.map((c) => ({ c, tf: tf(ngrams(c.text, 2)) }))
  const N = docsTf.length
  const avgdl = docsTf.reduce((s, d) => s + d.tf.size, 0) / Math.max(N, 1)
  const k1 = 1.5, b = 0.75
  return docsTf.map(({ c, tf: dtf }) => {
    let score = 0
    const hits: string[] = []
    for (const [term, qf] of qTermsBi.value) {
      const f = dtf.get(term)
      if (!f) continue
      let ni = 0
      for (const { tf: t2 } of docsTf) if (t2.has(term)) ni++
      const idf = Math.log(1 + (N - ni + 0.5) / (ni + 0.5))
      score += idf * ((f * (k1 + 1)) / (f + k1 * (1 - b + (b * dtf.size) / Math.max(avgdl, 1))))
      if (qf > 0) hits.push(term)
    }
    return { c, score, hits }
  })
}
function cosine(a: Map<string, number>, b: Map<string, number>): number {
  let dot = 0, na = 0, nb = 0
  for (const [, v] of a) na += v * v
  for (const [t, v] of b) { nb += v * v; const av = a.get(t); if (av) dot += av * v }
  return dot / (Math.sqrt(na) * Math.sqrt(nb) || 1)
}
function vecScores(): { c: Chunk; score: number }[] {
  const N = chunks.value.length
  const docTri = chunks.value.map((c) => ({ c, tf: tf(ngrams(c.text, 3)) }))
  const df = new Map<string, number>()
  for (const { tf: t } of docTri) for (const g of t.keys()) df.set(g, (df.get(g) || 0) + 1)
  const w = (m: Map<string, number>) => {
    const o = new Map<string, number>()
    for (const [g, f] of m) o.set(g, (1 + Math.log(f)) * Math.log(1 + N / (df.get(g) || 1)))
    return o
  }
  const qw = w(qTri.value)
  return docTri.map(({ c, tf: t }) => ({ c, score: cosine(qw, w(t)) }))
}

interface Ranked { c: Chunk; score: number; hits: string[]; rank: number }
const results = computed<Ranked[]>(() => {
  let base: { c: Chunk; score: number; hits: string[] }[]
  if (retriever.value === 'bm25') base = bm25Scores().sort((a, b) => b.score - a.score)
  else if (retriever.value === 'vec') base = vecScores().sort((a, b) => b.score - a.score)
  else {
    const r1 = bm25Scores().sort((a, b) => b.score - a.score)
    const r2 = vecScores().sort((a, b) => b.score - a.score)
    const rrf = new Map<string, { c: Chunk; score: number; hits: string[] }>()
    r1.forEach((x, i) => { const e = rrf.get(x.c.text + x.c.docId) || { c: x.c, score: 0, hits: x.hits }; e.score += 1 / (60 + i + 1); rrf.set(x.c.text + x.c.docId, e) })
    r2.forEach((x, i) => { const e = rrf.get(x.c.text + x.c.docId) || { c: x.c, score: 0, hits: [] }; e.score += 1 / (60 + i + 1); rrf.set(x.c.text + x.c.docId, e) })
    base = Array.from(rrf.values()).sort((a, b) => b.score - a.score)
  }
  return base.slice(0, k).map((x, i) => ({ ...x, rank: i + 1 }))
})

/* ============ 生成判定 ============ */
const goldPos = computed(() => {
  const gi = results.value.findIndex((r) => r.c.goldFull)
  return gi >= 0 ? gi + 1 : 0
})
const posProb = [0.95, 0.72, 0.5]
const verdict = computed(() => {
  if (goldPos.value === 0) {
    return { ok: false, tone: 'bad', title: '❌ 幻觉风险（召回天花板）',
      detail: '证据根本没进 top-3——分块把关键句切散了，或被干扰文档挤掉了。此刻模型只能编。对应失败动物园：检索侧·召回天花板。' }
  }
  const p = posProb[goldPos.value - 1]
  if (goldPos.value === 1) {
    return { ok: true, tone: 'good', title: `✅ 有据作答（把握约 ${(p * 100).toFixed(0)}%）`,
      detail: '证据排在第 1 位，组装进上下文后模型可靠引用作答。引用：' + goldDoc.value.name }
  }
  return { ok: true, tone: 'warn', title: `⚠️ 证据在第 ${goldPos.value} 位（把握约 ${(p * 100).toFixed(0)}%）`,
    detail: '证据进了上下文但不在头部——U 形曲线告诉你中间位置更容易被忽略（Lost in the Middle）。对策：重排，让最相关者居首。' }
})

function switchStage(i: number) { stage.value = i }
const stageHints = [
  '五份小文档构成语料库。注意 d5《校园生活.md》是干扰项：它含有"周四/排队/早上"这类与答疑问题相似但不相关的词——右上的开关可以把它扔进/扔出语料，看排名怎么变。',
  '换三种切分策略，盯住橙色高亮的关键证据句：固定 45 字会把"周四09:00平均3人"切断在边界上；加 20% 重叠后它在相邻块中完整出现；按结构切则整篇一块、自带上文。',
  '三道题各代表一种考法：A 考精确词（错误码）、B 考释义且干扰文档最凶、C 考跨文档竞争（两份文档都含"期末报告"）。',
  'BM25 看字面（二元组 + IDF），向量看邻近（三元组 TF-IDF 余弦——真实系统这里是神经嵌入，机制同构）；混合用 RRF 融合两份排名。命中词那一行就是"为什么是它"的证据。',
  '把 top-3 组装成上下文（证据位置一目了然），然后看判定：未命中=召回天花板，位置靠后=中间丢失风险。答案错了？回第②步改分块，或回第④步换检索器。',
]
</script>

<template>
  <div class="rlab">
    <div class="rail-row wrap">
      <button v-for="(s, i) in STAGES" :key="s" type="button" class="wbtn" :aria-pressed="i === stage"
        @click="switchStage(i)">{{ s }}</button>
      <span class="pill brand">管道：{{ { fixed: '固定45字', overlap: '固定+重叠', structure: '按结构' }[chunking] }} · {{ { bm25: 'BM25', vec: '向量', hybrid: '混合RRF' }[retriever] }} · 干扰文档{{ distractOn ? '开' : '关' }}</span>
    </div>
    <div class="rail-row wrap">
      <button type="button" class="wbtn" :disabled="stage === 0" @click="stage--">◀ 上一步</button>
      <button type="button" class="wbtn primary" :disabled="stage === 4" @click="stage++">下一步 ▶</button>
      <span class="meta">RAG 交互实验室 · 全部计算在你的浏览器里实时进行</span>
    </div>
    <div class="hint"><span class="k">现在做什么 · </span>{{ stageHints[stage] }}</div>

    <!-- ① 语料 -->
    <div v-if="stage === 0" class="stagebox">
      <div class="doccard" v-for="d in corpus" :key="d.id" :class="{ distract: d.distract }">
        <div class="docname">{{ d.name }} <span v-if="d.distract" class="pill">干扰项</span></div>
        <div class="doclines">
          <span v-for="(l, i) in d.lines" :key="i" class="ln" :class="{ gold: d.id === q.gold && d.gold === i }">{{ l }}</span>
        </div>
      </div>
      <div class="ctl-row">
        <label class="switch"><input type="checkbox" v-model="distractOn" /> 干扰文档《校园生活.md》{{ distractOn ? '在库中' : '已移除' }}</label>
      </div>
    </div>

    <!-- ② 分块 -->
    <div v-else-if="stage === 1" class="stagebox">
      <div class="ctl-row wrap">
        <button v-for="c in (['fixed', 'overlap', 'structure'] as Chunking[])" :key="c" type="button" class="wbtn"
          :aria-pressed="chunking === c" @click="chunking = c">{{ { fixed: '固定 45 字', overlap: '固定 + 重叠', structure: '按结构（整篇）' }[c] }}</button>
        <span class="pill">共 {{ chunks.length }} 块</span>
      </div>
      <div class="chunkgrid">
        <div v-for="(c, i) in chunks" :key="i" class="chunkcard" :class="{ goldfull: c.goldFull, goldcut: c.goldCut }">
          <div class="cname">{{ c.docName }} · 块{{ i + 1 }} <span v-if="c.goldFull" class="pill brand">关键证据完整</span><span v-else-if="c.goldCut" class="pill bad">证据被切断</span></div>
          <div class="ctext">{{ c.text }}</div>
        </div>
      </div>
    </div>

    <!-- ③ 提问 -->
    <div v-else-if="stage === 2" class="stagebox">
      <div class="ctl-row wrap">
        <button v-for="qq in QUESTIONS" :key="qq.id" type="button" class="wbtn" :aria-pressed="qid === qq.id"
          @click="qid = qq.id">{{ qq.label }}</button>
      </div>
      <div class="qbox">{{ q.text }}</div>
      <div class="qnote">金标准答案在 <b>{{ goldDoc.name }}</b>（① 中蓝色高亮的那句）。</div>
    </div>

    <!-- ④ 检索 -->
    <div v-else-if="stage === 3" class="stagebox">
      <div class="ctl-row wrap">
        <button v-for="r in (['bm25', 'vec', 'hybrid'] as Retriever[])" :key="r" type="button" class="wbtn"
          :aria-pressed="retriever === r" @click="retriever = r">{{ { bm25: 'BM25（字面·IDF）', vec: '向量（邻近·余弦）', hybrid: '混合（RRF 融合）' }[r] }}</button>
      </div>
      <div class="ranklist">
        <div v-for="r in results" :key="r.c.docId + r.c.text" class="rankrow" :class="{ hit: r.c.goldFull }">
          <span class="rnum">#{{ r.rank }}</span>
          <div class="rbody">
            <div class="rname">{{ r.c.docName }} <span v-if="r.c.goldFull" class="pill brand">✓ 金标准</span><span v-else-if="r.c.docId === 'd5'" class="pill bad">干扰项上榜</span></div>
            <div class="rtext">{{ r.c.text.slice(0, 40) }}…</div>
            <div class="rwhy">得分 {{ r.score.toFixed(4) }}<template v-if="retriever === 'bm25' && r.hits.length"> · 命中词：{{ r.hits.slice(0, 5).join(' / ') }}</template></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ⑤ 生成 -->
    <div v-else class="stagebox">
      <div class="ctxbox">
        <div class="ctxtitle">组装进上下文的 top-3（按排名）</div>
        <div v-for="r in results" :key="'ctx' + r.c.docId + r.c.text" class="ctxrow" :class="{ hit: r.c.goldFull }">
          <span class="cpos">{{ r.rank }}</span>
          <span>{{ r.c.docName }}</span>
          <span v-if="r.c.goldFull" class="pill brand">证据在此（{{ r.rank === 1 ? '头部 ✓' : '非头部 ⚠' }}）</span>
        </div>
      </div>
      <div class="verdict" :class="verdict.tone">
        <div class="vtitle">{{ verdict.title }}</div>
        <div class="vdetail">{{ verdict.detail }}</div>
      </div>
      <div class="ctl-row">
        <button type="button" class="wbtn" @click="stage = 1">↩ 回②改分块重试</button>
        <button type="button" class="wbtn" @click="stage = 3">↩ 回④换检索器</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.rlab { display: flex; flex-direction: column; gap: 10px; }
.rail-row { display: flex; align-items: center; gap: 8px; }
.rail-row.wrap { flex-wrap: wrap; }
.meta { color: var(--vp-c-text-3); font-size: 12.5px; }
.stagebox { display: flex; flex-direction: column; gap: 10px; margin-top: 4px; }
.ctl-row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.switch { display: flex; align-items: center; gap: 8px; font-size: 14px; cursor: pointer; }
.doccard { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 10px 14px; }
.doccard.distract { border-style: dashed; }
.docname { font-size: 13px; font-weight: 650; color: var(--vp-c-text-2); margin-bottom: 4px; display: flex; gap: 8px; align-items: center; }
.doclines { font-size: 14px; line-height: 1.8; }
.ln { margin-right: 6px; }
.ln.gold { background: rgba(37, 99, 235, 0.14); color: #2563eb; border-radius: 4px; padding: 0 3px; }
.chunkgrid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 8px; }
.chunkcard { border: 1px solid var(--vp-c-divider); border-radius: 9px; padding: 8px 11px; font-size: 12.5px; }
.chunkcard.goldfull { border-color: #2563eb; background: rgba(37, 99, 235, 0.06); }
.chunkcard.goldcut { border-color: #d97706; }
.cname { font-size: 11.5px; color: var(--vp-c-text-3); margin-bottom: 3px; display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.ctext { line-height: 1.6; color: var(--vp-c-text-2); word-break: break-all; }
.pill.bad { background: rgba(220, 38, 38, 0.1); color: #dc2626; }
.qbox { font-size: 16.5px; font-weight: 650; background: var(--vp-c-default-soft); border-radius: 9px; padding: 10px 16px; }
.qnote { font-size: 13.5px; color: var(--vp-c-text-3); }
.ranklist { display: flex; flex-direction: column; gap: 7px; }
.rankrow { display: flex; gap: 12px; border: 1px solid var(--vp-c-divider); border-radius: 9px; padding: 8px 12px; align-items: flex-start; }
.rankrow.hit { border-color: #2563eb; background: rgba(37, 99, 235, 0.05); }
.rnum { font-weight: 700; color: var(--vp-c-text-3); min-width: 28px; padding-top: 2px; }
.rname { font-size: 13.5px; font-weight: 650; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.rtext { font-size: 12.5px; color: var(--vp-c-text-2); margin-top: 2px; }
.rwhy { font-size: 11.5px; color: var(--vp-c-text-3); margin-top: 2px; }
.ctxbox { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 10px 14px; }
.ctxtitle { font-size: 12.5px; color: var(--vp-c-text-3); margin-bottom: 6px; }
.ctxrow { display: flex; gap: 10px; align-items: center; font-size: 14px; padding: 3px 0; }
.ctxrow.hit { color: #2563eb; font-weight: 650; }
.cpos { min-width: 20px; font-weight: 700; }
.verdict { border-radius: 10px; padding: 12px 16px; font-size: 14.5px; line-height: 1.7; }
.verdict.good { background: rgba(22, 163, 74, 0.1); }
.verdict.warn { background: rgba(217, 119, 6, 0.12); }
.verdict.bad { background: rgba(220, 38, 38, 0.1); }
.vtitle { font-weight: 700; margin-bottom: 4px; }
</style>
