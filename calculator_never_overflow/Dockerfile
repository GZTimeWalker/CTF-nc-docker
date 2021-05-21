FROM python:3.8-slim

RUN sed -i s@/deb.debian.org/@/mirrors.tuna.tsinghua.edu.cn/@g /etc/apt/sources.list

RUN apt update && apt -y upgrade
RUN apt install -y xinetd

RUN pip install -U sympy

COPY xinetd /etc/xinetd.d/ctf

RUN mkdir /home/ctf/
COPY ./ctf/* /home/ctf/

COPY ./run.sh /run.sh

CMD ["xinetd","-dontfork"]
