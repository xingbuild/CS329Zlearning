"""
第 3 步：硬约束 —— 自己动手实现一个 constrained decoding（本教程的核心）
=======================================================================

理论对应：解码层。把 JSON Schema / 正则文法【编译成有限状态自动机】，
解码每一步先用 FSM 算出"仍留在文法内的后继 token 集合"，把其余 token 的
logit 掩蔽（置 -inf）再采样。合法性由构造保证，与模型能力无关。

本文件完整实现（无任何 mock）：
  1) 文法：一个正则表达式（就是契约本身）
  2) Thompson 构造：正则 -> NFA（真实算法，Outlines 走的就是这条路）
  3) ε-闭包 + 步进：FSM 在字符层面前进
  4) token 级掩码：词表里有"多字符合并 token"，一个 token 部分越界就整体
     掩蔽 —— 这正是真实 BPE 词表 × 字符文法求交的难点（XGrammar 的核心问题）
  5) 解码循环：每步展示"模型最想要的 token" vs "掩蔽后实际选择的 token"

唯一"假"的东西：logits。真实中它来自神经网络的 forward pass；这里我们用
逐脚本注入（模拟模型的意图），让实验可复现。文法、掩码、解码循环全部真实。

运行：python3 step3_constrained_decoding.py
"""

import json
import string

# =====================================================================
# 一、文法：契约就是一个正则表达式
#    目标语言：{"name": "alice", "age": 30} 这一种形态
# =====================================================================
GRAMMAR = r'\{"name": *"[a-z]+", *"age": *[0-9]+\}'


class RegexNFA:
    """Thompson 构造：正则表达式 -> 非确定有限自动机（ε-NFA）。

    支持：字面量、[..]字符类(含区间)、| 、* 、+ 、? 、( )分组、\\x 转义。
    状态是整数；转移标签是 frozenset(字符集合)，None 表示 ε 转移。
    """

    def __init__(self, pattern: str):
        self.p, self.i = pattern, 0
        self.adj: dict[int, list] = {}
        self.start, self.accept = self._parse_alt()
        assert self.i == len(self.p), f"正则未消费完: 剩 {pattern[self.i:]!r}"

    # ---- 基础设施 ----
    def _st(self) -> int:
        n = len(self.adj)
        self.adj[n] = []
        return n

    def _link(self, a: int, label, b: int):
        self.adj[a].append((label, b))

    def _peek(self):
        return self.p[self.i] if self.i < len(self.p) else None

    def _leaf(self, chars: frozenset):
        s, e = self._st(), self._st()
        self._link(s, chars, e)
        return s, e

    # ---- 递归下降解析（优先级：alt < concat < repeat < atom）----
    def _parse_alt(self):
        s, e = self._parse_concat()
        while self._peek() == "|":
            self.i += 1
            s2, e2 = self._parse_concat()
            ns, ne = self._st(), self._st()
            self._link(ns, None, s)
            self._link(ns, None, s2)
            self._link(e, None, ne)
            self._link(e2, None, ne)
            s, e = ns, ne
        return s, e

    def _parse_concat(self):
        frags = []
        while self._peek() not in (None, "|", ")"):
            frags.append(self._parse_repeat())
        s, e = self._st(), self._st()
        prev = s
        for fs, fe in frags:
            self._link(prev, None, fs)
            prev = fe
        self._link(prev, None, e)
        return s, e

    def _parse_repeat(self):
        s, e = self._parse_atom()
        while self._peek() in ("*", "+", "?"):
            op = self.p[self.i]
            self.i += 1
            ns, ne = self._st(), self._st()
            self._link(ns, None, s)
            self._link(e, None, ne)
            if op in ("*", "+"):          # 回边：可循环
                self._link(e, None, s)
            if op in ("*", "?"):          # 旁路：可跳过
                self._link(ns, None, ne)
            s, e = ns, ne
        return s, e

    def _parse_atom(self):
        c = self.p[self.i]
        if c == "(":
            self.i += 1
            frag = self._parse_alt()
            assert self.p[self.i] == ")"
            self.i += 1
            return frag
        if c == "[":
            self.i += 1
            chars = set()
            while self.p[self.i] != "]":
                if self.p[self.i + 1] == "-" and self.p[self.i + 2] != "]":
                    a, b = self.p[self.i], self.p[self.i + 2]
                    chars.update(chr(x) for x in range(ord(a), ord(b) + 1))
                    self.i += 3
                else:
                    chars.add(self.p[self.i])
                    self.i += 1
            self.i += 1  # ']'
            return self._leaf(frozenset(chars))
        if c == "\\":
            self.i += 1
            ch = self.p[self.i]
            self.i += 1
            return self._leaf(frozenset([ch]))
        self.i += 1
        return self._leaf(frozenset([c]))   # 普通字面量：{ } " : , 空格 ...

    # ---- 运行时：ε-闭包、单字符步进 ----
    def eps_closure(self, states: set) -> set:
        stack, seen = list(states), set(states)
        while stack:
            s = stack.pop()
            for label, dst in self.adj[s]:
                if label is None and dst not in seen:
                    seen.add(dst)
                    stack.append(dst)
        return seen

    def step(self, states: set, ch: str) -> set:
        closed = self.eps_closure(states)
        nxt = set()
        for s in closed:
            for label, dst in self.adj[s]:
                if label is not None and ch in label:
                    nxt.add(dst)
        return self.eps_closure(nxt) if nxt else set()

    def legal_chars(self, states: set) -> set:
        closed = self.eps_closure(states)
        chars = set()
        for s in closed:
            for label, _ in self.adj[s]:
                if label is not None:
                    chars.update(label)
        return chars


