

[Linux下find命令详解_linux find 命令-CSDN博客](https://blog.csdn.net/l_liangkk/article/details/81294260)

目前已用

- ```bash
  find . -type f /var/www/html/webadmin/S0mextras #在当前目录和指定目录下查找普通文件 
  ```

- ```bash
  find / -perm -u=s -type f 2>/dev/null #从根目录查找 具有root权限的二进制普通文件，并且不会显错误
  ```

- ```bash
  find / -name flag* #从根目录查找文件名前4个字符为flag的文件
  ```

- 

# find命令

- 基本格式

  ```bash
  find   path  -option  【 -print 】  【 -exec   -ok   c  |grep  】 【  command  {} \;  】
  ```

  

- path 要寻找的目录

- print 将结果输出到标准输出

- exec 对匹配的文件执行该参数所给出的shell命令

- ok与exec参数一样，区别在于，在执行命令前会给出提示

- |xargs 与exec作用相同，不过主要用来删除操作

- options采用选项

  ```
  -name   filename               #查找名为filename的文件
  -perm                                #按执行权限来查找
  -user    username             #按文件属主来查找
  -group groupname            #按组来查找
  -mtime   -n +n                   #按文件更改时间来查找文件，-n指n天以内，+n指n天以前
  -atime    -n +n                   #按文件访问时间来查找文件，-n指n天以内，+n指n天以前
  -ctime    -n +n                  #按文件创建时间来查找文件，-n指n天以内，+n指n天以前
  -nogroup                          #查无有效属组的文件，即文件的属组在/etc/groups中不存在
  -nouser                            #查无有效属主的文件，即文件的属主在/etc/passwd中不存
  -type    b/d/c/p/l/f             #查是块设备、目录、字符设备、管道、符号链接、普通文件
  -size      n[c]                    #查长度为n块[或n字节]的文件
  -mount                            #查文件时不跨越文件系统mount点
  -follow                            #如果遇到符号链接文件，就跟踪链接所指的文件
  -prune                            #忽略某个目录
  ```

  