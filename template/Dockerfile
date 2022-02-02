FROM python:slim as base

ENV TZ Asia/Shanghai
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -m ctf && \
    mkdir /home/ctf/run/ && \
    mkdir /var/log/ctf && \
    mkdir /home/ctf/assets/ && \
    mkdir /home/ctf/files/ && \
    sed -i s@/deb.debian.org/@/{mirrors_base_url}/@g /etc/apt/sources.list && \
    cp /lib/x86_64-linux-gnu/libc-* /home/ctf/files && \
    cp -ld /home/ctf/files/libc-* /home/ctf/files/libc.so && \
    cp /lib/x86_64-linux-gnu/ld-linux* /home/ctf/files && \
    cp -ld /home/ctf/files/ld-* /home/ctf/files/ld.so

RUN apt update && \
  apt install -y --no-install-recommends xinetd && \
  apt clean && \
  rm -rf /var/lib/apt/lists/*

# pip requirements
RUN python -m pip install {pypi_index} --no-cache-dir --upgrade pip && \
    python -m pip install {pypi_index} --no-cache-dir {pip_requirements}

# extra command
{extra_cmd}

COPY tmp/run /home/ctf/run/
COPY tmp/index.html attachments /home/ctf/files/
COPY xinetd /etc/xinetd.d/ctf
COPY tmp/start.sh /

RUN chown -R root:root /home && \
  chmod -R 711 /home && \
  chmod 710 /start.sh && \
  chmod 711 /etc/xinetd.d/ctf

WORKDIR /home/ctf
# copy problem
{copy_problem_cmd}

# chown & chmod
{chmod_cmd}

WORKDIR /

CMD ["sh","./start.sh"]
