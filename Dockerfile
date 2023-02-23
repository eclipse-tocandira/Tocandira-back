FROM python:3.9.15-alpine3.16

WORKDIR /code
RUN apk add --no-cache gcc g++ musl-dev git
RUN apk add --no-cache openssh

ENV GROUP_ID=1000
ENV USER_ID=1000

RUN addgroup -g $GROUP_ID back
RUN adduser -D -u $USER_ID -G back back -s /bin/s

RUN chown -R back:back /code/
RUN chown -R back:back /home/back/

USER back
ENV PATH /home/back/.local/bin:$PATH

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN mkdir -p /code/db
COPY ./src /code/src
COPY ./config /code/config

EXPOSE 8000
ENTRYPOINT ["uvicorn", "src.main:app", "--port", "8000" ]
