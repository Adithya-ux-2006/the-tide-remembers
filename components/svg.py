"""Inline SVG marks used across the diary — tortoise motif + player icons."""

from __future__ import annotations

TORTOISE_SVG = (
    '<svg viewBox="0 0 64 40" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" aria-hidden="true">'
    '<path d="M8 29C8 15.5 18.6 6 32 6s24 9.5 24 23H8Z"/>'
    '<path d="M53.6 19.4c3.7-1.9 8.3-.5 9.3 3.2.6 2.3-.4 4.6-2.5 5.8l-5.3 2.2-.5-11.2Z"/>'
    '<path d="M43.4 29l-.5 5.3c-.2 1.9 1.3 3.3 3.1 2.8l3.8-1.1-1.2-7H43.4Z"/>'
    '<path d="M13.3 29v5.4c0 2 1.6 3.1 3.4 2.6l3.8-1.1-.6-6.9h-6.6Z"/>'
    '<path d="M8.3 24.6 2 27.7l6.4 2.5-.1-5.6Z"/>'
    '<g fill="none" stroke="#04070c" stroke-width="1.25" opacity="0.5">'
    '<path d="M32 6.5v22.5M13 29c1.4-9.7 8.8-16.9 19-17.7M32 11.3c10.2.8 17.6 8 19 17.7"/>'
    "</g>"
    '<circle cx="58.8" cy="23.4" r="1" fill="#04070c"/>'
    "</svg>"
)

PLAY_SVG = (
    '<svg viewBox="0 0 12 14" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" aria-hidden="true"><path d="M0 0v14l12-7L0 0Z"/></svg>'
)

PLUS_SVG = (
    '<svg viewBox="0 0 12 12" xmlns="http://www.w3.org/2000/svg" fill="none" '
    'stroke="currentColor" aria-hidden="true"><path d="M6 1v10M1 6h10"/></svg>'
)

CLOSE_SVG = (
    '<svg viewBox="0 0 14 14" xmlns="http://www.w3.org/2000/svg" fill="none" '
    'aria-hidden="true"><path d="M1.5 1.5l11 11M12.5 1.5l-11 11"/></svg>'
)

PREV_SVG = (
    '<svg viewBox="0 0 12 14" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" aria-hidden="true"><path d="M12 0 2 7l10 7V0Z"/></svg>'
)

NEXT_SVG = (
    '<svg viewBox="0 0 12 14" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" aria-hidden="true"><path d="M0 0l10 7L0 14V0Z"/></svg>'
)

PAUSE_SVG = (
    '<svg viewBox="0 0 12 14" xmlns="http://www.w3.org/2000/svg" '
    'fill="currentColor" aria-hidden="true"><path d="M0 0h3.6v14H0zM8.4 0H12v14H8.4z"/></svg>'
)
