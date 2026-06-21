import json
from pathlib import Path

# ---- CONFIG ----

MARKERS = ["# FEEDBACK CELL", "# SCORE CELL"]

TAGS_TO_ADD = ["remove-input"]

JS_CELL_SOURCE = [
    "# HIDE_INIT\n",
    "from IPython.display import Javascript\n",
    "\n",
    "Javascript(\"\"\"\n",
    "setTimeout(function() {\n",
    "  document.querySelectorAll('.jp-CodeCell').forEach(cell => {\n",
    "    if (cell.innerText.includes('# FEEDBACK CELL') ||\n",
    "        cell.innerText.includes('# SCORE CELL')) {\n",
    "      const btn = cell.querySelector('[title=\"Collapse Input\"]');\n",
    "      if (btn) btn.click();\n",
    "    }\n",
    "  });\n",
    "}, 2000);\n",
    "\"\"\")\n"
]

# ---- CORE FUNCTION ----

def process_notebook(nb_path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    changed = False

    # ---- Tag cells ----
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])

            if any(marker in source for marker in MARKERS):
                metadata = cell.setdefault("metadata", {})
                tags = metadata.setdefault("tags", [])

                for tag in TAGS_TO_ADD:
                    if tag not in tags:
                        tags.append(tag)
                        changed = True

    # ---- Ensure JS cell exists ----
    js_exists = any(
        cell["cell_type"] == "code" and "# HIDE_INIT" in "".join(cell["source"])
        for cell in nb["cells"]
    )

    if not js_exists:
        js_cell = {
            "cell_type": "code",
            "metadata": {},
            "source": JS_CELL_SOURCE,
            "outputs": [],
            "execution_count": None,
        }

        # insert at top
        nb["cells"].insert(0, js_cell)
        changed = True

    # ---- Save file ----
    if changed:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print(f"✅ Updated: {nb_path}")


def process_all():
    for nb_path in Path(".").rglob("*.ipynb"):
        process_notebook(nb_path)


if __name__ == "__main__":
    process_all()