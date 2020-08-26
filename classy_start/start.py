import enum
import pathlib
import subprocess
import sys
from typing import List, Optional

from . import file_contents, paths


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

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        sys.exit(1)


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

    create_accounts_app(manage_dir)


def rename_file(old_name: str, new_name: str, base_dir: pathlib.Path):
    (base_dir / old_name).rename(base_dir / new_name)


def create_accounts_app(directory: pathlib.Path):
    dest = directory / "accounts"
    dest.mkdir()

    start_app("accounts", dest)

    for (filename, content) in [
        ("models.py", file_contents.auth_user_model_file_content),
        ("admin.py", file_contents.auth_user_admin_file_content),
    ]:
        write_file(dest / filename, content)


def write_file(file: pathlib.Path, content: str):
    file.touch()
    file.write_text(content)
