# nmap常用命令

- ```bash
  nmap -T4 -sV -O -A -Pn //-T4(速度) -sV(版本扫描和开启的服务) -O(操作系统) -p-（所有端口）-Pn     将所有主机视为在在线，跳过主机发现
  ```

- ```bash
  nmap -A -p1-65535 //全端口扫描
  ```

- ```shell
  nmap -sS -sV // -sS 半开放式扫描，快且不易留迹 -sV探测服务
  ```

- ```shell
  nmap -F //扫描较少的常用端口（nmap-services 文件中定义的前100个端口）
  ```

- ```shell
  nmap -p-  //全端口扫描
  ```

- ```shell
  nmap -O //操作系统
  ```

- ```shell
  nmap -sC //脚本探测
  ```

- ```shell
  nmap -A //高级检测包括操作系统检测、版本检测、脚本扫描和traceroute。
  ```

- 

- 