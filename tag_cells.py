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


JS_SNIPPET = """from IPython.display import Javascript

Javascript(\"\"\"
setTimeout(function() {
    document.querySelectorAll('.jp-CodeCell').forEach(cell => {
        if (cell.innerText.includes("# FEEDBACK CELL") || 
            cell.innerText.includes("# SCORE CELL")) {

            const btn = cell.querySelector('[title="Collapse Input"]');
            if (btn) {
                btn.click();
            }
        }
    });
}, 800);
\"\"\")
"""


def tag_notebook(nb_path):
    """Tag FEEDBACK/SCORE cells and inject JS auto-collapse"""

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changed = False

    # ---- Tag FEEDBACK + SCORE cells ----
    for cell in nb.get("cells", []):
        source = "".join(cell.get("source", []))

        if any(marker in source for marker in MARKERS):
            metadata = cell.setdefault("metadata", {})
            tags = metadata.get("tags", [])

            for tag in TAGS_TO_ADD:
                if tag not in tags:
                    tags.append(tag)
                    changed = True

            metadata["tags"] = tags

            # enforce collapse metadata
            if metadata.get("hide_input") != True:
                metadata["hide_input"] = True
                changed = True

    # ---- Inject JS INIT CELL (only once) ----
    already_exists = any(
        "HIDE_INIT" in "".join(cell.get("source", []))
        for cell in nb.get("cells", [])
    )

    if not already_exists:
        js_cell = {
            "cell_type": "code",
            "metadata": {
                "tags": ["remove-input"]  # hide this in book
            },
            "source": ["# HIDE_INIT\n", JS_SNIPPET],
            "execution_count": None,
            "outputs": []
        }

        # Insert at top
        nb["cells"].insert(0, js_cell)
        changed = True

    # ---- Save if changed ----
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"✅ Updated: {nb_path}")
    else:
        print(f"➖ No changes: {nb_path}")


# ---- APPLY ----

for folder in BOOK_FOLDERS:
    path = Path(folder)

    if path.exists():
        for nb in path.rglob("A*.ipynb"):

            if ".ipynb_checkpoints" in str(nb):
                continue

            tag_notebook(nb)