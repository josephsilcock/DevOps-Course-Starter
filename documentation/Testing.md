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
