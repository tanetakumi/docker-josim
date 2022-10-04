FROM python:3.9-slim-buster

LABEL maintainer="tanetakumi"

# ENV HOME /home/${USER}
ENV SHELL /bin/bash

WORKDIR /code

# install essential packages
RUN set -ex\
    && apt-get update\
    && apt-get -y install build-essential git less python3-tk

# install josim
RUN set -ex\
    && pip install --upgrade pip\
    && pip install cmake\
    && git clone "https://github.com/JoeyDelp/JoSIM"\
    && cd JoSIM && mkdir build && cd build\
    && cmake ..\
    && cmake --build . --config Release\
    && make install

# install hfq-optimizer
WORKDIR /src

RUN set -ex\
    && pip install ipykernel\
    && git clone "https://github.com/tanetakumi/hfq-optimizer"\
    && pip install -r hfq-optimizer/requirements.txt\
    && pip install -e hfq-optimizer/scripts/optimize