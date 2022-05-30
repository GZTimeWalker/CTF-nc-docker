# CTF-nc-docker

[English](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/README.md) | [中文文档](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/README.zh_cn.md)

## 构建和运行

在安装好 docker 后，克隆本仓库到本地并在根目录执行 `python generate.py` 或 `python3 generate.py`。

运行过程中产生的访问日志可以由容器内目录的 `/var/log/ctf/*.log` 获取。若开启文件附件下载服务，则可以通过 `http://{hostname}:{download_port}` 查看到全部题目及其对应端口。若开启网络 netcat 终端服务，则可以通过 `http://{hostname}:{download_port}/wnc` 进行连接。初次运行脚本会在根目录生成 `global.json`，请根据脚本提示进行操作。

环境中自带 `python` 与 `nodejs`，支持基于他们的题目及二进制题目。

## 配置说明

全局设置见 `global.json`，题目特意化设置见各题目文件夹中的 `config.json`。

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

- `mirrors_base_url`: Debian 软件源（域名）
- `pypi_index_url`: PyPI 软件源
- `npm_mirror_url`: NPM 软件源
- `port_range_start`: 起始端口号
- `show_download_host`: 是否在题目echo信息中显示下载服务器地址
- `download_url`: 显示在下载位置的服务器地址
- `download_server`: 是否开启文件下载服务
- `web_netcat_server`: 是否开启网络 netcat 终端服务
- `server_port`: 服务器端口
- `show_echo_msg`: 显示题目信息
- `show_warn_msg`: 显示警告信息
- `resource_limit`: 运行时容器资源限制
  - `enable`: 是否启用限制
  - `max_memory`: 最大占用内存
  - `max_cpu`: 最大占用CPU
### config.json

```json
{
    "enable": true,
    "pip_requirements": [],
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

- `enable`: 是否启用该题目
- `pip_requirements`: 需要使用 pip 安装的包
- `all_copy`: 是否拷贝题目目录全部文件 (不拷贝`config.json`)
- `launch`: 启动程序
- `args`: 启动参数
- `extra_cmd`: 其余需要执行的指令 (如 pip)
- `copy_files`: 当不全部拷贝题目文件时，需要拷贝的文件 (相对于题目目录的路径)
- `echo_msg`: 执行程序前输出的说明
- `download_file_name`: 提供需要下载的题目文件
- `order`: 题目顺序，用于端口分配

## 注意事项

题目目录下不要再出现以题目名称命名的文件夹！

更多信息请参见：[CTF-nc-docker 配置指南](https://blog.gztime.cc/posts/2022/ac35dae6)

## 示例题目

- `tictactoe`

  Hackergame2020题目，pwn题目类型。

- `calculator_never_overflow`

  Hackergame2020题目，math题目类型。

- `unboxing_simulator`

  Hackergame2020题目，math题目类型。

- `cosmic_ray_simulator`

  Hackergame2020题目，pwn题目类型。

- `self_repeating_repeater`

  Hackergame2020题目，misc题目类型。

## 图片展示

![](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/images/problems.jpg)

![](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/images/webnc_portal.jpg)

![](https://github.com/GZTimeWalker/CTF-nc-docker/blob/master/images/webnc.jpg)
