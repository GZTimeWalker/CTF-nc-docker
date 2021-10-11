FROM python:slim as base

ENV TZ Asia/Shanghai
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN sed -i s@/archive.ubuntu.com/@/{mirrors_base_url}/@g /etc/apt/sources.list

RUN apt update && \
  apt install -y --no-install-recommends xinetd && \
  apt clean && \
  rm -rf /var/lib/apt/lists/*

# pip requirements
RUN python -m pip install --no-cache-dir {pip_requirements}

# extra command
{extra_cmd}

RUN useradd -m ctf

RUN mkdir /home/ctf/run/
RUN mkdir /home/ctf/assets/
RUN mkdir /home/ctf/files/
RUN cp /lib/x86_64-linux-gnu/libc-* /home/ctf/files && \
  cp -ld /home/ctf/files/libc-* /home/ctf/files/libc

COPY tmp/run /home/ctf/run
COPY download /home/ctf/files
COPY xinetd /etc/xinetd.d/ctf
COPY tmp/start.sh /
COPY tmp/index.html /home/ctf/files

RUN chown -R root:root /home && \
  chmod -R 711 /home && \
  chmod 710 /start.sh && \
  chmod 711 /etc/xinetd.d/ctf

# copy problem
{copy_problem_cmd}

# chown & chmod

{chmod_cmd}

WORKDIR /

CMD ["sh","./start.sh"]
