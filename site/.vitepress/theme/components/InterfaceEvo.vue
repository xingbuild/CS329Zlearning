<script setup lang="ts">
import { ref, computed } from 'vue'

// 三代标准接口对照，场景取自讲义 lecture04.pdf p.48-54
type Gen = 'rest' | 'fc' | 'mcp'

const GENS: {
  id: Gen
  name: string
  facing: string
  steps: { title: string; body: string; kind: 'req' | 'res' | 'note' }[]
  verdict: string
}[] = [
  {
    id: 'rest',
    name: '① REST API（面向人）',
    facing: '面向人',
    steps: [
      { title: '模型必须先读人类文档', body: 'GET https://api.weather.com/v1/current?city=Stanford\n（URL、参数名、响应结构全靠读文档背下来）', kind: 'note' },
      { title: '请求', body: 'GET /v1/current?city=Stanford', kind: 'req' },
      { title: '响应', body: '200 {"temp_f": 74, "conditions": "sunny"}', kind: 'res' },
      { title: '结论', body: '没有机器可读的契约——换一个 API，模型要重读一份新文档；认证每家各一套。', kind: 'note' },
    ],
    verdict: '为人类开发者设计，模型只是"硬着头皮读文档的实习生"。',
  },
  {
    id: 'fc',
    name: '② Function Calling（面向模型）',
    facing: '面向模型',
    steps: [
      { title: '工具以 JSON Schema 注册', body: '{ "name": "get_weather",\n  "description": "Current weather",\n  "parameters": { "properties":\n    { "city": {"type": "string"} },\n    "required": ["city"] } }', kind: 'note' },
      { title: '模型输出 tool_call', body: '{ "tool_call": { "name": "get_weather",\n  "arguments": {"city": "Stanford"} } }', kind: 'req' },
      { title: 'harness 校验并分发，结果回喂', body: '→ harness 校验 schema（lab01 的第二道闸）→ 执行 → 观察回上下文', kind: 'res' },
      { title: '结论', body: '契约机器可读了；但 schema 活在各家代码库里——为 A 平台写的工具，到 B 平台要重写。', kind: 'note' },
    ],
    verdict: '契约进代码、进运行时——这正是 lab01 第 5 步解剖过的协议。',
  },
  {
    id: 'mcp',
    name: '③ MCP（面向生态）',
    facing: '面向生态',
    steps: [
      { title: '发现：tools/list', body: '{ "jsonrpc": "2.0", "method": "tools/list" }\n→ 返回工具清单：名称 + 描述 + inputSchema（还有 ttlMs 缓存期）', kind: 'req' },
      { title: '选中 weather_current 的 schema', body: 'inputSchema: { location: string,\n  units: enum["metric","imperial"] }', kind: 'note' },
      { title: '执行：tools/call', body: '{ "method": "tools/call",\n  "params": { "name": "weather_current",\n    "arguments": {"location": "Stanford", "units": "imperial"} } }', kind: 'req' },
      { title: '响应（content 数组回给宿主）', body: '"Current weather in Stanford: 68°F, partly cloudy"', kind: 'res' },
      { title: '结论', body: '一个协议、任意客户端；工具一次编写、跨宿主复用；发现发生在运行时。入站/出站双 auth 各自独立。', kind: 'note' },
    ],
    verdict: '工具从"每家私有的 schema"变成"网络里可发现的生态资源"。',
  },
]

const gen = ref<Gen>('rest')
const idx = ref(0)
const cur = computed(() => GENS.find((g) => g.id === gen.value)!)
const step = computed(() => cur.value.steps[idx.value])

function switchGen(g: Gen) {
  gen.value = g
  idx.value = 0
}
</script>

<template>
  <div class="ievo">
    <div class="row wrap">
      <button v-for="g in GENS" :key="g.id" type="button" class="wbtn" :aria-pressed="g.id === gen"
        @click="switchGen(g.id)">{{ g.name }}</button>
      <span class="pill brand">{{ cur.facing }}</span>
    </div>
    <div class="row wrap">
      <button type="button" class="wbtn" :disabled="idx === 0" @click="idx--">◀ 上一步</button>
      <button type="button" class="wbtn primary" :disabled="idx === cur.steps.length - 1" @click="idx++">下一步 ▶</button>
      <span class="meta">第 {{ idx + 1 }} / {{ cur.steps.length }} 步</span>
    </div>
    <div class="stage">
      <div class="step-title">{{ step.title }}</div>
      <pre class="step-body" :class="step.kind">{{ step.body }}</pre>
    </div>
    <div class="hint"><span class="k">这一代的本质 · </span>{{ cur.verdict }}</div>
  </div>
</template>

<style scoped>
.ievo { display: flex; flex-direction: column; gap: 10px; }
.row { display: flex; align-items: center; gap: 8px; }
.row.wrap { flex-wrap: wrap; }
.meta { color: var(--vp-c-text-2); font-size: 13px; }
.stage { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 14px 18px; min-height: 120px; }
.step-title { font-weight: 600; font-size: 15px; margin-bottom: 8px; }
.step-body { margin: 0; white-space: pre-wrap; font-size: 13px; line-height: 1.65; font-family: var(--vp-font-family-mono, monospace); color: var(--vp-c-text-2); }
.step-body.req { color: var(--vp-c-brand-1); }
.step-body.res { color: #16a34a; }
</style>
