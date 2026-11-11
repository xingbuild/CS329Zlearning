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
