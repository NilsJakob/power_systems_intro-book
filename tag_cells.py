import json
from pathlib import Path

# ---- CONFIG ----

# Markers used to identify cells
MARKERS = [
    "# FEEDBACK CELL",
    "# SCORE CELL"
]

# Tags to apply
TAGS_TO_ADD = ["remove-input", "hide-input"]

# Book folders (only these are modified)
BOOK_FOLDERS = [
    "01_introduction",
    "02_fundamentals",
    "03_circuits",
    "04_threephase"
]


def tag_notebook(nb_path):
    """Add tags to marked cells in a notebook"""

    # Load notebook
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changed = False

    # Iterate through cells
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))

        # Check if cell contains any marker
        if any(marker in source for marker in MARKERS):

            # Ensure metadata exists
            metadata = cell.setdefault("metadata", {})

            # Get existing tags
            tags = metadata.get("tags", [])

            # Add tags only if missing
            for tag in TAGS_TO_ADD:
                if tag not in tags:
                    tags.append(tag)
                    changed = True

            # Save tags back
            metadata["tags"] = tags

    # Save notebook only if changes were made
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"✅ Tagged: {nb_path}")
    else:
        print(f"➖ No changes: {nb_path}")


# ---- APPLY TO BOOK NOTEBOOKS ONLY ----

for folder in BOOK_FOLDERS:
    path = Path(folder)

    if path.exists():
        for nb in path.rglob("A*.ipynb"):

            # Skip checkpoint files
            if ".ipynb_checkpoints" in str(nb):
                continue

            tag_notebook(nb)
