// Lab 11 · 六圈真实轨迹教学化数据（源自 agentminiswe 实跑 step-trajectory-B.json，GLM-5.3-flash · 2026-11-11 · mini-swe-agent v2.4.6）
// 红线：不含 config/model_kwargs（无凭据）；长输出为标注式剪辑（cut=true 表示有删节）
export interface Round {
  n: number
  thought: string
  command: string
  returncode: number
  output: string
  cut?: boolean
  memoryAfter: number
  duty: string
  gate: 'pass' | 'exit'
  outcome: string
}

export const META = {
  badge: '🧪 模拟回放 · 非实时运行 · 真实轨迹（GLM-5.3-flash · 2026-11-11 · mini-swe-agent v2.4.6）',
  task: '在当前目录创建 sorter.py，实现一个有 bug 的冒泡排序函数 sort_list；再创建 test_sorter.py，用 3 个 assert 测试并运行；发现失败就修改 sorter.py，直到全部测试通过；最后运行全部测试并展示全绿结果。完成后结束任务。',
  stepLimit: 8,
  model: 'GLM-5.3-flash',
  apiCalls: 6,
  exitStatus: 'Submitted',
  source: 'agentminiswe 实操仓库真实运行 · 模型 GLM-5.3-flash（bigmodel）· 2026-11-11 · 成本约 ¥0.1 · 轨迹 serialize 格式 v1.1',
}

export const ROUNDS: Round[] = [
  {
    n: 1,
    thought: 'THOUGHT: Let me first check the current directory to see what\'s there before creating the files.',
    command: 'pwd && ls -la',
    returncode: 0,
    output: '/Users/kingjin/.../playground\ntotal 136\n...\n-rw-r--r--  350 Nov 11 16:10 sorter.py\n-rw-r--r--  422 Nov 11 16:05 test_sorter.py\n（中间目录项有删节）',
    cut: true,
    memoryAfter: 4,
    duty: '首轮无职责A（没有上一圈结果可判断）；职责B=先侦察环境再动手',
    gate: 'pass',
    outcome: '发现目录里已有 sorter.py / test_sorter.py（前次尝试的残留）——先看再动。',
  },
  {
    n: 2,
    thought: 'THOUGHT: There are already `sorter.py` and `test_sorter.py` files. Let me read them to see their current content before deciding what to do.',
    command: 'echo "=== sorter.py ===" && cat sorter.py && echo "=== test_sorter.py ===" && cat test_sorter.py',
    returncode: 0,
    output: '=== sorter.py ===\ndef sort_list(lst):\n    """对列表进行冒泡排序（buggy 版本：比较符号写反了）"""\n    ... if result[j] > result[j + 1]:  # BUG: 应该是 >\n=== test_sorter.py ===\n3 个 assert + print("All 3 tests passed!")\n（两文件全文有删节）',
    cut: true,
    memoryAfter: 6,
    duty: '职责A=发现"注释声称有 bug，但代码（>）其实是对的" | 职责B=读全文再定策略',
    gate: 'pass',
    outcome: '关键发现：残留文件注释说有 bug、代码却是对的——任务要求"真 bug"，决定重建。',
  },
  {
    n: 3,
    thought: 'THOUGHT: The existing files are from a previous attempt — the sorter.py comment claims a bug but the code (`>`) is actually correct. To follow the task faithfully, I\'ll recreate sorter.py with a genuine bug (comparison operator reversed to `<`) … then run the tests to observe the failure.',
    command: 'cat <<\'EOF\' > sorter.py\n（真 bug 版：< 号降序排序）\nEOF\ncat <<\'EOF\' > test_sorter.py\n（3 个 assert 测试）\nEOF\necho "--- 运行测试（预期失败）---" && python3 test_sorter.py',
    returncode: 1,
    output: '--- 运行测试（预期失败）---\nTraceback (most recent call last):\n  File ".../test_sorter.py", line 4, in <module>\n    assert sort_list([3, 1, 2]) == [1, 2, 3]\nAssertionError: test1 失败: 基本排序结果错误\n（heredoc 写文件部分有删节，本圈命令共 3 段拼接）',
    cut: true,
    memoryAfter: 8,
    duty: '职责A=基于圈 2 发现决定重建 | 职责B=写真 bug 版 + 测试并运行',
    gate: 'pass',
    outcome: '🔴 测试当场变红（returncode 1，AssertionError）——这一圈是整个任务的"失败现场"。',
  },
  {
    n: 4,
    thought: 'THOUGHT: 测试如预期失败了（test1 失败，因为比较符号写反导致降序）。现在修改 sorter.py，把 `<` 改回 `>` 修复 bug，然后重新运行全部测试验证通过。',
    command: 'sed -i \'\' \'s/if result[j] < result[j + 1]…/if result[j] > result[j + 1]…/\' sorter.py && cat sorter.py && python3 test_sorter.py',
    returncode: 0,
    output: '--- 修复后的 sorter.py ---\n（代码有删节）\n--- 运行全部测试 ---\nAll 3 tests passed!',
    cut: true,
    memoryAfter: 10,
    duty: '职责A=引用圈 3 的红（AssertionError）定位根因 | 职责B=sed 修复 + 重跑全部测试',
    gate: 'pass',
    outcome: '🟢 3/3 全绿——修复完成。注意职责A正是"错误回喂"的读侧：圈的失败成为本圈的上下文。',
  },
  {
    n: 5,
    thought: 'THOUGHT: All 3 tests pass. The docstring still says "buggy 版本" which is now inaccurate — let me update it … then run the full test suite one final time.',
    command: 'sed -i \'\' \'s/（buggy 版本：比较符号写反了）/（已修复：按升序排列）/\' sorter.py && cat sorter.py && python3 test_sorter.py',
    returncode: 0,
    output: '=== 最终 sorter.py ===\n"""对列表进行冒泡排序（已修复：按升序排列）"""\n（代码有删节）\n=== 运行全部测试 ===\nAll 3 tests passed!\n✅ 全部 3 个测试通过 — 结果全绿',
    cut: true,
    memoryAfter: 12,
    duty: '职责A=验收圈 4 全绿 | 职责B=文档一致性扫尾 + 终验',
    gate: 'pass',
    outcome: '全绿之后的"多扫尾一轮"——模型侧收工阈值的不确定性活标本（它没有立刻交卷）。',
  },
  {
    n: 6,
    thought: 'THOUGHT: 任务已完成（五步总结：创建 buggy 版 → 3 assert → 红 → 修复 → 全绿）。现在提交并结束任务。\n\n（正文附五步中文总结）',
    command: 'echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT',
    returncode: 0,
    output: 'COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT',
    memoryAfter: 14,
    duty: '职责A=确认全绿可交卷 | 职责B=发出交卷暗号（且仅此一条命令，遵守 instance 模板禁令）',
    gate: 'exit',
    outcome: '🏁 暗号命中：观察被没收（观察形成/追加不发生）→ exit 消息入史（写给轨迹而非模型）→ exit_status=Submitted。',
  },
]


