import argparse
import copy
import json
import shutil
from pathlib import Path
from typing import Any


def main():
    args = arg_parser()
    input_folder = Path(args.input_folder)
    output_folder = Path(args.output_folder)

    if output_folder.exists():
        # remove all files in output folder
        shutil.rmtree(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

    generate_notebooks(input_folder, output_folder)
    generate_source_files(input_folder, output_folder, ".py")
    generate_source_files(input_folder, output_folder, ".md")
    generate_source_files(input_folder, output_folder, ".csv")
    generate_source_files(input_folder, output_folder, ".json")


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder", type=Path, required=True)
    parser.add_argument("--output_folder", type=Path, required=True)
    return parser.parse_args()


def generate_source_files(
    input_folder: Path, output_folder: Path, extension: str
) -> None:
    for path in input_folder.rglob(f"*{extension}"):
        relative_path = path.relative_to(input_folder)
        output_path = output_folder / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "r") as f:
            source = f.read()

        source_without_answer = remove_answer_from_source(source)

        with open(output_path, "w") as f:
            f.write(source_without_answer)


def generate_notebooks(input_folder: Path, output_folder: Path) -> None:
    for path in input_folder.rglob("*.ipynb"):
        relative_path = path.relative_to(input_folder)
        output_path = output_folder / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "r") as f:
            notebook = json.load(f)

        notebook_without_answer = remove_answer_from_notebook(notebook)

        with open(output_path, "w") as f:
            f.write(json.dumps(notebook_without_answer, indent=1))


def remove_answer_from_notebook(notebook_data: dict[str, Any]) -> dict[str, Any]:
    notebook_data = copy.deepcopy(notebook_data)

    for cell in notebook_data["cells"]:
        if cell["cell_type"] == "code":
            source_lines = cell["source"]

            lines_to_keep = []
            in_removing_mode = False
            for i, line in enumerate(source_lines):
                if "# YOUR CODE HERE END" in line:
                    in_removing_mode = False

                if not in_removing_mode:
                    lines_to_keep.append(line)

                if "# YOUR CODE HERE START" in line:
                    in_removing_mode = True

            cell["source"] = lines_to_keep

    return notebook_data


def remove_answer_from_source(source: str) -> str:
    lines = source.splitlines()

    lines_to_keep = []
    in_removing_mode = False
    for i, line in enumerate(lines):
        if "# YOUR CODE HERE END" in line:
            in_removing_mode = False

        if not in_removing_mode:
            lines_to_keep.append(line)

        if "# YOUR CODE HERE START" in line:
            in_removing_mode = True

    return "\n".join(lines_to_keep)


if __name__ == "__main__":
    main()
