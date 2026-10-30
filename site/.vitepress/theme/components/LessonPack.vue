<script setup lang="ts">
defineProps<{ mins: number; units: { t: string; href?: string; note?: string }[] }>()
</script>

<template>
  <div class="lpk">
    <span class="k">📦 本讲学习包</span>
    <span class="m">课文约 {{ mins }} 分钟</span>
    <template v-for="(u, i) in units" :key="i">
      <span class="sep">→</span>
      <a v-if="u.href" :href="u.href" class="u">{{ u.t }}</a>
      <span v-else class="u dim">{{ u.t }}<i v-if="u.note">（{{ u.note }}）</i></span>
    </template>
  </div>
</template>

<style scoped>
.lpk { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; font-size: 13.5px; background: var(--vp-c-default-soft); border-radius: 9px; padding: 8px 14px; margin: 12px 0 0; }
.k { font-weight: 700; color: var(--vp-c-brand-1); }
.m { color: var(--vp-c-text-2); }
.sep { color: var(--vp-c-text-3); }
.u { color: var(--vp-c-brand-1); text-decoration: none; font-weight: 600; }
.u:hover { text-decoration: underline; }
.u.dim { color: var(--vp-c-text-3); font-weight: 400; font-style: normal; }
.u.dim i { font-style: normal; font-size: 12px; }
</style>
