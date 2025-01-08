# 红日4



1、struct 2 rce 

![image-20241011192340820](W:\note\cyber_security\靶场\hongri\vulnstack-4\image-20241011192340820.png)

![image-20241011192352802](W:\note\cyber_security\靶场\hongri\vulnstack-4\image-20241011192352802.png)

确认docker容器环境

```shell
ls -alh /.dockerenv
cat /proc/1/cgroup

```

判断是否存在特权逃逸

````shell
cat /proc/self/status |grep Cap
````

![image-20241011192621055](W:\note\cyber_security\靶场\hongri\vulnstack-4\image-20241011192621055.png)

如果是以特权模式启动的话，CapEff对应的掩码值应该为0000003fffffffff。

访问2002端口，发现伟tomcacve-cve-2017-12615

上冰蝎马

![image-20241011194524807](W:\note\cyber_security\靶场\hongri\vulnstack-4\image-20241011194524807.png)

发现还是在docker中，看看能否逃逸

```shell
fdisk -l
```

![image-20241011194651194](W:\note\cyber_security\靶场\hongri\vulnstack-4\image-20241011194651194.png)

```shell
mkdir /julien
```

