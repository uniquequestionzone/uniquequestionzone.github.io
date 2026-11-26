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

  var lumenboardSpeech = (function () {
    var synth = window.speechSynthesis;
    var SpeechUtterance = window.SpeechSynthesisUtterance || window.webkitSpeechSynthesisUtterance || (typeof SpeechSynthesisUtterance !== "undefined" ? SpeechSynthesisUtterance : null);
    var currentToken = 0;
    var currentBtn = null;
    var currentPicker = null;
    var currentVoiceName = "";
    var wakeInterval = null;
    window._lumenboardUtterances = window._lumenboardUtterances || [];

    function getVoices() {
      if (!synth || !synth.getVoices) return [];
      try {
        var list = synth.getVoices() || [];
        return Array.prototype.slice.call(list);
      } catch (_) {
        return [];
      }
    }

    function pickBestVoice(voices, preferredName) {
      if (!voices || !voices.length) return null;
      if (preferredName) {
        for (var i = 0; i < voices.length; i++) {
          if (voices[i].name === preferredName) return voices[i];
        }
      }
      var langPref = (navigator.language || "en").slice(0, 2).toLowerCase();
      for (var a = 0; a < voices.length; a++) {
        var v = voices[a];
        var vLang = (v.lang || "").slice(0, 2).toLowerCase();
        var vName = (v.name || "").toLowerCase();
        if (vLang === langPref && (vName.indexOf("natural") >= 0 || vName.indexOf("neural") >= 0 || vName.indexOf("online") >= 0)) {
          return v;
        }
      }
      for (var b = 0; b < voices.length; b++) {
        var vb = voices[b];
        var vbLang = (vb.lang || "").slice(0, 2).toLowerCase();
        if (vbLang === langPref && vb.localService) {
          return vb;
        }
      }
      for (var c = 0; c < voices.length; c++) {
        var vc = voices[c];
        var vcLang = (vc.lang || "").slice(0, 2).toLowerCase();
        if (vcLang === langPref) return vc;
      }
      for (var d = 0; d < voices.length; d++) {
        if (voices[d].localService) return voices[d];
      }
      return voices[0] || null;
    }

    function setListenButtonState(btn, isReading) {
      if (!btn) return;
      btn.classList.toggle("reading", isReading);
      var listenIcon = btn.querySelector(".listen-icon");
      var stopIcon = btn.querySelector(".stop-icon");
      if (listenIcon) listenIcon.style.display = isReading ? "none" : "block";
      if (stopIcon) stopIcon.style.display = isReading ? "block" : "none";
      btn.setAttribute("aria-label", isReading ? "Stop reading" : "Listen to text");
      btn.setAttribute("title", isReading ? "Stop reading" : "Listen to text");
    }

    function populateVoicePicker(btn, selectedVoiceName) {
      var wrapper = btn && closest(btn, ".lumenboard-copy-wrapper");
      var picker = wrapper && wrapper.querySelector(".lumenboard-voice-picker");
      var select = picker && picker.querySelector(".lumenboard-voice-select");
      if (!picker || !select) return;

      var voices = getVoices();
      var currentVal = selectedVoiceName !== undefined ? selectedVoiceName : (select.value || currentVoiceName || "");

      select.innerHTML = "";
      var defaultOpt = document.createElement("option");
      defaultOpt.value = "";
      defaultOpt.textContent = "Human explanation";
      select.appendChild(defaultOpt);

      var bestVoice = pickBestVoice(voices, currentVal);
      var foundSelected = false;

      voices.forEach(function (voice) {
        var opt = document.createElement("option");
        opt.value = voice.name;
        var cleanName = voice.name
          .replace(/^Microsoft\s+/i, "")
          .replace(/^Google\s+/i, "")
          .replace(/\s+Online\s+\(Natural\)/i, " (Natural)")
          .replace(/\s+Desktop/i, "");
        var langTag = voice.lang ? " [" + voice.lang.split("-")[0].toUpperCase() + "]" : "";
        opt.textContent = cleanName + langTag;
        if (voice.name === currentVal || (!currentVal && bestVoice && voice.name === bestVoice.name)) {
          opt.selected = true;
          foundSelected = true;
        }
        select.appendChild(opt);
      });

      if (!foundSelected && defaultOpt) defaultOpt.selected = true;
      picker.hidden = false;
      currentPicker = picker;
    }

    function splitIntoSentences(text) {
      if (!text) return [];
      var clean = text.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
      var chunks = [];
      var current = "";
      for (var i = 0; i < clean.length; i++) {
        var ch = clean[i];
        current += ch;
        if (ch === "." || ch === "!" || ch === "?" || ch === "\n" || ch === ":") {
          var trimmed = current.trim();
          if (trimmed.length > 0) chunks.push(trimmed);
          current = "";
        } else if (current.length > 140 && (ch === "," || ch === ";")) {
          var tPart = current.trim();
          if (tPart.length > 0) chunks.push(tPart);
          current = "";
        }
      }
      var remainder = current.trim();
      if (remainder.length > 0) chunks.push(remainder);
      return chunks.length ? chunks : [clean.trim()];
    }

    function stop() {
      currentToken += 1;
      if (wakeInterval) {
        clearInterval(wakeInterval);
        wakeInterval = null;
      }
      if (synth) {
        try { synth.cancel(); } catch (_) {}
      }
      window._lumenboardUtterances = [];
      if (currentBtn) setListenButtonState(currentBtn, false);
      if (currentPicker) currentPicker.hidden = true;
      currentBtn = null;
      currentPicker = null;
    }

    function play(btn, chosenVoiceName) {
      if (!synth || !SpeechUtterance) {
        btn.setAttribute("title", "Text-to-speech is not available in this browser");
        btn.setAttribute("aria-label", "Text-to-speech is not available in this browser");
        setTimeout(function () { setListenButtonState(btn, false); }, 2200);
        return;
      }

      var payload = btn.getAttribute("data-copy-html") || "";
      if (!payload) {
        var wrapper = closest(btn, ".lumenboard-copy-wrapper");
        var template = wrapper ? wrapper.querySelector("template") : null;
        payload = template ? template.innerHTML : "";
      }
      var plain = plainTextFromHtml(payload);
      if (!plain) return;

      var sentences = splitIntoSentences(plain);
      if (!sentences.length) return;

      var token = ++currentToken;

      try {
        if (synth.speaking || synth.pending) {
          synth.cancel();
        }
      } catch (_) {}

      if (currentBtn && currentBtn !== btn) {
        setListenButtonState(currentBtn, false);
        if (currentPicker) currentPicker.hidden = true;
      }

      currentBtn = btn;
      currentVoiceName = chosenVoiceName || currentVoiceName || "";
      setListenButtonState(btn, true);
      populateVoicePicker(btn, chosenVoiceName);

      if (wakeInterval) clearInterval(wakeInterval);
      wakeInterval = setInterval(function () {
        if (token !== currentToken) {
          clearInterval(wakeInterval);
          return;
        }
        try {
          if (synth && synth.paused) synth.resume();
        } catch (_) {}
      }, 4000);

      var voices = getVoices();
      var voiceToUse = pickBestVoice(voices, chosenVoiceName);
      var sentenceIndex = 0;

      function speakNext() {
        if (token !== currentToken) return;
        if (sentenceIndex >= sentences.length) {
          stop();
          return;
        }

        var textChunk = sentences[sentenceIndex++];
        var utterance = new SpeechUtterance(textChunk);
        utterance.rate = 0.93;
        utterance.pitch = 1.0;
        if (voiceToUse) utterance.voice = voiceToUse;

        window._lumenboardUtterances.push(utterance);

        utterance.onstart = function () {
          if (token !== currentToken) return;
          setListenButtonState(btn, true);
          try {
            if (synth && synth.paused) synth.resume();
          } catch (_) {}
        };

        utterance.onend = function () {
          var idx = window._lumenboardUtterances.indexOf(utterance);
          if (idx >= 0) window._lumenboardUtterances.splice(idx, 1);
          if (token !== currentToken) return;
          setTimeout(function () {
            if (token === currentToken) speakNext();
          }, 120);
        };

        utterance.onerror = function (ev) {
          var idx = window._lumenboardUtterances.indexOf(utterance);
          if (idx >= 0) window._lumenboardUtterances.splice(idx, 1);

          if (ev && (ev.error === "interrupted" || ev.error === "canceled")) return;

          if (ev && (ev.error === "network" || ev.error === "synthesis-failed") && utterance.voice) {
            utterance.voice = null;
            try {
              synth.speak(utterance);
              return;
            } catch (_) {}
          }

          if (token !== currentToken) return;

          if (sentenceIndex < sentences.length) {
            speakNext();
          } else {
            stop();
          }
        };

        try {
          if (synth && synth.paused) synth.resume();
          synth.speak(utterance);
          setTimeout(function () {
            if (token === currentToken) {
              try { if (synth && synth.paused) synth.resume(); } catch (_) {}
            }
          }, 200);
        } catch (_) {
          utterance.onerror({ error: "speak_exception" });
        }
      }

      setTimeout(function () {
        if (token === currentToken) {
          try { if (synth && synth.paused) synth.resume(); } catch (_) {}
          speakNext();
        }
      }, 40);
    }

    return {
      play: play,
      stop: stop,
      isPlaying: function (btn) {
        return currentBtn === btn && Boolean(btn && btn.classList.contains("reading"));
      },
      populateVoicePicker: populateVoicePicker,
      getVoices: getVoices
    };
  })();

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
    var listenButton = closest(target, ".lumenboard-listen-btn");
    if (listenButton) {
      event.preventDefault();
      if (lumenboardSpeech.isPlaying(listenButton)) {
        lumenboardSpeech.stop();
      } else {
        lumenboardSpeech.play(listenButton);
      }
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

  document.addEventListener("change", function (event) {
    if (event.defaultPrevented) return;
    var select = closest(event.target, ".lumenboard-voice-select");
    if (!select) return;
    var wrapper = closest(select, ".lumenboard-copy-wrapper");
    var listenBtn = wrapper && wrapper.querySelector(".lumenboard-listen-btn");
    if (listenBtn) {
      lumenboardSpeech.play(listenBtn, select.value);
    }
  }, true);

  if (window.speechSynthesis) {
    try { window.speechSynthesis.getVoices(); } catch (_) {}
    var onVoicesChanged = function () {
      var readingBtn = document.querySelector(".lumenboard-listen-btn.reading");
      if (readingBtn) lumenboardSpeech.populateVoicePicker(readingBtn);
    };
    if (window.speechSynthesis.addEventListener) {
      window.speechSynthesis.addEventListener("voiceschanged", onVoicesChanged);
    } else {
      window.speechSynthesis.onvoiceschanged = onVoicesChanged;
    }
  }

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
