#! /bin/bash

apt-get update

apt-get -y install build-essential python3-pip cmake


git clone "https://github.com/JoeyDelp/JoSIM"\
    && cd JoSIM\
    && mkdir build\ 
    && cd build\
    && cmake ..\
    && cmake --build . --config Release\
    && make install
    
git clone "https://github.com/tanetakumi/hfq-optimizer"\
    && pip install -r hfq-optimizer/requirements.txt\
    && pip install -e hfq-optimizer/scripts/optimize\
    pip install ipykernel\
