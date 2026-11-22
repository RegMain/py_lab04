FROM alpine:3.24.4

WORKDIR /app

LABEL org.opencontainers.image.source=https://github.com/regmain/py_lab04

COPY ./src/py_lab04/sort.py ./src/py_lab04/benchmark.py /app/py_lab04/
