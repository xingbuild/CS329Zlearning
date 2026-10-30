import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import L01Theater from './components/L01Theater.vue'
import PnCalc from './components/PnCalc.vue'
import LessonDone from './components/LessonDone.vue'
import HomeProgress from './components/HomeProgress.vue'
import PaperPara from './components/PaperPara.vue'
import SamplingLab from './components/SamplingLab.vue'
import KvCacheDemo from './components/KvCacheDemo.vue'
import ChunkingLab from './components/ChunkingLab.vue'
import RagFailureZoo from './components/RagFailureZoo.vue'
import InterfaceEvo from './components/InterfaceEvo.vue'
import PassKCalc from './components/PassKCalc.vue'
import AgencySpectrum from './components/AgencySpectrum.vue'
import HarnessCompare from './components/HarnessCompare.vue'
import WorkflowPatterns from './components/WorkflowPatterns.vue'
import ContextPatterns from './components/ContextPatterns.vue'
import MemoryTaxonomy from './components/MemoryTaxonomy.vue'
import MemoryDesignBoard from './components/MemoryDesignBoard.vue'
import MasTopology from './components/MasTopology.vue'
import MasFailureZoo from './components/MasFailureZoo.vue'
import AgentPanorama from './components/AgentPanorama.vue'
import TransformerFlow from './components/TransformerFlow.vue'
import RagPipeline from './components/RagPipeline.vue'
import ToolCallAnatomy from './components/ToolCallAnatomy.vue'
import RagLab from './components/RagLab.vue'
import Lab01FailZoo from './components/Lab01FailZoo.vue'
import Lab01Gates from './components/Lab01Gates.vue'
import Lab01MaskLab from './components/Lab01MaskLab.vue'
import Lab01Protocol from './components/Lab01Protocol.vue'
import Lab01Loop from './components/Lab01Loop.vue'
import CodingLoopLab from './components/CodingLoopLab.vue'
import PassKSim from './components/PassKSim.vue'
import EvoChain from './components/EvoChain.vue'
import TermCard from './components/TermCard.vue'
import LineageMap from './components/LineageMap.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('L01Theater', L01Theater)
    app.component('PnCalc', PnCalc)
    app.component('LessonDone', LessonDone)
    app.component('HomeProgress', HomeProgress)
    app.component('PaperPara', PaperPara)
    app.component('SamplingLab', SamplingLab)
    app.component('KvCacheDemo', KvCacheDemo)
    app.component('ChunkingLab', ChunkingLab)
    app.component('RagFailureZoo', RagFailureZoo)
    app.component('InterfaceEvo', InterfaceEvo)
    app.component('PassKCalc', PassKCalc)
    app.component('AgencySpectrum', AgencySpectrum)
    app.component('HarnessCompare', HarnessCompare)
    app.component('WorkflowPatterns', WorkflowPatterns)
    app.component('ContextPatterns', ContextPatterns)
    app.component('MemoryTaxonomy', MemoryTaxonomy)
    app.component('MemoryDesignBoard', MemoryDesignBoard)
    app.component('MasTopology', MasTopology)
    app.component('MasFailureZoo', MasFailureZoo)
    app.component('AgentPanorama', AgentPanorama)
    app.component('TransformerFlow', TransformerFlow)
    app.component('RagPipeline', RagPipeline)
    app.component('ToolCallAnatomy', ToolCallAnatomy)
    app.component('RagLab', RagLab)
    app.component('Lab01FailZoo', Lab01FailZoo)
    app.component('Lab01Gates', Lab01Gates)
    app.component('Lab01MaskLab', Lab01MaskLab)
    app.component('Lab01Protocol', Lab01Protocol)
    app.component('Lab01Loop', Lab01Loop)
    app.component('CodingLoopLab', CodingLoopLab)
    app.component('PassKSim', PassKSim)
    app.component('EvoChain', EvoChain)
    app.component('TermCard', TermCard)
    app.component('LineageMap', LineageMap)
  },
} satisfies Theme
