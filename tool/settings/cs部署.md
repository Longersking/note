# 配置搭建cs工具

## 两种方式

cs工具 =》狐狸工具箱,微信上搜索

或者[cs - OneDrive (sharepoint.com)](https://ddosi-my.sharepoint.com/personal/netsparker_ddosi_onmicrosoft_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fnetsparker_ddosi_onmicrosoft_com%2FDocuments%2F渗透测试%2Fcs%2FCobaltStrike4.8_www.ddosi.org.rar&parent=%2Fpersonal%2Fnetsparker_ddosi_onmicrosoft_com%2FDocuments%2F渗透测试%2Fcs&ga=1)提取密码**www.ddosi.org**

需要云服务器（个人猜测如果是靶场的话，可以采用一台所有主机都能访问的主机作为服务端配置）

### 非docker方式搭建

将cs整个文件上传到服务器端，这里注意，最好上传版本略低的cs工具，否则会因为服务器内核问题导致无法运行，笔者采用4.7版本，即狐狸工具箱自带的cs

安装配置java环境，我这里采用jdk

![image-20231212204938480](http://111.229.225.13:81/i/2023/12/12/xw4yt4-2.png)

进入文件夹后

赋给文件执行权限

```bash
chmod +x teamserver 
```

然后运行

```bash
./teamserver 服务器ip 服务器密码
```

运行结果

![image-20231212205338475](http://111.229.225.13:81/i/2023/12/12/xyizuq-2.png)

![image-20231212205535749](http://111.229.225.13:81/i/2023/12/12/xzovps-2.png)

用户名，密码随便写

### docker搭建

当cs版本过高时，对服务器GLIBC版本也有提高，而服务器为了稳定性，一般对应的GLIBC不会过高，盲目升级，不排除会出现意想不到的的问题,所以这时采用docker方式搭建

首先安装docker

推荐博客[Docker 安装 (完整详细版)_docker安装-CSDN博客](https://blog.csdn.net/BThinker/article/details/123358697)

配置[Docker的安装、镜像拉取、创建容器、应用部署、备份迁移-CSDN博客](https://blog.csdn.net/qq_45299673/article/details/119810149)

拉取Docker运行镜像

```bash
sudo docker pull ubuntu:20.04
docker run -d -it --network=host -p 50050:50050 --name my_container your_image
```

将宿主机中的文件复制到容器内部

```bash
docker cp /path/to/host/file_or_directory container_name:/path/inside/container
```

在docker容器中安装java环境

进入镜像

```bash
apt-get update && apt-get install -y openjdk-11-jdk
```

这里面会要求设置时区，选择亚洲，上海即可

如果前面配置没有问题的话

和非docker方式一样运行

```bash
./teamserver 服务器ip 服务器密码
```

顺便解释一下docker run -d -it --network=host -p 50050:50050 --name my_container your_image这段命令

```bash
docker 后台运行结合前台运行（-it不加的话，虽然会后台运行，但是由于没有任务执行，导致直接容器被杀） ip和主机ip地址一样，主机端口50050映射容器端口50050 命名为{你自己取名} 对应的镜像
```

查看运行的容器

```bash
docker ps
```

![image-20231212211428372](http://111.229.225.13:81/i/2023/12/12/yys3gj-2.png)

进入容器

```bash
docker exec -it 容器名|容器对应id /bin/bash
```

退出容器 按Ctrl+p 然后再按Ctrl + q

![image-20231212211550263](http://111.229.225.13:81/i/2023/12/12/yzi0j7-2.png)

不过还是建议采用服务器搭建，因为docker对新手不是很友好

