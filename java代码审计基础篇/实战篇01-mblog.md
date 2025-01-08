# Java代码审计01 - mblog 

## 1.部署

[mblog: mblog开源免费的博客系统, Java语言开发, 支持mysql/h2数据库, 采用spring-boot、jpa、shiro、bootstrap等流行框架开发](https://gitee.com/mtons/mblog)

同时使用idea 根据pom.xml自动配置

有些组件无法直接使用maven安装则采用手动下载到本地

如lombok1.18.4版本则可以去https://projectlombok.org/download.html 下载安装

```cmd
mvn install:install-file -Dfile=lombok-1.18.4.jar -DgroupId=org.projectlombok -DartifactId=lombok -Dversion=1.18.4 -Dpackaging=jar
```



使用

## 2.代码审计

### 首先查看配置文件pom.xml

![image-20241201225053378](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241201225053378.png)

可以发现使用这些组件可能存在问题

```
h2
fastjson
shiro
```

### 逐步分析

根据h2组件查找相关配置

![image-20241201230635401](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241201230635401.png)

#### 01、h2 database未授权访问

![image-20241201231902089](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241201231902089.png)

使用jndi工具生成

![image-20241201235401551](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241201235401551.png)

![image-20241201235716977](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241201235716977.png)

#### 02、fastjson 反序列化测试

![image-20241202001218666](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202001218666.png)

版本![image-20241202001230413](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202001230413.png)

未找到poc

此版本fastjson较为安全

03、shiro 测试

发现了疑似key的生成地方

![image-20241202002514104](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202002514104.png)

但是并没有利用成功

![image-20241202002534495](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202002534495.png)

至此配置组件的历史漏洞分析完毕

### 分析owasp top10常见漏洞

#### 01.xxe

危险函数查找

```cmd
javax.xml.parsers.DocumentBuilder
javax.xml.stream.XMLStreamReader
org.jdom.input.SAXBuilder
org.jdom2.input.SAXBuilder
javax.xml.parsers.SAXParser
org.dom4j.io.SAXReader 
org.xml.sax.XMLReader
javax.xml.transform.sax.SAXSource 
javax.xml.transform.TransformerFactory 
javax.xml.transform.sax.SAXTransformerFactory 
javax.xml.validation.SchemaFactory
javax.xml.bind.Unmarshaller
javax.xml.xpath.XPathExpression
```

未找到

#### 02.反序列化

未找到存在漏洞的相关组件

#### 0.3ssrf

危险函数查找

```
HttpClient.execute
HttpClient.executeMethod
HttpURLConnection.connect
HttpURLConnection.getInputStream
URL.openStream
HttpURLConnection
```

这里发现了对应的危险函数存在，出现在HttpKit.java类中

![image-20241202004116586](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202004116586.png)

查看此接口

![image-20241202004243798](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202004243798.png)

发现是有url参数，尝试再寻找以下HttpKit的实例化情况

![image-20241202004327903](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202004327903.png)

![image-20241202004357857](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202004357857.png)

再去找Oauth的实例化

![image-20241202004604064](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202004604064.png)

发现有控制器，尝试去控制器里碰碰运气

![image-20241202005009468](W:\note\java代码审计基础篇\实战篇01-mblog\image-20241202005009468.png)

发现接口不可控制，遂放弃

#### 0.4rce

危险函数查找，未找到

```
Runtime.exec
ProcessBuilder.start
GroovyShell.evaluate
```

