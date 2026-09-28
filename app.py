"""THE TIDE REMEMBERS — a cinematic digital diary, served through Streamlit."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from components.page import build_document, render_document
from components.styles import STREAMLIT_CSS
from data import store
from data.diary import SITE, build_site, load_images

BASE_DIR = Path(__file__).resolve().parent

_FLASH_KEY = "tide_flash"
_SEEN_KEY = "tide_seen_event"


def main() -> None:
    st.set_page_config(
        page_title=f"{SITE['brand']} — {SITE['kicker'].title()}",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(STREAMLIT_CSS, unsafe_allow_html=True)

    flash = st.session_state.pop(_FLASH_KEY, None)
    entries = store.load_entries()
    html = build_document(
        build_site(entries), entries, load_images(str(BASE_DIR), entries), flash
    )
    event = render_document(html)

    if (
        isinstance(event, dict)
        and event.get("nonce")
        and event.get("nonce") != st.session_state.get(_SEEN_KEY)
    ):
        st.session_state[_SEEN_KEY] = event["nonce"]
        try:
            error = store.apply_event(event)
        except Exception as exc:  # noqa: BLE001 — surfaced inside the page
            error = f"The diary could not save that: {exc}"
        st.session_state[_FLASH_KEY] = {
            "kind": "error" if error else "ok",
            "message": error
            or (
                "Removed from the diary."
                if event.get("op") == "delete"
                else "Added to the diary."
            ),
        }
        st.rerun()


if __name__ == "__main__":
    main()
