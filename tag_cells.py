import json
from pathlib import Path

# ---- CONFIG ----

MARKERS = [
    "# FEEDBACK CELL",
    "# SCORE CELL"
]

TAGS_TO_ADD = ["remove-input", "hide-input"]

BOOK_FOLDERS = [
    "01_introduction",
    "02_fundamentals",
    "03_circuits",
    "04_threephase"
]


def tag_notebook(nb_path):
    """Add tags and hide metadata to marked cells"""

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changed = False

    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))

        if any(marker in source for marker in MARKERS):

            metadata = cell.setdefault("metadata", {})
            tags = metadata.get("tags", [])

            # ✅ add tags
            for tag in TAGS_TO_ADD:
                if tag not in tags:
                    tags.append(tag)
                    changed = True

            metadata["tags"] = tags

            # ✅ FORCE AUTO COLLAPSE (this was missing!)
            if metadata.get("hide_input") != True:
                metadata["hide_input"] = True
                changed = True

    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"✅ Tagged: {nb_path}")
    else:
        print(f"➖ No changes: {nb_path}")


# ---- APPLY TO BOOK NOTEBOOKS ----

for folder in BOOK_FOLDERS:
    path = Path(folder)

    if path.exists():
        for nb in path.rglob("A*.ipynb"):

            # skip checkpoints
            if ".ipynb_checkpoints" in str(nb):
                continue

            tag_notebook(nb)