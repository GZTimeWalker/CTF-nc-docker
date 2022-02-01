## netcat-docker

CTF中netcat题目有关docker的相关构造文件。

因作为本地测试使用，不过多考虑安全性问题，以便捷性为主。后续计划使用 `chroot` 进行进一步加固。

全部题目在相同环境，但是通过不同的脚本启动。题目特性化设置见`config.json`，全局设置见`global.json`。

脚本不会拷贝`config.json`至目录。

## 配置说明

### `global.json`

```json
{
    "mirrors_base_url": "mirrors.tuna.tsinghua.edu.cn",
    "pypi_index_url": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "port_range_start": 65100,
    "download_port": 65199,
    "hostname": "localhost",
    "download_server": true,
    "show_echo_msg": true,
    "show_warn_msg": true
}
```

`mirrors_base_url`: Debian软件源

`pypi_index_url`: pypi 软件源

`port_range_start`: 起始端口号

`download_port`: 文件下载服务所开放的端口

`hostname`: 访问该容器的主机名

`download_server`: 是否开启文件下载服务

`show_echo_msg`: 显示题目信息

`show_warn_msg`: 显示警告信息

### `config.json`

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
    "download_file_name": ""
}
```

`enable`: 是否启用该题目

`pip_requirements`: 需要使用 pip 安装的包

`all_copy`: 是否拷贝题目目录全部文件

`launch`: 启动程序

`args`: 启动参数

`extra_cmd`: 其余需要执行的指令 (如 pip)

`copy_files`: 当不全部拷贝题目文件时，需要拷贝的文件 (相对于题目目录的路径)

`echo_msg`: 执行程序前输出的说明

`download_file_name`: 提供需要下载的题目文件

## 构建和运行

在根目录执行`python generate.py`

## 示例题目

- `build_yourself_in`

  一道python沙箱逃逸题目，运行时将有限制的python终端暴露给连接方。

- `tictactoe`

  Hackergame2020题目，pwn题目类型。
  使用栈溢出进行执行流控制，同时可通过构造 rop chain 进行 getshell。无 `canary` 栈溢出防护。

- `string_tools`

  Hackergame2020题目，misc题目类型。
  一些在字符串格式转换和编解码中的小技巧。

- `calculator_never_overflow`

  Hackergame2020题目，math题目类型。
  较为基础的一道密码学题目，[可见这里](https://crypto.stackexchange.com/questions/34061/factoring-large-n-given-oracle-to-find-square-roots-modulo-n)

- `theorem_prover`

  Hackergame2020题目，math题目类型。
  搜索与暴力

- `unboxing_simulator`

  Hackergame2020题目，math题目类型。
  建议手写 bfcode

- `cosmic_ray_simulator`

  Hackergame2020题目，pwn题目类型。
  这是无穷的宇宙射线。

- `self_repeating_repeater`

  Hackergame2020题目，misc题目类型。

- `man_in_the_middle`

  Hackergame2020题目，crypto题目类型。

- 后期更新...

## 注意事项

题目目录下不要再出现以题目名称命名的文件夹！
