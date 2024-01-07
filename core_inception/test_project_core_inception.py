from pathlib import Path

from weasel.cli.run import project_run
from weasel.cli.assets import project_assets


def test_core_inception_project():
    root = Path(__file__).parent
    project_assets(root)
    project_run(root, "all", capture=True, overrides={"vars.max_epochs": 1})
    project_run(root, "evaluate-model", capture=True)
    project_run(root, "package-model", capture=True)
