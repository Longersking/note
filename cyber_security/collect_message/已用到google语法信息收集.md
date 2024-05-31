﻿﻿1. site

  ```
  域名搜索
  site:edu.cn 
  ```


2.filetype

```
文件后缀搜索
filetype:doc
```

3.Index of,inurl,allinurl

```
目录搜索
Index of /passwd
inurl:.bash_history
inurl:config.txt
最基本的edu的网站后缀
inurl:login|admin|manage|member|admin_login|login_admin|system|login|user|main|cms
查找文本内容：
site:域名 intext:管理|后台|登陆|用户名|密码|验证码|系统|帐号|admin|login|sys|managetem|password|username
查找可注入点：
site:域名 inurl:aspx|jsp|php|asp
查找上传漏洞：
site:域名 inurl:file|load|editor|Files
找eweb编辑器：
site:域名 inurl:ewebeditor|editor|uploadfile|eweb|edit
存在的数据库：
site:域名 filetype:mdb|asp|#
查看脚本类型：
site:域名 filetype:asp/aspx/php/jsp
迂回策略入侵：
inurl:cms/data/templates/images/index/
```

4.intext

```
内容搜索
intext:工号
```
