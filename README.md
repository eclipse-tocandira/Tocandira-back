# Backend
This repository contains a pre-configured version of a FastAPI application build using SQLite as the database to do the internal processes of the Data Collector.

## Dependencies
This repository is a docker image. To use it one will need:
```
$ sudo apt install docker docker.io
```
Also some configurations regarding the addition of your user to the docker group may be needed.
```
$ sudo usermod -aG docker $USER
```
After the execution of the past command a Logout and Login is needed.

## Building the image
```
$ docker build -t backend:<tag> .
```
With:
- `<tag>`: as the image version, i.e. `0.1.0`

## Running the image
Once the image is in docker, to run this frontend use:
```
$ docker run -p 8000:8000 backend:<tag> --host 0.0.0.0
```
With:
- `<tag>`: as the image version, i.e. `0.1.0`
