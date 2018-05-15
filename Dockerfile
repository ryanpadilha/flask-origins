#
# Dockerfile -- Container Image for Debian 9.3 / Python 3.x
#
# build : docker build -f debian-oracle-java8.dockerfile -t debian-oracle-java8 .
# tag   : docker tag debian-oracle-java8 wplex/debian-oracle-java8:latest
# push  : docker push wplex/debian-oracle-java8
#

FROM debian:latest
LABEL maintainer="Ryan Padilha <ryan.padilha@gmail.com>"

RUN \
  apt-get update \
  && apt-get install -f \
  && apt-get install -y wget gnupg \
  && apt-get install -y oracle-java8-installer \
  && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-8-oracle


RUN apt-get update \
  && apt-get install -y python3-pip python3-dev python3-venv \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

ENTRYPOINT ["python3"]

