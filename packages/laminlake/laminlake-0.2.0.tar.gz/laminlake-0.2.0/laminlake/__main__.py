import argparse
from pathlib import Path


# consider changing to click
# * https://click.palletsprojects.com/en/5.x/
# * https://collectiveacuity.medium.com/argparse-vs-click-227f53f023dc
parser = argparse.ArgumentParser(description="Setup laminlake.")
aa = parser.add_argument
aa("command", type=str, choices=["configure"], help="basic setup")
NOTION_HELP = "Notion integration token"
aa("--notion", type=str, metavar="token", default=None, help=NOTION_HELP)
args = parser.parse_args()


def configure(notion=None):

    # integrate with Notion
    if notion is None:
        notion = input(
            f"Please paste your internal {NOTION_HELP}"
            " (https://notion.so/my-integrations): "
        )

    # write a _secrets.py file that's in .gitignore
    root_dir = Path(__file__).parent.resolve()
    with open(root_dir / "_secrets.py", "w") as f:
        f.write(f"NOTION_API_KEY = {notion!r}")


def main():
    if args.command == "configure":
        configure(notion=args.notion)
