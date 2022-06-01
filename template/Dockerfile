FROM nikolaik/python-nodejs:python3.10-nodejs18-slim as final

ENV TZ Asia/Shanghai
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN useradd -m ctf && \
    mkdir /home/ctf/run/ && \
    mkdir /var/log/ctf && \
    mkdir /home/ctf/assets/ && \
    sed -i s@/deb.debian.org/@/{mirrors_base_url}/@g /etc/apt/sources.list && \
    sed -i s@/security.debian.org/@/{mirrors_base_url}/@g /etc/apt/sources.list && \
    npm config set registry {npm_mirror_url}

RUN apt update && apt upgrade -y &&\
  apt install -y --no-install-recommends xinetd {apt_requirements} &&\
  apt clean && rm -rf /var/lib/apt/lists/*

# pip requirements
RUN python -m pip install {pypi_index} --no-cache-dir --upgrade pip && \
    python -m pip install {pypi_index} --no-cache-dir {pip_requirements}

# extra command
{extra_cmd}

COPY tmp/run /home/ctf/run/
COPY web/favicon.ico /home/ctf/web/static/
COPY xinetd /etc/xinetd.d/ctf
COPY tmp/start.sh /

RUN chown -R root:root /home && \
  chmod -R 711 /home && \
  chmod 710 /start.sh && \
  chmod 711 /etc/xinetd.d/ctf

WORKDIR /home/ctf
# copy challenge
{copy_challenge_cmd}

# chown & chmod
{chmod_cmd}

WORKDIR /

CMD ["sh","./start.sh"]
