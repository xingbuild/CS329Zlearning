<script setup lang="ts">
import { ref, computed } from 'vue'

// Lab 08 站② · 优化策略决策台（据讲义 lecture09 "Reasons to use context/weight optimization"）
// 问题先行：选错先弹代价账单
type Strat = 'context' | 'weight'
const STRAT_NAME: Record<Strat, string> = { context: 'Context 优化', weight: 'Weight 优化' }

interface Card { id: string; name: string; brief: string; answer: Strat; why: string; costs: Record<Strat, string> }
const CARDS: Card[] = [
  {
    id: 'api', name: '闭源 API 模型',
    brief: '你的主力是 GPT-5 级闭源模型，没有微调权限。',
    answer: 'context',
    why: '权重根本动不了——讲义列出的 context 优化第一理由：强模型不提供微调接口（p.选型节）。',
    costs: { weight: '选 weight 优化 = 无处下手的方案：没有训练权限，这条路的门是锁死的', context: '' },
  },
  {
    id: 'fast', name: '每周要重跑优化',
    brief: '任务分布每周漂移，优化必须快速迭代、简单基建。',
    answer: 'context',
    why: 'context 优化跑得更快、基建更简单——weight 优化的训练管线赶不上周级迭代。',
    costs: { weight: '每次重训一条 GPU 管线——时间与成本都追不上周级漂移', context: '' },
  },
  {
    id: 'rollout', name: '环境交互昂贵',
    brief: '每次 agent rollout 花 $1（真实 API/沙箱），样本极其金贵。',
    answer: 'context',
    why: 'context 优化样本效率高得多（GEPA：prompt 优化比 RL 省一个量级以上的样本）。',
    costs: { weight: 'RL 要成千上万次 rollout——$1 × 10k 次起步，预算直接爆炸', context: '' },
  },
  {
    id: 'small', name: '小模型不听话',
    brief: '7B 小模型的指令遵循很差，prompt 怎么改都不稳定。',
    answer: 'weight',
    why: '讲义明说：context 优化对小模型常常失败（指令遵循技能太弱）——SFT/蒸馏才能把能力练进权重。',
    costs: { context: 'prompt 再怎么雕花，7B 连指令都读不稳——上下文优化在这里先天失效', weight: '' },
  },
  {
    id: 'teacher', name: '有强老师要便宜学生',
    brief: 'GPT-5 老师 + 部署成本压力，需要一个便宜的小模型干活。',
    answer: 'weight',
    why: '蒸馏路线正解：老师 rollout → SFT 学生（FireAct：Llama2-13B 微调后超 prompted GPT-3.5；OpenThoughts-Agent 同理）。',
    costs: { context: '小模型 + 好提示仍是小模型——部署账单省不下来，能力天花板还在', weight: '' },
  },
  {
    id: 'bloat', name: '上下文已经膨胀',
    brief: 'prompt 优化几轮后塞满示例与指令，上下文又贵又慢。',
    answer: 'weight',
    why: '讲义：用 weight 优化把"prompt 里长出来的知识"烧进权重，消解上下文膨胀。',
    costs: { context: '继续往 prompt 里堆——上下文越长越贵、模型越难读，优化收益被成本吃掉', weight: '' },
  },
]

const idx = ref(0)
const card = computed(() => CARDS[idx.value])
const picks = ref<Record<string, Strat | undefined>>({})
const doneCount = computed(() => CARDS.filter((c) => picks.value[c.id]).length)
function choose(s: Strat) { picks.value[card.value.id] = s }
</script>

<template>
  <div class="osd">
    <div class="rail">
      <button v-for="(c, i) in CARDS" :key="c.id" type="button" class="wbtn cardbtn" :aria-pressed="i === idx" @click="idx = i">
        <span class="cn">{{ c.name }}</span>
        <span class="cb" :class="picks[c.id] ? (picks[c.id] === c.answer ? 'good' : 'bad') : 'todo'">
          {{ picks[c.id] ? (picks[c.id] === c.answer ? '✓' : '✗') : '·' }}
        </span>
      </button>
      <div class="score">已判 {{ doneCount }}/6</div>
    </div>

    <div class="stage">
      <h4 class="tname">{{ card.name }}</h4>
      <p class="tbrief">{{ card.brief }}</p>
      <div class="stepq"><span class="sq">？</span>这个场景该走哪条优化路线？</div>
      <div class="opts">
        <button v-for="s in (['context', 'weight'] as Strat[])" :key="s" type="button" class="wbtn"
          :aria-pressed="picks[card.id] === s" @click="choose(s)">{{ STRAT_NAME[s] }}（改提示与示例 / SFT·RL·蒸馏）</button>
      </div>

      <div v-if="picks[card.id]" class="bill">
        <div class="b-row" :class="picks[card.id] === card.answer ? 'ok' : 'off'">
          <span v-if="picks[card.id] !== card.answer" class="bk">代价</span>
          <span v-else class="bk">判定</span>
          <span>{{ picks[card.id] === card.answer ? '✓ 正解——' + card.why : '✗ 你的选择会付出：' + card.costs[picks[card.id]] + '。讲义判据：' + card.why }}</span>
        </div>
      </div>
    </div>

    <div class="hint"><span class="k">判据一句话 · </span>三条 context 信号：动不了权重 / 要快跑 / 样本金贵；三条 weight 信号：context 已失败 / 有强老师要便宜学生 / 上下文在膨胀。都不满足？BetterTogether：先 prompt 后 weight 再 prompt 交替（第四/六幕）。</div>
  </div>
</template>

<style scoped>
.osd { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.cardbtn { display: inline-flex; gap: 6px; align-items: center; }
.cb { display: inline-flex; width: 18px; height: 18px; align-items: center; justify-content: center; border-radius: 50%; font-size: 11px; }
.cb.good { background: var(--vp-c-brand-1); color: var(--vp-c-white); }
.cb.bad { background: var(--vp-c-danger-1); color: var(--vp-c-white); }
.cb.todo { color: var(--vp-c-text-3); }
.score { margin-left: auto; font-size: 12px; color: var(--vp-c-text-2); }
.stage { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
.tname { margin: 0; font-size: 16px; }
.tbrief { margin: 0; color: var(--vp-c-text-2); font-size: 13px; }
.stepq { font-size: 13px; font-weight: 600; }
.sq { color: var(--vp-c-brand-1); margin-right: 4px; }
.opts { display: flex; flex-wrap: wrap; gap: 6px; }
.bill { border-top: 1px dashed var(--vp-c-divider); padding-top: 10px; }
.b-row { display: flex; gap: 8px; font-size: 13px; line-height: 1.65; }
.bk { min-width: 32px; color: var(--vp-c-text-3); }
.ok { color: var(--vp-c-brand-1); }
.off { color: var(--vp-c-danger-1); }
</style>
