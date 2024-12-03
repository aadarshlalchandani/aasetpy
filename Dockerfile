## Modify DOckerfile as per your project

FROM ubuntu:22.04
FROM python:3.11-alpine

WORKDIR /prj_name

COPY ./requirements.txt /prj_name/requirements.txt

RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install --no-cache-dir --upgrade -r /prj_name/requirements.txt

COPY ./src /prj_name/src
COPY ./logs /prj_name/logs
COPY ./main.py /prj_name/main.py
COPY ./run.sh /prj_name/run.sh

RUN sed -i "/env\/bin/d" /prj_name/run.sh
RUN apk add --no-cache bash

CMD ["/bin/bash", "-c", "/prj_name/run.sh main"]