FROM ubuntu

RUN apt-get update && apt-get install -y python-dev python3-dev python-pip python3-pip gcc clang wget git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip install cython && pip3 install cython

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

COPY ./install_talib.sh ./
RUN sh install_talib.sh

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
