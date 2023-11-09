###  WEB架构

- 开发语言&中间件&数据库&操作系统
- web源码
- web域名&子域名&相似域名&反查域名&旁注

### 信息点

- 基础信息
- 系统信息
- 应用信息
- 人员信息
- 其他信息

### 技术点

- CMS识别
- 端口扫描
- CDN绕过
- 源码获取
- 子域名查询
- WAF识别
- 负载均衡识别

1. 直接采用浏览器的F12抓包判断网站语言，中间件和CMS

2. 操作系统判断可以通过ping命令已

3. 经访问网站时采用大小写区分判断，windows不区分大小写，linux区分

4. 判断数据库，根据中间件搭配，以及端口扫描

5. 寻找cms历史漏洞，去对应官网上下载对应源码，进行分析

   举例

   <img src="C:\Users\longersking\AppData\Roaming\Typora\typora-user-images\image-20231030213350857.png" alt="image-20231030213350857" style="zoom:100%;" />

   据图可知开发语言为ASP.NET,中间件为nginx，同时可以推测出操作系统为windows因为asp.net只能在windows服务器上使用，而其常常与mssql数据库搭配

   

