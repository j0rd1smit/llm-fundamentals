pip install poetry
poetry config virtualenvs.in-project true
poetry install
poetry run ipython kernel install --user --name=venv