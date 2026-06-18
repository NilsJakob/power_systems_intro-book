import json
from pathlib import Path

# ---- CONFIG ----
# Define markers you use in your notebooks
MARKERS = [
    "# FEEDBACK CELL",
    "# SCORE CELL"
]

# Set tag here (change to "hide-input" if you prefer collapsible)
TAG_TO_ADD = "remove-input"


def tag_notebook(nb_path):
    # Load notebook
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changed = False

    for cell in nb["cells"]:
        source = "".join(cell.get("source", []))

        # Match cells using markers
        if any(marker in source for marker in MARKERS):

            # Ensure metadata exists
            cell.setdefault("metadata", {})

            # Get existing tags safely
            tags = cell["metadata"].get("tags", [])

            # Add tag only if missing (IMPORTANT: do NOT overwrite!)
            if TAG_TO_ADD not in tags:
                tags.append(TAG_TO_ADD)
                cell["metadata"]["tags"] = tags
                changed = True

    # Save only if changed
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"Tagged: {nb_path}")
    else:
        print(f"No changes: {nb_path}")


# ---- APPLY TO BOOK NOTEBOOKS ONLY ----
# (important: do NOT touch source notebooks)

BOOK_FOLDERS = [
    "01_introduction",
    "02_fundamentals",
    "03_circuits",
    "04_threephase"
]

for folder in BOOK_FOLDERS:
    path = Path(folder)
    if path.exists():
        for nb in path.rglob("A*.ipynb"):
            tag_notebook(nb)