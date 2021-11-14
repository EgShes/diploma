# diploma
Diploma project

## Run

Copy environments which are needed for docker-compose and during building

```bash
cd docker-compose
cp envs/.env .env
cat envs/<dev or prod> | grep 'POSTGRES_DB\|POSTGRES_USER' >> .env
```

As a result `.env` file should contain `COMPOSE_PROJECT_NAME`, `POSTGRES_DB`, `POSTGRES_USER`

### Prod environment

```bash
DOCKER_BUILDKIT=1 docker-compose -f prod.yml up --build --force-recreate
```

### Dev environment

```bash
DOCKER_BUILDKIT=1 docker-compose -f prod.yml -f dev_override.yml up --build --force-recreate
```
