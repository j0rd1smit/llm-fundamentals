from pathlib import Path

from invoke import task

REPO_ROOT = Path(__file__).parent


@task()
def generate_exercises(c):
    """Generate the exercise folder based on the solutions folder. Without the answers of course."""
    path = REPO_ROOT / "scripts" / "generate_exercises.py"
    path = path.resolve().absolute()

    input_folder = REPO_ROOT / "solutions"
    input_folder = input_folder.resolve().absolute()

    output_folder = REPO_ROOT / "exercises"
    output_folder = output_folder.resolve().absolute()
    c.run(
        f"python {path} --input_folder {input_folder} --output_folder {output_folder}"
    )
