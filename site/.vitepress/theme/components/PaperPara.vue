<script setup lang="ts">
// 论文精读统一模具：一段 = 英文原文 + 中文直译 + 可选本质要点
// 三层分工铁律（AGENTS.md §4.1）：原文保证一致性，直译不掺私货，解读只进要点层。
defineProps<{ label?: string }>()
</script>

<template>
  <div class="ppara">
    <div v-if="label" class="pp-label">{{ label }}</div>
    <blockquote class="pp-en">
      <slot name="en" />
    </blockquote>
    <div class="pp-zh">
      <slot name="zh" />
    </div>
    <div v-if="$slots.hint" class="pp-hint">
      <span class="pp-hint-k">💡 本质要点</span>
      <slot name="hint" />
    </div>
  </div>
</template>

<style scoped>
.ppara {
  margin: 22px 0;
  padding: 14px 18px;
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  background: var(--vp-c-bg-soft-up, var(--vp-c-bg-soft));
}
.pp-label {
  font-size: 12.5px;
  font-weight: 700;
  color: var(--vp-c-brand-1);
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}
.pp-en {
  margin: 0 0 10px;
  padding: 4px 0 4px 14px;
  border-left: 3px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  font-size: 14.5px;
  line-height: 1.75;
}
.pp-en :deep(p) { margin: 0 0 8px; }
.pp-en :deep(p:last-child) { margin-bottom: 0; }
.pp-zh {
  font-size: 15.5px;
  line-height: 1.85;
}
.pp-zh :deep(p) { margin: 0 0 8px; }
.pp-hint {
  margin-top: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  background: var(--vp-c-brand-soft);
  font-size: 14.5px;
  line-height: 1.7;
}
.pp-hint-k {
  font-weight: 700;
  color: var(--vp-c-brand-1);
  margin-right: 8px;
}
</style>
