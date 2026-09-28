"""The add / edit / delete memory dialog — markup plus its client behaviour.

The diary lives inside an iframe, so this module owns the two pieces of
client code that belong to *authoring* rather than to scrolling:

* ``window.tideMem`` — opens the dialog, validates the form and posts the
  finished memory back to Python through :func:`window.tideSend` (see
  :mod:`components.page` for the other half of that bridge);
* the diary index filters — search box, mood chips, empty state.
"""

from __future__ import annotations

import json
from html import escape

from components.svg import CLOSE_SVG, PLUS_SVG
from data.diary import MOODS

# The JSON the dialog needs to pre-fill the edit form. Kept tiny on purpose:
# the full entry is re-read from the store on save.
_MEM_TEMPLATE = r"""
<script>
window.__TIDE_MEM__ = __TIDE_MEM__;
</script>
"""

_JS = r"""
(function () {
  "use strict";
  var MEM = window.__TIDE_MEM__ || {};
  var modal = document.getElementById("memModal");
  if (!modal) return;

  var $ = function (s) { return modal.querySelector(s); };
  var card = $(".mm-form-card");
  var delCard = $(".mm-del-card");
  var kicker = document.getElementById("mmKicker");
  var heading = document.getElementById("mmHeading");
  var err = document.getElementById("mmError");
  var saveBtn = document.getElementById("mmSave");
  var delBtn = document.getElementById("mmDelGo");
  var delWhere = document.getElementById("mmDelWhere");

  var fTitle = document.getElementById("mmTitle");
  var fDate = document.getElementById("mmDate");
  var fPlace = document.getElementById("mmPlace");
  var fTags = document.getElementById("mmTags");
  var fMem = document.getElementById("mmMemory");
  var fStory = document.getElementById("mmStory");
  var file = document.getElementById("mmFile");
  var pick = document.getElementById("mmPick");
  var prev = document.getElementById("mmPrev");
  var prevImg = document.getElementById("mmPrevImg");
  var prevMeta = document.getElementById("mmPrevMeta");
  var clearBtn = document.getElementById("mmClearPhoto");
  var moods = modal.querySelectorAll(".mm-mood");

  /* ---------------- index: search + mood chips ---------------- */
  var search = document.getElementById("diarySearch");
  var list = document.getElementById("diaryList");
  var countEl = document.getElementById("diaryCount");
  var emptyEl = document.getElementById("diaryEmpty");
  var chips = document.querySelectorAll(".di-chip");
  var mood = "";

  function applyFilter() {
    if (!list) return;
    var q = (search && search.value || "").trim().toLowerCase();
    var rows = list.querySelectorAll(".di-row");
    var shown = 0;
    rows.forEach(function (row) {
      var ok = true;
      if (q && (row.dataset.search || "").indexOf(q) === -1) ok = false;
      if (ok && mood && (row.dataset.mood || "") !== mood) ok = false;
      row.hidden = !ok;
      if (ok) shown += 1;
    });
    /* hide season/month headings that have nothing under them any more */
    var kids = list.children;
    for (var i = 0; i < kids.length; i++) {
      var el = kids[i];
      if (el.classList.contains("di-year") || el.classList.contains("di-month")) {
        var visible = false;
        for (var j = i + 1; j < kids.length; j++) {
          var n = kids[j];
          if (n.classList.contains("di-year") || n.classList.contains("di-month")) break;
          if (!n.hidden) { visible = true; break; }
        }
        el.hidden = !visible;
      }
    }
    if (countEl) countEl.textContent = String(shown);
    if (emptyEl) emptyEl.hidden = shown > 0;
  }

  if (search) search.addEventListener("input", applyFilter);
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      mood = chip.dataset.mood || "";
      chips.forEach(function (c) { c.classList.toggle("is-on", c === chip); });
      applyFilter();
    });
  });

  /* ---------------- photo ---------------- */
  var photo = "none";   /* none | keep | data-url */
  var stem = "";

  function stemOf(path) {
    return (path || "").split("/").pop().split(".").slice(0, -1).join(".").toLowerCase();
  }

  function paintPhoto() {
    if (photo === "none") {
      prev.hidden = true;
      pick.hidden = false;
      prevImg.style.backgroundImage = "";
      return;
    }
    pick.hidden = true;
    prev.hidden = false;
    if (photo === "keep") {
      prevImg.style.backgroundImage = "var(--img-" + stem + ")";
      prevMeta.textContent = "CURRENT PHOTO";
      clearBtn.hidden = !state.editing;
    } else {
      prevImg.style.backgroundImage = 'url("' + photo + '")';
      prevMeta.textContent = "NEW PHOTO";
      clearBtn.hidden = false;
    }
  }

  function shrink(fileObj, done) {
    var url = URL.createObjectURL(fileObj);
    var img = new Image();
    img.onload = function () {
      var max = 1800;
      var w = img.naturalWidth, h = img.naturalHeight;
      var k = Math.min(1, max / Math.max(w, h));
      var c = document.createElement("canvas");
      c.width = Math.max(1, Math.round(w * k));
      c.height = Math.max(1, Math.round(h * k));
      var ctx = c.getContext("2d");
      ctx.fillStyle = "#0a1420";
      ctx.fillRect(0, 0, c.width, c.height);
      ctx.drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(url);
      try { done(c.toDataURL("image/jpeg", 0.86)); } catch (e) { done(null); }
    };
    img.onerror = function () { URL.revokeObjectURL(url); done(null); };
    img.src = url;
  }

  if (file) file.addEventListener("change", function () {
    var f = file.files && file.files[0];
    if (!f) return;
    if (f.size > 24 * 1024 * 1024) { fail("That photo is larger than 24 MB."); return; }
    shrink(f, function (data) {
      if (!data) { fail("That photo could not be read."); return; }
      photo = data;
      fail("");
      paintPhoto();
    });
    file.value = "";
  });
  if (clearBtn) clearBtn.addEventListener("click", function () {
    photo = "none";
    paintPhoto();
  });

  /* ---------------- dialog plumbing ---------------- */
  var state = { editing: false, id: null };
  var lastFocus = null;

  function fail(msg) {
    if (!err) return;
    err.textContent = msg || "";
    err.hidden = !msg;
  }

  function toast(msg, kind) {
    var t = document.getElementById("tideToast");
    if (!t || !msg) return;
    t.textContent = msg;
    t.className = "tide-toast show" + (kind === "error" ? " is-error" : "");
    clearTimeout(t._timer);
    t._timer = setTimeout(function () { t.className = "tide-toast"; }, 4200);
  }

  function moodsSet(value) {
    var v = (value || "").toLowerCase();
    moods.forEach(function (m) { m.classList.toggle("is-on", m.dataset.mood === v); });
  }

  function openForm(entry, id) {
    state.editing = !!id;
    state.id = id || null;
    var e = entry || {};
    kicker.textContent = id ? "EDIT MEMORY" : "NEW MEMORY";
    heading.textContent = id ? "Edit this memory" : "Add a memory";
    saveBtn.textContent = id ? "SAVE CHANGES" : "SAVE MEMORY";
    fTitle.value = e.title || "";
    fDate.value = e.date || "";
    fPlace.value = e.location || "";
    fTags.value = (e.tags || []).join(", ");
    fMem.value = e.memory || "";
    fStory.value = e.story || "";
    moodsSet(e.mood || "");
    stem = stemOf(e.image || "");
    photo = id && e.image ? "keep" : "none";
    fail("");
    delCard.hidden = true;
    card.hidden = false;
    paintPhoto();
    show();
    setTimeout(function () { fTitle.focus(); }, 60);
  }

  function openDelete(entry, id) {
    state.editing = true;
    state.id = id;
    card.hidden = true;
    delCard.hidden = false;
    delWhere.textContent = "“" + (entry && entry.title ? entry.title : "this memory") + "”";
    show();
    setTimeout(function () { delBtn.focus(); }, 60);
  }

  function show() {
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
    document.documentElement.style.overflow = "hidden";
    document.body.style.overflow = "hidden";
  }

  function close() {
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    document.documentElement.style.overflow = "";
    document.body.style.overflow = "";
    if (lastFocus && lastFocus.focus) { try { lastFocus.focus(); } catch (e) {} }
  }

  function send(payload) {
    payload.nonce = Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
    try {
      sessionStorage.setItem("tideReturn", "1");
      sessionStorage.setItem("tideY", String(window.scrollY || 0));
    } catch (e) {}
    saveBtn.disabled = true;
    saveBtn.textContent = "SAVING…";
    window.tideSend(payload);
  }

  function save() {
    var title = fTitle.value.trim();
    var memory = fMem.value.trim();
    if (!title) { fail("Give this memory a title."); fTitle.focus(); return; }
    if (!memory) { fail("Write a line or two about it."); fMem.focus(); return; }
    if (!state.editing && photo === "none") { fail("Choose a photo for this memory."); return; }
    var tagList = fTags.value.split(",").map(function (t) { return t.trim(); })
      .filter(function (t) { return t; });
    var active = modal.querySelector(".mm-mood.is-on");
    fail("");
    send({
      op: "save",
      id: state.id,
      photo: photo === "keep" ? null : (photo === "none" ? "" : photo),
      fields: {
        title: title,
        date: fDate.value || "",
        location: fPlace.value.trim(),
        mood: active ? active.dataset.mood : "",
        tags: tagList,
        memory: memory,
        story: fStory.value.trim()
      }
    });
  }

  /* ---------------- events ---------------- */
  modal.addEventListener("click", function (e) {
    var t = e.target;
    var act = t.closest ? t.closest("[data-mm]") : null;
    if (!act) return;
    e.stopPropagation();
    var a = act.dataset.mm;
    if (a === "close") close();
    else if (a === "save") save();
    else if (a === "del") {
      send({ op: "delete", id: state.id, photo: null, fields: {} });
      delBtn.disabled = true;
      delBtn.textContent = "DELETING…";
    } else if (a === "mood") {
      var on = act.classList.contains("is-on");
      moods.forEach(function (m) { m.classList.remove("is-on"); });
      if (!on) act.classList.add("is-on");
    } else if (a === "pick") file.click();
  });

  document.addEventListener("keydown", function (e) {
    if (!modal.classList.contains("open")) return;
    if (e.key === "Escape") { e.preventDefault(); close(); }
  });

  window.tideMem = {
    /* Called first by the shared click handler in components.scripts. */
    handle: function (e) {
      var t = e.target;
      if (!t || !t.closest) return false;
      if (t.closest("[data-add-memory]")) {
        lastFocus = t;
        openForm(null, null);
        return true;
      }
      var edit = t.closest("[data-edit]");
      if (edit) {
        lastFocus = edit;
        var id = edit.dataset.edit;
        openForm(MEM[id], id);
        return true;
      }
      var del = t.closest("[data-del]");
      if (del) {
        lastFocus = del;
        var did = del.dataset.del;
        openDelete(MEM[did], did);
        return true;
      }
      return false;
    },
    toast: toast
  };

  var flash = window.__TIDE_FLASH__;
  if (flash && flash.message) toast(flash.message, flash.kind || "info");
})();
"""


