# src/frontend/lib/runtime_paths.py
from __future__ import annotations
import os, sys, shutil
from pathlib import Path
from importlib import resources

ASSET_TOPS = ("static", "templates")

def _inside_zipapp() -> bool:
    # zipapps can be a single file (…/pyshelf.pyz) or an executable file without .pyz
    # When invoked, sys.argv[0] is the archive path; treat non-directory as zipapp
    return not Path(sys.argv[0]).is_dir()

def assets_root() -> Path:
    """
    Directory that *contains* static/ and templates/.
    Priority:
      1) PYSHELF_ASSETS
      2) ./pyshelf (sibling dir next to the archive) when running as zipapp
      3) frontend/ (package dir) when running from source/unpacked tree
    """
    env = os.environ.get("PYSHELF_ASSETS")
    if env:
        return Path(env)

    if _inside_zipapp():
        # e.g. /opt/pyshelf/pyshelf  -> use /opt/pyshelf/pyshelf{,/static,/templates}
        base = Path(sys.argv[0]).resolve()
        # strip suffix like ".pyz" if present to get a nice folder name
        return base.with_suffix("")

    # Dev/regular run: __file__ = …/frontend/lib/runtime_paths.py => parents[1] == …/frontend
    return Path(__file__).resolve().parents[1]

def _copy_traversable_tree(src_trav, dst_dir: Path) -> None:
    """Recursively copy a Traversable (importlib.resources) tree to dst_dir."""
    for child in src_trav.iterdir():
        target = dst_dir / child.name
        if child.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            _copy_traversable_tree(child, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            with child.open("rb") as r, open(target, "wb") as w:
                shutil.copyfileobj(r, w)

def ensure_assets() -> tuple[Path, Path]:
    """
    Ensure static/ and templates/ exist on disk and return their paths.
    If running from zipapp and they don't exist yet, extract packaged copies.
    """
    root = assets_root()
    static_dir = root / "static"
    tmpl_dir = root / "templates"

    # If both already exist, use them (works in repo tree and next to .pyz)
    if static_dir.exists() and tmpl_dir.exists():
        return static_dir, tmpl_dir

    # Extract from package data into root/{static,templates}
    pkg = "frontend"  # package that contains 'static' and 'templates'
    for top in ASSET_TOPS:
        src = resources.files(pkg) / top  # Traversable
        dst = root / top
        dst.mkdir(parents=True, exist_ok=True)
        _copy_traversable_tree(src, dst)

    return static_dir, tmpl_dir

