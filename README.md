# soundations

Sound recommendations project.

## Development

### Requirements

- [nodejs](https://nodejs.org/en/download/) (recommended via [nvm](https://github.com/nvm-sh/nvm#installing-and-updating))
- [poetry](https://python-poetry.org/docs/#installation)

### Create local `.env` file

```sh
cp .env.sample .env
```

### Install dependencies

```sh
./bin/install.sh
```

### Start server in development mode

```sh
./bin/start-server.sh
```

or inside docker:

```sh
rm -rf .venv
docker compose -f docker-compose.yml -f docker-compose.dev.yml build snd-server
docker compose -f docker-compose.yml -f docker-compose.dev.yml up snd-server
```

### Start client in development mode

```sh
./bin/start-client.sh
```

### Generate server API client

After making changes in `snd-server` http/api endpoints, we need to also regenerate API client library:

```sh
./bin/build-server-api-client.sh
```
