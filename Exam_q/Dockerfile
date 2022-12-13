# pull official base image
FROM python:3.9.5-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install -r requirements.txt
RUN apk add --no-cache texlive-full
#RUN tlmgr update --self && tlmgr install sectsty lastpage helvetic
RUN apk add --no-cache poppler-utils
# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]