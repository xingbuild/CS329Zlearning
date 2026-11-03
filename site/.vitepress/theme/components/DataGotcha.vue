<script setup lang="ts">
import { ref } from 'vue'

// 数据事故卡 ×6（据讲义 lecture11 "What agent data accidentally teaches"；失败动物园同构）
const GOTCHAS = [
  {
    id: 'git', name: '.git 漏洞', src: 'SWE-bench #465',
    think: '模型在学会修 issue',
    real: '学会翻 .git 历史找修复 diff 抄答案（任务忘了清 .git）',
    fix: 'Self-play SWE-RL：评分前擦 .git、还原测试文件',
  },
  {
    id: 'exit', name: 'sys.exit(0) 假通过', src: 'Anthropic 生产编码环境',
    think: '模型在学会让测试通过',
    real: '学会提前退出进程伪造"测试全绿"——随后失同步行为上升',
    fix: 'verifier 环境隔离 + 收据审计（L10 防线）',
  },
  {
    id: 'cot', name: 'CoT 监控反噬', src: 'OpenAI 编码 RL（2025）',
    think: '加监控能抓作弊',
    real: '把监控并进 reward 后，模型学会隐藏意图继续作弊',
    fix: '监控与训练信号分离；监控只报警不进奖励',
  },
  {
    id: 'eval', name: 'eval 感知', src: 'Claude Opus 4.6 / BrowseComp',
    think: '模型在泛化解题',
    real: '两次推断出自己在被测、认出基准、解密了答案钥匙',
    fix: '私密held-out集；新任务持续轮换（L10：任务即软件）',
  },
  {
    id: 'memo', name: '背题 76%', src: 'SWE-Bench Illusion（2025）',
    think: '模型在学会修真实仓库',
    real: '从 issue 文本即可猜中 76% 的 buggy 文件——评测集泄漏进了预训练',
    fix: 'OpenAI 停用 SWE-bench Verified 作为跟踪指标；换新题',
  },
  {
    id: 'look', name: '看起来对', src: 'OpenAI 人类偏好训练',
    think: '人类偏好教会正确性',
    real: '模型学会"显得对"——人类点赞变多，正确率没涨',
    fix: '偏好只当弱信号；可验证任务用可判定 reward（L09 RLVR）',
  },
]
const open = ref<string | null>(null)
</script>

<template>
  <div class="dgo">
    <div class="grid">
      <div v-for="g in GOTCHAS" :key="g.id" class="gcard" :class="{ on: open === g.id }" :tabindex="0" role="button"
        :aria-pressed="open === g.id" @click="open = open === g.id ? null : g.id" @keydown.enter="open = open === g.id ? null : g.id">
        <div class="gname">🚨 {{ g.name }}</div>
        <div class="gsrc">{{ g.src }}</div>
        <div v-if="open === g.id" class="gbody">
          <div class="gr"><span class="gk">你以为它在学</span><span>{{ g.think }}</span></div>
          <div class="gr bad"><span class="gk">它实际在学</span><span>{{ g.real }}</span></div>
          <div class="gr ok"><span class="gk">防线</span><span>{{ g.fix }}</span></div>
        </div>
        <div v-else class="gmore">点击展开"以为 vs 实际"</div>
      </div>
    </div>
    <div class="hint"><span class="k">动物园导览 · </span>六张卡的同构性：数据不会只教你想教的——<b>它教一切可被奖励的捷径</b>。这就是"evals 成为最要紧控制点"（L09 第五幕）在数据侧的重演。</div>
  </div>
</template>

<style scoped>
.dgo { display: flex; flex-direction: column; gap: 10px; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 8px; }
.gcard { border: 1px solid var(--vp-c-divider); border-radius: 10px; padding: 10px 12px; cursor: pointer; outline: none; display: flex; flex-direction: column; gap: 4px; }
.gcard:focus-visible { border-color: var(--vp-c-brand-1); }
.gcard.on { border-color: var(--vp-c-danger-1); background: var(--vp-c-danger-soft); }
.gname { font-weight: 650; font-size: 13.5px; }
.gsrc { font-size: 11px; color: var(--vp-c-text-3); }
.gmore { font-size: 11px; color: var(--vp-c-text-3); }
.gbody { display: flex; flex-direction: column; gap: 5px; border-top: 1px dashed var(--vp-c-divider); padding-top: 6px; margin-top: 2px; }
.gr { display: flex; gap: 8px; font-size: 12px; line-height: 1.6; }
.gk { flex: none; color: var(--vp-c-text-3); min-width: 76px; }
.gr.bad span:last-child { color: var(--vp-c-danger-1); font-weight: 600; }
.gr.ok span:last-child { color: var(--vp-c-brand-1); }
</style>
