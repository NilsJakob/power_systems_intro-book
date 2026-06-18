import json
from pathlib import Path

def tag_check_cells(nb_path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb["cells"]:
        source = "".join(cell.get("source", []))

        # Identify your feedback cells
        if "Checking answers" in source:
            cell.setdefault("metadata", {})
            cell["metadata"]["tags"] = ["remove-input"]

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)

# Apply to all notebooks in your book
for nb in Path(".").rglob("A*.ipynb"):
    tag_check_cells(nb)
    print(f"Tagged: {nb}")
