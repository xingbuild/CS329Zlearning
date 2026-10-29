<script setup lang="ts">
import { ref, computed } from 'vue'

// 裸接口失败动物园：8 个真实失败形态过 json.loads（讲义 lab01 step1）
const FAILS = [
  { name: 'Python 布尔值', out: '{ "human": True }', err: 'NameError/JSONDecodeError：JSON 只有 true/false' },
  { name: '尾随逗号', out: '{ "a": 1, }', err: 'Expecting property name：JSON 不允许尾逗号' },
  { name: '单引号', out: "{ 'a': 1 }", err: 'Expecting property name：字符串必须双引号' },
  { name: '裸键名', out: '{ a: 1 }', err: '键名必须加双引号' },
  { name: 'markdown 围栏', out: '```json\n{ "a": 1 }\n```', err: '开头就不是 {：模型"好心"包了一层' },
  { name: '中文引号', out: '{ “a”: 1 }', err: '全角引号不是引号： tokenizer 层面的静默错' },
  { name: '数组还是对象', out: '["a", 1]', err: '合法 JSON、错误形状：loads 成功，后续代码崩溃' },
  { name: '解释性开场白', out: '好的，以下是 JSON：\n{ "a": 1 }', err: '前置自然语言污染载荷' },
]
const cur = ref(0)
const f = computed(() => FAILS[cur.value])
const passed = computed(() => cur.value === 6) // 唯一"语法过、语义埋雷"的
</script>

<template>
  <div class="fz">
    <div class="rail">
      <button v-for="(x, i) in FAILS" :key="i" type="button" class="wbtn" :aria-pressed="i === cur"
        @click="cur = i">{{ i + 1 }}</button>
    </div>
    <div class="out"><span class="k">模型输出 →</span><pre>{{ f.out }}</pre></div>
    <div class="verdict" :class="passed ? 'warn' : 'bad'">
      <template v-if="passed">△ json.loads <b>通过</b>——但形状错了：{{ f.err }}。<b>语法闸拦不住它，语义闸（schema 校验）才能。</b></template>
      <template v-else>❌ json.loads 抛异常：{{ f.err }}</template>
    </div>
    <div class="hint"><span class="k">结论 · </span>8 个形态 7 个语法死、1 个语义雷——模型"会"写 JSON，缺的是让它"必须"写的机制。</div>
  </div>
</template>

<style scoped>
.fz { display: flex; flex-direction: column; gap: 10px; }
.rail { display: flex; gap: 6px; flex-wrap: wrap; }
.out { display: flex; gap: 10px; align-items: center; background: var(--vp-c-default-soft); border-radius: 8px; padding: 8px 14px; }
.out pre { margin: 0; font-size: 13.5px; white-space: pre-wrap; }
.k { font-size: 12px; color: var(--vp-c-text-3); flex: none; }
.verdict { border-radius: 9px; padding: 10px 14px; font-size: 14px; line-height: 1.65; }
.verdict.bad { background: rgba(220,38,38,.09); }
.verdict.warn { background: rgba(217,119,6,.1); }
</style>
