FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY ./src /code/src

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir -p /code/db

EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.main:app", "--port", "8000" ]