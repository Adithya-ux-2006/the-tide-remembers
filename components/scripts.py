"""Client-side behaviour: scroll choreography, chapter tracking, story player."""

from __future__ import annotations

import json

DWELL_MS = 6500


def get_scripts(entries: list[dict]) -> str:
    chapters = [
        {"n": e["chapter"], "title": e["title"], "caption": e["caption"]}
        for e in entries
    ]
    data = json.dumps(chapters, ensure_ascii=False).replace("</", "<\\/")
    return "<script>\n" + _JS.replace("__CHAPTERS__", data) + "\n</script>"


_JS = r"""
(function () {
  "use strict";
  var CHAPTERS = __CHAPTERS__;
  var DWELL = """ + str(DWELL_MS) + r""";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- reveal on scroll ---------------- */
  var revealIO = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add("in");
        revealIO.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -5% 0px" });
  $$(".reveal").forEach(function (el) { revealIO.observe(el); });

  /* ---------------- scroll: chrome, progress, parallax ---------------- */
  var topbar = $("#topbar");
  var fill = $("#progressFill");
  var parallaxEls = $$("[data-parallax]");
  var ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      var y = window.scrollY || document.documentElement.scrollTop;
      if (topbar) topbar.classList.toggle("scrolled", y > 40);
      var h = document.documentElement.scrollHeight - window.innerHeight;
      if (fill) fill.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + "%";
      if (!reduced) {
        var vh = window.innerHeight;
        parallaxEls.forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.bottom < -120 || r.top > vh + 120) return;
          var mid = r.top + r.height / 2 - vh / 2;
          var off = Math.max(-26, Math.min(26, -mid * 0.045));
          var media = el.querySelector(".frame-media");
          if (media) media.style.setProperty("--py", off.toFixed(1) + "px");
        });
      }
      ticking = false;
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  /* ---------------- active chapter tracking ---------------- */
  var tns = $$(".tn");
  var rails = $$(".rail-item");
  var ticks = $$(".si-tick");

  function setActive(i) {
    tns.forEach(function (b) { b.classList.toggle("active", +b.dataset.goto === i); });
    rails.forEach(function (b) { b.classList.toggle("active", +b.dataset.goto === i); });
    ticks.forEach(function (b) { b.classList.toggle("on", +b.dataset.goto === i); });
  }

  var chapterIO = new IntersectionObserver(function (list) {
    list.forEach(function (e) {
      if (e.isIntersecting) setActive(+e.target.dataset.chapter);
    });
  }, { rootMargin: "-42% 0px -42% 0px", threshold: 0 });
  $$(".chapter").forEach(function (c) { chapterIO.observe(c); });

  /* ---------------- story mode ---------------- */
  var story = $("#story");
  var slides = $$(".story-slide");
  var bars = $$(".sbar");
  var fills = $$(".sbar-fill");
  var center = $("#storyCenter");
  var elChap = $("#storyChap");
  var elTitle = $("#storyTitle");
  var elText = $("#storyText");
  var elIdx = $("#storyIndex");
  var endCard = $("#storyEnd");
  var btnToggle = $("[data-s-toggle]");

  var ICON_PLAY = '<svg viewBox="0 0 12 14" xmlns="http://www.w3.org/2000/svg" fill="currentColor" aria-hidden="true"><path d="M0 0v14l12-7L0 0Z"/></svg>';
  var ICON_PAUSE = '<svg viewBox="0 0 12 14" xmlns="http://www.w3.org/2000/svg" fill="currentColor" aria-hidden="true"><path d="M0 0h3.6v14H0zM8.4 0H12v14H8.4z"/></svg>';

  var idx = 0, playing = false, opened = false, acc = 0, last = 0, raf = 0;

  function paint() {
    slides.forEach(function (s, i) { s.classList.toggle("active", i === idx); });
    var c = CHAPTERS[idx];
    elChap.textContent = "CHAPTER " + c.n;
    elTitle.textContent = c.title;
    elText.textContent = c.caption;
    elIdx.textContent = c.n;
    center.classList.remove("anim");
    void center.offsetWidth;
    center.classList.add("anim");
    var img = slides[idx].querySelector(".story-img");
    if (img && !reduced) {
      img.style.animation = "none";
      void img.offsetWidth;
      img.style.animation = "";
    }
    fills.forEach(function (f, i) { f.style.width = i < idx ? "100%" : "0%"; });
    bars.forEach(function (b, i) { b.classList.toggle("done", i < idx); });
    acc = 0;
  }

  function loop(now) {
    if (!opened) { raf = 0; return; }
    var dt = Math.min(64, now - last);
    last = now;
    if (playing && !endCard.classList.contains("show")) {
      acc += dt;
      var p = Math.min(1, acc / DWELL);
      fills[idx].style.width = (p * 100).toFixed(2) + "%";
      if (p >= 1) next();
    }
    raf = requestAnimationFrame(loop);
  }

  function next() {
    if (idx >= CHAPTERS.length - 1) { finish(); return; }
    idx += 1;
    paint();
  }

  function prev() {
    if (idx <= 0) return;
    idx -= 1;
    paint();
  }

  function finish() {
    playing = false;
    endCard.classList.add("show");
    endCard.setAttribute("aria-hidden", "false");
  }

  function setPlaying(on) {
    playing = on;
    if (!btnToggle) return;
    btnToggle.innerHTML = on ? ICON_PAUSE : ICON_PLAY;
    btnToggle.setAttribute("aria-label", on ? "Pause" : "Play");
  }

  function openStory(start) {
    idx = Math.max(0, Math.min(CHAPTERS.length - 1, start || 0));
    opened = true;
    endCard.classList.remove("show");
    endCard.setAttribute("aria-hidden", "true");
    story.classList.add("open");
    story.setAttribute("aria-hidden", "false");
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
    paint();
    setPlaying(true);
    last = performance.now();
    if (!raf) raf = requestAnimationFrame(loop);
    var closeBtn = $("[data-story-close]");
    if (closeBtn) closeBtn.focus({ preventScroll: true });
  }

  function closeStory() {
    opened = false;
    setPlaying(false);
    story.classList.remove("open");
    story.setAttribute("aria-hidden", "true");
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
  }

  function gotoChapter(v) {
    var el = /^\d+$/.test(v) ? document.getElementById("chapter-" + v) : document.getElementById(v);
    if (el) el.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
  }

  /* ---------------- delegated interactions ---------------- */
  document.addEventListener("click", function (e) {
    var t;
    if ((t = e.target.closest("[data-goto]"))) {
      e.preventDefault();
      gotoChapter(t.dataset.goto);
      return;
    }
    if (e.target.closest("[data-play-story]")) { openStory(0); return; }
    if (e.target.closest("[data-story-close]")) { closeStory(); return; }
    if (e.target.closest("[data-s-next]")) { next(); return; }
    if (e.target.closest("[data-s-prev]")) { prev(); return; }
    if (e.target.closest("[data-s-toggle]")) {
      if (endCard.classList.contains("show")) return;
      setPlaying(!playing);
      return;
    }
    if (e.target.closest("[data-s-replay]")) {
      idx = 0;
      endCard.classList.remove("show");
      endCard.setAttribute("aria-hidden", "true");
      paint();
      setPlaying(true);
      return;
    }
    if (e.target.closest("[data-s-explore]")) {
      closeStory();
      setTimeout(function () { gotoChapter("diary"); }, 380);
    }
  });

  document.addEventListener("keydown", function (e) {
    if (!opened) return;
    if (e.key === "Escape") { closeStory(); return; }
    if (e.key === "ArrowRight") { next(); return; }
    if (e.key === "ArrowLeft") { prev(); return; }
    if (e.key === " " || e.code === "Space") {
      e.preventDefault();
      if (!endCard.classList.contains("show")) setPlaying(!playing);
    }
  });

  /* small hooks used by automated visual tests */
  window.tideStory = { open: openStory, close: closeStory, end: finish };
})();
"""
