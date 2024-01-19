# llm-fundamentals


## Developing exercises
The exercises are generated automatically.
Please develop and make changes only in the solutions folder.
Then run the following command to generate the exercises:

```bash
poetry run invoke generate-exercises
```

This will automatically generate the exercises and copy them to the `exercises` folder.
It also automatically removes all the code between the `# START CODE HERE` and `# END CODE HERE` comments in the notebooks and python files.

If you use pre-commit, this will be run automatically before each commit.
So you don't have to worry about it.
You can add the pre-commit hook by running the following command:

```bash
poetry run pre-commit install
```

If you don't use pre-commit, the CI will fail if you forget to run this command.


