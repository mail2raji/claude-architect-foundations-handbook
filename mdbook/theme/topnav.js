// Inject a horizontal nav bar at the top of every page.
// Reads the current depth so links resolve correctly from /index.html,
// /ch01/index.html, /appendix-a/index.html, etc.
(function () {
  "use strict";

  // Don't insert twice if mdBook re-runs scripts during preview.
  if (document.getElementById("ccaf-topnav")) return;

  // depth = number of "../" hops needed to reach the site root.
  // mdBook sets the <html> "data-path-to-root" attribute via the template.
  // Fall back to deriving it from the URL pathname if not present.
  function pathToRoot() {
    var attr = document.documentElement.getAttribute("data-path-to-root");
    if (attr) return attr;
    var p = window.location.pathname.replace(/\/[^/]*$/, "/");
    // depth = number of slash-separated segments after the site root.
    // We can't know the site root cheaply, so we infer "deepness" from the
    // <base> href if mdBook left one. Default to "./".
    var base = document.querySelector("base");
    if (base && base.href) {
      try {
        var u = new URL(base.href);
        var here = new URL(window.location.href);
        var diff = here.pathname.replace(u.pathname, "").split("/").length - 1;
        return diff > 0 ? new Array(diff + 1).join("../") : "./";
      } catch (_) {
        return "./";
      }
    }
    return "./";
  }

  var root = pathToRoot();
  var repo = "https://github.com/mail2raji/claude-architect-foundations-handbook";

  var links = [
    { label: "🏠 Home",           href: root + "introduction.html" },
    { label: "📘 Preface",        href: root + "preface.html" },
    { label: "🧭 How to use",     href: root + "how-to-use.html" },
    { label: "1️⃣ Agents",        href: root + "ch01/index.html",     title: "Domain 1 — 27%" },
    { label: "2️⃣ Tools",         href: root + "ch02/index.html",     title: "Domain 2a — function calling" },
    { label: "🔌 MCP",            href: root + "ch03/index.html",     title: "Domain 2b — Model Context Protocol" },
    { label: "3️⃣ Claude Code",   href: root + "ch04/index.html",     title: "Domain 3 — 20%" },
    { label: "4️⃣ API",           href: root + "ch05/index.html",     title: "Domain 4a — foundations & API" },
    { label: "✍️ Prompts",        href: root + "ch06/index.html",     title: "Domain 4b — prompt engineering" },
    { label: "5️⃣ RAG",           href: root + "ch07/index.html",     title: "Domain 5 — 15%" },
    { label: "📝 Exam prep",      href: root + "appendix-a/index.html", title: "Appendices A–G" },
    { label: "🐙 Repo",           href: repo, external: true },
  ];

  var nav = document.createElement("nav");
  nav.id = "ccaf-topnav";
  nav.setAttribute("aria-label", "Domain navigation");

  var inner = document.createElement("div");
  inner.className = "ccaf-topnav-inner";

  links.forEach(function (l) {
    var a = document.createElement("a");
    a.href = l.href;
    a.textContent = l.label;
    if (l.title) a.title = l.title;
    if (l.external) {
      a.target = "_blank";
      a.rel = "noopener";
    }
    // Highlight the active chapter
    var hereFile = window.location.pathname.split("/").slice(-2).join("/");
    if (!l.external && l.href.indexOf(hereFile) !== -1 && hereFile !== "/") {
      a.classList.add("active");
    }
    inner.appendChild(a);
  });

  nav.appendChild(inner);

  // Insert just under mdBook's menu bar (.menu-bar) so it sits between
  // the top toolbar and the page content.
  var menuBar = document.querySelector(".menu-bar");
  var page = document.querySelector(".page-wrapper") || document.body;
  if (menuBar && menuBar.parentNode) {
    menuBar.parentNode.insertBefore(nav, menuBar.nextSibling);
  } else {
    page.insertBefore(nav, page.firstChild);
  }
})();
