"""The diary document — assembled once per run and served to the host page.

``streamlit.components.v1.html`` is one-way: the page can never talk back to
Python, which would make “add a memory” impossible. So the document is served
as a tiny custom component instead:

* Python writes the finished HTML to ``build/page/index.html`` and hands the
  component a content hash (``v``);
* the page posts ``streamlit:componentReady`` on load and reloads itself when
  the hash it receives no longer matches the one it was served with;
* the add / edit / delete dialog posts its payload with
  ``streamlit:setComponentValue`` — including a photo — which shows up as this
  module's return value on the next run.
"""

from __future__ import annotations

import hashlib
import json
from html import escape
from pathlib import Path

from streamlit.components.v1 import declare_component

from components.chapters import (
    render_atmosphere,
    render_dedication,
    render_diary,
    render_footer,
    render_rail,
    render_topbar,
)
from components.hero import render_hero
from components.memory import render_memory
from components.scripts import get_scripts
from components.story import render_story
from components.styles import get_styles

VERSION_KEY = "%%TIDE_V%%"
PAGE_KEY = "tide_page"

COMPONENT_DIR = Path(__file__).resolve().parents[1] / "build" / "page"

_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Inter:wght@300;400;500;600;700&amp;"
    "family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&amp;"
    'display=swap">'
)

# Runs before anything else in the page: it opens the channel to the host and
# reloads the document whenever Python serves a newer version of it.
_BRIDGE = r"""
<script>
window.__TIDE_V__ = "%%TIDE_V%%";
window.__TIDE_FLASH__ = %%TIDE_FLASH%%;
(function () {
  "use strict";
  function post(msg) {
    msg.isStreamlitMessage = true;
    try { window.parent.postMessage(msg, "*"); } catch (err) {}
  }
  window.addEventListener("message", function (e) {
    var d = e.data;
    if (!d || d.type !== "streamlit:render") return;
    var v = d.args && d.args.v;
    if (v && v !== window.__TIDE_V__) {
      location.replace(location.pathname + "?v=" + encodeURIComponent(v));
    }
  });
  window.tideSend = function (payload) {
    post({ type: "streamlit:setComponentValue", value: payload, dataType: "json" });
  };
  post({ type: "streamlit:componentReady", apiVersion: 1 });
  post({ type: "streamlit:setFrameHeight", height: window.innerHeight || 900 });
})();
</script>
"""

_TIDE_COMPONENT = None


def build_document(
    site: dict,
    entries: list[dict],
    images: dict[str, str],
    flash: dict | None = None,
) -> str:
    """Assemble the complete standalone page served inside the host iframe."""
    title = f"{escape(site['brand'])} — {escape(site['kicker'].title())}"
    bridge = _BRIDGE.replace(
        "%%TIDE_FLASH%%", json.dumps(flash, ensure_ascii=False) if flash else "null"
    )
    return (
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="color-scheme" content="dark">'
        f"<title>{title}</title>"
        + _FONT_LINK
        + bridge
        + "<style>"
        + get_styles(images)
        + "</style>"
        "</head>"
        "<body>"
        + render_atmosphere()
        + render_topbar(site, entries)
        + render_rail(entries)
        + "<main id='page'>"
        + render_hero(site)
        + render_diary(site, entries)
        + render_dedication(site)
        + render_footer(site)
        + "</main>"
        + render_story(site, entries)
        + render_memory(entries)
        + get_scripts(entries)
        + "</body>"
        "</html>"
    )


def _component():
    global _TIDE_COMPONENT
    if _TIDE_COMPONENT is None:
        COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
        _TIDE_COMPONENT = declare_component("tide", path=str(COMPONENT_DIR))
    return _TIDE_COMPONENT


def render_document(html: str):
    """Write the page out and ask the host to render it; returns the last event."""
    version = hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]
    COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
    (COMPONENT_DIR / "index.html").write_text(
        html.replace(VERSION_KEY, version), encoding="utf-8"
    )
    return _component()(v=version, key=PAGE_KEY, default=None)
