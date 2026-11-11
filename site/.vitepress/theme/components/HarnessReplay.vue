<script setup lang="ts">
import { ref, computed } from 'vue'
import { ROUNDS, META } from './harnessTrajectory'

/* Lab 11 · 六阶段回放剧场：想/做两半 × 逐圈预测-对照；诚实红线=模拟回放非实时（徽章在页面 md） */
type Phase = 'predict' | 'think' | 'do' | 'final'
const cur = ref(0)            // 0=未开始；1..6=当前圈
const phase = ref<Phase>('predict')
const finished = ref(false)

const round = computed(() => (cur.value >= 1 ? ROUNDS[cur.value - 1] : null))
const started = computed(() => cur.value >= 1)

function begin() { cur.value = 1; phase.value = 'predict' }
function toThink() { phase.value = 'think' }
function toDo() { phase.value = 'do' }
function nextRound() {
  if (!round.value) return
  if (round.value.gate === 'exit') { phase.value = 'final'; finished.value = true; return }
  if (cur.value >= ROUNDS.length) return
  cur.value++; phase.value = 'predict'
}
function resetAll() { cur.value = 0; phase.value = 'predict'; finished.value = false }

/* 预测-对照（localStorage） */
const predictKey = computed(() => `eaia-harness-predict-${cur.value}`)
const myPredict = ref('')
function loadPredict() {
  try { myPredict.value = localStorage.getItem(predictKey.value) || '' } catch { myPredict.value = '' }
}
function savePredict() {
  try { localStorage.setItem(predictKey.value, myPredict.value) } catch { /* 私隐模式兜底 */ }
}
function onEnterPredict() { loadPredict() }

/* 五格进度条（阶段首要：想=1✓2▶；做=1✓2✓3▶4▶；闸门时 5 判定） */
const stageCells = computed(() => {
  if (phase.value === 'think') return ['✓', '▶', '·', '·', '·']
  if (phase.value === 'do') return ['✓', '✓', '▶', '▶', '·']
  if (phase.value === 'final') return ['✓', '✓', '✓', '✓', '✓']
  return ['·', '·', '·', '·', '·']
})

/* 记忆序列（角色链，当前圈高亮、旧圈暗化） */
const memoryRoles = computed(() => {
  if (!started.value) return [{ role: 'system' }, { role: 'user(任务)' }]
  const out: { role: string; cur: boolean }[] = [{ role: 'system', cur: false }, { role: 'user(任务)', cur: false }]
  ROUNDS.slice(0, cur.value).forEach((r, i) => {
    const isCur = i === cur.value - 1
    out.push({ role: `圈${r.n} assistant(想)`, cur: isCur })
    const showObs = !(isCur && phase.value !== 'final' && (phase.value === 'predict' || phase.value === 'think'))
    if (r.gate === 'exit') {
      out.push({ role: `圈${r.n} 暗号命中→观察被没收`, cur: isCur })
      if (isCur && phase.value === 'final') out.push({ role: 'exit(Submitted)', cur: true })
    } else if (showObs || !isCur) {
      out.push({ role: `圈${r.n} user(观察)`, cur: isCur })
    }
  })
  return out
})
const STAGES = [
  { n: 0, name: '任务摄入', side: 'det' },
  { n: 1, name: '预算门', side: 'det' },
  { n: 2, name: 'Reason', side: 'llm' },
  { n: 3, name: '解析+执行', side: 'det' },
  { n: 4, name: '观察形成与记忆追加', side: 'det' },
  { n: 5, name: '终止判定', side: 'det' },
]
</script>

