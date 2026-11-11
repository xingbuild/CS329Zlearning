<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { ROUNDS, META, HINTS, ORIGIN, CODE, FILES } from './harnessTrajectory'

/* Lab 11 v3 · 单步闭环（规格=终端 stepper.py：溯源6站 → 每圈[想拍暂停→想结果→做拍暂停→做结果] → 终局）
   暂停拍输入语义：空=行动不记预测 / 文字=记为预测 / 秘技1(模型眼中的世界) 2(代码原文) 3(文件现状) */
type Kind = 'origin' | 'pauseThink' | 'runThink' | 'pauseDo' | 'runDo' | 'final'
interface Step { k: Kind; r?: number; o?: number }
const STEPS: Step[] = ORIGIN.map((_, i) => ({ k: 'origin', o: i + 1 }))
ROUNDS.forEach((rd) => {
  STEPS.push({ k: 'pauseThink', r: rd.n }, { k: 'runThink', r: rd.n }, { k: 'pauseDo', r: rd.n }, { k: 'runDo', r: rd.n })
})
STEPS.push({ k: 'final' })

const idx = ref(0)
const step = computed(() => STEPS[idx.value])
const rno = computed(() => step.value.r ?? 0)
const round = computed(() => (rno.value ? ROUNDS[rno.value - 1] : null))
const isPause = computed(() => step.value.k === 'pauseThink' || step.value.k === 'pauseDo')
const isLast = computed(() => idx.value >= STEPS.length - 1)
const beat = computed<'think' | 'do'>(() => (step.value.k === 'pauseDo' || step.value.k === 'runDo' ? 'do' : 'think'))

function next() { if (!isLast.value) idx.value++ }
function prev() { if (idx.value > 0) idx.value-- }
function resetAll() { idx.value = 0; myPredict.value = ''; trick.value = null }

const stepLabel = computed(() => {
  if (step.value.k === 'origin') return `第 0 幕 · 溯源 ${step.value.o}/6`
  if (step.value.k === 'final') return '终局'
  const names: Record<string, string> = { pauseThink: '想拍·暂停', runThink: '想·结果', pauseDo: '做拍·暂停', runDo: '做·结果' }
  return `圈 ${rno.value} · ${names[step.value.k]}`
})
const todo = computed(() => beat.value === 'think' ? '限额检查+调 GLM（default.py L132-151）' : '执行命令+观察入史（default.py L156-157）')
const pos = computed(() => (step.value.k === 'pauseThink' || step.value.k === 'runThink' ? 1 : 3))
const cells = computed(() => Array.from({ length: 5 }, (_, i) => {
  const n = i + 1
  if (step.value.k === 'final') return '✓'
  if (step.value.k === 'origin') return '·'
  if (n < pos.value) return '✓'
  if (n === pos.value) return '▶'
  return '·'
}))
const memCount = computed(() => {
  if (step.value.k === 'origin') return 2
  if (step.value.k === 'final') return 14
  let m = 2
  ROUNDS.slice(0, rno.value).forEach((rd, i) => {
    const doneCircle = i < rno.value - 1 || beat.value === 'do' || step.value.k === 'runDo'
    m += doneCircle ? 2 : 1
  })
  return m
})
const nCalls = computed(() => (isPause.value && beat.value === 'think' ? rno.value - 1 : rno.value))

/* 预测 */
const myPredict = ref('')
const pkey = computed(() => `eaia-harness-predict-${rno.value}-${beat.value}`)
function loadPredict() { try { myPredict.value = localStorage.getItem(pkey.value) || '' } catch { myPredict.value = '' } }
function savePredict() { try { if (myPredict.value.trim()) localStorage.setItem(pkey.value, myPredict.value.trim()) } catch { /* 兜底 */ } }
watch(step, () => { if (isPause.value) { loadPredict(); trick.value = null } })

