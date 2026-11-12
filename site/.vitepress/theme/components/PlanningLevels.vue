<script setup lang="ts">
import { ref, computed } from 'vue'

/* L06 · 规划的三级落点（kingjin 学习心得反哺 2026-11-12）：权重/代码/上下文 + 下沉循环 + 元策略
   问题先行：站①千次账单——全在上下文级在线规划的代价，拨滑杆看账单翻转 */
const REPEAT = ref(1000)

const ONLINE = { perUse: '每次在线推理：慢、贵、pⁿ 误差复利', unit: 1.0 }
const CODE = { perUse: '一次开发，999 次确定性执行', unit: 0.02 }
const WEIGHT = { perUse: '零边际调用（已蒸进参数）', unit: 0.01 }

const bill = computed(() => {
  const n = REPEAT.value
  const online = { dev: 0, run: n * ONLINE.unit, note: `${n} 次在线推理` }
  const code = { dev: 5, run: n * CODE.unit, note: `1 次开发 + ${n - 1} 次确定执行` }
  const weight = { dev: 30, run: n * WEIGHT.unit, note: `1 次训练（轨迹蒸馏）+ ${n} 次零成本调用` }
  return [
    { name: '全上下文级', ...online, total: +(online.dev + online.run).toFixed(1), cost: online.note, bad: true },
    { name: '下沉到代码级', ...code, total: +(code.dev + code.run).toFixed(1), cost: code.note },
    { name: '下沉到权重级', ...weight, total: +(weight.dev + weight.run).toFixed(1), cost: weight.note },
  ].sort((a, b) => a.total - b.total)
})

/* 站②：下沉循环 + 元策略判定 */
const TASKS = [
  { id: 'invoice', name: '发票字段抽取', feat: '路径完全可预知 · 每天千次 · 环境稳定', lv: 2, why: '可预知+高频 → 最该下沉：技能/代码级（甚至固化 API），上下文零规划' },
  { id: 'refund', name: '客服退款处理', feat: '路径依赖观察 · 常见但多变', lv: 3, why: '残余不确定性高 → 留在上下文级在线循环（ReAct），但子流程（查订单）可下沉' },
  { id: 'novel', name: '第一次见的故障排查', feat: '全新任务 · 无先例', lv: 3, why: '只能第三级探索——探索成功后观察是否值得下沉（这是循环的入口）' },
  { id: 'pattern', name: '"先想后做"本身', feat: '跨任务通用规律', lv: 1, why: '最高频的规律 → 已被后训练蒸进权重——今天的模型"天生"会 ReAct' },
]
const LV = { 1: '第一级 · 权重', 2: '第二级 · 代码/技能库', 3: '第三级 · 上下文即时规划' }
const lvPick = ref<Record<string, number>>({})
const curTask = ref(0)
const task = computed(() => TASKS[curTask.value])
function pick(lv: number) { lvPick.value[task.value.id] = lv }
const doneN = computed(() => TASKS.filter(t => lvPick.value[t.id]).length)
</script>