<template>
  <div class="hrp">
    <!-- 架构总览：六阶段条（边界自证）+ 两横切 -->
    <div class="arch">
      <div class="archrow">
        <div v-for="st in STAGES" :key="st.n" class="stage" :class="st.side">
          <span class="sn">[阶段{{ st.n }}]</span><span class="sname">{{ st.name }}</span>
        </div>
      </div>
      <div class="cross">
        <span class="xcell">⧉ 横切 · 轨迹落盘（每步 serialize）</span>
        <span class="xcell">⧉ 横切 · 模型层重试（本局未触发）</span>
        <span class="archnote">阶段首要，圈数是属性；想/做=半程标签。阶段 2 是唯一概率段（模型生成）——其余全是 harness 确定性代码。</span>
      </div>
    </div>

    <!-- 开场 -->
    <div v-if="!started" class="beginbox">
      <p>六个模型调用、十四条消息、一次真失败与真修复。每圈开始前<b>先写下你的预测</b>：模型这一圈会想什么、做什么？看完对照——预测-对照是本实验的灵魂。</p>
      <button type="button" class="wbtn" @click="begin">▶ 开始第 1 圈</button>
    </div>

    <template v-if="round">
      <!-- 圈头：仪表 + 进度条 -->
      <div class="dash">
        <span class="pill brand">圈 {{ round.n }}/{{ META.stepLimit }} · 调用 {{ round.n }}/{{ META.apiCalls }} · 记忆 {{ round.memoryAfter }} 条</span>
        <div class="cells">
          <span v-for="(c, i) in stageCells" :key="i" class="cell" :class="{ done: c === '✓', now: c === '▶' }">[阶段{{ i + 1 }}{{ c }}]</span>
        </div>
      </div>

      <!-- 预测 -->
      <div v-if="phase === 'predict'" class="pane predict">
        <div class="ph">🔮 先预测——圈 {{ round.n }} 模型会怎么想、怎么做？（可选，但值得被打脸）</div>
        <textarea v-model="myPredict" rows="2" placeholder="我的预测：…" @focus="onEnterPredict" />
        <div class="prow">
          <button type="button" class="wbtn" @click="savePredict(); toThink()">记下预测，看「想」→</button>
          <button type="button" class="wbtn" @click="toThink()">跳过预测 →</button>
        </div>
      </div>

      <!-- 想 -->
      <div v-if="phase === 'think' || phase === 'do' || phase === 'final'" class="pane think">
        <div class="ph">🧠 想（[阶段1✓预算门]→[阶段2 Reason·模型生成]）<span class="phsub">概率段</span></div>
        <pre class="thought">{{ round.thought }}</pre>
        <div class="duty">{{ round.duty }}</div>
        <div v-if="phase === 'think'" class="prow"><button type="button" class="wbtn" @click="toDo">看「做」→</button></div>
      </div>

      <!-- 做 -->
      <div v-if="phase === 'do' || phase === 'final'" class="pane act">
        <div class="ph">⚙️ 做（[阶段3 解析+执行]→[阶段4 观察形成与记忆追加]）<span class="phsub">确定段</span></div>
        <div class="pipe">
          <div class="pstep">① 解析器选择：构造时由模型类决定（正则 action_regex）</div>
          <div class="pstep">② 工具判定：无注册表——固定 bash，唯一动作形态</div>
          <div class="pstep">③ 入参抽取：findall 捕获组 → 本圈命令（下框）</div>
          <div class="pstep">④ 体检：恰好 1 个代码块？✓（多/少则触发格式错误回喂，本局未触发）</div>
          <div class="pstep">⑤ 打包：extra.actions 提交执行</div>
        </div>
        <pre class="cmd">{{ round.command }}</pre>
        <div class="rc" :class="round.returncode === 0 ? 'ok' : 'bad'">returncode {{ round.returncode }}</div>
        <pre class="output" :class="{ badout: round.returncode !== 0 }">{{ round.output }}<span v-if="round.cut" class="cutnote">…（标注式剪辑）</span></pre>
        <!-- 观察判断闸门 -->
        <div v-if="round.gate === 'pass'" class="gate pass">观察判断闸门：stdout 首行比对暗号 → <b>未命中</b> → 观察正常形成（信封模板包裹 returncode/output）→ 追加进记忆</div>
        <div v-else class="gate exit">
          <div class="gline">观察判断闸门：stdout 首行比对暗号 → <b>命中 COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT</b></div>
          <div class="gline bad">→ 观察被没收：阶段 4 的观察形成/记忆追加<b>不发生</b>（模型永远看不到这条输出）</div>
          <div class="gline bad">→ exit 消息追加进轨迹（写给轨迹而非模型）→ exit_status = Submitted</div>
        </div>
        <div class="outcome">{{ round.outcome }}</div>
        <!-- 预测对照 -->
        <div v-if="myPredict.trim()" class="compare">
          <div class="cmp-h">你的预测 vs 实际</div>
          <div class="cmp-row"><span class="cmp-k">预测</span><span>{{ myPredict }}</span></div>
          <div class="cmp-row"><span class="cmp-k">实际</span><span>{{ round.thought.slice(0, 80) }}… → {{ round.command.split('\n')[0].slice(0, 50) }}…</span></div>
        </div>
        <div class="prow">
          <button v-if="round.gate === 'pass' && cur < ROUNDS.length" type="button" class="wbtn" @click="nextRound">进入第 {{ cur + 1 }} 圈 →</button>
          <button v-else-if="round.gate === 'exit'" type="button" class="wbtn" @click="nextRound">看终局面板 →</button>
        </div>
      </div>
    </template>

    <!-- 终点面板 -->
    <div v-if="finished" class="fin">
      <div class="fin-h">🏁 终局</div>
      <div class="fin-grid">
        <div class="fin-cell"><b>{{ META.exitStatus }}</b><span>exit_status</span></div>
        <div class="fin-cell"><b>{{ META.apiCalls }}</b><span>模型调用</span></div>
        <div class="fin-cell"><b>14</b><span>消息总数</span></div>
        <div class="fin-cell"><b>3/3</b><span>测试终态</span></div>
      </div>
      <div class="fin-note">{{ META.source }}</div>
    </div>

    <!-- 记忆序列（累积可见） -->
    <div class="mem">
      <div class="mem-h">记忆序列（消息历史 · 累积可见，当前圈高亮）</div>
      <div class="memlist">
        <span v-for="(m, i) in memoryRoles" :key="i" class="memcell" :class="{ cur: m.cur, gone: !m.cur && m.role.includes('圈') }">{{ m.role }}</span>
      </div>
    </div>

    <div class="ops">
      <button type="button" class="wbtn" @click="resetAll">↺ 重置回放</button>
    </div>

    <div class="hint"><span class="k">对照课文 · </span>圈 3 的红 → 圈 4 的职责A 引用失败换路 = 错误回喂；每圈记忆 +2 = 状态就是消息列表；圈 5"多扫尾一轮" = 模型侧收工阈值的不确定性；圈 6 暗号 = "模糊交给模型，精确留给自己"的终止设计。</div>
  </div>