NFA = RegexNFA(GRAMMAR)


# =====================================================================
# 二、词表：模拟 BPE —— 除了单字符，还有"合并 token"
#    合并 token 是真实分词器的常态（": "、"name"、true 都是单 token）
# =====================================================================
SINGLES = sorted(set(string.ascii_lowercase + string.digits + ' {}":,'))
EXTRA_SINGLES = ["A", "L", "T", " ", "`", "是"]     # 模型可能想输出、但文法外的字符
# 两种"冒号"合并 token：name 的值是字符串（冒号后跟开引号），age 的值是
# 数字（冒号后直接数字）——真实 BPE 词表里 '":' 和 '": ' 也都是常见单 token
T_NAME, T_AGE = '"name"', '"age"'
T_COLON_STR, T_COLON_NUM, T_COMMA = ': "', ': ', ', '
MERGES = [T_NAME, T_AGE, T_COLON_STR, T_COLON_NUM, T_COMMA,
          'ice":', "True", "```json", "是"]
VOCAB = sorted(set(SINGLES) | set(EXTRA_SINGLES)) + MERGES


def token_verdict(states: set, token: str):
    """token 级合法性：所有字符必须能逐个穿过 FSM。部分越界 = 整体掩蔽。"""
    cur = set(states)
    for i, ch in enumerate(token, 1):
        cur = NFA.step(cur, ch)
        if not cur:
            return False, i
    return True, None


def legal_tokens(states: set):
    return [t for t in VOCAB if token_verdict(states, t)[0]]


def consume(states: set, token: str) -> set:
    """让 FSM 吃掉一个（可能多字符的）token：逐字符步进，中途死亡返回空集。"""
    cur = set(states)
    for ch in token:
        cur = NFA.step(cur, ch)   # step 只接受单字符——token 必须拆开喂
        if not cur:
            return set()
    return cur


# =====================================================================
# 三、解码循环：logits 脚本（模拟模型意图） × 掩码开关
# =====================================================================
DEFAULT_LOGIT = -1.0


def score_of(script_row: dict, token: str) -> float:
    return script_row.get(token, DEFAULT_LOGIT)