def _payload(entries: list[dict]) -> str:
    data = {
        str(e.get("id")): {
            "title": str(e.get("title") or ""),
            "date": str(e.get("date") or ""),
            "location": str(e.get("location") or ""),
            "mood": str(e.get("mood") or "").lower(),
            "tags": [str(t) for t in e.get("tags") or []],
            "memory": str(e.get("memory") or e.get("caption") or ""),
            "story": str(e.get("story") or ""),
            "image": str(e.get("image") or ""),
            "chapter": e.get("chapter") or 0,
        }
        for e in entries
    }
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def _mood_chips() -> str:
    return "".join(
        f'<button type="button" class="mm-mood" data-mm="mood" '
        f'data-mood="{escape(m)}" aria-pressed="false">{escape(m.upper())}</button>'
        for m in MOODS
    )


def render_memory(entries: list[dict]) -> str:
    """Dialog markup, the entry payload, and every script that edits a memory."""
    mood_chips = _mood_chips()
    markup = f"""
<div class="mm" id="memModal" aria-hidden="true">
  <div class="mm-veil" data-mm="close"></div>

  <div class="mm-card mm-form-card" role="dialog" aria-modal="true" aria-labelledby="mmHeading">
    <header class="mm-head">
      <div class="mm-kicker" id="mmKicker">NEW MEMORY</div>
      <h3 class="mm-heading" id="mmHeading">Add a memory</h3>
      <button class="mm-x" type="button" data-mm="close" aria-label="Close dialog">{CLOSE_SVG}</button>
    </header>

    <div class="mm-scroll">
      <div class="mm-grid">
        <label class="mm-f mm-wide">
          <span>TITLE</span>
          <input type="text" id="mmTitle" maxlength="80" placeholder="Where the water begins" autocomplete="off">
        </label>
        <label class="mm-f">
          <span>DATE</span>
          <input type="date" id="mmDate">
        </label>
        <label class="mm-f">
          <span>PLACE</span>
          <input type="text" id="mmPlace" maxlength="60" placeholder="Marina shore" autocomplete="off">
        </label>
        <div class="mm-f mm-wide">
          <span>MOOD</span>
          <div class="mm-moods" role="group" aria-label="Mood">{mood_chips}</div>
        </div>
        <label class="mm-f mm-wide">
          <span>TAGS</span>
          <input type="text" id="mmTags" maxlength="90" placeholder="sea, morning, just us" autocomplete="off">
        </label>
        <label class="mm-f mm-wide">
          <span>THE MEMORY</span>
          <textarea id="mmMemory" rows="3" maxlength="400" placeholder="One or two lines you want to keep."></textarea>
        </label>
        <label class="mm-f mm-wide">
          <span>THE STORY <i>(OPTIONAL)</i></span>
          <textarea id="mmStory" rows="4" maxlength="2000" placeholder="The longer version, if there is one."></textarea>
        </label>
        <div class="mm-f mm-wide">
          <span>PHOTO</span>
          <div class="mm-photo">
            <input type="file" id="mmFile" accept="image/jpeg,image/png,image/webp" hidden>
            <button type="button" class="mm-pick" id="mmPick" data-mm="pick">{PLUS_SVG}CHOOSE PHOTO</button>
            <div class="mm-prev" id="mmPrev" hidden>
              <div class="mm-prev-img" id="mmPrevImg" role="img" aria-label="Photo preview"></div>
              <div class="mm-prev-side">
                <div class="mm-prev-meta" id="mmPrevMeta">NEW PHOTO</div>
                <button type="button" class="mm-prev-x" id="mmClearPhoto">REMOVE PHOTO</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <p class="mm-error" id="mmError" hidden></p>
    </div>

    <footer class="mm-foot">
      <button class="btn btn-ghost" type="button" data-mm="close">CANCEL</button>
      <button class="btn btn-play" type="button" id="mmSave" data-mm="save">SAVE MEMORY</button>
    </footer>
  </div>

  <div class="mm-card mm-del-card" role="alertdialog" aria-modal="true" aria-labelledby="mmDelTitle">
    <div class="mm-kicker">DELETE MEMORY</div>
    <h3 class="mm-heading" id="mmDelTitle">Remove it from the diary?</h3>
    <p class="mm-del-body"><span id="mmDelWhere"></span> will be taken out of the timeline,
       and its photo will be deleted. The other memories stay where they are.</p>
    <footer class="mm-foot">
      <button class="btn btn-ghost" type="button" data-mm="close">KEEP IT</button>
      <button class="btn btn-danger" type="button" id="mmDelGo" data-mm="del">DELETE</button>
    </footer>
  </div>
</div>

<div class="tide-toast" id="tideToast" role="status" aria-live="polite"></div>
"""
    script = _MEM_TEMPLATE.replace("__TIDE_MEM__", _payload(entries))
    return markup + script + "<script>\n" + _JS + "\n</script>"