/* 秘技 */
const trick = ref<1 | 2 | 3 | null>(null)
const dumpInput = computed(() => {
  const out: string[] = ['system: You are a helpful assistant…（说明书全文，截断）', 'user: Please solve this issue: 在当前目录创建 sorter.py…（信纸全文，截断）']
  ROUNDS.slice(0, rno.value).forEach((rd, i) => {
    const isCurrent = i === rno.value - 1
    out.push(`assistant(圈${rd.n}): THOUGHT: ${rd.thought.slice(0, 90)}…${isCurrent && beat.value === 'think' ? '（本拍将随全量记忆发给模型）' : ''}`)
    if (!isCurrent) out.push(`user(观察·圈${rd.n}): 返回码 ${rd.returncode}，输出: ${rd.output.slice(0, 55).replace(/\n/g, ' ')}…`)
  })
  return out
})

/* 记忆序列 */
const memoryRoles = computed(() => {
  const out: { role: string; cur: boolean }[] = [{ role: 'system', cur: false }, { role: 'user(任务)', cur: false }]
  const upto = step.value.k === 'origin' ? 0 : (step.value.k === 'final' ? ROUNDS.length : rno.value - (isPause.value && beat.value === 'think' ? 1 : 0))
  ROUNDS.slice(0, upto).forEach((rd, i) => {
    const cur = i === upto - 1 && !(isPause.value && beat.value === 'think')
    out.push({ role: `圈${rd.n} assistant(想)`, cur })
    if (rd.gate === 'exit') { out.push({ role: `圈${rd.n} 暗号→没收`, cur }); out.push({ role: 'exit(Submitted)', cur: true }) }
    else out.push({ role: `圈${rd.n} user(观察)`, cur })
  })
  return out
})

/* dock 控制条 */
const docked = ref(false)
const dockStyle = ref<{ left: string; width: string }>({ left: '0px', width: '0px' })
function syncDock() { const el = document.querySelector('.hrp') as HTMLElement | null; if (el) { const r = el.getBoundingClientRect(); dockStyle.value = { left: `${r.left}px`, width: `${r.width}px` } } }
let io: IntersectionObserver | null = null
onMounted(() => {
  const root = document.querySelector('.hrp') as HTMLElement | null
  if (!root) return
  io = new IntersectionObserver((es) => { docked.value = es[0].isIntersecting }, { threshold: 0.03 })
  io.observe(root); window.addEventListener('resize', syncDock)
})
onBeforeUnmount(() => { io?.disconnect(); window.removeEventListener('resize', syncDock) })
watch(docked, async (d) => { if (d) { await nextTick(); syncDock() } })
function go() { if (isPause.value) savePredict(); next() }
const mainLabel = computed(() => {
  if (step.value.k === 'origin') return idx.value === 0 ? '开始溯源 ▶' : '下一站 ▶'
  if (isPause.value) return '行动（回车）▶'
  if (step.value.k === 'final') return '终局'
  return '下一拍 ▶'
})
</script>

<template>
  <div class="hrp">
    <div v-if="step.k === 'origin'" class="pane">
      <div class="ph c-arch">🎬 [阶段0] 任务摄入与上下文构建 · 溯源 {{ step.o }}/6 —— {{ ORIGIN[step.o - 1].title }}</div>
      <div v-for="(l, i) in ORIGIN[step.o - 1].body" :key="i" class="oline">{{ l }}</div>
      <div v-if="step.o === 3" class="sysbox">说明书前两行原文：<pre class="syspre">You are a helpful assistant that can interact with a computer.
