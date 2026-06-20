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

# ✅ WORKING JS FOR JUPYTERLAB 4 (DOM-based hide)
JS_SNIPPET = """from IPython.display import Javascript

Javascript(\"\"\"
setTimeout(function() {
    document.querySelectorAll('.jp-CodeCell').forEach(cell => {
        const text = cell.innerText;

        if (text.includes("# FEEDBACK CELL") ||
            text.includes("# SCORE CELL")) {

            const input = cell.querySelector('.jp-Cell-inputWrapper');
            if (input) {
                input.style.display = 'none';
            }
        }
    });
}, 2000);
\"\"\")
"""


def tag_notebook(nb_path):
    """Tag FEEDBACK/SCORE cells and inject JS auto-hide"""

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changed = False

    # ---- TAG FEEDBACK + SCORE CELLS ----
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

    # ---- ADD JS INIT CELL (ONLY ONCE) ----
    already_exists = any(
        "HIDE_INIT" in "".join(cell.get("source", []))
        for cell in nb.get("cells", [])
    )

    if not already_exists:
        js_cell = {
            "cell_type": "code",
            "metadata": {
                "tags": ["remove-input"]  # hidden in Book
            },
            "source": [
                "# HIDE_INIT\n",
                JS_SNIPPET
            ],
            "execution_count": None,
            "outputs": []
        }

        nb["cells"].insert(0, js_cell)
        changed = True

    # ---- SAVE ----
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"✅ Updated: {nb_path}")
    else:
        print(f"➖ No changes: {nb_path}")


# ---- APPLY TO BOOK NOTEBOOKS ----

for folder in BOOK_FOLDERS:
    path = Path(folder)

    if path.exists():
        for nb in path.rglob("A*.ipynb"):

            if ".ipynb_checkpoints" in str(nb):
                continue

            tag_notebook(nb)