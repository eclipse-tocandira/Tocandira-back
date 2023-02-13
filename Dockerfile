FROM python:3.9.15-alpine3.16

WORKDIR /code
RUN apk add --no-cache gcc g++ musl-dev

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir -p /code/db
COPY ./src /code/src
COPY ./config /code/config

EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.main:app", "--port", "8000" ]
