FROM ubuntu:20.04
ENV LANG C.UTF-8

RUN sed -i s@/archive.ubuntu.com/@/{mirrors_base_url}/@g /etc/apt/sources.list

RUN useradd -m ctf

RUN apt update && apt -y upgrade
RUN apt install -y xinetd python3

# apt requirements
{apt_requirements}

# extra command
{extra_cmd}

RUN rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*

# copy problem
{copy_problem_cmd}

RUN mkdir /home/ctf/run/
RUN mkdir /home/ctf/assets/
RUN mkdir /home/ctf/files/

COPY ./download/ /home/ctf/files/

# run scripts
{run_scripts}

# chown & chmod
RUN chown -R root:root /home
RUN chmod -R 711 /home

{chmod_cmd}

# download service
WORKDIR /home/ctf/files
RUN nohup python3 -m http.server {download_port} > /var/log/file.log 2>&1 &

WORKDIR /
COPY xinetd /etc/xinetd.d/ctf

CMD ["xinetd","-dontfork"]
