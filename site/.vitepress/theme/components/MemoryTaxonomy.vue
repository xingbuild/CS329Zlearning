<script setup lang="ts">
import { ref, computed } from 'vue'

// CoALA 记忆类型学，整理自讲义 lecture07.pdf p.15-22（L01 p.46 的深化版）
const TYPES = [
  {
    id: 'working',
    name: '工作记忆 Working',
    what: '当下正在看、正在推理的内容：观察、目标、用户输入、内部思考',
    where: '就是上下文窗口',
    write: '循环的每一步自动写入',
    read: '天然在场（无需检索）',
    limit: '容量小、一关就没了——L02 的 context rot 也住在这里',
  },
  {
    id: 'episodic',
    name: '情景记忆 Episodic',
    what: '过去行为经历的原始日志：轨迹、历史会话',
    where: '事件流 / 数据库',
    write: '追加式（append-only）记录',
    read: '按相关性/时间检索',
    limit: '体积大；"发生过"不等于"有用"',
  },
  {
    id: 'semantic',
    name: '语义记忆 Semantic',
    what: '关于世界的事实：用户偏好、规则、通用知识',
    where: '向量库 / 文件 / 知识图谱',
    write: 'LLM 对事件做推理后提炼写入',
    read: '检索（RAG 同款机制）',
    limit: '会过时、会冲突（用户偏好会变）',
  },
  {
    id: 'procedural',
    name: '程序记忆 Procedural',
    what: 'HOW：技能、流程、行为规则',
    where: '技能文件（代码/MD）/ 权重',
    write: '从成功轨迹归纳（Voyager/AWM）或人写（Skill Files）',
    read: '按任务加载进系统提示',
    limit: '对动态环境不鲁棒（Cao et al. 2026）',
  },
]

const cur = ref('semantic')
const item = computed(() => TYPES.find((t) => t.id === cur.value)!)
</script>

<template>
  <div class="mt">
    <div class="rail">
      <button v-for="t in TYPES" :key="t.id" type="button" class="wbtn" :aria-pressed="t.id === cur"
        @click="cur = t.id">{{ t.name.split(' ')[0] }}·{{ t.name.split(' ')[1] }}</button>
    </div>
    <div class="detail">
      <div class="title">{{ item.name }}</div>
      <div class="d-row"><span class="dk">存什么</span><span>{{ item.what }}</span></div>
      <div class="d-row"><span class="dk">放在哪</span><span>{{ item.where }}</span></div>
      <div class="d-row"><span class="dk">怎么写</span><span>{{ item.write }}</span></div>
      <div class="d-row"><span class="dk">怎么读</span><span>{{ item.read }}</span></div>
      <div class="d-row"><span class="dk">天花板</span><span>{{ item.limit }}</span></div>
    </div>
    <div class="hint"><span class="k">另一根轴 · </span>每型都可以放在<b>参数</b>里（微调进权重：语义=预训练知识、程序=指令遵循、情景=不适用）或<b>上下文</b>里（检索式：事实/技能/历史对话）——参数版便宜但静态，上下文版动态但占窗口。</div>
  </div>
</template>

<style scoped>
.mt { display: flex; flex-direction: column; gap: 12px; }
.rail { display: flex; gap: 8px; flex-wrap: wrap; }
.detail { border: 1px dashed var(--vp-c-divider); border-radius: 10px; padding: 12px 16px; display: flex; flex-direction: column; gap: 8px; }
.title { font-weight: 700; font-size: 15.5px; }
.d-row { display: flex; gap: 10px; font-size: 14.5px; line-height: 1.65; }
.dk { flex: none; color: var(--vp-c-text-3); font-size: 13px; min-width: 56px; padding-top: 2px; }
</style>
