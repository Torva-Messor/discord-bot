from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class Plugin:
    path: Path
    module_path: str  # Python import path for the plugin entrypoint


def find_plugins(base_dir: Path) -> List[Plugin]:
    """
    Scan a directory for plugin folders containing a main.py file.
    Returns:
        List[Plugin]: A list of discovered plugin entry modules.
    """
    if not base_dir.is_dir():
        raise FileNotFoundError(f"Base plugin directory not found: {base_dir}")

    plugins: List[Plugin] = []

    for entry in base_dir.iterdir():
        if not entry.is_dir():
            continue

        main_file = entry / "main.py"
        if main_file.is_file():
            try:
                # Determine module import path safely
                relative = main_file.relative_to(base_dir.parent)
                module_path = ".".join(relative.with_suffix("").parts)
            except ValueError:
                # Fallback: best-effort replacement
                module_path = str(main_file.with_suffix("")).replace("/", ".")

            plugins.append(Plugin(path=main_file, module_path=module_path))

    # Deterministic output
    plugins.sort(key=lambda p: p.module_path)
    return plugins


