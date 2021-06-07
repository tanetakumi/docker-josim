FROM ubuntu:20.04

LABEL maintainer="tanetakumi"

ENV DISPLAY host.docker.internal:0.0

ENV DEBIAN_FRONTEND=noninteractive

# ENV HOME /home/${USER}
ENV SHELL /bin/bash

RUN apt-get update && apt-get -y upgrade

RUN apt-get -y install build-essential

RUN apt-get -y install python3 && apt-get -y install python3-pip


RUN apt -y install git\
    && apt -y install wget\
    && apt -y install tar\
    && apt -y install vim\
    && apt -y install x11-apps\
    && apt-get -y install python3-tk


# set -ex コマンドの実行に失敗したらその場で終了する
RUN set -ex\ 
    \
    && pip install cmake\
    && git clone "https://github.com/JoeyDelp/JoSIM.git"\
    && cd JoSIM && mkdir build && cd build\
    && cmake ..\
    && cmake --build . --config Release\
    && make install

RUN set -ex\ 
    \
    && cp JoSIM/scripts/josim-plot /usr/local/bin\
    && chmod 755 /usr/local/bin/josim-plot\
    && sed -i -e "1d" josim-plot\
    && sed -i -e "1i #! /bin/python3"

RUN pip install -r requirements.txt