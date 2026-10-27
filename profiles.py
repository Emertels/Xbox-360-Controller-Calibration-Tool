"""
Profile Manager
===============
Save and load calibration profiles as human-readable JSON files.

Profiles are stored in a ``profiles/`` sub-directory next to this script,
making the whole project folder self-contained and portable.

Author: Emerson Teles (projeto criado com auxílio do Antigravity)
License: MIT
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from calibration import CalibrationSettings

# Profiles live right beside the source tree so the project stays portable.
DEFAULT_PROFILE_DIR = Path(__file__).resolve().parent / "profiles"
DEFAULT_PROFILE_NAME = "default.json"


def get_profile_dir() -> Path:
    """Return (and create if needed) the profile directory."""
    DEFAULT_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_PROFILE_DIR


def save_profile(
    settings: CalibrationSettings,
    filename: str = DEFAULT_PROFILE_NAME,
    *,
    profile_dir: Path | None = None,
) -> Path:
    """Persist *settings* to a JSON file.

    Args:
        settings:    The calibration data to store.
        filename:    File name inside the profile directory.
        profile_dir: Override the default profile directory.

    Returns:
        Absolute ``Path`` of the written file.
    """
    directory = profile_dir or get_profile_dir()
    directory.mkdir(parents=True, exist_ok=True)
    filepath = directory / filename

    data = {
        "version": 1,
        "tool": "Xbox 360 Controller Calibration Tool",
        "created_at": datetime.now().isoformat(),
        "calibration": settings.to_dict(),
    }

    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)

    return filepath


def load_profile(
    filename: str = DEFAULT_PROFILE_NAME,
    *,
    profile_dir: Path | None = None,
) -> CalibrationSettings:
    """Load calibration settings from a JSON file.

    Args:
        filename:    File name to load.
        profile_dir: Override the default profile directory.

    Returns:
        A ``CalibrationSettings`` instance.

    Raises:
        FileNotFoundError: Profile does not exist.
        ValueError:        Profile is malformed.
    """
    directory = profile_dir or get_profile_dir()
    filepath = directory / filename

    if not filepath.exists():
        raise FileNotFoundError(f"Perfil não encontrado: {filepath}")

    with open(filepath, "r", encoding="utf-8") as fh:
        data = json.load(fh)

    if "calibration" not in data:
        raise ValueError(f"Formato de perfil inválido: {filepath}")

    return CalibrationSettings.from_dict(data["calibration"])


def list_profiles(*, profile_dir: Path | None = None) -> list[str]:
    """Return the names of all ``.json`` profiles in the profile directory."""
    directory = profile_dir or get_profile_dir()
    if not directory.exists():
        return []
    return sorted(f.name for f in directory.glob("*.json"))


def delete_profile(
    filename: str,
    *,
    profile_dir: Path | None = None,
) -> bool:
    """Delete a profile file.  Returns *True* if it existed."""
    directory = profile_dir or get_profile_dir()
    filepath = directory / filename
    if filepath.exists():
        filepath.unlink()
        return True
    return False
