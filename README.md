## netcat-docker

CTF中netcat题目有关docker的相关构造文件。

## 构建和运行

在对应目录执行`docker compose up --build -d`

## 目前进度

- `build_yourself_in`

  一道python沙箱逃逸题目，运行时将有限制的python终端暴露给连接方。

  默认连接：`nc 127.0.0.1 65101`

- `tictactoe`

  Hackergame2020题目，pwn题目类型。

  默认连接：`nc 127.0.0.1 65102`

- `string_tools`

  Hackergame2020题目，misc题目类型。

  默认连接：`nc 127.0.0.1 65103`

- `calculator_never_overflow`

  Hackergame2020题目，math题目类型。

  默认连接：`nc 127.0.0.1 65104`

- 后期更新...
