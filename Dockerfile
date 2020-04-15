FROM ubuntu
MAINTAINER lpshkn

RUN apt-get update && apt-get install -y python3 && apt-get install -y python3-setuptools \
&& apt-get install -y python3-pip

COPY . /wordanalyzer
WORKDIR /wordanalyzer

RUN python3 setup.py install && python3 setup.py test  

