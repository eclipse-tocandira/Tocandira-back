FROM python:3.9

WORKDIR /code

COPY requirements.txt /code/requirements.txt
COPY ./src /code/src

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir -p /code/db

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]