##
# Dockerfile -- Container Image for Debian 9.3 / Python 3.5
##
# build : docker build -f debian-python3.dockerfile -t debian-python3 .
# tag   : docker tag debian-python3 wplex/debian-python3:latest
# push  : docker push wplex/debian-python3

FROM debian:latest
LABEL maintainer="Ryan Padilha <ryan.padilha@gmail.com>"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip