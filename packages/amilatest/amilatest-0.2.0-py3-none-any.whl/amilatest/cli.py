from amilatest.main import Analyzer
from argparse import ArgumentParser


def main() -> None:
    parser = ArgumentParser(
        description="A dependency-analyzer for requirements.txt files",
        allow_abbrev=False,
    )

    parser.add_argument(
        "-r",
        "--requirements",
        dest="requirements_file",
        default="./requirements.txt",
        help="Path to requirements.txt file",
    )

    parser.add_argument(
        "-j",
        "--json",
        dest="json_output",
        default=False,
        help="Output in JSON format",
        action="store_true",
    )

    args = parser.parse_args()

    requirements_file_path = args.requirements_file

    output = Analyzer(requirements_file_path, args.json_output).analyze()

    print(output)
