import enum
import pathlib
import subprocess
from typing import List, Optional

from . import paths


@enum.unique
class Startable(enum.Enum):
    PROJECT = 0
    APP = 1


def _start(what: Startable, name: str, directory: Optional[str] = None):
    directive = f"start{what.name.lower()}"
    cmd: List[str]
    cmd = ["django-admin", directive, name]

    if directory is not None:
        cmd.append(directory)

    templates_dir_name = f"{what.name}_TEMPLATES_DIR"
    cmd.extend(["--template", str(getattr(paths, templates_dir_name))])

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def start_app(name: str, directory: Optional[str] = None):
    _start(Startable.APP, name, directory)


def start_project(name: str, directory: Optional[str] = None):
    _start(Startable.PROJECT, name, directory)

    follow_up_start_project(name, directory)


def follow_up_start_project(name: str, directory: Optional):
    if directory is None:
        manage_dir = pathlib.Path(".") / name
    else:
        manage_dir = pathlib.Path(directory)

    manage_dir.resolve(strict=True)

    # rename secrets file
    secrets_dot_py = manage_dir / "secrets.py"
    dot_env = manage_dir / ".env"
    secrets_dot_py.rename(dot_env)

    # rename gitignore file
    gitignore_dot_py = manage_dir / "gitignore.py"
    dot_gitignore = manage_dir / ".gitignore"
    gitignore_dot_py.rename(dot_gitignore)

    # rename requirements file
    requirements_dot_py = manage_dir / "requirements.py"
    requirements_dot_txt = manage_dir / "requirements.txt"
    requirements_dot_py.rename(requirements_dot_txt)
