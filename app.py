"""THE TIDE REMEMBERS — a cinematic digital diary, served through Streamlit."""

from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from components.chapters import (
    render_atmosphere,
    render_diary,
    render_footer,
    render_rail,
    render_topbar,
)
from components.hero import render_hero
from components.scripts import get_scripts
from components.story import render_story
from components.styles import STREAMLIT_CSS, get_styles
from data.diary import DIARY_ENTRIES, SITE, load_images

BASE_DIR = Path(__file__).resolve().parent

_FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Inter:wght@300;400;500;600;700&amp;"
    "family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&amp;"
    'display=swap">'
)


def build_document() -> str:
    """Assemble the complete standalone page rendered inside the app."""
    styles = get_styles(load_images(str(BASE_DIR)))
    return (
        "<!DOCTYPE html>"
        '<html lang="en">'
        "<head>"
        '<meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="color-scheme" content="dark">'
        f"<title>{SITE['brand']} — {SITE['kicker'].title()}</title>"
        + _FONT_LINK
        + "<style>"
        + styles
        + "</style>"
        "</head>"
        "<body>"
        + render_atmosphere()
        + render_topbar(SITE)
        + render_rail(DIARY_ENTRIES)
        + "<main id='page'>"
        + render_hero(SITE)
        + render_diary(SITE, DIARY_ENTRIES)
        + render_footer(SITE)
        + "</main>"
        + render_story(SITE, DIARY_ENTRIES)
        + get_scripts(DIARY_ENTRIES)
        + "</body>"
        "</html>"
    )


def main() -> None:
    st.set_page_config(
        page_title=f"{SITE['brand']} — {SITE['kicker'].title()}",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    st.markdown(STREAMLIT_CSS, unsafe_allow_html=True)
    components.html(build_document(), height=900, scrolling=True)


if __name__ == "__main__":
    main()
