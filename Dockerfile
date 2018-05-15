##
# docker-container for Python 3.5
##
# generate-image  : docker build -t flask-origins --build-arg VERSION=1.0.0 .
# tag-image       : docker tag flask-origins wplex/flask-origins:latest
# push-image      : docker push wplex/flask-origins
##
# run-container   : docker run -d -p 8000:8000 --name flask_origins flask-origins
# container-limit : docker run --memory=750m --memory-swap=750m --oom-kill-disable -d -p 8000:8000 --name flask_origins flask-origins
##
# save-image : sudo docker save flask-origins > /var/company/devops/flask-origins-docker.tar
# load-image : docker load < /var/company/devops/flask-origins-docker.tar
##

FROM debian-python3
LABEL maintainer="Ryan Padilha <ryan.padilha@gmail.com>"

# define commonly used variables
ENV APP_DIR /var/company/www/flask-origins

ARG VERSION
ENV VERSION $VERSION

# define working directory
RUN mkdir -p /var/company/www
WORKDIR /var/company/www
ADD target/flask-origins-$VERSION.tar.gz .

EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r $APP_DIR/bin/requirements.txt
RUN mkdir -p /var/company/logs/flask-origins

ENTRYPOINT /usr/local/bin/gunicorn -w 3 --bind=0.0.0.0:8000 --user=root --log-level=debug --log-file=/var/company/logs/flask-origins/gunicorn.log 2>>/var/company/logs/flask-origins/gunicorn.log wsgi:application
