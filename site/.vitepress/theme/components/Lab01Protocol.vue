<script setup lang="ts">
import { ref, computed } from 'vue'

// function calling 协议解剖：schema 一份三吃（菜单/文法/校验）
const FIELDS = [
  { id: 'name', label: 'tools[].name', body: '工具名。进上下文当"菜单"；严格模式还能当文法（约束解码只放行合法调用）——一份 schema 三处复用。' },
  { id: 'desc', label: 'tools[].description', body: '给模型看的自然语言说明——模型选不选这个工具，全看这段话写得好不好（prompt 工程躲在协议里）。' },
  { id: 'params', label: 'tools[].parameters', body: 'JSON Schema（type/properties/required）。既是菜单的"参数表"，也是校验闸的依据——同一份契约。' },
  { id: 'args', label: 'tool_calls[].arguments', body: '⭐ 它是【字符串】不是对象！服务端逐 token 生成的痕迹：协议在数据边界上诚实暴露了"输出本是概率文本"。你的代码要 JSON.parse 它——并拦住解析失败。' },
  { id: 'id', label: 'tool_calls[].id', body: '调用编号：tool 结果回喂时靠它配对（call_xxx ↔ role:tool）。多轮并行的生命线。' },
]
const cur = ref('args')
const f = computed(() => FIELDS.find((x) => x.id === cur.value)!)
</script>

<template>
  <div class="pt">
    <div class="cols">
      <pre class="code">{
  "tools": [{
    "name": "get_weather",
    "description": "当前天气",
    "parameters": {
      "type": "object",
      "properties": {
        "city": { "type": "string" }
      },
      "required": ["city"]
    }
  }]
}
—— 模型输出 ——
{
  "tool_calls": [{
    "id": "call_01",
    "arguments": "{\"city\": \"Stanford\"}"
  }]
}</pre>
      <div class="panel">
        <div class="rail">
          <button v-for="x in FIELDS" :key="x.id" type="button" class="wbtn" :aria-pressed="x.id === cur"
            @click="cur = x.id">{{ x.label }}</button>
        </div>
        <div class="body">{{ f.body }}</div>
      </div>
    </div>
    <div class="hint"><span class="k">一句话 · </span>协议 = 把 L04 三代接口剧场里的 Function Calling 载荷拆开看：<b>契约集中在 schema，风险集中在 arguments 字符串</b>。</div>
  </div>
</template>

<style scoped>
.pt .cols { display: flex; gap: 16px; flex-wrap: wrap; }
.code { flex: 1; min-width: 260px; margin: 0; background: var(--vp-c-default-soft); border-radius: 10px; padding: 14px; font-size: 12px; line-height: 1.6; font-family: var(--vp-font-family-mono, monospace); }
.panel { flex: 1; min-width: 260px; display: flex; flex-direction: column; gap: 10px; }
.rail { display: flex; gap: 6px; flex-wrap: wrap; }
.body { font-size: 14.5px; line-height: 1.7; border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 14px; }
</style>