Your response must contain exactly ONE bash code block with ONE command…</pre></div>
      <div v-if="step.o === 6" class="oline c-ok">✓ 头两条入史（记忆 2 条）——agent 的一切"经验"从这个底座开始增长。</div>
      <div class="oline dim">数据血统链：键盘 → sys.argv → task → jinja2 填 <code v-pre>{{task}}</code> 占位符 → messages[0]=system + messages[1]=user → 主循环</div>
    </div>

    <div v-if="step.k !== 'origin'" class="archrow">
      <div v-for="st in [{n:0,name:'任务摄入'},{n:1,name:'预算门'},{n:2,name:'Reason'},{n:3,name:'解析+执行'},{n:4,name:'观察形成与记忆追加'},{n:5,name:'终止判定'}]" :key="st.n" class="stage" :class="st.n === 2 ? 'llm' : ''">
        <span class="sn">[阶段{{ st.n }}]</span><span class="sname">{{ st.name }}</span>
      </div>
    </div>

    <template v-if="round && isPause">
      <div class="pausehead c-arch">==== [{{ beat === 'think' ? '阶段1·预算门]→[阶段2·Reason' : '阶段3·解析+执行]→[阶段4·结果入史' }}] · {{ beat === 'think' ? '想' : '做' }} · 第{{ rno }}圈 · 待办：{{ todo }} ====</div>
      <div class="dash">
        <div class="cells"><span v-for="(c, i) in cells" :key="i" class="cell" :class="{ done: c === '✓', now: c === '▶' }">[阶段{{ i + 1 }}{{ c }}]</span></div>
        <span class="pill brand">🧯 圈 {{ rno }}/8 · 调用 {{ nCalls }} · 记忆 {{ memCount }} 条 · 连击 0/3</span>
      </div>
      <div class="pane">
        <div class="ph">【预测】{{ beat === 'think' ? HINTS.think : HINTS.do }}</div>
        <div class="inrow"><span class="c-arch mono inlabel">[我在这: {{ beat === 'think' ? '阶段1→2·想' : '阶段3→4·做' }} · 第{{ rno }}圈] ></span>
          <input v-model="myPredict" class="tinput" placeholder="直接行动（留空）｜输入文字=记为预测">
          <button type="button" class="wbtn mini" @click="savePredict()">💾 记预测</button>
        </div>
        <div class="tricks">
          <span class="dim">秘技：</span>
          <button type="button" class="wbtn mini" :aria-pressed="trick === 1" @click="trick = trick === 1 ? null : 1">1 看将发给模型的记忆</button>
          <button type="button" class="wbtn mini" :aria-pressed="trick === 2" @click="trick = trick === 2 ? null : 2">2 本拍代码原文</button>
          <button type="button" class="wbtn mini" :aria-pressed="trick === 3" @click="trick = trick === 3 ? null : 3">3 playground 文件现状</button>
        </div>
        <div v-if="trick === 1" class="trickbox">
          <div class="th c-arch">此刻将发给模型的完整内容（{{ dumpInput.length }} 条 · 模型眼中的世界）：</div>
          <div v-for="(m, i) in dumpInput" :key="i" class="tline mono">[{{ i }}] {{ m }}</div>
        </div>
        <pre v-if="trick === 2" class="trickbox codebox">{{ CODE[beat] }}</pre>
        <div v-if="trick === 3" class="trickbox">
          <div class="th c-arch">playground 现状（由轨迹输出推导）：</div>
          <div class="tline mono">{{ FILES[rno] }}</div>
        </div>
      </div>
    </template>

    <div v-if="round && step.k === 'runThink'" class="pane">
      <div class="ph c-ok">[阶段2·Reason ✓] 模型回复全文（已入史 L151）</div>
      <div class="duty">想的双职责：{{ rno > 1 ? '职责A=判断上圈结果（读全量记忆——回喂此刻才真正生效）｜职责B=提议下一动作（围栏）' : '首轮无职责A（无上圈可判）｜职责B=提议首个动作（围栏）' }}</div>
      <pre class="thought">{{ round.thought }}</pre>
      <div class="ph c-arch subph">[阶段3·Act] 🧠 解析五步流水线实况（actions_text.py）</div>
      <div class="pipe">
        <div class="pstep">① 解析器选择（构造时由模型类决定）：LitellmTextbasedModel → 文本方言，契约=围栏协议</div>
        <div class="pstep mono">　 action_regex = ```mswea_bash_command\s*\n(.*?)\n```</div>
        <div class="pstep">② 工具判定：无注册表 → 工具固定=bash；入参=围栏内命令文本</div>
        <div class="pstep">③ 入参抽取：findall 命中 1 个围栏，捕获组=下方命令</div>
        <div class="pstep c-ok">④ 体检：恰好 1 个 → 通过</div>
        <div class="pstep">⑤ 打包：extra.actions = [{ command: … }]</div>
      </div>
      <pre class="cmd">{{ round.command }}</pre>
    </div>

    <div v-if="round && step.k === 'runDo'" class="pane">
      <div v-if="round.gate === 'pass'" class="ph c-arch">[阶段4·观察判断] 首行比对暗号：未命中 → 信封放行</div>
      <div v-else class="ph c-bad">[阶段3→4·观察判断闸门] echo 已真实执行；信封首行命中交卷暗号（local.py L48）</div>
      <div class="rc" :class="round.returncode === 0 ? 'c-ok' : 'c-bad'">🖥 返回码 {{ round.returncode }}，输出：</div>
      <pre class="output" :class="{ badout: round.returncode !== 0 }">{{ round.output }}<span v-if="round.cut" class="cutnote">…（标注式剪辑）</span></pre>
      <div v-if="round.gate === 'pass'" class="ph c-ok">[阶段4·结果入史 ✓] 📥 观察形成与记忆追加（L157）：新增 1 条</div>
      <div v-else>
        <div class="gline c-bad">→ 观察被没收（观察形成/追加不发生——模型永远看不到这条输出）</div>
        <div class="gline c-bad">→ exit 消息追加（L115-116）→ [阶段5] 终止</div>
      </div>
      <div class="cross-line c-cross">【横切·轨迹记录】本步已落盘（L120-121 行车记录仪）</div>
      <div class="outcome">{{ round.outcome }}</div>
      <div v-if="myPredict.trim()" class="compare">
        <div class="cmp-h">你的预测 vs 实际</div>
        <div class="cmp-row"><span class="cmp-k">预测</span><span>{{ myPredict }}</span></div>
        <div class="cmp-row"><span class="cmp-k">实际</span><span>{{ round.thought.slice(0, 70) }}… / 返回码 {{ round.returncode }}</span></div>
      </div>
    </div>

    <div v-if="step.k === 'final'" class="fin">
      <div class="fin-h c-ok">🏁 [阶段5·终止判定 ✓] 末条 role==exit → break（L122-123）</div>
      <div class="fin-replay">圈 6 终止演出回放：交卷暗号 echo 已真实执行 → 信封首行比对命中 → <b class="c-bad">观察被没收</b>（观察形成/追加不发生）→ exit 消息入史（写给轨迹而非模型）→ Submitted</div>
      <div class="fin-grid">
        <div class="fin-cell"><b>{{ META.exitStatus }}</b><span>exit_status（五值：Submitted / LimitsExceeded / TimeExceeded / RepeatedFormatError / 异常）</span></div>
        <div class="fin-cell"><b>{{ META.apiCalls }}</b><span>模型调用</span></div>
        <div class="fin-cell"><b>14</b><span>记忆总条数</span></div>
        <div class="fin-cell"><b>3/3</b><span>测试终态</span></div>
      </div>
      <div class="fin-note">{{ META.source }}</div>
    </div>

    <div class="mem">
      <div class="mem-h">记忆序列（消息历史 · 累积可见，当前高亮）</div>
      <div class="memlist"><span v-for="(m, i) in memoryRoles" :key="i" class="memcell" :class="{ cur: m.cur, gone: !m.cur && m.role.includes('圈') }">{{ m.role }}</span></div>
    </div>

    <div class="ctrlbar" :class="{ dock: docked }" :style="docked ? { left: dockStyle.left, width: dockStyle.width } : undefined">
      <button type="button" class="wbtn" :disabled="idx === 0" @click="prev">◀</button>
      <span class="ctrllabel">{{ stepLabel }} · 第 {{ idx + 1 }}/{{ STEPS.length }} 拍</span>
      <button type="button" class="wbtn" @click="resetAll">↺</button>
      <button type="button" class="wbtn primary" :disabled="isLast" @click="go()">{{ mainLabel }}</button>
    </div>

    <div class="hint"><span class="k">对照课文 · </span>溯源 6 站=harness 说明书的数据血统链（harness tax）；秘技 1 是本实验的灵魂——任何时刻看"模型眼中的世界"，回喂的生效一目了然；圈 3 红→圈 4 职责A 引用=错误回喂；圈 6 暗号=「模糊交给模型，精确留给自己」。</div>
  </div>
