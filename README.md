# diploma
Diploma project

## Run

### Dev environment

```bash
cd docker-compose
cp envs/dev .env
DOCKER_BUILDKIT=1 docker-compose -f prod.yml -f dev_override.yml down && DOCKER_BUILDKIT=1 docker-compose -f prod.yml -f dev_override.yml up --build
```
