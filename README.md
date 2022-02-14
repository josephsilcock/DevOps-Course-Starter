# DevOps Apprenticeship: Project Exercise

## Quick  Set-up

The following script installs poetry, installs the dependencies and starts the app:
```bash
python3 setup.py
```

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your 
system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following 
commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## Prerequisite Setup

We use [Trello's](https://trello.com/) API to save and fetch to-do tasks. In order to call their API, you need to first 
[create an account](https://trello.com/signup), then generate an API key and token by following the 
[instructions here](https://trello.com/app-key).

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install 
required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a 
one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like 
development mode (which also enables features like hot reloading when you make a file change).

The `.env` file also needs updating with the Trello API key and token created earlier, along with the board ID you are
using for development. The board must have headings: "Not Started", "In Progress" and "Completed".

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by 
running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Deploying on a VM

There are scripts to deploy the app on a VM using ansible. The controller needs SSH access to the host, and ansible must
be installed. If ansible is not already installed on the controller, install it using:
```bash
$ sudo pip install ansible
```
Add the IP address of the host machines to `ansible-inventory`, and change the `remote_user` in `ansible-playbook.yml`
to the username of the host machines, then run the following to deploy the app:
```bash
ansible-playbook ansible-playbook.yml -i ansible-inventory
```


## Testing

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