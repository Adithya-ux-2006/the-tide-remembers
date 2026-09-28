"""Persistent storage for the diary — one JSON file, seeded from the six chapters.

The diary lives in ``data/memories.json``. On first run the file is seeded from
the built-in chapters in :mod:`data.diary` so the original six behave exactly
like memories the user adds later (they can be edited and deleted too).

Uploaded photos are stored under ``assets/uploads/`` with collision-proof
``<uuid>`` filenames.

Set ``TIDE_DIARY_ROOT`` to relocate the whole store (used by tests).
"""

from __future__ import annotations

import base64
import json
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path

from data.diary import SEED_ENTRIES, USER_LAYOUTS

REPO_ROOT = Path(__file__).resolve().parent.parent

_MIME_EXT = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
_ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def root_dir() -> Path:
    env = os.environ.get("TIDE_DIARY_ROOT")
    return Path(env) if env else REPO_ROOT


def diary_file() -> Path:
    return root_dir() / "data" / "memories.json"


def uploads_dir() -> Path:
    return root_dir() / "assets" / "uploads"


# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

_DEFAULTS = {
    "id": "",
    "chapter": 0,
    "title": "",
    "date": "",
    "location": "",
    "image": "",
    "memory": "",
    "story": "",
    "mood": "",
    "tags": [],
    "layout": "full",
    "origin": "user",
    "created": "",
}


def _normalize(raw: dict) -> dict:
    """Fill in every key the renderer expects and coerce types."""
    entry = dict(_DEFAULTS)
    entry.update(raw or {})
    try:
        entry["chapter"] = int(entry.get("chapter") or 0)
    except (TypeError, ValueError):
        entry["chapter"] = 0
    entry["title"] = str(entry.get("title") or "").strip()
    entry["date"] = str(entry.get("date") or "").strip()
    entry["location"] = str(entry.get("location") or "").strip()
    entry["image"] = str(entry.get("image") or "").strip()
    entry["memory"] = str(entry.get("memory") or "")
    entry["story"] = str(entry.get("story") or "")
    entry["mood"] = str(entry.get("mood") or "").strip()
    entry["layout"] = str(entry.get("layout") or "full").strip() or "full"
    entry["origin"] = str(entry.get("origin") or "user").strip() or "user"
    if not entry["id"]:
        entry["id"] = "m_" + uuid.uuid4().hex[:12]
    tags = entry.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    entry["tags"] = [str(t).strip() for t in tags if str(t).strip()]
    # The chapter renderers display `caption`; user content writes `memory`.
    entry["caption"] = entry["memory"]
    return entry


# ---------------------------------------------------------------------------
# Load / save
# ---------------------------------------------------------------------------


def _write(entries: list[dict]) -> None:
    path = diary_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "entries": entries}
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    tmp.replace(path)


def seed_entries() -> list[dict]:
    return [_normalize(dict(e)) for e in SEED_ENTRIES]


def load_entries() -> list[dict]:
    """Return every memory, chapter order, fully normalised."""
    path = diary_file()
    if not path.exists():
        entries = seed_entries()
        _write(entries)
        return entries
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = None
    raw = []
    if isinstance(data, dict):
        raw = data.get("entries") or []
    elif isinstance(data, list):
        raw = data
    if not isinstance(raw, list) or not raw:
        entries = seed_entries()
        _write(entries)
        return entries
    entries = [_normalize(e) for e in raw if isinstance(e, dict)]
    entries = [e for e in entries if e["title"] or e["image"]]
    entries.sort(key=lambda e: e["chapter"])
    return entries


def save_entries(entries: list[dict]) -> None:
    _write([_normalize(e) for e in entries])


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


def get_entry(entries: list[dict], entry_id: str) -> dict | None:
    for e in entries:
        if e["id"] == entry_id:
            return e
    return None


def next_chapter(entries: list[dict]) -> int:
    if not entries:
        return 1
    return max(int(e.get("chapter") or 0) for e in entries) + 1


def chronological(entries: list[dict]) -> list[dict]:
    """Timeline order — oldest first, chapter number as the tie breaker."""
    return sorted(
        entries,
        key=lambda e: (e.get("date") or "9999-99-99", int(e.get("chapter") or 0)),
    )


# ---------------------------------------------------------------------------
# Mutations
# ---------------------------------------------------------------------------


def add_entry(fields: dict, image: str) -> dict:
    entries = load_entries()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entry = _normalize(
        {
            **fields,
            "id": "m_" + uuid.uuid4().hex[:12],
            "chapter": next_chapter(entries),
            "image": image,
            "origin": "user",
            "created": now,
        }
    )
    entries.append(entry)
    entries.sort(key=lambda e: e["chapter"])
    save_entries(entries)
    return entry


