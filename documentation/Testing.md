# Testing

Default test configurations are stored for both Visual Studio Code and Pycharm. Running these will run all the tests.
If, for any reason, these are not working, you can run the tests by running:
```bash
$ poetry run pytest
```
To run tests in a particular module, pass the module as an argument, e.g:
```bash
$ poetry run pytest tests/unit/data
```
To run a single test in a particular file, pass the module as an argument, followed by the test name, e.g:
```bash
$ poetry run pytest tests/unit/data/test_items.py::test_item_view_completed_items
```
To run a single parameter in a parameterised test, pass the id of the single test, e.g:
```bash
$ poetry run pytest tests/unit/data/test_items.py::test_item_view_completed_items["single completed item"]
```

## Docker

To run the tests in docker, either use `docker compose` as specified [here](./Docker.md), which creates a docker 
container which runs the tests when changes are detected, or run the following commands having created the development
image manually:

#### UNIX systems (and powershell)
```bash
docker run --env-file ./.env.test --mount type=bind,source="$(pwd)"/todo_app,target=/todo-app/todo_app --mount type=bind,source="$(pwd)"/tests,target=/todo-app/tests --entrypoint poetry todo-app:dev run pytest
```
#### Windows (CMD)
```bash
docker run --env-file ./.env.test --mount type=bind,source=C:\Path\To\App\todo_app,target=/todo-app/todo_app --mount type=bind,source=C:\Path\To\App\tests,target=/todo-app/tests --entrypoint poetry todo-app:dev run pytest
```