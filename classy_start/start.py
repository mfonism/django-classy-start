import subprocess
from typing import List, Optional

from .paths import APP_TEMPLATES_DIR


def start_app(name: str, directory: Optional[str] = None):
    cmd: List[str]
    cmd = ["django-admin", "startapp", name]

    if directory is not None:
        cmd.append(directory)

    cmd.extend(["--template", str(APP_TEMPLATES_DIR)])

    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
