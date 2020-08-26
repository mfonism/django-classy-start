import argparse
import sys

from . import start

parser = argparse.ArgumentParser()


parser.add_argument(
    "what", type=str, help="What is to be started: 'app' for app, 'project' for project"
)
parser.add_argument(
    "name", type=str, help="The name of the app or project to be started"
)
parser.add_argument(
    "directory",
    nargs="?",
    type=str,
    help="Optional base directory to start the app or project in",
    default=None,
)


def main():
    args = parser.parse_args()

    if args.what in ("a", "app"):
        start.start_app(args.name, args.directory)
    elif args.what in ("p", "project"):
        start.start_project(args.name, args.directory)
    else:
        sys.stderr.write(
            f"'{args.what}' is not a valid thing to start. "
            f"It should be either 'app' or 'project'\n"
        )
        sys.exit(1)
