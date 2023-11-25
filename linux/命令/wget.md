# wget命令

## 摘要：[linux wget 命令用法详解(附实例说明) - Rooker - 博客园 (cnblogs.com)](https://www.cnblogs.com/lukelook/p/11201098.html)

## 目前已用:

下载单个文件并且保存在当前目录

```bash
wget http://example.com
```

`-S` 选项在执行 `wget` 命令时会将服务器响应的 HTTP 头信息输出到控制台。这些信息包括服务器响应的 HTTP 状态码、日期、内容类型、大小等等。这个选项可以帮助你更详细地了解与所下载文件相关的服务器信息，如是否成功连接到服务器、文件大小、服务器类型等等

```bash
wget -S http://example.com
```



常用参数

```
-i url.txt #批量下载存放在url.txt中的文件链接
 –user-agent=”Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.204 Safari/534.16″ #伪造头
 -b #后台下载
 -c #断点下载
 -O #下载以不同的文件名保存，wget默认会以最后一个符合”/”的后面的字符来命令，对于动态链接的下载通常文件名会不正确。 
错误：下面的例子会下载一个文件并以名称download.php?id=1080保存 

wget http://www.centos.bz/download?id=1 
即使下载的文件是zip格式，它仍然以download.php?id=1080命令。
wget -O wordpress.zip http://www.centos.bz/download.php?id=1080 
```



