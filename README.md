## netcat-doceker

CTF中netcat题目有关docker的相关构造文件。

从简单到复杂的docker构造文件逐渐更新，目前进度：

- 直接可以访问
  - `build_yourself_in`

    一道python沙箱逃逸题目，运行时将有限制的python终端暴露给连接方。

    默认连接：`nc 127.0.0.1 65101`

  - `tictactoe`
  
    Hackergame2020题目，pwn题目类型。

    默认连接：`nc 127.0.0.1 65102`

- 后期更新...