</template>

<style scoped>
.hrp { display: flex; flex-direction: column; gap: 12px; padding-bottom: 4px; min-height: 640px; }
.c-arch { color: var(--vp-c-brand-1); }
.c-ok { color: var(--vp-c-green-1, #16a34a); }
.c-bad { color: var(--vp-c-danger-1); }
.c-cross { color: var(--vp-c-purple-1, #7c3aed); }
.pane { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
.ph { font-size: 13px; font-weight: 650; }
.subph { margin-top: 4px; }
.oline { font-size: 13px; line-height: 1.75; font-family: var(--vp-font-family-mono, monospace); }
.oline.dim { color: var(--vp-c-text-3); font-size: 12px; }
.sysbox { border: 1px dashed var(--vp-c-divider); border-radius: 8px; padding: 8px 12px; font-size: 12px; }
.syspre { margin: 4px 0 0; font-size: 11.5px; white-space: pre-wrap; font-family: var(--vp-font-family-mono, monospace); }
.archrow { display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px; }
@media (max-width: 720px) { .archrow { grid-template-columns: repeat(3, 1fr); } }
.stage { border: 1.5px solid var(--vp-c-divider); border-radius: 8px; padding: 6px 8px; display: flex; flex-direction: column; gap: 2px; font-size: 12px; background: var(--vp-c-default-soft); }
.stage.llm { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.sn { font-size: 11px; color: var(--vp-c-text-3); }
.stage.llm .sn { color: var(--vp-c-brand-1); font-weight: 650; }
.sname { font-weight: 600; font-size: 12.5px; }
.pausehead { font-size: 12.5px; font-weight: 650; }
.dash { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.cells { display: flex; gap: 4px; flex-wrap: wrap; }
.cell { font-family: var(--vp-font-family-mono, monospace); font-size: 11.5px; color: var(--vp-c-text-3); padding: 2px 6px; border-radius: 6px; background: var(--vp-c-default-soft); }
.cell.done { color: var(--vp-c-text-2); }
.cell.now { color: var(--vp-c-brand-1); font-weight: 700; background: var(--vp-c-brand-soft); }
.inrow { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.inlabel { font-size: 11.5px; white-space: nowrap; }
.tinput { flex: 1; min-width: 200px; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 10px; font-size: 13px; background: var(--vp-c-bg); color: var(--vp-c-text-1); font-family: var(--vp-font-family-mono, monospace); }
.wbtn.mini { padding: 3px 10px; font-size: 12px; }
.tricks { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; }
.dim { color: var(--vp-c-text-3); font-size: 12px; }
.trickbox { border: 1px dashed var(--vp-c-brand-1); border-radius: 8px; padding: 8px 12px; display: flex; flex-direction: column; gap: 4px; }
.th { font-size: 12.5px; font-weight: 650; }
.tline { font-size: 11.5px; line-height: 1.65; }
.mono { font-family: var(--vp-font-family-mono, monospace); }
.codebox { margin: 0; white-space: pre-wrap; font-size: 11.5px; font-family: var(--vp-font-family-mono, monospace); }
.duty { font-size: 12px; color: var(--vp-c-text-2); border-left: 3px solid var(--vp-c-brand-1); padding-left: 10px; }
.thought { margin: 0; font-size: 12.5px; line-height: 1.7; background: var(--vp-c-brand-soft); border-radius: 8px; padding: 10px 12px; white-space: pre-wrap; }
.pipe { display: flex; flex-direction: column; gap: 3px; }
.pstep { font-size: 12px; color: var(--vp-c-text-2); background: var(--vp-c-default-soft); border-radius: 6px; padding: 3px 10px; }
.cmd { margin: 0; font-size: 12px; background: var(--vp-c-bg-soft); border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px 12px; overflow-x: auto; font-family: var(--vp-font-family-mono, monospace); white-space: pre-wrap; }
.rc { font-size: 12.5px; font-weight: 650; }
.output { margin: 0; font-size: 12px; background: var(--vp-c-default-soft); border-radius: 8px; padding: 10px 12px; white-space: pre-wrap; overflow-x: auto; font-family: var(--vp-font-family-mono, monospace); }
.badout { border: 1px solid var(--vp-c-danger-1); }
.cutnote { color: var(--vp-c-text-3); font-style: italic; }
.gline { font-size: 12.5px; font-weight: 600; }
.cross-line { font-size: 12px; font-weight: 600; }
.outcome { font-size: 12.5px; color: var(--vp-c-text-2); border-top: 1px dashed var(--vp-c-divider); padding-top: 6px; }
.compare { border: 1px dashed var(--vp-c-brand-1); border-radius: 8px; padding: 8px 12px; }
.cmp-h { font-size: 12px; font-weight: 650; color: var(--vp-c-brand-1); margin-bottom: 4px; }
.cmp-row { display: flex; gap: 8px; font-size: 12px; line-height: 1.6; }
.cmp-k { flex: none; color: var(--vp-c-text-3); min-width: 34px; }
.fin { border: 1.5px solid var(--vp-c-green-1, #16a34a); border-radius: 10px; padding: 12px 14px; }
.fin-h { font-weight: 700; font-size: 14px; margin-bottom: 8px; }
.fin-replay { font-size: 12.5px; line-height: 1.7; background: var(--vp-c-danger-soft); border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; }
.fin-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }
.fin-cell { display: flex; flex-direction: column; align-items: center; background: var(--vp-c-default-soft); border-radius: 8px; padding: 8px; text-align: center; }
.fin-cell b { font-size: 17px; }
.fin-cell span { font-size: 10.5px; color: var(--vp-c-text-3); }
.fin-note { margin-top: 8px; font-size: 11.5px; color: var(--vp-c-text-3); }
.mem { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 10px 12px; }
.mem-h { font-size: 12px; font-weight: 650; color: var(--vp-c-text-2); margin-bottom: 6px; }
.memlist { display: flex; flex-wrap: wrap; gap: 4px; }
.memcell { font-size: 11px; border: 1px solid var(--vp-c-divider); border-radius: 999px; padding: 1px 8px; color: var(--vp-c-text-3); }
.memcell.gone { opacity: .55; }
.memcell.cur { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 650; background: var(--vp-c-brand-soft); }
.ctrlbar { position: sticky; bottom: 0; z-index: 10; margin-top: auto; display: flex; gap: 8px; align-items: center; background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); border-radius: 999px; padding: 8px 14px; box-shadow: 0 4px 14px rgba(0,0,0,.08); flex-wrap: wrap; }
.ctrlbar.dock { position: fixed; bottom: 10px; margin-top: 0; }
.ctrllabel { flex: 1; text-align: center; font-size: 12.5px; font-weight: 650; color: var(--vp-c-text-2); min-width: 140px; }
</style>
