## netcat-docker

CTF中netcat题目有关docker的相关构造文件。

因作为本地测试使用，不过多考虑安全性问题，以便捷性为主。

全部题目在相同环境，但是通过不同的脚本启动。题目特性化设置见`config.json`，全局设置见`global.json`。

脚本不会拷贝`config.json`至目录。

```json
{
    "apt_requirements": [],     // 需要使用 apt 安装的包
    "all_copy": true,           // 是否拷贝题目目录全部文件
    "launch": "python3",        // 启动程序
    "args": ["-u","./src.py"],  // 启动参数
    "extra_cmd": [],            // 其余需要执行的指令 (如 pip)
    "copy_files": []            // 当不全部拷贝题目文件时，需要拷贝的文件 (相对于题目目录的路径)
}
```

## 构建和运行

在根目录执行`python generate.py`

## 目前进度

- `build_yourself_in`

  一道python沙箱逃逸题目，运行时将有限制的python终端暴露给连接方。

- `tictactoe`

  Hackergame2020题目，pwn题目类型。

- `string_tools`

  Hackergame2020题目，misc题目类型。

- `calculator_never_overflow`

  Hackergame2020题目，math题目类型。

- 后期更新...