</template>

<style scoped>
.hrp { display: flex; flex-direction: column; gap: 12px; }
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
/* 开场 */
.beginbox { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 14px; display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.beginbox p { margin: 0; font-size: 13.5px; flex: 1; min-width: 260px; line-height: 1.7; }
/* 仪表 */
.dash { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
.cells { display: flex; gap: 4px; flex-wrap: wrap; }
.cell { font-family: var(--vp-font-family-mono, monospace); font-size: 11.5px; color: var(--vp-c-text-3); padding: 2px 6px; border-radius: 6px; background: var(--vp-c-default-soft); }
.cell.done { color: var(--vp-c-text-2); }
.cell.now { color: var(--vp-c-brand-1); font-weight: 700; background: var(--vp-c-brand-soft); }
/* 面板通用 */
.pane { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 8px; }
.ph { font-size: 13px; font-weight: 650; }
.phsub { font-size: 11px; color: var(--vp-c-brand-1); border: 1px solid var(--vp-c-brand-1); border-radius: 999px; padding: 0 8px; margin-left: 6px; }
.pane.act .phsub { color: var(--vp-c-text-3); border-color: var(--vp-c-divider); }
.predict textarea { width: 100%; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 10px; font-size: 13px; background: var(--vp-c-bg); color: var(--vp-c-text-1); resize: vertical; }
.prow { display: flex; gap: 8px; flex-wrap: wrap; }
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
.ops { display: flex; gap: 8px; }
</style>
