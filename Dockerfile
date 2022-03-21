FROM python:3.7-slim-buster AS base
WORKDIR /todo-app
RUN pip3 install poetry
COPY poetry.lock pyproject.toml wsgi.py ./
RUN poetry config virtualenvs.create false && poetry install

FROM base as production
COPY todo_app ./todo_app
ENTRYPOINT ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:80", "wsgi:run()"]

FROM base as development
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
