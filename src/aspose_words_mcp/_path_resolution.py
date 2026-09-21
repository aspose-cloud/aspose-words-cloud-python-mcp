"""Shared, audited local-path resolution (FR15).

**Deliberate, self-contained copy** of `aspose_storage_core_mcp._path_resolution` (itself a copy of
`mcp_builder/generated/_shared/path_resolution.py`) — this package must have zero import dependency
on `mcp_builder` (Sprint 7 requirements.md, Requirement 5.1, extended to every product package by
Sprint 11), so its design (not its code) is shared, never imported across that boundary.

Governs *local disk* access only: `words_convert_to_format`'s local input-file read and its local
output-file write are the tools in this package that touch the local filesystem — every other Words
tool's `filename`/`folder_name` arguments name a *Cloud Storage* path forwarded straight to the Aspose
API, never routed through here (same distinction `aspose_storage_core_mcp` draws for its own tools).

Two modes:

- **Sandboxed root mode** (`ASPOSE_FILES_PATH` configured): the incoming name is rejected outright if
  it contains any directory component at all (a forward or back slash, or a bare `..` segment) or was
  given as an absolute path — a path-traversal attempt such as `../../etc/passwd` fails this check
  directly rather than being silently reinterpreted as a safe basename, matching PRD rubric gate 23's
  literal "rejected with a clear error" wording. Only a bare filename with no directory components at
  all is accepted, joined to the configured root, and the joined result is re-verified to still
  resolve under that root (defense in depth) before being returned.
- **Local-desktop fallback mode** (`ASPOSE_FILES_PATH` unset): there is no shared root to sandbox
  against, so the given path is trusted largely as-is — still checked for null bytes and directory-name
  collisions, a narrower (not absent) safety guarantee, disclosed explicitly rather than silently
  assumed equivalent to sandboxed mode.
"""

from __future__ import annotations

import os
from pathlib import Path


class PathResolutionError(Exception):
    """Raised for any rejected filename/folder-name input (mapped to `bad_input` by `_errors.py`)."""


def _reject_null_bytes(name: str) -> None:
    if "\x00" in name:
        raise PathResolutionError(f"filename/folder name must not contain a null byte: {name!r}")


def resolve_local_path(name: str, *, root_env: str = "ASPOSE_FILES_PATH", is_output: bool = False) -> Path:
    """Resolve `name` to a safe local filesystem `Path` (FR15).

    Raises:
        PathResolutionError: null byte, absolute-path input under sandboxed mode, a resolved path
            that would escape the configured root, or a collision with an existing directory.
    """
    if not name and is_output:
        name = "output"
    _reject_null_bytes(name)

    root = os.environ.get(root_env)
    if not root:
        # Local-desktop fallback: no shared root configured, trust the given path largely as-is.
        candidate = Path(name).expanduser()
        if candidate.is_dir():
            raise PathResolutionError(f"{name!r} resolves to an existing directory, not a file")
        return candidate

    if Path(name).is_absolute() or (len(name) >= 2 and name[1] == ":"):
        # len==2 letter-colon check covers Windows-style absolute paths ("C:\\...") that
        # Path(...).is_absolute() only recognizes on a Windows host.
        raise PathResolutionError(f"absolute paths are not allowed when {root_env} is configured: {name!r}")

    if "/" in name or "\\" in name or name in ("..", "."):
        raise PathResolutionError(
            f"{name!r} contains directory components — only a bare filename is accepted when "
            f"{root_env} is configured (path-traversal protection)"
        )

    root_path = Path(root).expanduser().resolve()
    if not name:
        raise PathResolutionError("filename must not be empty")

    resolved = (root_path / name).resolve()
    if root_path not in resolved.parents and resolved != root_path:
        raise PathResolutionError(f"{name!r} would resolve outside the configured root {root_env}")

    if resolved.is_dir():
        raise PathResolutionError(f"{name!r} resolves to an existing directory, not a file")

    return resolved
