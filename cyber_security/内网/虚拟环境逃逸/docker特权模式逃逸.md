# Docker特权逃逸

## 漏洞说明

获得目标系统shell后，发现是在对方的docker环境中时，需要通过docker逃逸来拿到真正宿主的权限

## 利用条件

docker版本小于18.09.2

## 漏洞原理

当管理员执行`docker run -privileged`时，Docker容器将被允许访问主机上的所有设备，并可以执行mount命令进行挂载。

## 漏洞复现

这里通过红日7靶场进行复现

进入交互式终端

![image-20231205185915045](http://111.229.225.13:81/i/2023/12/12/xl9keu-2.png)

现在考虑逃逸Docker,利用漏洞Docker runC漏洞逃逸和Docker特权模式逃逸，前者没有成功（需要管理员用户重新启动docker感觉条件有的严苛，并且我手动没有成功）

在docker中新建一个/hack目录挂载文件

```bash
mkdir /hack
```

然后

```bash
ls /dev
```

可以发现很多设备文件

![image-20231205203010364](http://111.229.225.13:81/i/2023/12/12/xl8x8b-2.png)

尝试将/dev/sda1挂载到/hack目录中

```bash
mount /dev/sda1 /hack
```

挂载成功后，可以通过访问/hack文件达到访问整个主机的作用

![image-20231206192257931](http://111.229.225.13:81/i/2023/12/12/xl8lxp-2.png)

