FROM ubuntu:20.04
ENV LANG C.UTF-8

RUN sed -i s@/archive.ubuntu.com/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list

RUN apt update && apt -y upgrade
RUN apt install -y xinetd python3

COPY xinetd /etc/xinetd.d/ctf

RUN mkdir /home/ctf/
COPY ./ctf/* /home/ctf/

COPY ./run.sh /run.sh

CMD ["xinetd","-dontfork"]
