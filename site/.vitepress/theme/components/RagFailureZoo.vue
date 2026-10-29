<script setup lang="ts">
import { ref, computed } from 'vue'

// 九种失败模式整理自讲义 lecture03.pdf p.63（检索侧 / 阅读侧 / 循环侧）
const FAMILIES = [
  {
    id: 'retrieval',
    name: '检索侧',
    color: '#d97706',
    items: [
      {
        name: '召回天花板',
        symptom: 'agent 答不出库里明明有的信息，或者干脆编一个。',
        cause: '证据根本没进 top-k——分块切散、索引过期、查询改写不当。缺了原料，再强的阅读器也做不出菜。',
        fix: '先测 Hit@k / Recall@k 再怪模型；分块与查询改写（contextual retrieval、hybrid）常是第一杠杆。',
      },
      {
        name: '索引过期',
        symptom: '源文档更新了，答案还是旧的。',
        cause: '向量库不随源自动更新——embedding 是快照，不是订阅。',
        fix: '把重建索引接进数据变更管道；文档加版本/时间戳，检索时过滤。',
      },
      {
        name: '权限泄漏',
        symptom: '检索把用户无权看的内容喂给了模型，答案里泄露出来。',
        cause: '检索器只认相似度，不认 ACL——越权文档照样进 top-k。',
        fix: '按身份过滤索引（索引分租户）或检索后过滤；权限边界要在检索层做，不能指望生成层"嘴严"。',
      },
    ],
  },
  {
    id: 'reader',
    name: '阅读侧',
    color: '#2563eb',
    items: [
      {
        name: '中间丢失（位置偏差）',
        symptom: '证据明明在上下文里，模型却当没看见。',
        cause: '长上下文中注意力对头尾强、中间弱（lost in the middle）——塞得越多，中间越容易被忽略。',
        fix: '重排（rerank）让最相关者居首尾；控制上下文长度；关键信息前置。',
      },
      {
        name: '干扰项',
        symptom: '答案被"相似但不相关"的段落带偏。',
        cause: '向量相似 ≠ 任务相关——top-k 里混进高相似低价值的段落，模型一律当证据用。',
        fix: '提高检索精度（rerank、过滤阈值）；提示词要求"只依据标注来源作答"。',
      },
      {
        name: '证据冲突',
        symptom: '两个来源说法矛盾，模型随机站队或和稀泥。',
        cause: '多源知识本就冲突（版本、口径、时间），检索把矛盾双方一起端上来。',
        fix: '按时间/权威度排序；显式要求模型指出冲突而非硬选；上游做知识治理。',
      },
    ],
  },
  {
    id: 'loop',
    name: '循环侧',
    color: '#dc2626',
    items: [
      {
        name: '误差复利',
        symptom: '第一轮检索错一点，后面步步放大，最后彻底跑偏。',
        cause: '每一步都依赖上一步的观察——pⁿ 的老朋友（L01 第三幕）。',
        fix: '关键节点校验与重试（L01/lab01 的修复回路）；中途自检（Self-RAG 的反思 token）。',
      },
      {
        name: '无停止规则',
        symptom: 'agent 反复检索同一类内容，停不下来，账单暴涨。',
        cause: '缺"够好了"的可判定条件——检索何时收敛没有定义。',
        fix: '设定显式停止条件（步数上限、答案稳定度、置信度阈值）——ReAct 论文的 7 步上限就是一例。',
      },
      {
        name: '提示注入',
        symptom: '检索回来的网页/文档里藏着指令，agent 照做了。',
        cause: '检索文本直接进上下文——数据被当成了指令（L01 第四幕的 87% 弹窗攻击同族）。',
        fix: '检索内容隔离标注（quote 机制）；高危动作加人工确认；来源白名单。',
      },
    ],
  },
]

const fam = ref('retrieval')
const sel = ref(0)
const curFam = computed(() => FAMILIES.find((f) => f.id === fam.value)!)
const cur = computed(() => curFam.value.items[sel.value])

function switchFam(id: string) {
  fam.value = id
  sel.value = 0
}
</script>

<template>
  <div class="zoo">
    <div class="row wrap">
      <button v-for="f in FAMILIES" :key="f.id" type="button" class="wbtn" :aria-pressed="f.id === fam"
        @click="switchFam(f.id)">{{ f.name }}（{{ f.items.length }}）</button>
    </div>
    <div class="zoo-body">
      <div class="zoo-list">
        <button v-for="(it, i) in curFam.items" :key="it.name" type="button" class="zoo-item" :aria-pressed="i === sel"
          :style="i === sel ? { borderColor: curFam.color } : {}" @click="sel = i">{{ it.name }}</button>
      </div>
      <div class="zoo-detail">
        <div class="zoo-title" :style="{ color: curFam.color }">{{ curFam.name }} · {{ cur.name }}</div>
        <div class="zoo-row"><span class="zk">症状</span><span>{{ cur.symptom }}</span></div>
        <div class="zoo-row"><span class="zk">根因</span><span>{{ cur.cause }}</span></div>
        <div class="zoo-row"><span class="zk">对策</span><span>{{ cur.fix }}</span></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.zoo { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.zoo-body { display: flex; gap: 14px; align-items: stretch; flex-wrap: wrap; }
.zoo-list { display: flex; flex-direction: column; gap: 6px; flex: none; }
.zoo-item { text-align: left; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--vp-c-divider); background: var(--vp-c-bg); color: var(--vp-c-text-1); font-size: 14.5px; cursor: pointer; min-width: 150px; }
.zoo-item[aria-pressed='true'] { background: var(--vp-c-brand-soft); font-weight: 600; }
.zoo-detail { flex: 1; min-width: 260px; border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.zoo-title { font-weight: 700; font-size: 15.5px; }
.zoo-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.zk { flex: none; color: var(--vp-c-text-3); font-size: 13px; padding-top: 2px; }
</style>
