FROM ubuntu:20.04

RUN apt update && apt -y upgrade
RUN apt install -y xinetd python3

COPY xinetd /etc/xinetd.d/ctf

RUN mkdir /home/ctf/

COPY ./tictactoe /home/ctf/tictactoe
COPY ./flag /home/ctf/flag
COPY ./run.sh /run.sh

CMD ["xinetd","-dontfork"]


