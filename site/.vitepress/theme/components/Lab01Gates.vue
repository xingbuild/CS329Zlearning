<script setup lang="ts">
import { ref, computed } from 'vue'

// 两道闸修复回路：语法闸(json.loads) × 语义闸(schema) + 报错回喂
type Mode = 'none' | 'syntax' | 'both'
const MODES: { id: Mode; name: string }[] = [
  { id: 'none', name: '① 无闸（裸用）' },
  { id: 'syntax', name: '② 仅语法闸' },
  { id: 'both', name: '③ 双闸 + 回喂' },
]
const FRAMES: Record<Mode, { t: string; body: string; tone: 'bad' | 'warn' | 'good' | 'dim' }[]> = {
  none: [
    { t: '任务：抽取 {"name": str, "age": int}', body: '模型输出：{ "name": "Ada", "age": -5, "human": True }', tone: 'dim' },
    { t: '直接 json.loads(out)["age"] 使用', body: '💥 JSONDecodeError（True 不合法）——生产代码崩了', tone: 'bad' },
    { t: '失败率', body: '单次生成语法失败率 e ≈ 30%（失败动物园实测口径）——全部直接打到你的代码', tone: 'bad' },
  ],
  syntax: [
    { t: '第 1 次生成', body: 'json.loads → ❌ True 不合法 → 抛错', tone: 'warn' },
    { t: '报错回喂重试', body: '第 2 次生成：{ "name": "Ada", "age": -5 } → json.loads ✓', tone: 'good' },
    { t: '但语义闸缺席', body: 'age = -5 顺利入库——语法对 ≠ 语义对；下游"负年龄"业务雷', tone: 'bad' },
    { t: '失败率', body: '语法失败 e → e²（回喂一次）；语义失败仍 100% 放行', tone: 'warn' },
  ],
  both: [
    { t: '第 1 次生成', body: '语法闸 ✓ → 语义闸（Pydantic：age ≥ 0）→ ❌ age=-5', tone: 'warn' },
    { t: '报错回喂（带上校验错误信息）', body: '第 2 次生成：{ "name": "Ada", "age": 36 } → 双闸 ✓✓', tone: 'good' },
    { t: '产线效果', body: '失败率 e → e^k（k 次回喂后趋近可忽略）——但永远不为零：这是概率世界的地板', tone: 'good' },
    { t: '本质', body: '闸门 = 确定性代码包住概率输出；回喂 = 把失败变成信息。L01 的"确定性边界"在数据层的实现', tone: 'good' },
  ],
}
const mode = ref<Mode>('both')
const idx = ref(0)
const frames = computed(() => FRAMES[mode.value])
const cur = computed(() => frames.value[idx.value])
const isFeed = computed(() => cur.value.t.includes('回喂'))
function sw(m: Mode) { mode.value = m; idx.value = 0 }
</script>

<template>
  <div class="gt">
    <div class="row wrap">
      <button v-for="m in MODES" :key="m.id" type="button" class="wbtn" :aria-pressed="m.id === mode"
        @click="sw(m.id)">{{ m.name }}</button>
    </div>
    <div class="row wrap">
      <button type="button" class="wbtn" :disabled="idx === 0" @click="idx--">◀</button>
      <button type="button" class="wbtn primary" :disabled="idx === frames.length - 1" @click="idx++">下一步 ▶</button>
      <span class="meta">{{ idx + 1 }} / {{ frames.length }}</span>
    </div>
    <div v-if="isFeed" class="feedmark">↺ 报错回喂：控制流回到第 1 次生成——不是下一帧，是回路</div>
    <div class="stage" :class="cur.tone">
      <div class="st">{{ cur.t }}</div>
      <div class="sb">{{ cur.body }}</div>
    </div>
  </div>
</template>

<style scoped>
.gt { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.meta { color: var(--vp-c-text-3); font-size: 12.5px; }
.feedmark { font-size: 13px; color: var(--vp-c-brand-1); font-weight: 650; }
.stage { border-radius: 10px; padding: 14px 18px; border: 1px solid var(--vp-c-divider); }
.stage.bad { background: rgba(220,38,38,.08); }
.stage.warn { background: rgba(217,119,6,.09); }
.stage.good { background: rgba(22,163,74,.08); }
.stage.dim { background: var(--vp-c-default-soft); }
.st { font-weight: 650; font-size: 15px; margin-bottom: 6px; }
.sb { font-size: 14.5px; line-height: 1.7; }
</style>