def decode(logits_script, masked: bool, label: str = ""):
    """贪心解码。masked=False 时模型可以为所欲为（一旦越轨 FSM 追不回来）。

    logits_script 的每个元素可以是 dict（静态偏好），也可以是
    callable(t, 已生成文本) -> dict（随前缀重算的条件偏好，见实验 C）。
    """
    states = {NFA.start}
    out, left_at = [], None
    print(f"\n>>> 解码 [{label}]（掩码={'开' if masked else '关'}）")
    for t, row in enumerate(logits_script):
        if callable(row):
            row = row(t, "".join(out))
        if row is None:                    # 模型主动停止（相当于 EOS）
            print(f"  step {t:>2} | 模型发出 EOS -> 解码终止")
            break
        if masked:
            allowed = legal_tokens(states)
            if not allowed:            # 接受态：没有任何合法后继 -> 自然终止
                print(f"  step {t:>2} | FSM 已到接受态且无合法后继 -> 解码终止")
                break
        else:
            allowed = VOCAB
        scores = {tok: score_of(row, tok) for tok in VOCAB}
        wanted = max(VOCAB, key=lambda k: scores[k])       # 模型最想要的（全词表）
        chosen = max(allowed, key=lambda k: scores[k])     # 实际能选的
        if chosen != wanted:
            print(f"  step {t:>2} | 想要 {wanted!r}({scores[wanted]:+.1f}) "
                  f"✗被掩蔽 -> 改选 {chosen!r}({scores[chosen]:+.1f})")
        states = consume(states, chosen) if states else set()
        if masked:
            assert states, "掩码开着却越界了？不可能——这就是'由构造保证'"
        elif not states and left_at is None:
            left_at = t
            print(f"  step {t:>2} | ⚠ 选择了 {chosen!r}，离开文法！"
                  f"此后 FSM 失去保护，全靠模型自觉")
        out.append(chosen)
    text = "".join(out)
    try:
        json.loads(text)
        verdict = "json.loads ✓"
    except json.JSONDecodeError as e:
        verdict = f"json.loads ✗ ({e.msg})"
    accepted = NFA.accept in NFA.eps_closure(states) if states else False
    print(f"  最终输出: {text!r}")
    print(f"  FSM 终态: {'接受 ✓' if accepted else '不接受 ✗'} | {verdict}")
    return text


# =====================================================================
# 四、掩码解剖：站在某个状态上，看每个 token 的判定
# =====================================================================
def dissect(prefix: str):
    states = {NFA.start}
    for ch in prefix:
        states = NFA.step(states, ch)
        assert states, f"前缀本身就不合法: {prefix!r} 在 {ch!r} 处"
    menu = "".join(sorted(NFA.legal_chars(states)))
    print(f"\n  已生成前缀: {prefix!r}")
    print(f"  FSM 活跃状态: {len(NFA.eps_closure(states))} 个 | 合法单字符菜单: {menu!r}")
    for tok in MERGES:
        ok, die = token_verdict(states, tok)
        if ok:
            print(f"    合并 token {tok!r:>10} -> ✓ 合法（可作为一步吐出）")
        else:
            print(f"    合并 token {tok!r:>10} -> ✗ 掩蔽（第 {die} 个字符处离开文法，"
                  f"整体作废，解码器只能退回更碎的单字符 token）")


