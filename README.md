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

## Tests

### Unit tests

```bash
pytest -vv tests/unit
```

### Functional tests of db api

```bash
DOCKER_BUILDKIT=1 docker-compose -f test_functional.yml up --build --force-recreate -V --exit-code-from tests
```

### Integration tests

```bash
DOCKER_BUILDKIT=1 docker-compose -f prod.yml -f test_integration_override.yml up --build -V --exit-code-from tests
```

## Dumps

### Make dump

```bash
docker exec -i diploma_db_1 /bin/bash -c "PGPASSWORD=postgres pg_dump --username postgres texts" > dumps/dump.sql
```

### Restore dump

```bash
docker exec -i diploma_db_1 /bin/bash -c "PGPASSWORD=postgres psql --username postgres texts" < dumps/dump.sql
```
