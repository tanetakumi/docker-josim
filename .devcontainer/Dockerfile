FROM python:3.9

LABEL maintainer="tanetakumi"

ENV DISPLAY host.docker.internal:0.0

ENV DEBIAN_FRONTEND=noninteractive

# ENV HOME /home/${USER}
ENV SHELL /bin/bash

WORKDIR /code

COPY requirements.txt /code

COPY scripts /code

RUN pip install --upgrade pip

RUN pip install -e simplot

RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install build-essential\
    && apt -y install git\
    && apt -y install x11-apps\
    && apt-get -y install python3-tk

RUN pip install -r requirements.txt

# set -ex コマンドの実行に失敗したらその場で終了する
RUN set -ex\
    && pip install cmake\
    && git clone "https://github.com/JoeyDelp/JoSIM"\
    && cd JoSIM && mkdir build && cd build\
    && cmake ..\
    && cmake --build . --config Release\
    && make install


