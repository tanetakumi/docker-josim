FROM python:3.9

LABEL maintainer="tanetakumi"

# ENV HOME /home/${USER}
ENV SHELL /bin/bash

WORKDIR /code

RUN apt update

RUN apt -y install build-essential\
    && apt -y install git\
    && apt -y install less\
    && apt -y install python3-tk



# set -ex コマンドの実行に失敗したらその場で終了する
# josim installation
RUN set -ex\
    && pip install cmake\
    && git clone "https://github.com/JoeyDelp/JoSIM"\
    && cd JoSIM && mkdir build && cd build\
    && cmake ..\
    && cmake --build . --config Release\
    && make install

WORKDIR /root
RUN pip install --upgrade pip

# hfq-optimizer
RUN set -ex\
    && git clone -b v1.1 "https://github.com/tanetakumi/hfq-optimizer"\
    && pip install -r hfq-optimizer/requirements.txt\
    && pip install -e hfq-optimizer/scripts/optimize

