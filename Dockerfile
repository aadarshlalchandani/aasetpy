## Modify Dockerfile as per your project
## credits: aadarshlalchandani/aasetpy

FROM ubuntu:22.04
FROM python:3.11-alpine

ENV PROJECT_NAME=your_project_name

WORKDIR $PROJECT_NAME

COPY ./requirements.txt $PROJECT_NAME/requirements.txt

RUN apk add gcc python3-dev musl-dev linux-headers
RUN pip install --no-cache-dir --upgrade -r $PROJECT_NAME/requirements.txt

COPY ./src $PROJECT_NAME/src
COPY ./logs $PROJECT_NAME/logs
COPY ./main.py $PROJECT_NAME/main.py
COPY ./run.sh $PROJECT_NAME/run.sh

RUN sed -i "/env\/bin/d" $PROJECT_NAME/run.sh
RUN apk add --no-cache bash

CMD ["/bin/bash", "-c", "$PROJECT_NAME/run.sh main"]
