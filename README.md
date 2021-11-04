# diploma
Diploma project

## Run

### Dev environment

```bash
cd docker-compose
cp envs/dev .env
DOCKER_BUILDKIT=1 docker-compose down && DOCKER_BUILDKIT=1 docker-compose up --build
```
