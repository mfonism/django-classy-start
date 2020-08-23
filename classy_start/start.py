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


def follow_up_start_project(name: str, directory: Optional[str] = None):
    if directory is None:
        manage_dir = pathlib.Path(".") / name
    else:
        manage_dir = pathlib.Path(directory)

    manage_dir.resolve(strict=True)
    name_change_map = {
        "secrets.py": ".env",
        "gitignore.py": ".gitignore",
        "requirements.py": "requirements.txt",
    }

    for (old_name, new_name) in name_change_map.items():
        rename_file(old_name, new_name, base_dir=manage_dir)


def rename_file(old_name, new_name, base_dir):
    (base_dir / old_name).rename(base_dir / new_name)
