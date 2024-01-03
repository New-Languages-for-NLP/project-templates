"""
Adapted from:
https://github.com/explosion/projects/blob/v3/.github/update_projects_jsonl.py
"""

from pathlib import Path
from weasel.cli.main import PROJECT_FILE
from weasel.util import load_project_config
from wasabi import msg
import json
import typer


def main(root: Path = typer.Argument(Path.cwd(), help="Root path to look in")):
    """
    Update the projects.jsonl file for the repo.

    Unlike the docs update script, this is designed to only be run on the root
    of the whole repository.
    """
    msg.info(f"Updating projects.jsonl in {root}")
    entries = []
    # We look specifically for project directories
    for path in root.glob(f"**/*/{PROJECT_FILE}"):
        path = path.parent

        # prep data for the json file
        config = load_project_config(path)
        entry = {"shortname": path.name}
        entry["title"] = config["title"]
        entry["description"] = config.get("description", "")
        entries.append(entry)

    with open("projects.jsonl", "w", encoding="utf-8") as json_file:
        for entry in entries:
            json_file.write(json.dumps(entry))
            json_file.write("\n")


if __name__ == "__main__":
    typer.run(main)
