# CTF-nc-docker

[English](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/README.md) | [中文文档](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/README.zh_cn.md)

## Build and run

After installing docker, clone this repository and run `python generate.py` or `python3 generate.py` in it.

The logs generated during the running can be got from `/var/log/ctf/*.log` and `/var/log/server.log` inside the container. If the attached files download service is enabled, you can view all the challenges and their corresponding ports via `http://{hostname}:{download_port}`. If the web netcat service is enabled, you can connect to it via `http://{hostname}:{download_port}/wnc`. When running the script for the first time, `global.json` will be generated in the current folder, and please operate following the prompts in the script.

The environment includes `python` and `nodejs`, so challenges based on them and binary challenges are supported.
## Configuration

Edit `global.json` for global configuration, and `config.json` in each challenge directory for challenge specific configuration.

### global.json

```json
{
    "mirrors_base_url": "mirrors.tuna.tsinghua.edu.cn",
    "pypi_index_url": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "npm_mirror_url": "http://registry.npmmirror.com/",
    "port_range_start": 65100,
    "show_download_host": true,
    "download_url": "http://localhost:65199",
    "download_server": true,
    "web_netcat_server": true,
    "server_port": 65199,
    "show_echo_msg": true,
    "show_warn_msg": true,
    "resource_limit": {
        "enable": true,
        "max_memory": "512M",
        "max_cpu": "0.5"
    }
}
```

- `mirrors_base_url`: Debian mirror source (domain)
- `pypi_index_url`: PyPI package source
- `npm_mirror_url`: NPM package source
- `port_range_start`: The start port for the range of ports for challenges
- `show_download_host`: Show the download host in the challenge echo message
- `download_url`: The download url shown in the challenge echo message
- `download_server`: Whether to enable the download server
- `web_netcat_server`: Whether to enable the web netcat server
- `server_port`: The port of the download server
- `show_echo_msg`: Whether to show the echo message
- `show_warn_msg`: Whether to show the warning message
- `resource_limit`: Configuration for resource limit
  - `enable`: Whether to enable resource limit
  - `max_memory`: The maximum memory usage
  - `max_cpu`: The maximum CPU usage
### config.json

```json
{
    "enable": true,
    "pip_requirements": [],
    "apt_requirements": [],
    "all_copy": true,
    "launch": "python3",
    "args": ["-u", "./src.py"],
    "extra_cmd": [],
    "copy_files": [],
    "echo_msg": ["Write some descr here."],
    "download_file_name": "",
    "order": 10
}
```

- `enable`: Whether to enable this challenge
- `pip_requirements`: The requirements for pip packages
- `apt_requirements`: Extra apt packages
- `all_copy`: Whether to copy all files in the challenge directory (`config.json` is not included)
- `launch`: The launch command
- `args`: The arguments for the launch command
- `extra_cmd`: The extra commands to run when build the challenge
- `copy_files`: The files to copy to the container (when `all_copy` is false)
- `echo_msg`: The echo message
- `download_file_name`: The file name of the challenge file
- `order`: Specific the order of the challenge (port order)

## Notice

Do not put the dictionary with the same name as the challenge in the same directory!

For more information, please refer to the [CTF-nc-docker 配置指南](https://blog.gztime.cc/posts/2022/ac35dae6) (chinese only).

## Examples

- `tictactoe`

  A pwn challenge from Hackergame 2020.

- `calculator_never_overflow`

  A math challenge from Hackergame 2020.

- `unboxing_simulator`

  A math challenge from Hackergame 2020.

- `cosmic_ray_simulator`

  A pwn challenge from Hackergame 2020.

- `self_repeating_repeater`

  A misc challenge from Hackergame 2020.

## Images

![](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/images/problems.jpg)

![](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/images/webnc_portal.jpg)

![](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/images/webnc.jpg)