/* ===== 单步闭环扩展数据（规格源：notes/stepper.py v3.4 + 手册 + replay 终端取证）===== */

// 分拍预测提示语（终端 pause() 原文）
export const HINTS = {
  think: '模型接下来会执行什么命令？先在心里/纸上写下来',
  do: '这条命令会成功吗？返回码几？输出是什么？',
}

// 溯源 6 站（阶段 0 · 数据血统链：键盘 → 头两条消息入史）
export const ORIGIN = [
  { n: 1, title: '终端输入——源头中的源头', body: [
    '你敲的整行命令: python notes/stepper.py "在当前目录创建 sorter.py，实现一个有 bug 的冒泡排序…（任务全文）"',
    'Python 收到的参数数组 sys.argv: [0]="notes/stepper.py" [1]="任务全文（引号把一串字捆成一个参数）"',
  ]},
  { n: 2, title: 'task 变量诞生', body: [
    '代码: task = " ".join(a for a in sys.argv[1:] if a not in ("--fast","--menu"))',
    'task 的值 = 你的任务全文（一个普通字符串）',
  ]},
  { n: 3, title: '说明书产地：default.yaml → system_template', body: [
    '共 15 行、无变量占位符——宪法在配置文件里躺着，不在代码里',
    '前两行：You are a helpful assistant… / Your response must contain exactly ONE bash code block…',
    '（终端此处可输 2 看说明书全文——网页版点页面下方"说明书全文"）',
  ]},
  { n: 4, title: '信纸产地：default.yaml → instance_template', body: [
    '共 85 行、含 {{task}} 填空处——任务将以模板变量填进信纸',
    '关键行：Please solve this issue: {{task}} … Submit … echo COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT',
  ]},
  { n: 5, title: '填空渲染（jinja2）——你的字进入信纸的瞬间', body: [
    'agent._render_template(ins_tpl)：{{task}} 处被替换为你的任务文本',
    '渲染结果 = user 消息全文（含推荐工作流六步、格式禁令、系统信息）',
  ]},
  { n: 6, title: '头两条消息入史 → 主循环启动', body: [
    'messages[0] = system（渲染后的说明书） · messages[1] = user（渲染后的信纸）',
    '此刻记忆 2 条——agent 的一切"经验"从这个底座开始增长',
  ]},
]

// 秘技 2 · 本拍将执行的代码原文（default.py 关键行，据 stepper.py CODE 字典照录）
export const CODE = {
  think: 'L132  if 0 < step_limit <= n_calls or 0 < cost_limit <= cost:\nL133      raise LimitsExceeded(...)          <- 超步数/超钱: 当场跳车\nL148  self.n_calls += 1\nL149  message = self.model.query(self.messages)   <- 真正调 GLM\nL150  self.cost += message["extra"]["cost"]\nL151  self.add_messages(message)                  <- 回复入史',
  do: 'L156  outputs = [self.env.execute(action) for action in message["extra"]["actions"]]\n           <- local.py 开子进程执行\nL157  return self.add_messages(...format_observation_messages...)  <- 观察入史\nlocal.py L48  if 输出首行 == "COMPLETE_TASK_AND_SUBMIT_FINAL_OUTPUT":\n           <- 交卷暗号命中 -> 抛 Submitted',
}

// 秘技 3 · playground 文件现状（由轨迹输出推导，页面须标注）
export const FILES: Record<number, string> = {
  1: 'hello.txt 22B · hi.txt 19B · hi2.txt 13B · hi3.txt 15B · sorter.py 350B(前次残留) · test_sorter.py 422B(前次残留) · …（据圈1 ls 输出）',
  2: 'hello.txt 22B · hi.txt 19B · hi2.txt 13B · hi3.txt 15B · sorter.py 350B(前次残留) · test_sorter.py 422B(前次残留) · …（据圈1 ls 输出）',
  3: 'sorter.py（本轮重写·真bug版 `<`） · test_sorter.py（本轮重写·3 assert）——据圈3 heredoc 命令推导',
  4: 'sorter.py（`<`→`>` 已修复）——据圈4 sed 命令推导',
  5: 'sorter.py（docstring 更新为「已修复」）——据圈5 sed 推导',
  6: 'sorter.py（docstring 更新为「已修复」）——据圈5 sed 推导',
}
