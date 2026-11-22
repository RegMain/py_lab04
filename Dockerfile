FROM alpine:3.24.4

WORKDIR /app

LABEL org.opencontainers.image.source=https://github.com/regmain/py_lab04

COPY ./src/py_lab04/sort.py ./src/py_lab04/benchmark.py ./src/py_lab04/data_generator.py ./src/py_lab04/__init__.py /app/src/py_lab04/

RUN apk add --no-cache python3 vim

ENV PYTHONPATH="/app/src"
