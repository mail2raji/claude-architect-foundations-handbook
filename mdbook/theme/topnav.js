// Inject a horizontal nav bar + per-chapter "domain badge" on every page.
// Labels match the cert exam-domain folder names so the site mirrors the repo.
(function () {
  "use strict";
  if (document.getElementById("ccaf-topnav")) return;

  // ---------- 1. Compute relative path to site root ----------
  // mdBook exposes a global `path_to_root` variable (set in head template) on
  // every page. It's already a correct relative path like "" or "../" or
  // "../../". Prefer it over any heuristic. Fall back to deriving from the
  // current URL only as a last resort.
  function pathToRoot() {
    try {
      if (typeof path_to_root === "string") return path_to_root || "./";
    } catch (_) { /* not defined */ }
    if (typeof window !== "undefined" && typeof window.path_to_root === "string") {
      return window.path_to_root || "./";
    }
    var attr = document.documentElement.getAttribute("data-path-to-root");
    if (attr) return attr;
    // Derive from URL: assume site root is the GitHub Pages project path
    // (everything up to and including the repo name). Count remaining path
    // segments (excluding trailing index.html or empty) to determine depth.
    try {
      var parts = window.location.pathname.split("/").filter(function (s) { return s.length > 0; });
      // For project pages the first segment is the repo name; drop it.
      // For user/org sites we'd want depth from root, but this site is a
      // project page so dropping one segment is correct.
      if (parts.length > 0) parts.shift();
      // If the last segment looks like a file, drop it.
      if (parts.length > 0 && /\.[a-zA-Z0-9]+$/.test(parts[parts.length - 1])) parts.pop();
      var depth = parts.length;
      return depth > 0 ? new Array(depth + 1).join("../") : "./";
    } catch (_) { return "./"; }
  }

  var root = pathToRoot();
  var repo = "https://github.com/mail2raji/claude-architect-foundations-handbook";

  // ---------- 2. Chapter <-> folder map (one source of truth) ----------
  var CHAPTERS = [
    { id: "ch01", num: "1", short: "Domain 1 \u00b7 Agents",      weight: "27%", folder: "Domain1_AgentArchitecture_27pct"                  },
    { id: "ch02", num: "2", short: "Domain 2 \u00b7 Tools + MCP", weight: "18%", folder: "Domain2_ToolDesign_MCP_18pct"                     },
    { id: "ch03", num: "3", short: "Domain 3 \u00b7 Claude Code", weight: "20%", folder: "Domain3_ClaudeCode_Workflows_20pct"               },
    { id: "ch04", num: "4", short: "Domain 4 \u00b7 Prompts/API", weight: "20%", folder: "Domain4_PromptEngineering_StructuredOutput_20pct" },
    { id: "ch05", num: "5", short: "Domain 5 \u00b7 RAG",         weight: "15%", folder: "Domain5_ContextMgmt_Reliability_15pct"            }
  ];

  // Top-bar groups one entry per cert domain (Domain 1..5). Each button maps
  // to the matching chapter (1:1 with the on-disk Domain*/ folder).
  var DOMAINS = [
    { label: "Domain 1", chapterId: "ch01", title: "Agent Architecture & Orchestration (27%)" },
    { label: "Domain 2", chapterId: "ch02", title: "Tool Design & MCP Integration (18%)" },
    { label: "Domain 3", chapterId: "ch03", title: "Claude Code Configuration & Workflows (20%)" },
    { label: "Domain 4", chapterId: "ch04", title: "Prompt Engineering & Structured Output (20%)" },
    { label: "Domain 5", chapterId: "ch05", title: "Context Management & Retrieval / RAG (15%)" }
  ];

  // ---------- 3. Build the top nav ----------
  var navLinks = [];
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