def update_entry(entry_id: str, fields: dict, image: str | None = None) -> dict | None:
    """Update one memory. ``image``: a path replaces it, ``""`` clears it,
    ``None`` leaves the current photo alone."""
    entries = load_entries()
    entry = get_entry(entries, entry_id)
    if entry is None:
        return None
    entry.update(fields)
    if image is not None:
        old = entry.get("image", "")
        entry["image"] = image
        if old and old != image:
            delete_upload(old)
    entry["caption"] = entry.get("memory", "")
    save_entries(entries)
    return entry


def delete_entry(entry_id: str) -> bool:
    entries = load_entries()
    entry = get_entry(entries, entry_id)
    if entry is None:
        return False
    entries = [e for e in entries if e["id"] != entry_id]
    save_entries(entries)
    delete_upload(entry.get("image", ""))
    return True


# ---------------------------------------------------------------------------
# Events coming from the dialog inside the page
# ---------------------------------------------------------------------------

_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_MAX_IMAGE_BYTES = 24 * 1024 * 1024


def _event_fields(raw: dict) -> dict:
    data = raw.get("fields")
    if not isinstance(data, dict):
        data = {}
    date = str(data.get("date") or "").strip()
    if date and not _ISO_DATE.match(date):
        date = ""
    tags = data.get("tags")
    if isinstance(tags, str):
        tags = [t for t in tags.split(",")]
    return {
        "title": str(data.get("title") or "").strip(),
        "date": date,
        "location": str(data.get("location") or "").strip()[:60],
        "mood": str(data.get("mood") or "").strip().lower(),
        "tags": [str(t).strip() for t in (tags or []) if str(t).strip()][:8],
        "memory": str(data.get("memory") or "").strip(),
        "story": str(data.get("story") or "").strip(),
    }


def _next_layout(entries: list[dict]) -> str:
    """A layout for a new memory — never ``feature`` (it owns the quote)."""
    previous = entries[-1].get("layout") if entries else None
    choices = [name for name in USER_LAYOUTS if name != previous] or USER_LAYOUTS
    return choices[len(entries) % len(choices)]


def apply_event(event: dict) -> str | None:
    """Apply one dialog payload. Returns an error message, or ``None`` on success."""
    try:
        op = str(event.get("op") or "")
        entry_id = str(event.get("id") or "")
        entries = load_entries()

        if op == "delete":
            if not entry_id or not delete_entry(entry_id):
                return "That memory is already gone."
            return None

        if op != "save":
            return "That action is not part of the diary."

        fields = _event_fields(event)
        if not fields["title"]:
            return "A memory needs a title."
        if not fields["memory"]:
            return "A memory needs a line or two about it."

        photo = event.get("photo")
        if photo == "":
            image: str | None = ""
        elif isinstance(photo, str) and photo.startswith("data:image/"):
            if len(photo) > _MAX_IMAGE_BYTES:
                return "That photo is larger than 24 MB."
            image = save_upload(photo)
        else:
            image = None

        if entry_id:
            if get_entry(entries, entry_id) is None:
                return "That memory is already gone."
            update_entry(entry_id, fields, image)
            return None

        if not image:
            return "Choose a photo for a new memory."
        fields["layout"] = _next_layout(entries)
        add_entry(fields, image)
        return None
    except ValueError as exc:
        return str(exc)
    except Exception as exc:  # noqa: BLE001 — reported inside the page
        return f"The diary could not save that: {exc}"


# ---------------------------------------------------------------------------
# Photo uploads
# ---------------------------------------------------------------------------

_DATA_URL = re.compile(r"^data:(image/(?:jpeg|jpg|png|webp));base64,(.+)$", re.S)


def save_upload(data_url: str, slot: str | None = None) -> str:
    """Write a base64 photo into ``assets/uploads`` and return its relative path.

    Filenames are ``<uuid><ext>`` so uploads never collide with each other or
    with the original six photos.
    """
    match = _DATA_URL.match((data_url or "").strip())
    if not match:
        raise ValueError("unsupported image data")
    mime, b64 = match.group(1), match.group(2)
    ext = _MIME_EXT.get(mime, ".jpg")
    if ext == ".jpeg":
        ext = ".jpg"
    try:
        blob = base64.b64decode(b64, validate=True)
    except Exception as exc:  # noqa: BLE001 - surfaced to the user
        raise ValueError("image data could not be decoded") from exc
    if not blob:
        raise ValueError("image data was empty")
    stem = re.sub(r"[^a-zA-Z0-9_-]", "", slot or "") or uuid.uuid4().hex[:12]
    directory = uploads_dir()
    directory.mkdir(parents=True, exist_ok=True)
    name = f"{stem}_{uuid.uuid4().hex[:8]}{ext}"
    (directory / name).write_bytes(blob)
    return f"assets/uploads/{name}"


def delete_upload(rel: str) -> None:
    """Remove an uploaded photo (never touches the original six)."""
    if not rel or not rel.startswith("assets/uploads/"):
        return
    name = Path(rel).name
    if not name or name in {".", ".."}:
        return
    target = uploads_dir() / name
    try:
        target.unlink()
    except OSError:
        pass
