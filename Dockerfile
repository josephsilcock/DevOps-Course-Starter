FROM python:3.7-slim-buster
WORKDIR /todo-app
RUN pip3 install poetry
COPY poetry.lock pyproject.toml wsgi.py ./
RUN poetry config virtualenvs.create false && poetry install
COPY todo_app ./todo_app
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:80", "wsgi:run()"]