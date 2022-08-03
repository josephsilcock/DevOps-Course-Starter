# Docker

We have configuration files set up for using Docker (to install docker, follow the instructions 
[here](https://docs.docker.com/get-docker/))

## Development

### Using Docker Compose

Simply run:
```bash
docker compose up -d
```
> **_NOTE:_**  This includes a MongoDb image, and will connect to this, ignoring the value for 
> `MONGODB_CONNECTION_STRING` in the env file.

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

## MongoDB

To create the MongoDB image, run: 
```bash
docker pull mongo
```

To run the image:
```bash
docker run -d -p 27017:27017 --name todo-mongo mongo:latest
```

Setting the `MONGODB_CONNECTION_STRING` environment variable to `mongodb://localhost:27017` will then connect to this 
database