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
{pip_requirements}

# extra command
{extra_cmd}

RUN useradd -m ctf

# copy problem
{copy_problem_cmd}

RUN mkdir /home/ctf/run/
RUN mkdir /home/ctf/assets/
RUN mkdir /home/ctf/files/

COPY tmp/run /home/ctf/run

# chown & chmod
RUN chown -R root:root /home && chmod -R 711 /home

{chmod_cmd}

COPY download /home/ctf/files
COPY xinetd /etc/xinetd.d/ctf
COPY tmp/start.sh /
COPY tmp/index.html /home/ctf/files

RUN chmod +x /start.sh

WORKDIR /

CMD ["sh","./start.sh"]
