<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { isDone, markDone } from '../progress'

const props = defineProps<{ id: string }>()
const done = ref(false)
onMounted(() => {
  done.value = isDone(props.id)
})
function toggle() {
  done.value = !done.value
  markDone(props.id, done.value)
}
</script>

<template>
  <div class="done-wrap">
    <button type="button" class="wbtn" :class="{ on: done }" :aria-pressed="done" @click="toggle">
      {{ done ? '✓ 已学完（点击撤销）' : '✓ 标记本讲已学完' }}
    </button>
    <span class="note">进度保存在本机浏览器</span>
  </div>
</template>

<style scoped>
.done-wrap { display: flex; align-items: center; gap: 12px; margin-top: 34px; flex-wrap: wrap; }
.wbtn.on {
  background: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  color: #fff;
  font-weight: 600;
}
.note { color: var(--vp-c-text-2); font-size: 14px; }
</style>
