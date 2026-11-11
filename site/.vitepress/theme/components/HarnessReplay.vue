<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { ROUNDS, META } from './harnessTrajectory'

/* Lab 11 v2 · 源头优先 + 固定控制条：
   线性步进 steps = [局前(preflight)] + 6×[预测,想,做] + [终局]；
   控制条 sticky 底部、位置恒定（§5.2）；局前面板 = 第一次模型调用之前 harness 已就位的一切 */
type StepKind = 'preflight' | 'predict' | 'think' | 'do' | 'final'
interface Step { kind: StepKind; round?: number }
const STEPS: Step[] = [
  { kind: 'preflight' },
  ...ROUNDS.flatMap((r) => ([
    { kind: 'predict' as StepKind, round: r.n },
    { kind: 'think' as StepKind, round: r.n },
    { kind: 'do' as StepKind, round: r.n },
  ])),
  { kind: 'final' },
]
const idx = ref(0)
const step = computed(() => STEPS[idx.value])
const roundNo = computed(() => step.value.round ?? 0)
const round = computed(() => (roundNo.value ? ROUNDS[roundNo.value - 1] : null))
const isLast = computed(() => idx.value >= STEPS.length - 1)
const stepLabel = computed(() => {
  if (step.value.kind === 'preflight') return '第 0 幕 · 局前（考场布置）'
  if (step.value.kind === 'final') return '终局'
  const names = { predict: '预测', think: '想（阶段1→2）', do: '做（阶段3→4·闸门）' } as Record<string, string>
  return `圈 ${roundNo.value} · ${names[step.value.kind]}`
})
function next() { if (!isLast.value) idx.value++ }
function prev() { if (idx.value > 0) idx.value-- }
function resetAll() { idx.value = 0; myPredict.value = '' }

/* 固定控制条：组件在视口内时 dock 到视口底（按钮恒定位置）；离窗还原（§5.2 控件位置固定） */
const barEl = ref<HTMLElement | null>(null)
const rootEl = ref<HTMLElement | null>(null)
const docked = ref(false)
const dockStyle = ref<{ left: string; width: string }>({ left: '0px', width: '0px' })
function syncDockGeometry() {
  const root = rootEl.value
  if (!root) return
  const r = root.getBoundingClientRect()
  dockStyle.value = { left: `${r.left}px`, width: `${r.width}px` }
}
let io: IntersectionObserver | null = null
onMounted(() => {
  const root = document.querySelector('.hrp') as HTMLElement | null
  rootEl.value = root
  if (!root) return
  io = new IntersectionObserver((es) => { docked.value = es[0].isIntersecting }, { threshold: 0.03 })
  io.observe(root)
  window.addEventListener('resize', syncDockGeometry)
})
onBeforeUnmount(() => { io?.disconnect(); window.removeEventListener('resize', syncDockGeometry) })
watch(docked, async (d) => { if (d) { await nextTick(); syncDockGeometry() } })

/* 五格进度条 */
const stageCells = computed(() => {
  if (!round.value) return ['·', '·', '·', '·', '·']
  const k = step.value.kind
  if (k === 'predict') return ['·', '·', '·', '·', '·']
  if (k === 'think') return ['✓', '▶', '·', '·', '·']
  return ['✓', '✓', '▶', '▶', '·']
})
const STAGES = [
  { n: 0, name: '任务摄入', side: 'det' },
  { n: 1, name: '预算门', side: 'det' },
  { n: 2, name: 'Reason', side: 'llm' },
  { n: 3, name: '解析+执行', side: 'det' },
  { n: 4, name: '观察形成与记忆追加', side: 'det' },
  { n: 5, name: '终止判定', side: 'det' },
]

/* 预测-对照（localStorage） */
const myPredict = ref('')
const predictKey = computed(() => `eaia-harness-predict-${roundNo.value}`)
function loadPredict() { try { myPredict.value = localStorage.getItem(predictKey.value) || '' } catch { myPredict.value = '' } }
function savePredict() { try { localStorage.setItem(predictKey.value, myPredict.value) } catch { /* 隐私模式兜底 */ } }

