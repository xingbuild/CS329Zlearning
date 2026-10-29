<script setup lang="ts">
import { ref, computed } from 'vue'

// 上下文管理五模式，整理自讲义 lecture06.pdf p.60-71
const PATTERNS = [
  {
    id: 'eventlog',
    name: '持久事件日志 Persistent Event Log',
    core: '一切以事件落盘，LLM 输入每次从事件重建',
    diagram: '[事件1][事件2][事件3] …(append-only)\n        ↓ 重建\n   [LLM 输入视图]',
    case: 'OpenHands：每步一个 JSON 事件存磁盘；不可变、可回放；外部观察者可挂钩子',
    gain: '真实历史与模型视图解耦——想怎么裁剪上下文都不丢事实',
  },
  {
    id: 'offload',
    name: '记忆卸载 Memory Offloading',
    core: '把知识挪进记忆/文件，腾出上下文可裁剪',
    diagram: '[上下文] --写出--> [记忆/文件]\n[上下文] <--按需取回-- [记忆/文件]',
    case: 'MemGPT：主上下文当 RAM，外部存储当磁盘，自主分页',
    gain: '上下文保持专注（L02：塞满会 rot）；代价是取回时机要对（L07 主讲）',
  },
  {
    id: 'compact',
    name: '压缩 Compaction',
    core: '让 LLM 把历史总结成压缩描述',
    diagram: '[长历史] → [LLM 摘要] → [短上下文] 续跑',
    case: '通用模式；讲义特别指出：压缩本身也可以是 agentic 的（自己决定保什么）',
    gain: '续命长任务；取舍 = 留多了很快又满、丢多了丢关键（L02 的两难）',
  },
  {
    id: 'mask',
    name: '观察遮蔽 Observation Masking',
    core: '不摘要，直接截断旧的工具输出',
    diagram: '[Obs1 5000 tok] --老化--> [Obs1 200 tok]',
    case: '编码 agent 的观察动辄几千 token（文件内容、命令输出）——截断比摘要便宜且无损于近期',
    gain: '零 LLM 调用、可预测；丢的是远端细节（通常已无关）',
  },
  {
    id: 'isolate',
    name: '上下文隔离 Context Isolation',
    core: '子任务交给子 agent，只回传结果不回传过程',
    diagram: '[主 agent] --任务--> [子 agent 独立上下文]\n[主 agent] <--只回结论-- [子 agent]',
    case: '渐进披露（Progressive Disclosure）同族：工具/技能不必初始全给，用到再加载（Anthropic Agent Skills）',
    gain: '主上下文不被污染；代价是信息经过子 agent 的压缩可能有损',
  },
]

const cur = ref('compact')
const item = computed(() => PATTERNS.find((p) => p.id === cur.value)!)
</script>

<template>
  <div class="cp">
    <div class="rail">
      <button v-for="p in PATTERNS" :key="p.id" type="button" class="wbtn" :aria-pressed="p.id === cur"
        @click="cur = p.id">{{ p.name.split(' ')[0] }}·{{ p.name.split(' ')[1] }}</button>
    </div>
    <div class="detail">
      <div class="title">{{ item.name }}</div>
      <div class="core">{{ item.core }}</div>
      <pre class="diag">{{ item.diagram }}</pre>
      <div class="d-row"><span class="dk">实例</span><span>{{ item.case }}</span></div>
      <div class="d-row"><span class="dk">得失</span><span>{{ item.gain }}</span></div>
    </div>
    <div class="hint"><span class="k">注意 · </span>五大模式<b>互相兼容、可叠加</b>（先卸载再压缩、事件日志 + 观察截断）——真实系统是组合体；两条总原则：聚焦上下文、保持连续性（含 KV Cache，L02）。</div>
  </div>
</template>

<style scoped>
.cp { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; gap: 8px; flex-wrap: wrap; }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.title { font-weight: 700; font-size: 15.5px; }
.core { font-size: 14.5px; color: var(--vp-c-brand-1); }
.diag { margin: 0; background: var(--vp-c-default-soft); border-radius: 8px; padding: 10px 14px; font-size: 12.5px; line-height: 1.6; font-family: var(--vp-font-family-mono, monospace); color: var(--vp-c-text-2); white-space: pre; overflow-x: auto; }
.d-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 13px; min-width: 44px; padding-top: 2px; }
</style>
