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

JS_SNIPPET = """# HIDE_INIT
from IPython.display import Javascript
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


# ---- CORE FUNCTION ----

def tag_notebook(nb_path):
    """Tag FEEDBACK/SCORE cells and inject JS auto-hide"""

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    modified = False
    js_present = False

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue

        source = "".join(cell.get("source", []))

        # Check if JS already exists
        if "HIDE_INIT" in source:
            js_present = True

        # Tag matching cells
        if any(marker in source for marker in MARKERS):
            tags = cell.setdefault("metadata", {}).setdefault("tags", [])

            for tag in TAGS_TO_ADD:
                if tag not in tags:
                    tags.append(tag)
                    modified = True

    # Inject JS snippet at top if missing
    if not js_present:
        js_cell = {
            "cell_type": "code",
            "metadata": {"tags": ["remove-input"]},
            "source": [line + "\n" for line in JS_SNIPPET.split("\n")],
            "outputs": [],
            "execution_count": None,
        }
        nb["cells"].insert(0, js_cell)
        modified = True

    # Save only if changed
    if modified:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)

        print(f"✅ Updated: {nb_path}")
    else:
        print(f"✔ No change: {nb_path}")


# ---- APPLY TO BOOK NOTEBOOKS ----

def process_all():
    root = Path(".")

    for folder in BOOK_FOLDERS:
        folder_path = root / folder

        if not folder_path.exists():
            print(f"⚠ Folder not found: {folder_path}")
            continue

        for nb_file in folder_path.rglob("*.ipynb"):
            tag_notebook(nb_file)


# ---- MAIN ----

if __name__ == "__main__":
    process_all()
