/* ============================================================
   Engineering AI Agents · 课程站共享脚本
   职责：课程清单（唯一事实源）、顶栏/页脚渲染、主题切换、学习进度
   进度存储：localStorage key = "eaia-progress"（JSON 数组，元素为讲次 id）
   ============================================================ */

window.COURSE = {
  title: "Engineering AI Agents · 交互式课程",
  source: "斯坦福 CS329Z（Diyi Yang / Michael Ryan / John Yang）讲义的学习演绎",
  phases: [
    { id: "p1", name: "① 入口 · 全景" },
    { id: "p2", name: "② 组件 · 单个 agent 的器官" },
    { id: "p3", name: "③ 组织 · 让 agent 可靠运转" },
    { id: "p4", name: "④ 群体 · agent 社会" },
  ],
  lectures: [
    {
      id: "l01", num: "L01", phase: "p1", status: "ready", mins: 35,
      title: "Agent 是什么：一个循环的五十年",
      desc: "同一道题、三种接线：控制流的归属如何决定成败；解剖图与四大挑战。",
    },
    { id: "l02", num: "L02", phase: "p2", status: "soon",
      title: "LLM 作为建筑材料",
      desc: "概率采样机、上下文窗口、成本结构：动手前必须懂的物理性质。" },
    { id: "l03", num: "L03", phase: "p2", status: "soon",
      title: "RAG：外挂知识器官",
      desc: "检索 → 增强 → 生成，以及它如何天然成为 agent 的第一个工具。" },
    { id: "l04", num: "L04", phase: "p2", status: "soon",
      title: "工具使用：从会说到会做",
      desc: "结构化输出与函数调用协议（已可先玩配套实验室 lab01）。" },
    { id: "l05", num: "L05", phase: "p3", status: "soon",
      title: "框架与编排：看穿打包术",
      desc: "框架到底替你做了什么；用不用框架，是一道架构决策题。" },
    { id: "l06", num: "L06", phase: "p3", status: "soon",
      title: "设计模式与脚手架",
      desc: "ReAct、Reflexion、规划-执行：被实践验证过的循环形状。" },
    { id: "l07", num: "L07", phase: "p3", status: "soon",
      title: "记忆架构",
      desc: "上下文窗口 ≠ 记忆：存什么、怎么压缩、何时取回的工程系统。" },
    { id: "l08", num: "L08", phase: "p4", status: "soon",
      title: "多智能体系统",
      desc: "分工、通信与失控成本：本质是组织设计问题。" },
  ],
  labs: [
    {
      num: "Lab 01", tag: "配套 L04 / L06",
      title: "Structured I/O 实验室",
      desc: "从裸接口失败动物园，到正则→NFA→掩码解码，再到函数调用协议与最小 agent 闭环。浏览器双击即玩。",
      path: "../labs/01-structured-io/structured-io-lab.html",
    },
  ],
};

