import { defineConfig } from 'vitepress'
import { readFileSync } from 'node:fs'

// 版本号写入页脚（GitHub 上的工作记录在产品内可见）
let ver = ''
try {
  ver = readFileSync(new URL('../../VERSION', import.meta.url), 'utf-8').trim()
} catch {
  /* 本地无 VERSION 时静默 */
}

export default defineConfig({
  lang: 'zh-CN',
  // GitHub Pages 部署在 /CS329Zlearning/ 子路径；本地与 Netlify 等根路径托管用 '/'
  base: process.env.BASE || '/',
  title: 'Engineering AI Agents',
  description:
    '把「会用 AI」变成「会工程化 AI」——以斯坦福 CS329Z 讲义为底本的交互式课程',
  head: [['meta', { name: 'viewport', content: 'width=device-width, initial-scale=1' }]],
  markdown: { math: true },

  themeConfig: {
    nav: [
      { text: '课程地图', link: '/' },
      { text: '技术谱系', link: '/lineage/' },
      { text: 'L01 · 全景', link: '/l01/' },
      { text: '实验室', link: '/labs/' },
    ],

    outline: { level: [2, 3], label: '本讲结构' },
    docFooter: { prev: '上一讲', next: '下一讲' },
    lastUpdated: { text: '最后更新' },
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索课程', buttonAriaLabel: '搜索课程' },
          modal: {
            noResultsText: '没有找到结果',
            resetButtonTitle: '清除查询',
            displayDetails: '显示详情',
          },
        },
      },
    },

    sidebar: [
      {
        text: 'L01 · Agent 是什么：一个循环的五十年',
        items: [
          { text: '课文', link: '/l01/' },
          { text: '术语与复刻', link: '/l01/guide/' },
          { text: '论文精读 · ReAct', link: '/l01/readings/react/' },
        ],
      },
      {
        text: 'L02 · LLM 作为建筑材料',
        items: [
          { text: '课文', link: '/l02/' },
          { text: '术语与复刻', link: '/l02/guide/' },
          { text: '外部资源与视频', link: '/l02/resources/' },
        ],
      },
      {
        text: 'L03 · RAG：外挂知识器官',
        items: [
          { text: '课文', link: '/l03/' },
          { text: '术语与复刻', link: '/l03/guide/' },
          { text: '交互实验室 · Lab 02', link: '/l03/lab/' },
          { text: '外部资源与视频', link: '/l03/resources/' },
        ],
      },
      {
        text: 'L04 · 工具使用：从会说到会做',
        items: [
          { text: '课文', link: '/l04/' },
          { text: '术语与复刻', link: '/l04/guide/' },
          { text: '交互实验室 · Lab 01', link: '/l04/lab/' },
          { text: 'Coding 闭环 · Lab 03', link: '/l04/lab2/' },
          { text: '外部资源与视频', link: '/l04/resources/' },
        ],
      },
      {
        text: 'L05 · 框架与编排：看穿打包术',
        items: [{ text: '课文', link: '/l05/' },
          { text: '术语与复刻', link: '/l05/guide/' }],
      },
      {
        text: 'L06 · 设计模式与脚手架',
        items: [
          { text: '课文', link: '/l06/' },
          { text: '术语与复刻', link: '/l06/guide/' },
          { text: '配套实验 · Lab 01', link: '/labs/' },
        ],
      },
      {
        text: 'L07 · 记忆架构',
        items: [{ text: '课文', link: '/l07/' },
          { text: '术语与复刻', link: '/l07/guide/' }],
      },
      {
        text: 'L08 · 多智能体系统',
        items: [{ text: '课文', link: '/l08/' },
          { text: '术语与复刻', link: '/l08/guide/' }],
      },
      // 未上线的讲次不进侧栏；上线时在此追加（AGENTS.md §6 流程）
      {
        text: '实验室',
        items: [{ text: 'Lab 01 · Structured I/O', link: '/labs/' }],
      },
    ],

    footer: {
      message:
        `本课程是斯坦福 CS329Z 讲义的学习笔记式原创演绎，讲义版权归原作者；文本与交互组件为原创。v${ver}`,
      copyright: 'Learning in public · 持续迭代中',
    },
  },
})
