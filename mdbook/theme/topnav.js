// Inject a horizontal nav bar + per-chapter "domain badge" on every page.
// Labels match the cert exam-domain folder names so the site mirrors the repo.
(function () {
  "use strict";
  if (document.getElementById("ccaf-topnav")) return;

  // ---------- 1. Compute relative path to site root ----------
  function pathToRoot() {
    var attr = document.documentElement.getAttribute("data-path-to-root");
    if (attr) return attr;
    var base = document.querySelector("base");
    if (base && base.href) {
      try {
        var u = new URL(base.href);
        var here = new URL(window.location.href);
        var diff = here.pathname.replace(u.pathname, "").split("/").length - 1;
        return diff > 0 ? new Array(diff + 1).join("../") : "./";
      } catch (_) { return "./"; }
    }
    return "./";
  }

  var root = pathToRoot();
  var repo = "https://github.com/mail2raji/claude-architect-foundations-handbook";

  // ---------- 2. Chapter <-> folder map (one source of truth) ----------
  var CHAPTERS = [
    { id: "ch01", num: "1",  short: "Domain 1 \u00b7 Agents",       weight: "27%", folder: "Domain1_AgentArchitecture_27pct"                                          },
    { id: "ch02", num: "2a", short: "Domain 2a \u00b7 Tool Use",    weight: "",    folder: "Domain2_ToolDesign_MCP_18pct/tool_use"                                    },
    { id: "ch03", num: "2b", short: "Domain 2b \u00b7 MCP",         weight: "18%", folder: "Domain2_ToolDesign_MCP_18pct/mcp"                                         },
    { id: "ch04", num: "3",  short: "Domain 3 \u00b7 Claude Code",  weight: "20%", folder: "Domain3_ClaudeCode_Workflows_20pct"                                       },
    { id: "ch05", num: "4a", short: "Domain 4a \u00b7 API",         weight: "",    folder: "Domain4_PromptEngineering_StructuredOutput_20pct/api_basics"              },
    { id: "ch06", num: "4b", short: "Domain 4b \u00b7 Prompts",     weight: "20%", folder: "Domain4_PromptEngineering_StructuredOutput_20pct/prompt_engineering"      },
    { id: "ch07", num: "5",  short: "Domain 5 \u00b7 RAG",          weight: "15%", folder: "Domain5_ContextMgmt_Reliability_15pct"                                    }
  ];

  // Top-bar groups one entry per cert domain (Domain 1..5). Domains 2 and 4 each
  // contain two chapters on the site; the top-bar button opens the first one and
  // the sidebar exposes the second (sub-chapter).
  var DOMAINS = [
    { label: "Domain 1", chapterId: "ch01", title: "Agent Architecture & Orchestration (27%)" },
    { label: "Domain 2", chapterId: "ch02", title: "Tool Design & MCP (18%) \u2014 Tool Use + MCP" },
    { label: "Domain 3", chapterId: "ch04", title: "Claude Code Configuration & Workflows (20%)" },
    { label: "Domain 4", chapterId: "ch05", title: "Prompt Engineering & Structured Output (20%) \u2014 API + Prompts" },
    { label: "Domain 5", chapterId: "ch07", title: "Context Management & Retrieval / RAG (15%)" }
  ];

  // ---------- 3. Build the top nav ----------
  var navLinks = [
    { label: "\ud83c\udfe0 Home",       href: root + "introduction.html" },
    { label: "\ud83d\udcd8 Preface",    href: root + "preface.html" },
    { label: "\ud83e\udded How to use", href: root + "how-to-use.html" }
  ];
  DOMAINS.forEach(function (d) {
    navLinks.push({
      label: d.label,
      href: root + d.chapterId + "/index.html",
      title: d.title
    });
  });
  navLinks.push({ label: "\ud83d\udcdd Exam prep", href: root + "appendix-a/index.html", title: "Appendices A\u2013G" });
  navLinks.push({ label: "\ud83d\udc19 Repo",      href: repo, external: true });

  var nav = document.createElement("nav");
  nav.id = "ccaf-topnav";
  nav.setAttribute("aria-label", "Domain navigation");
  var inner = document.createElement("div");
  inner.className = "ccaf-topnav-inner";

  var hereFile = window.location.pathname.split("/").slice(-2).join("/");
  navLinks.forEach(function (l) {
    var a = document.createElement("a");
    a.href = l.href;
    a.textContent = l.label;
    if (l.title) a.title = l.title;
    if (l.external) { a.target = "_blank"; a.rel = "noopener"; }
    if (!l.external && l.href.indexOf(hereFile) !== -1 && hereFile !== "/") {
      a.classList.add("active");
    }
    inner.appendChild(a);
  });
  nav.appendChild(inner);

  var menuBar = document.querySelector(".menu-bar");
  var page = document.querySelector(".page-wrapper") || document.body;
  if (menuBar && menuBar.parentNode) {
    menuBar.parentNode.insertBefore(nav, menuBar.nextSibling);
  } else {
    page.insertBefore(nav, page.firstChild);
  }

  // ---------- 4. Inject per-chapter domain badge ----------
  var match = window.location.pathname.match(/\/(ch\d{2})\//);
  var current = null;
  if (match) {
    var id = match[1];
    for (var i = 0; i < CHAPTERS.length; i++) {
      if (CHAPTERS[i].id === id) { current = CHAPTERS[i]; break; }
    }
  }
  if (current) {
    var content = document.querySelector(".content main") || document.querySelector("main");
    if (content) {
      var badge = document.createElement("div");
      badge.className = "ccaf-domain-badge";
      badge.innerHTML =
        '<span class="ccaf-badge-num">Domain ' + current.num + '</span>' +
        '<span class="ccaf-badge-sep">\u00b7</span>' +
        '<a class="ccaf-badge-folder" href="' + repo + '/tree/main/' + current.folder + '" target="_blank" rel="noopener" title="Open this folder on GitHub">' +
          current.folder.replace("/", " / ") +
        '</a>' +
        (current.weight ? '<span class="ccaf-badge-weight">' + current.weight + '</span>' : '');
      content.insertBefore(badge, content.firstChild);
    }
  }

  var amatch = window.location.pathname.match(/\/appendix-([a-g])\//);
  if (amatch) {
    var content2 = document.querySelector(".content main") || document.querySelector("main");
    if (content2) {
      var bd = document.createElement("div");
      bd.className = "ccaf-domain-badge ccaf-domain-badge-appendix";
      bd.innerHTML =
        '<span class="ccaf-badge-num">Appendix ' + amatch[1].toUpperCase() + '</span>' +
        '<span class="ccaf-badge-sep">\u00b7</span>' +
        '<span class="ccaf-badge-folder">Exam prep</span>';
      content2.insertBefore(bd, content2.firstChild);
    }
  }
})();
