# Set-up

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your 
system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following 
commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Prerequisites

#### Trello

We use [Trello's](https://trello.com/) API to save and fetch to-do tasks. In order to call their API, you need to first 
[create an account](https://trello.com/signup), then generate an API key and token by following the 
[instructions here](https://trello.com/app-key).

#### .env File

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a 
one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like 
development mode (which also enables features like hot reloading when you make a file change).

The `.env` file also needs updating with the Trello API key and token created earlier, along with the board ID you are
using for development. The board must have headings: "Not Started", "In Progress" and "Completed".


## Quick  Set-up

The following script installs poetry, installs the dependencies and starts the app:
```bash
python3 setup.py
```

## Manual Set-up

### Poetry

The project uses a poetry virtual environment to isolate package dependencies.

#### Poetry installation (Bash)

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

To create the virtual environment and install 
required packages, run the following from your preferred shell:

```bash
$ poetry install
```

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