# =====================================================================
# 五、三组实验
# =====================================================================
def main():
    n_trans = sum(len(v) for v in NFA.adj.values())
    print("=" * 76)
    print("第 3 步：constrained decoding —— 把保证从'概率'搬进'解码过程'")
    print("=" * 76)
    print(f"\n[编译] 文法: {GRAMMAR}")
    print(f"[编译] Thompson 构造完成: {len(NFA.adj)} 个状态, {n_trans} 条转移 "
          f"(start={NFA.start}, accept={NFA.accept})")
    print(f"[词表] {len(VOCAB)} 个 token = {len(SINGLES)} 个文法内单字符 + "
          f"{len(EXTRA_SINGLES)} 个文法外字符 + {len(MERGES)} 个多字符合并 token")
    print("       （真实 BPE 词表同理：'\\\": \\\"'、'name'、'true' 常是单个 token）")

    print("\n" + "-" * 76)
    print("【掩码解剖】多字符 token 怎么被逐字符审判")
    dissect('{')
    dissect('{"name": "al')

    # ---- 实验 A：乖模型，掩码前后都成功（基线）----
    good = [
        {"{": 5}, {T_NAME: 5}, {T_COLON_STR: 5},
        {"a": 5}, {"l": 5}, {"i": 5}, {"c": 5}, {"e": 5}, {'"': 5},
        {T_COMMA: 5}, {T_AGE: 5}, {T_COLON_NUM: 5},
        {"3": 5}, {"0": 5}, {"}": 5},
    ]
    print("\n" + "-" * 76)
    print("【实验 A】乖模型：意图本来就在文法内")
    decode(good, masked=False, label="A-无掩码")
    decode(good, masked=True, label="A-有掩码")

    # ---- 实验 B：Python 习惯 True（JSON 只认小写 true，而本文法此处要数字）----
    py = list(good[:12]) + [{"True": 9, "3": 2}, {"0": 4, "}": 2}, {"}": 5}]
    print("\n" + "-" * 76)
    print("【实验 B】模型想写 Python 风格的 True")
    decode(py, masked=False, label="B-无掩码")
    decode(py, masked=True, label="B-有掩码")

    # ---- 实验 C：条件 logits —— 模型想说 "Ada Lovelace"，文法只许 [a-z]+ ----
    # 这次的 logits 不是死板脚本，而是一个随前缀重算的迷你"条件模型"：
    # 它心里有一句完整的目标输出，每步给出"最想接着打的字符 + 若干次选"。
    # 真实模型正是如此：logits 是 P(next|prefix)，前缀被掩码改变后，
    # 分布会自动重新规划续写——这是掩码通常不会毁掉输出的根本原因。
    def make_intent_model(intent: str):
        def row(t, emitted):
            low_e, low_i = emitted.lower(), intent.lower()
            i = 0
            for ch in low_e:        # 贪心对齐：已表达到了 intent 的哪个位置
                while i < len(low_i) and low_i[i] != ch:
                    i += 1
                i += 1
            if i >= len(intent):
                return None         # 意图表达完毕 -> 相当于 EOS
            prefs, score, j = {}, 9.0, i
            while j < len(intent) and len(prefs) < 4:
                for cand in (intent[j], intent[j].lower()):
                    if cand and cand not in prefs:
                        prefs[cand] = score
                        score -= 1.0
                j += 1
            return prefs
        return row

    # 迷你模型偏好单字符（每步 9.0），完整输出约 35 步，剧本给足余量
    ada = [make_intent_model('{"name": "Ada Lovelace", "age": 30}')] * 45
    print("\n" + "-" * 76)
    print("【实验 C】模型想说 'Ada Lovelace'，但文法只允许 [a-z]+")
    decode(ada, masked=False, label="C-无掩码")
    decode(ada, masked=True, label="C-有掩码")

    print("\n" + "=" * 76)
    print("结论：")
    print("  1) 掩码开 -> 非法输出在数学上不可能产生。这不是'模型更努力了'，")
    print("     而是非法 token 根本进不了采样池（真实实现是把 logit 置 -inf）。")
    print("  2) 文法分叉处（空格可有可无、数字写几位、何时收 '}'）依然是模型在")
    print("     选择——文法划定菜单，模型在菜单内点菜。")
    print("  3) 实验C 是代价的诚实展示：语法被保证，语义可能被扭（Ada Lovelace")
    print("     -> adalovelace）。文法设计过紧时，掩蔽掉的是模型的意图。")
    print("     掩码保证的是'能被解析'，不保证'是 你想要的'。")
    print("  4) 解剖一节就是 XGrammar 解决的问题缩影：token 与字符粒度不一致，")
    print("     需要把词表和文法自动机求交（部分合法的合并 token 必须整体作废）。")


if __name__ == "__main__":
    main()
