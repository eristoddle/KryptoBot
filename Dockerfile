FROM python:3

COPY ./requirements.txt ./
RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
# To install in order
RUN cat requirements.txt | xargs -n 1 -L 1 pip install
