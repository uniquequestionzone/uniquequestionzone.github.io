/*
 * Interaction fallback for Lumenboard website exports.
 *
 * The generated page also contains an inline runtime. This file intentionally
 * runs after it and only responds to clicks the inline runtime did not handle.
 * Keeping it as a real asset means downloaded/file:// pages still have working
 * controls if an inline script is blocked or interrupted by a browser.
 */
(function () {
  "use strict";

  function closest(element, selector) {
    while (element && element.nodeType === 1) {
      if (element.matches ? element.matches(selector) : false) return element;
      element = element.parentElement;
    }
    return null;
  }

  function fullscreenElement() {
    return document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement;
  }

  function requestFullscreen() {
    var root = document.documentElement;
    var request = root.requestFullscreen || root.webkitRequestFullscreen || root.mozRequestFullScreen || root.msRequestFullscreen;
    if (!request) return;
    try {
      var result = request.call(root);
      if (result && result.catch) result.catch(function () {});
    } catch (_) {}
  }

  function leaveFullscreen() {
    var leave = document.exitFullscreen || document.webkitExitFullscreen || document.mozCancelFullScreen || document.msExitFullscreen;
    if (!leave || !fullscreenElement()) return;
    try {
      var result = leave.call(document);
      if (result && result.catch) result.catch(function () {});
    } catch (_) {}
  }

  function setFocusNavigation(enabled) {
    document.querySelectorAll(".lumenboard-previous-page, .lumenboard-next-page").forEach(function (link) {
      if (!link.href || link.getAttribute("aria-disabled") === "true") return;
      try {
        var url = new URL(link.href, window.location.href);
        if (enabled) url.searchParams.set("focus", "1");
        else url.searchParams.delete("focus");
        link.href = url.pathname.split("/").pop() + url.search + url.hash;
      } catch (_) {}
    });
    try {
      if (enabled) sessionStorage.setItem("lumenboard_focus", "1");
      else sessionStorage.removeItem("lumenboard_focus");
    } catch (_) {}
  }

  function enterFocus() {
    document.body.classList.add("lumenboard-focus-mode");
    setFocusNavigation(true);
    requestFullscreen();
  }

  function exitFocus() {
    document.body.classList.remove("lumenboard-focus-mode");
    setFocusNavigation(false);
    leaveFullscreen();
  }

  function zoom(delta) {
    var scroll = document.querySelector(".lumenboard-diagram-scroll");
    if (!scroll) return;
    var diagram = scroll.querySelector(".lumenboard-diagram");
    if (!diagram) return;
    var stage = diagram.parentElement;
    if (!stage || !stage.classList.contains("lumenboard-zoom-stage")) {
      stage = document.createElement("div");
      stage.className = "lumenboard-zoom-stage";
      diagram.parentNode.insertBefore(stage, diagram);
      stage.appendChild(diagram);
    }
    if (!diagram.dataset.baseWidth) {
      diagram.dataset.baseWidth = String(parseFloat(diagram.style.width) || diagram.offsetWidth || 1);
      diagram.dataset.baseHeight = String(parseFloat(diagram.style.height) || diagram.offsetHeight || 1);
      diagram.style.transformOrigin = "top left";
    }
    var current = Number(diagram.dataset.zoom || "1");
    var next = Math.round(Math.max(0.3, Math.min(3.5, current + delta)) * 100) / 100;
    diagram.dataset.zoom = String(next);
    stage.style.width = (Number(diagram.dataset.baseWidth) * next) + "px";
    stage.style.height = (Number(diagram.dataset.baseHeight) * next) + "px";
    diagram.style.transform = "scale(" + next + ")";
  }

  function plainTextFromHtml(html) {
    var container = document.createElement("div");
    container.innerHTML = html;
    return (container.innerText || container.textContent || "")
      .replace(/\u00a0/g, " ")
      .replace(/\r/g, "")
      .replace(/\n{3,}/g, "\n\n")
      .trim();
  }

  function copyHtml(html, button) {
    var plain = plainTextFromHtml(html);
    var copied = false;
    var source = document.createElement("div");
    source.contentEditable = "true";
    source.setAttribute("aria-hidden", "true");
    source.style.cssText = "position:fixed;left:0;top:0;width:1px;height:1px;opacity:.01;overflow:hidden;z-index:-1";
    source.innerHTML = html;
    var selection = window.getSelection ? window.getSelection() : null;
    var onCopy = function (event) {
      if (!event.clipboardData) return;
      event.preventDefault();
      event.clipboardData.clearData();
      event.clipboardData.setData("text/html", html);
      event.clipboardData.setData("text/plain", plain);
      copied = true;
    };
    try {
      document.body.appendChild(source);
      if (selection) {
        var range = document.createRange();
        range.selectNodeContents(source);
        selection.removeAllRanges();
        selection.addRange(range);
      }
      document.addEventListener("copy", onCopy, true);
      copied = document.execCommand("copy") || copied;
    } catch (_) {
      // The Clipboard API below is available in secure contexts.
    } finally {
      document.removeEventListener("copy", onCopy, true);
      if (source.parentNode) source.parentNode.removeChild(source);
      if (selection) selection.removeAllRanges();
    }

    if (copied) showCopyResult(button, true);
    if (window.isSecureContext && navigator.clipboard && navigator.clipboard.write && window.ClipboardItem) {
      try {
        navigator.clipboard.write([new ClipboardItem({
          "text/html": new Blob([html], { type: "text/html" }),
          "text/plain": new Blob([plain], { type: "text/plain" })
        })]).then(function () {
          showCopyResult(button, true);
        }).catch(function () {
          if (!copied) showCopyResult(button, false);
        });
        return;
      } catch (_) {}
    }
    if (!copied) showCopyResult(button, false);
  }

  function showCopyResult(button, copied) {
    if (!button) return;
    button.setAttribute("title", copied ? "Copied text with formatting" : "Copy was blocked by this browser");
    button.setAttribute("aria-label", copied ? "Copied text with formatting" : "Copy was blocked by this browser");
    if (!copied) return;
    button.classList.add("copied");
    var copyIcon = button.querySelector(".copy-icon");
    var checkIcon = button.querySelector(".check-icon");
    if (copyIcon) copyIcon.style.display = "none";
    if (checkIcon) checkIcon.style.display = "block";
    window.setTimeout(function () {
      button.classList.remove("copied");
      if (copyIcon) copyIcon.style.display = "block";
      if (checkIcon) checkIcon.style.display = "none";
      button.setAttribute("title", "Copy text with formatting");
      button.setAttribute("aria-label", "Copy text with formatting");
    }, 1500);
  }

  document.addEventListener("click", function (event) {
    // A working inline runtime already calls preventDefault. Do not duplicate
    // its copy/fullscreen/zoom actions.
    if (event.defaultPrevented) return;
    var target = event.target;
    var enter = closest(target, "[data-lumenboard-enter-focus]");
    if (enter) {
      event.preventDefault();
      enterFocus();
      return;
    }
    var exit = closest(target, "[data-lumenboard-exit-focus]");
    if (exit) {
      event.preventDefault();
      exitFocus();
      return;
    }
    var zoomIn = closest(target, "[data-lumenboard-zoom-in]");
    if (zoomIn) {
      event.preventDefault();
      zoom(0.2);
      return;
    }
    var zoomOut = closest(target, "[data-lumenboard-zoom-out]");
    if (zoomOut) {
      event.preventDefault();
      zoom(-0.2);
      return;
    }
    var copyButton = closest(target, ".lumenboard-copy-btn");
    if (!copyButton) return;
    event.preventDefault();
    var payload = copyButton.getAttribute("data-copy-html") || "";
    if (!payload) {
      var template = copyButton.parentElement && copyButton.parentElement.querySelector("template");
      payload = template ? template.innerHTML : "";
    }
    if (payload) copyHtml(payload, copyButton);
  }, true);

  // The native Fullscreen API is deliberately not re-requested here: browsers
  // only permit that from a fresh user gesture. The full-screen lesson layout,
  // however, persists when a reader follows Previous/Next in an export.
  try {
    if (new URLSearchParams(window.location.search).get("focus") === "1" || sessionStorage.getItem("lumenboard_focus") === "1") {
      document.body.classList.add("lumenboard-focus-mode");
      setFocusNavigation(true);
    }
  } catch (_) {}
}());