/* 记忆序列 */
const memoryRoles = computed(() => {
  const upto = step.value.kind === 'preflight' ? 0 : roundNo.value - (step.value.kind === 'predict' ? 1 : 0)
  const out: { role: string; cur: boolean }[] = [{ role: 'system', cur: false }, { role: 'user(任务)', cur: false }]
  ROUNDS.slice(0, upto).forEach((r, i) => {
    const isCur = i === upto - 1 && step.value.kind !== 'predict'
    out.push({ role: `圈${r.n} assistant(想)`, cur: isCur })
    if (r.gate === 'exit') {
      out.push({ role: `圈${r.n} 暗号命中→观察被没收`, cur: isCur })
      if (isCur) out.push({ role: 'exit(Submitted)', cur: true })
    } else {
      out.push({ role: `圈${r.n} user(观察)`, cur: isCur })
    }
  })
  if (step.value.kind === 'preflight') return out.slice(0, 1) // 局前：只有 system 已就位
  return out
})
</script>

<template>
  <div class="hrp">
    <!-- 第 0 幕 · 局前：源头（第一次模型调用之前，harness 已就位的一切） -->
    <div v-if="step.kind === 'preflight'" class="pane pre">
      <div class="ph">🎬 第 0 幕 · 局前——在第一次模型调用之前，考场已经布置完毕</div>
      <div class="pre-grid">
        <div class="pre-item"><span class="pk">① 宪法（system 消息）</span><span class="pv">「必须恰好一个 bash 代码块 + THOUGHT 段」——agent 的一切行为约束先于 agent 存在</span></div>
        <div class="pre-item"><span class="pk">② 任务信封（instance 模板）</span><span class="pv">任务文本 + 推荐工作流 + 交卷暗号指令（echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT，且禁与其他命令合并）+ 格式示例</span></div>
        <div class="pre-item"><span class="pk">③ 工具方言</span><span class="pv">```mswea_bash_command 围栏 + 解析正则 action_regex——工具表不是注册表，是文本约定</span></div>
        <div class="pre-item"><span class="pk">④ 预算</span><span class="pv">step_limit=8 圈 · 连续格式错误上限 3——循环壳与安全绳先装好</span></div>
      </div>
      <details class="sysdetail">
        <summary>展开看 system 消息全文（harness 说明书——这就是 L05 说的 harness tax）</summary>
        <pre class="syspre">You are a helpful assistant that can interact with a computer.

Your response must contain exactly ONE bash code block with ONE command (or commands connected with && or ||).
Include a THOUGHT section before your command where you explain your reasoning process.
…（格式示例与拒绝条款，全文见轨迹 JSON 第 1 条消息）</pre>
      </details>
      <div class="pre-note">看清楚这四件东西——接下来六圈里模型做的每一个动作，都发生在这张考卷之内。**harness 先于 agent 存在。**</div>
    </div>

    <!-- 架构总览（局后常驻第一屏之后的圈头区） -->
    <div v-if="step.kind !== 'preflight' && step.kind !== 'final'" class="arch">
      <div class="archrow">
        <div v-for="st in STAGES" :key="st.n" class="stage" :class="st.side">
          <span class="sn">[阶段{{ st.n }}]</span><span class="sname">{{ st.name }}</span>
        </div>
      </div>
      <div class="cross">
        <span class="xcell">⧉ 横切 · 轨迹落盘</span>
        <span class="xcell">⧉ 横切 · 模型层重试（本局未触发）</span>
        <span class="archnote">阶段 2 是唯一概率段（模型生成）——其余全是 harness 确定性代码。</span>
      </div>
    </div>

    <template v-if="round">
      <div class="dash">
        <span class="pill brand">圈 {{ round.n }}/{{ META.stepLimit }} · 调用 {{ round.n }}/{{ META.apiCalls }} · 记忆 {{ round.memoryAfter }} 条</span>
        <div class="cells">
          <span v-for="(c, i) in stageCells" :key="i" class="cell" :class="{ done: c === '✓', now: c === '▶' }">[阶段{{ i + 1 }}{{ c }}]</span>
        </div>
      </div>

      <div v-if="step.kind === 'predict'" class="pane predict" @vue:mounted="loadPredict">
        <div class="ph">🔮 圈 {{ round.n }} 先预测——模型这一圈会怎么想、做什么？</div>
        <textarea v-model="myPredict" rows="2" placeholder="我的预测：…" @focus="loadPredict" />
        <button type="button" class="wbtn mini" @click="savePredict()">💾 记下预测（随下方 ▶ 继续）</button>
      </div>

      <div v-if="step.kind !== 'predict'" class="pane think">
        <div class="ph">🧠 想（[阶段1✓预算门]→[阶段2 Reason·模型生成]）<span class="phsub">概率段</span></div>
        <pre class="thought">{{ round.thought }}</pre>
        <div class="duty">{{ round.duty }}</div>
      </div>

      <div v-if="step.kind === 'do'" class="pane act">
        <div class="ph">⚙️ 做（[阶段3 解析+执行]→[阶段4 观察形成与记忆追加]）<span class="phsub">确定段</span></div>
        <div class="pipe">
          <div class="pstep">① 解析器选择：构造时由模型类决定（action_regex）</div>
          <div class="pstep">② 工具判定：无注册表——固定 bash</div>
          <div class="pstep">③ 入参抽取：findall 捕获组 → 本圈命令</div>
          <div class="pstep">④ 体检：恰好 1 个代码块？✓</div>
          <div class="pstep">⑤ 打包：extra.actions 提交执行</div>
        </div>
        <pre class="cmd">{{ round.command }}</pre>
        <div class="rc" :class="round.returncode === 0 ? 'ok' : 'bad'">returncode {{ round.returncode }}</div>
        <pre class="output" :class="{ badout: round.returncode !== 0 }">{{ round.output }}<span v-if="round.cut" class="cutnote">…（标注式剪辑）</span></pre>
        <div v-if="round.gate === 'pass'" class="gate pass">观察判断闸门：stdout 首行比对暗号 → <b>未命中</b> → 观察形成（信封模板包裹）→ 追加进记忆</div>
        <div v-else class="gate exit">
          <div class="gline">观察判断闸门：stdout 首行比对 → <b>命中 COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT</b></div>
          <div class="gline bad">→ 观察被没收（观察形成/追加不发生——模型永远看不到这条输出）</div>
          <div class="gline bad">→ exit 消息入史（写给轨迹而非模型）→ Submitted</div>
        </div>
        <div class="outcome">{{ round.outcome }}</div>
        <div v-if="myPredict.trim()" class="compare">
          <div class="cmp-h">你的预测 vs 实际</div>
          <div class="cmp-row"><span class="cmp-k">预测</span><span>{{ myPredict }}</span></div>
          <div class="cmp-row"><span class="cmp-k">实际</span><span>{{ round.thought.slice(0, 80) }}… → {{ round.command.split('\n')[0].slice(0, 50) }}…</span></div>
        </div>
      </div>
    </template>

    <!-- 终点面板 -->
    <div v-if="step.kind === 'final'" class="fin">
      <div class="fin-h">🏁 终局——从考场布置（第 0 幕）到交卷，完整七幕</div>
      <div class="fin-grid">
        <div class="fin-cell"><b>{{ META.exitStatus }}</b><span>exit_status</span></div>
        <div class="fin-cell"><b>{{ META.apiCalls }}</b><span>模型调用</span></div>
        <div class="fin-cell"><b>14</b><span>消息总数</span></div>
        <div class="fin-cell"><b>3/3</b><span>测试终态</span></div>
      </div>
      <div class="fin-note">{{ META.source }}</div>
    </div>

    <!-- 记忆序列 -->
    <div class="mem">
      <div class="mem-h">记忆序列（消息历史 · 累积可见，当前圈高亮）</div>
      <div class="memlist">
        <span v-for="(m, i) in memoryRoles" :key="i" class="memcell" :class="{ cur: m.cur, gone: !m.cur && m.role.includes('圈') }">{{ m.role }}</span>
      </div>
    </div>

    <!-- 固定控制条（§5.2 控件位置固定：sticky 底部，全程恒定） -->
    <div ref="barEl" class="ctrlbar" :class="{ dock: docked }" :style="docked ? { left: dockStyle.left, width: dockStyle.width } : undefined">
      <button type="button" class="wbtn" :disabled="idx === 0" @click="prev">◀</button>
      <span class="ctrllabel">{{ stepLabel }} · 第 {{ idx + 1 }}/{{ STEPS.length }} 拍</span>
      <button type="button" class="wbtn" @click="resetAll">↺ 重置</button>
      <button type="button" class="wbtn primary" :disabled="isLast" @click="next">下一步 ▶</button>
    </div>

    <div class="hint"><span class="k">对照课文 · </span>第 0 幕四件（宪法/信封/方言/预算）= harness 说明书（harness tax）；圈 3 红→圈 4 职责A 引用 = 错误回喂；圈 6 暗号 = "模糊交给模型，精确留给自己"的终止设计。</div>
  </div>
</template>

<style scoped>
.hrp { display: flex; flex-direction: column; gap: 12px; padding-bottom: 4px; min-height: 640px; }
/* 局前 */
.pre-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 8px; }
.pre-item { display: flex; flex-direction: column; gap: 4px; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px 12px; background: var(--vp-c-default-soft); }
.pk { font-size: 12.5px; font-weight: 650; color: var(--vp-c-brand-1); }
.pv { font-size: 12px; color: var(--vp-c-text-2); line-height: 1.65; }
.sysdetail { font-size: 12.5px; }
.sysdetail summary { cursor: pointer; color: var(--vp-c-text-2); font-weight: 600; padding: 4px 0; }
.syspre { margin: 6px 0 0; font-size: 11.5px; background: var(--vp-c-default-soft); border-radius: 8px; padding: 10px 12px; white-space: pre-wrap; font-family: var(--vp-font-family-mono, monospace); }
.pre-note { font-size: 13px; font-weight: 600; border-left: 3px solid var(--vp-c-brand-1); padding-left: 10px; line-height: 1.7; }
/* 架构条 */
.archrow { display: grid; grid-template-columns: repeat(6, 1fr); gap: 4px; }
@media (max-width: 720px) { .archrow { grid-template-columns: repeat(3, 1fr); } }
.stage { border: 1.5px solid var(--vp-c-divider); border-radius: 8px; padding: 6px 8px; display: flex; flex-direction: column; gap: 2px; font-size: 12px; background: var(--vp-c-default-soft); }
.stage.llm { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.sn { font-size: 11px; color: var(--vp-c-text-3); }
.stage.llm .sn { color: var(--vp-c-brand-1); font-weight: 650; }
.sname { font-weight: 600; font-size: 12.5px; }
.cross { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-top: 4px; }
.xcell { font-size: 11.5px; color: var(--vp-c-purple-1, #7c3aed); border: 1px dashed var(--vp-c-purple-1, #7c3aed); border-radius: 6px; padding: 2px 8px; }
.archnote { font-size: 11.5px; color: var(--vp-c-text-3); }
/* 仪表 */
.dash { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.cells { display: flex; gap: 4px; flex-wrap: wrap; }
.cell { font-family: var(--vp-font-family-mono, monospace); font-size: 11.5px; color: var(--vp-c-text-3); padding: 2px 6px; border-radius: 6px; background: var(--vp-c-default-soft); }
.cell.done { color: var(--vp-c-text-2); }
.cell.now { color: var(--vp-c-brand-1); font-weight: 700; background: var(--vp-c-brand-soft); }
/* 面板 */
.pane { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
.ph { font-size: 13px; font-weight: 650; }
.phsub { font-size: 11px; color: var(--vp-c-brand-1); border: 1px solid var(--vp-c-brand-1); border-radius: 999px; padding: 0 8px; margin-left: 6px; }
.predict textarea { width: 100%; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 10px; font-size: 13px; background: var(--vp-c-bg); color: var(--vp-c-text-1); resize: vertical; }
.wbtn.mini { align-self: flex-start; padding: 3px 10px; font-size: 12px; }
.thought { margin: 0; font-size: 12.5px; line-height: 1.7; background: var(--vp-c-brand-soft); border-radius: 8px; padding: 10px 12px; white-space: pre-wrap; }
.duty { font-size: 12px; color: var(--vp-c-text-2); border-left: 3px solid var(--vp-c-brand-1); padding-left: 10px; }
.pipe { display: flex; flex-direction: column; gap: 3px; }
.pstep { font-size: 12px; color: var(--vp-c-text-2); background: var(--vp-c-default-soft); border-radius: 6px; padding: 3px 10px; }
.cmd { margin: 0; font-size: 12px; background: var(--vp-c-bg-soft); border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px 12px; overflow-x: auto; font-family: var(--vp-font-family-mono, monospace); white-space: pre-wrap; }
.rc { font-size: 12px; font-weight: 650; }
.rc.ok { color: var(--vp-c-green-1, #16a34a); }
.rc.bad { color: var(--vp-c-danger-1); }
.output { margin: 0; font-size: 12px; background: var(--vp-c-default-soft); border-radius: 8px; padding: 10px 12px; white-space: pre-wrap; overflow-x: auto; font-family: var(--vp-font-family-mono, monospace); }
.badout { border: 1px solid var(--vp-c-danger-1); }
.cutnote { color: var(--vp-c-text-3); font-style: italic; }
.gate { font-size: 12.5px; border-radius: 8px; padding: 8px 12px; line-height: 1.7; }
.gate.pass { background: var(--vp-c-brand-soft); }
.gate.exit { background: var(--vp-c-danger-soft); }
.gline { display: block; }
.gline.bad { color: var(--vp-c-danger-1); font-weight: 600; }
.outcome { font-size: 12.5px; color: var(--vp-c-text-2); border-top: 1px dashed var(--vp-c-divider); padding-top: 6px; }
.compare { border: 1px dashed var(--vp-c-brand-1); border-radius: 8px; padding: 8px 12px; }
.cmp-h { font-size: 12px; font-weight: 650; color: var(--vp-c-brand-1); margin-bottom: 4px; }
.cmp-row { display: flex; gap: 8px; font-size: 12px; line-height: 1.6; }
.cmp-k { flex: none; color: var(--vp-c-text-3); min-width: 34px; }
/* 终点 */
.fin { border: 1.5px solid var(--vp-c-green-1, #16a34a); border-radius: 10px; padding: 12px 14px; }
.fin-h { font-weight: 700; font-size: 14px; margin-bottom: 8px; }
.fin-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; }
.fin-cell { display: flex; flex-direction: column; align-items: center; background: var(--vp-c-default-soft); border-radius: 8px; padding: 8px; }
.fin-cell b { font-size: 18px; }
.fin-cell span { font-size: 11px; color: var(--vp-c-text-3); }
.fin-note { margin-top: 8px; font-size: 11.5px; color: var(--vp-c-text-3); }
/* 记忆 */
.mem { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 10px 12px; }
.mem-h { font-size: 12px; font-weight: 650; color: var(--vp-c-text-2); margin-bottom: 6px; }
.memlist { display: flex; flex-wrap: wrap; gap: 4px; }
.memcell { font-size: 11px; border: 1px solid var(--vp-c-divider); border-radius: 999px; padding: 1px 8px; color: var(--vp-c-text-3); }
.memcell.gone { opacity: .55; }
.memcell.cur { border-color: var(--vp-c-brand-1); color: var(--vp-c-brand-1); font-weight: 650; background: var(--vp-c-brand-soft); }
/* 固定控制条 */
.ctrlbar { position: sticky; bottom: 0; z-index: 10; margin-top: auto; display: flex; gap: 8px; align-items: center; background: var(--vp-c-bg); border: 1px solid var(--vp-c-divider); border-radius: 999px; padding: 8px 14px; box-shadow: 0 4px 14px rgba(0,0,0,.08); flex-wrap: wrap; }
.ctrlbar.dock { position: fixed; bottom: 10px; margin-top: 0; }
.ctrllabel { flex: 1; text-align: center; font-size: 12.5px; font-weight: 650; color: var(--vp-c-text-2); min-width: 140px; }
</style>
