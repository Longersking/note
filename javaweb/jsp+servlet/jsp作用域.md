# jsp四大域对象

### page

只在当前页面有效，跳转后无效

### request

服务器跳转有效，客户端发生跳转无效，（因为客户端跳转，相当于发生两次跳转）

### session

保存在浏览器会话中，服务器或客户端跳转均有效，改变浏览器访问则无效

### application

保存在服务器端



先介绍以下方法

```jsp
<% 
	pageContext.setAttribute("被设置属性","属性值") //设置page属性 
	request.setAttribute("被设置属性","属性值") //设置request属性,依次类推
	session.setAttribute("被设置属性","属性值")
	application.setAttribute("被设置属性","属性值")   
%>

<% out.print(pageContext.getAttribute("name-1")+"<br>");%> //获取page属性依次类推
    <% out.print(request.getAttribute("name-2")+"<br>");%>
    <% out.println(session.getAttribute("name-3")+"<br>");%>
    <% out.print(application.getAttribute("name-4")+"<br>");%>
```



一般设置jsp页面跳转有两种方法

jsp 的forward指令

```jsp
<jsp:forward page="跳转文件相对路径"></jsp:forward>
```

相当于对服务端进行一次跳转

a标签的超链接

```html
<a href="url"></a>
```

 相当于对客户端进行一次跳转，服务器端两次跳转



for example

range.jsp

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <%
        pageContext.setAttribute("name-1","lihua");
        request.setAttribute("name-2","zhangsang");
        session.setAttribute("name-3","wemz");
        application.setAttribute("name-4","niuma");
    %>

<%--    jsp跳转--%>
    <jsp:forward page="getName.jsp"></jsp:forward>
</body>
</html>
```

getName.jsp

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <% out.print(pageContext.getAttribute("name-1")+"<br>");
out.print(request.getAttribute("name-2")+"<br>");
     out.println(session.getAttribute("name-3")+"<br>");
     out.print(application.getAttribute("name-4")+"<br>");%>
</body>
</html>
```

访问range.jsp时浏览器显示

![image-20231231221231301](http://111.229.225.13:81/i/2023/12/31/10l5d58-2.png)

page设置的属性无法获取，因为经过了一次跳转

修改range.jsp代码改为超链接跳转

range.jsp

```jsp
<%--
  Created by IntelliJ IDEA.
  User: longersking
  Date: 2023/12/31
  Time: 21:45
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" pageEncoding="UTF-8" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
    <%
        pageContext.setAttribute("name-1","lihua");
        request.setAttribute("name-2","zhangsang");
        session.setAttribute("name-3","wemz");
        application.setAttribute("name-4","niuma");
    %>

<%--    jsp跳转--%>
<%--    <jsp:forward page="getName.jsp"></jsp:forward>--%>
    <a href="getName.jsp">获取属性</a>
</body>
</html>
```

![image-20231231221519963](http://111.229.225.13:81/i/2023/12/31/10mvf5b-2.png)

![image-20231231221531341](http://111.229.225.13:81/i/2023/12/31/10mxw3z-2.png)

request获取不到属性，因为超链接两次跳转，超出request范围

现在关闭浏览器，再次访问

![image-20231231221819957](http://111.229.225.13:81/i/2023/12/31/10onlbi-2.png)

可以发现只有application属性可以访问

重启服务器（idea重启按钮）

![image-20231231221928678](http://111.229.225.13:81/i/2023/12/31/10pay6f-2.png)