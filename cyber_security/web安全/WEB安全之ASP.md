## WEB安全之ASP

### ASP安全

- asp建站经典组合

  windows iis asp access(操作系统、中间件、开发语言、数据库)\

  access数据库 一般后缀名 asp asa mdb(可下载) 

- mdb文件在网站目录下

  #### 思路：如果知道数据库地址，可以尝试下载MDB文件

- asp文件

  如果是asp文件可以尝试留马比如留言板中上传一句话木马

-  IIS短文件名漏洞

  允许攻击者在web根目录下公开文件和文件夹名称，使攻击者可以找到一些敏感文件

  受影响版本

  IIS 1.0，Windows NT 3.51 
  IIS 3.0，Windows NT 4.0 Service Pack 2 
  IIS 4.0，Windows NT 4.0选项包
  IIS 5.0，Windows 2000 
  IIS 5.1，Windows XP Professional和Windows XP Media Center Edition 
  IIS 6.0，Windows Server 2003和Windows XP Professional x64 Edition 
  IIS 7.0，Windows Server 2008和Windows Vista 
  IIS 7.5，Windows 7（远程启用<customErrors>或没有web.config）

  IIS 7.5，Windows 2008（经典管道模式）

  #### 漏洞危害

  可利用“~”字符猜解暴露短文件名/文件夹名	

- iis写权限漏洞

  原因：对iis服务器没有设置好

  判断漏洞是否存在，向服务器发送http://服务器地址/no-such-file.dll

  随便写的文件名，若服务器访问500内部错误则说明这个目录的**执行写入是开着的**

  若返回404则没有漏洞则**没有写入权限**

  

- iis解析漏洞

  以*.asp命名的文件夹，文件夹中所有的文件均以asp文件解析

  以*.asp;jpg文件(;后面任意文件)都会按照 *.asp文件解析

  版本iis6.0

  当开启cgi.fix_pathinfo功能时

  访问*.jpg/.php文件iis服务器会将该文件交给php处理,最后以php的方式解析jpg

  

  

  

  ​	

  
