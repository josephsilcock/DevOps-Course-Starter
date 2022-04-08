# Docker

We have configuration files set up for using Docker (to install docker, follow the instructions 
[here](https://docs.docker.com/get-docker/))

## Development

### Using Docker Compose

Simply run:
```bash
docker compose up -d
```

### Manually

Create the image by running:
```bash
docker build --target development --tag todo-app:dev .
```

Then run the image by running:
#### UNIX systems (and powershell)
```bash
docker run -d -p 5000:5000 --env-file ./.env --mount type=bind,source="$(pwd)"/todo_app,target=/todo-app/todo_app todo-app:dev
```

#### Windows (CMD)
```bash
docker run -d -p 5000:5000 --env-file ./.env --mount type=bind,source=C:\Path\To\App\todo_app,target=/todo-app/todo_app todo-app:dev
```

## Production

To create the docker image run:
```bash
docker build --target production --tag todo-app:prod .
```

To run the image:
```bash
docker run -d -p 5000:80 --env-file ./.env todo-app:prod
```