(function () {
  /* ---------- 主题 ---------- */
  var savedTheme = null;
  try { savedTheme = localStorage.getItem("eaia-theme"); } catch (e) {}
  if (savedTheme) document.documentElement.dataset.theme = savedTheme;

  window.toggleTheme = function () {
    var cur = document.documentElement.dataset.theme ||
      (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    var next = cur === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem("eaia-theme", next); } catch (e) {}
  };

  /* ---------- 进度 ---------- */
  function getProgress() {
    try { return JSON.parse(localStorage.getItem("eaia-progress") || "[]"); } catch (e) { return []; }
  }
  window.COURSE.getProgress = getProgress;
  window.COURSE.isDone = function (id) { return getProgress().indexOf(id) >= 0; };
  window.COURSE.markDone = function (id, on) {
    var p = getProgress();
    var i = p.indexOf(id);
    if (on && i < 0) p.push(id);
    if (!on && i >= 0) p.splice(i, 1);
    try { localStorage.setItem("eaia-progress", JSON.stringify(p)); } catch (e) {}
  };

  /* ---------- 顶栏 ---------- */
  var head = document.getElementById("site-head");
  if (head && head.tagName === "DIV") {
    var isLesson = !!document.body.dataset.page;
    head.className = "site-head";
    head.innerHTML =
      '<div class="inner">' +
      (isLesson
        ? '<a class="back" href="../index.html">← 课程地图</a>'
        : "") +
      '<span class="brand"><a href="' + (isLesson ? "../index.html" : "index.html") + '">Engineering AI Agents</a></span>' +
      '<span class="spacer"></span>' +
      '<button class="theme-btn" onclick="toggleTheme()" type="button">◐ 主题</button>' +
      "</div>";
  }

  /* ---------- 讲次页：页脚导航 + 完成按钮 ---------- */
  var pageId = document.body.dataset.page;
  if (pageId) {
    var ls = window.COURSE.lectures;
    var idx = -1;
    for (var i = 0; i < ls.length; i++) if (ls[i].id === pageId) idx = i;
    if (idx >= 0) {
      var prev = ls[idx - 1], next = ls[idx + 1];
      var nav = document.createElement("div");
      nav.className = "lesson-nav";
      nav.innerHTML =
        (prev
          ? '<a href="../' + prev.id + '/index.html"><div class="dir">← 上一讲</div><div class="t">' + prev.num + " · " + prev.title + "</div></a>"
          : "<span></span>") +
        (next
          ? (next.status === "ready"
              ? '<a class="next" href="../' + next.id + '/index.html"><div class="dir">下一讲 →</div><div class="t">' + next.num + " · " + next.title + "</div></a>"
              : '<div class="next lesson-card soon" style="cursor:default;"><div class="dir">下一讲 · 即将上线</div><div class="t">' + next.num + " · " + next.title + "</div></div>")
          : "<span></span>");
      var main = document.querySelector("main");
      if (main) main.appendChild(nav);
    }

    var doneBtn = document.getElementById("mark-done");
    if (doneBtn) {
      var refresh = function () {
        var done = window.COURSE.isDone(pageId);
        doneBtn.textContent = done ? "✓ 已学完（点击撤销）" : "✓ 标记本讲已学完";
        doneBtn.classList.toggle("btn-primary", !done);
      };
      doneBtn.addEventListener("click", function () {
        window.COURSE.markDone(pageId, !window.COURSE.isDone(pageId));
        refresh();
      });
      refresh();
    }
  }

  /* ---------- 首页：hero CTA 与进度联动（当前位置可见性） ---------- */
  var doneIds = getProgress();
  var heroCta = document.getElementById("hero-cta");
  if (heroCta) {
    var readyLs = window.COURSE.lectures.filter(function (l) { return l.status === "ready"; });
    var nextL = null;
    for (var k = 0; k < readyLs.length; k++) {
      if (doneIds.indexOf(readyLs[k].id) < 0) { nextL = readyLs[k]; break; }
    }
    if (nextL) {
      var started = readyLs.some(function (l) { return doneIds.indexOf(l.id) >= 0; });
      heroCta.textContent = started ? "继续学习 " + nextL.num + " →" : "从 " + nextL.num + " 开始 →";
      heroCta.setAttribute("href", nextL.id + "/index.html");
    } else {
      heroCta.textContent = "✓ 已学完全部已上线讲次";
      heroCta.removeAttribute("href");
      heroCta.style.opacity = "0.75";
      heroCta.style.cursor = "default";
    }
  }

  /* ---------- 讲次页：本讲结构目录 scrollspy（当前位置可见性） ---------- */
  var toc = document.querySelector(".lesson-toc");
  if (toc) {
    var links = Array.prototype.slice.call(toc.querySelectorAll(".toc-link"));
    var pairs = links
      .map(function (a) {
        var sel = a.getAttribute("href") || "";
        var sec = sel.charAt(0) === "#" ? document.getElementById(sel.slice(1)) : null;
        return sec ? { a: a, sec: sec } : null;
      })
      .filter(Boolean);
    var setActive = function (id) {
      pairs.forEach(function (p) { p.a.setAttribute("aria-pressed", p.sec.id === id ? "true" : "false"); });
    };
    var lock = null; // 点击目录后短暂锁定目标，避免平滑滚动途中高亮闪烁
    var update = function () {
      var line = window.innerHeight * 0.25;
      var cur = pairs[0].sec.id;
      for (var i = 0; i < pairs.length; i++) {
        if (pairs[i].sec.getBoundingClientRect().top <= line) cur = pairs[i].sec.id;
      }
      // 页底规则：滚到底时最后一项必然是当前位置（末尾区块顶部到不了参考线）
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
        cur = pairs[pairs.length - 1].sec.id;
      }
      if (lock) {
        if (Date.now() < lock.until) cur = lock.id;
        else lock = null;
      }
      setActive(cur);
    };
    links.forEach(function (a) {
      a.addEventListener("click", function () {
        var sel = (a.getAttribute("href") || "").slice(1);
        var hit = pairs.filter(function (p) { return p.sec.id === sel; })[0];
        if (hit) lock = { id: hit.sec.id, until: Date.now() + 1600 };
      });
    });
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  /* ---------- 首页：静态卡片的进度增强（渐进增强：无 JS 时卡片本身完整可用） ---------- */
  var mapRoot = document.getElementById("course-map");
  if (mapRoot) {
    var cards = mapRoot.querySelectorAll(".lesson-card[data-id]");
    cards.forEach(function (card) {
      if (doneIds.indexOf(card.dataset.id) < 0) return;
      var pill = card.querySelector(".pill");
      if (pill) { pill.className = "pill done"; pill.textContent = "已完成 ✓"; }
      var meta = card.querySelector(".lc-meta");
      if (meta) meta.textContent += " · 已完成 ✓";
    });
  }

  var progRoot = document.getElementById("progress-line");
  if (progRoot) {
    var ready = window.COURSE.lectures.filter(function (l) { return l.status === "ready"; }).length;
    var doneCount = window.COURSE.lectures.filter(function (l) {
      return l.status === "ready" && doneIds.indexOf(l.id) >= 0;
    }).length;
    var pct = ready ? Math.round((doneCount / ready) * 100) : 0;
    progRoot.innerHTML =
      '<div class="progress-track"><div class="progress-fill" style="width:' + pct + '%"></div></div>' +
      '<span class="pill">' + doneCount + " / " + ready + " 讲已完成</span>";
  }
})();
