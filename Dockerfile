FROM python:3.6
ARG bonum_docker_user_id='1000'
RUN apt-get clean; \
    apt-get update; \
    DEBIAN_FRONTEND=noninteractive apt-get -y install sudo apt-utils locales net-tools iputils-ping iproute2 htop mc wget ffmpeg curl nano; \
    pip install --upgrade pip; \
    pip install ipython; \
    sed -i 's/# ru_RU\.UTF-8 UTF-8/ru_RU\.UTF-8 UTF-8/' /etc/locale.gen; \
    locale-gen ru_RU.UTF-8; \
    useradd -r -m -u $bonum_docker_user_id bonum_docker_user; \
    rm -rf /tmp/*; \
    apt-get clean; \
    rm -rf /var/log/*
ENV LANG ru_RU.UTF-8

RUN mkdir /app
WORKDIR /app
ADD ./ /app/

RUN pip install -r requirements.txt
CMD run.sh
