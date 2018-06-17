FROM python:3

COPY ./install_talib.sh ./
RUN sh install_talib.sh

COPY ./requirements.txt ./
RUN pip install --upgrade pip
RUN pip install cython
RUN pip install --no-cache-dir -r requirements.txt