<template>
  <div class="plv">
    <!-- 站① 千次账单 -->
    <div class="ops">
      <span class="q">同一个任务要做 <b>{{ REPEAT }}</b> 次，规划发生在哪一级？——拨动次数看账单翻转：</span>
      <input type="range" min="10" max="5000" step="10" v-model.number="REPEAT" />
    </div>
    <div class="bills">
      <div v-for="b in bill" :key="b.name" class="brow" :class="{ worst: b.bad, best: bill[0] === b }">
        <span class="bname">{{ b.name }}</span>
        <span class="bcost">{{ b.cost }}</span>
        <span class="btotal">{{ b.total }}</span>
      </div>
      <div class="bnote">账单单位=任意成本刻度（延迟×不确定性×钱）。关键读数：<b>重复次数越多，"下沉"越是赢</b>——全上下文级线性烧钱，代码级与权重级几乎平坦。这正是"学习的本质是把搜索的结果摊销掉"。</div>
    </div>

    <!-- 站② 三级地图 + 下沉循环 -->
    <div class="levels">
      <div class="lv l1">
        <div class="lvh">第一级 · 权重 <span class="lvtag">最稳定 · 零边际成本</span></div>
        <div class="lvb">反复出现的规划直觉被后训练蒸进参数（无数 ReAct 轨迹 → "天生"会先想后做）。对应：L02 后训练 / L11 蒸馏数据。</div>
      </div>
      <div class="lv l2">
        <div class="lvh">第二级 · 代码/技能库 <span class="lvtag">已验证 · 确定性执行</span></div>
        <div class="lvb">验证有效的流程结晶为 workflow 或技能文件（Pi 技能渐进披露、Voyager 技能库、Temporal）。不消耗不确定性预算，可缓存。</div>
      </div>
      <div class="lv l3">
        <div class="lvh">第三级 · 上下文即时规划 <span class="lvtag">最贵 · 残余不确定性</span></div>
        <div class="lvb">真正陌生的任务才在线推理（ReAct 循环）。贵且 pⁿ 复利——但它是循环的起点：一切下沉都从这里开始。</div>
      </div>
      <div class="cycle">
        <span class="cy">③ 探索</span>→<span class="cy">② 成功路径结晶为代码</span>→<span class="cy">① 普遍规律蒸入权重</span>→<span class="cy dim">环境变化使存量失效</span>→<span class="cy">回到 ③ 再探索</span>
      </div>
      <div class="bnote">三个同构系统：习惯化（刻意练习→直觉）、JIT 编译（热点解释→机器码）、AlphaGo（MCTS 在线搜索→蒸馏进 policy——<b>policy 就是摊销掉的搜索</b>）。</div>
    </div>

    <!-- 站③ 元策略判定 -->
    <div class="rail">
      <button v-for="(t, i) in TASKS" :key="t.id" type="button" class="wbtn" :aria-pressed="i === curTask" @click="curTask = i">
        {{ t.name }}<span class="mk" :class="lvPick[t.id] === t.lv ? 'ok' : lvPick[t.id] ? 'bad' : ''">{{ lvPick[t.id] ? (lvPick[t.id] === t.lv ? '✓' : '✗') : '·' }}</span>
      </button>
      <span class="score">已判 {{ doneN }}/4</span>
    </div>
    <div class="stage">
      <div class="tname">{{ task.name }}</div>
      <div class="tfeat">{{ task.feat }}</div>
      <div class="opts">
        <button v-for="l in [1, 2, 3]" :key="l" type="button" class="wbtn" :aria-pressed="lvPick[task.id] === l" @click="pick(l)">{{ LV[l as 1 | 2 | 3] }}</button>
      </div>
      <div v-if="lvPick[task.id]" class="verdict" :class="lvPick[task.id] === task.lv ? 'ok' : 'bad'">
        {{ lvPick[task.id] === task.lv ? '✓ ' : '✗ 你的选择会付出：' + (lvPick[task.id] === 3 ? '把可预知的路径留在在线推理——每次都付最贵的价格（账单已算过）' : lvPick[task.id] === 2 ? '把通用规律锁进代码——换个任务就失效，维护成本反噬' : '为低频任务付训练成本——摊销次数不够，血本无归') + '。' }}{{ task.why }}
      </div>
    </div>

    <div class="hint"><span class="k">元策略一句话 · </span>模型真正要学的不是每条路径，而是<b>判断控制流熵</b>：路径可预知 → 降级为 ReWOO 式一次性规划或命中技能库；路径必须在探索中浮现 → 保持 ReAct 在线循环；执行中发现前提错了 → 触发重规划（LLMCompiler 回退）。这就是 L01 那把刀的熵化版本。</div>
  </div>
</template>

<style scoped>
.plv { display: flex; flex-direction: column; gap: 12px; }
.ops { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 10px 12px; }
.q { font-size: 13.5px; font-weight: 600; }
.bills { display: flex; flex-direction: column; gap: 5px; }
.brow { display: grid; grid-template-columns: 110px 1fr 60px; gap: 10px; align-items: center; border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 8px 12px; font-size: 12.5px; }
.brow.worst { border-color: var(--vp-c-danger-1); background: var(--vp-c-danger-soft); }
.brow.best { border-color: var(--vp-c-green-1, #16a34a); }
.bname { font-weight: 650; }
.bcost { color: var(--vp-c-text-2); }
.btotal { font-weight: 700; font-size: 15px; text-align: right; }
.bnote { font-size: 12px; color: var(--vp-c-text-2); line-height: 1.7; border-top: 1px dashed var(--vp-c-divider); padding-top: 6px; }
.levels { display: flex; flex-direction: column; gap: 6px; }
.lv { border: 1.5px solid var(--vp-c-divider); border-radius: 10px; padding: 10px 14px; display: flex; flex-direction: column; gap: 3px; }
.lv.l3 { border-color: var(--vp-c-danger-1); background: var(--vp-c-danger-soft); }
.lv.l2 { border-color: var(--vp-c-brand-1); background: var(--vp-c-brand-soft); }
.lv.l1 { border-color: var(--vp-c-green-1, #16a34a); }
.lvh { font-weight: 700; font-size: 13.5px; }
.lvtag { font-size: 11px; font-weight: 400; color: var(--vp-c-text-3); margin-left: 8px; }
.lvb { font-size: 12.5px; color: var(--vp-c-text-2); line-height: 1.65; }
.cycle { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-size: 12.5px; padding: 8px 12px; border: 1px dashed var(--vp-c-purple-1, #7c3aed); border-radius: 8px; color: var(--vp-c-purple-1, #7c3aed); }
.cy { font-weight: 650; }
.cy.dim { color: var(--vp-c-text-3); font-weight: 400; }
.rail { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.mk { display: inline-flex; width: 16px; height: 16px; align-items: center; justify-content: center; border-radius: 50%; font-size: 10px; margin-left: 4px; }
.mk.ok { background: var(--vp-c-brand-1); color: var(--vp-c-white); }
.mk.bad { background: var(--vp-c-danger-1); color: var(--vp-c-white); }
.score { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); }
.stage { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
.tname { font-weight: 700; font-size: 15px; }
.tfeat { font-size: 12.5px; color: var(--vp-c-text-2); }
.opts { display: flex; flex-wrap: wrap; gap: 6px; }
.verdict { font-size: 12.5px; line-height: 1.7; border-radius: 8px; padding: 8px 12px; }
.verdict.ok { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); }
.verdict.bad { background: var(--vp-c-danger-soft); color: var(--vp-c-danger-1); }
</style>
