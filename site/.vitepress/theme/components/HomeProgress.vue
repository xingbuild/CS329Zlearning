<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getProgress } from '../progress'

const props = defineProps<{ ids: string[] }>()
const doneCount = ref(0)
onMounted(() => {
  const p = getProgress()
  doneCount.value = props.ids.filter((id) => p.includes(id)).length
})
</script>

<template>
  <div class="hp">
    <div class="track">
      <div class="fill" :style="{ width: (ids.length ? (doneCount / ids.length) * 100 : 0) + '%' }" />
    </div>
    <span class="pill">{{ doneCount }} / {{ ids.length }} 讲已完成</span>
  </div>
</template>

<style scoped>
.hp { display: flex; align-items: center; gap: 14px; margin: 18px 0 6px; max-width: 520px; }
.track { flex: 1; height: 8px; background: var(--vp-c-default-soft); border-radius: 999px; overflow: hidden; }
.fill { height: 100%; background: var(--vp-c-brand-1); border-radius: 999px; transition: width 0.4s ease; }
</style>
