<script setup lang="ts">
defineProps<{ term: string; from: string; replaced: string; is: string; isNot: string }>()
</script>

<template>
  <details class="termcard">
    <summary>🧭 术语考古 · {{ term }}</summary>
    <div class="tgrid">
      <span class="tk">从哪来</span><span>{{ from }}</span>
      <span class="tk">替代了什么</span><span>{{ replaced }}</span>
      <span class="tk">它是</span><span><b>{{ is }}</b></span>
      <span class="tk">它不是</span><span>{{ isNot }}</span>
    </div>
  </details>
</template>

<style scoped>
.termcard { border: 1px dashed var(--vp-c-brand-1); border-radius: 10px; padding: 10px 14px; margin: 10px 0; background: var(--vp-c-brand-soft); }
.termcard summary { cursor: pointer; font-weight: 650; font-size: 14px; color: var(--vp-c-brand-1); }
.tgrid { display: grid; grid-template-columns: 88px 1fr; gap: 6px 12px; margin-top: 10px; font-size: 14px; line-height: 1.7; }
.tk { color: var(--vp-c-text-3); font-size: 12.5px; padding-top: 2px; }
</style>
