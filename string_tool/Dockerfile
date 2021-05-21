FROM ubuntu:20.04
RUN sed -i s@/archive.ubuntu.com/@/mirrors.matrix.moe/@g /etc/apt/sources.list

RUN apt update && apt -y upgrade
RUN apt install -y xinetd python3

COPY xinetd /etc/xinetd.d/ctf

RUN mkdir /home/ctf/
COPY ./ctf/* /home/ctf/

ENV LANG C.UTF-8

COPY ./run.sh /run.sh

CMD ["xinetd","-dontfork"]


