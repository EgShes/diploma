FROM python:3.8

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip

COPY requirements/database.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /code

# TODO use multi-stage bulid to make it insalled only in dev containers
COPY requirements/dev.txt requirements_dev.txt
RUN pip install -r requirements_dev.txt

COPY src /code/src/

CMD ["uvicorn", "src.database.main:app", "--host", "0.0.0.0", "--port", "8000"]
