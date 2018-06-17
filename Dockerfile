FROM python:3

COPY ./requirements.txt ./
COPY ./install_talib.sh ./
RUN pip install --upgrade pip
RUN pip install cython
RUN cat requirements.txt | xargs -n 1 -L 1 pip install
RUN sh install_talib.sh
