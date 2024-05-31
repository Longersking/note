# JSP

一种编写动态网页的语言，可以嵌入java代码和html代码，其底层本质上为servlet,html部分为输出流，编译为java文件

例如

源jsp文件

```jsp
<%@ page contentType="text/html; charset=utf-8" language="java" pageEncoding="UTF-8" %>
<html>
<head>
    <title>Title</title>
</head>
<body>
<pre>
    /* whoami */
<%--    whoami --%>
    <!-- whoami -->
</pre>
</body>
</html>

```



```java
package org.apache.jsp;

import javax.servlet.*;
import javax.servlet.http.*;
import javax.servlet.jsp.*;

public final class hellojsp_jsp extends org.apache.jasper.runtime.HttpJspBase
    implements org.apache.jasper.runtime.JspSourceDependent,
                 org.apache.jasper.runtime.JspSourceImports {

  private static final javax.servlet.jsp.JspFactory _jspxFactory =
          javax.servlet.jsp.JspFactory.getDefaultFactory();

  private static java.util.Map<java.lang.String,java.lang.Long> _jspx_dependants;

  private static final java.util.Set<java.lang.String> _jspx_imports_packages;

  private static final java.util.Set<java.lang.String> _jspx_imports_classes;

  static {
    _jspx_imports_packages = new java.util.HashSet<>();
    _jspx_imports_packages.add("javax.servlet");
    _jspx_imports_packages.add("javax.servlet.http");
    _jspx_imports_packages.add("javax.servlet.jsp");
    _jspx_imports_classes = null;
  }

  private volatile javax.el.ExpressionFactory _el_expressionfactory;
  private volatile org.apache.tomcat.InstanceManager _jsp_instancemanager;

  public java.util.Map<java.lang.String,java.lang.Long> getDependants() {
    return _jspx_dependants;
  }

  public java.util.Set<java.lang.String> getPackageImports() {
    return _jspx_imports_packages;
  }

  public java.util.Set<java.lang.String> getClassImports() {
    return _jspx_imports_classes;
  }

  public javax.el.ExpressionFactory _jsp_getExpressionFactory() {
    if (_el_expressionfactory == null) {
      synchronized (this) {
        if (_el_expressionfactory == null) {
          _el_expressionfactory = _jspxFactory.getJspApplicationContext(getServletConfig().getServletContext()).getExpressionFactory();
        }
      }
    }
    return _el_expressionfactory;
  }

  public org.apache.tomcat.InstanceManager _jsp_getInstanceManager() {
    if (_jsp_instancemanager == null) {
      synchronized (this) {
        if (_jsp_instancemanager == null) {
          _jsp_instancemanager = org.apache.jasper.runtime.InstanceManagerFactory.getInstanceManager(getServletConfig());
        }
      }
    }
    return _jsp_instancemanager;
  }

  public void _jspInit() {
  }

  public void _jspDestroy() {
  }

  public void _jspService(final javax.servlet.http.HttpServletRequest request, final javax.servlet.http.HttpServletResponse response)
      throws java.io.IOException, javax.servlet.ServletException {

    if (!javax.servlet.DispatcherType.ERROR.equals(request.getDispatcherType())) {
      final java.lang.String _jspx_method = request.getMethod();
      if ("OPTIONS".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        return;
      }
      if (!"GET".equals(_jspx_method) && !"POST".equals(_jspx_method) && !"HEAD".equals(_jspx_method)) {
        response.setHeader("Allow","GET, HEAD, POST, OPTIONS");
        response.sendError(HttpServletResponse.SC_METHOD_NOT_ALLOWED, "JSP 只允许 GET、POST 或 HEAD。Jasper 还允许 OPTIONS");
        return;
      }
    }

    final javax.servlet.jsp.PageContext pageContext;
    javax.servlet.http.HttpSession session = null;
    final javax.servlet.ServletContext application;
    final javax.servlet.ServletConfig config;
    javax.servlet.jsp.JspWriter out = null;
    final java.lang.Object page = this;
    javax.servlet.jsp.JspWriter _jspx_out = null;
    javax.servlet.jsp.PageContext _jspx_page_context = null;


    try {
      response.setContentType("text/html; charset=utf-8");
      pageContext = _jspxFactory.getPageContext(this, request, response,
      			null, true, 8192, true);
      _jspx_page_context = pageContext;
      application = pageContext.getServletContext();
      config = pageContext.getServletConfig();
      session = pageContext.getSession();
      out = pageContext.getOut();
      _jspx_out = out;

      out.write("\r\n");
      out.write("<html>\r\n");
      out.write("<head>\r\n");
      out.write("    <title>Title</title>\r\n");
      out.write("</head>\r\n");
      out.write("<body>\r\n");
      out.write("<pre>\r\n");
      out.write("    \\\\whoami\r\n");
      out.write("\r\n");
      out.write("    <!-- whoami -->\r\n");
      out.write("</pre>\r\n");
      out.write("</body>\r\n");
      out.write("</html>\r\n");
    } catch (java.lang.Throwable t) {
      if (!(t instanceof javax.servlet.jsp.SkipPageException)){
        out = _jspx_out;
        if (out != null && out.getBufferSize() != 0)
          try {
            if (response.isCommitted()) {
              out.flush();
            } else {
              out.clearBuffer();
            }
          } catch (java.io.IOException e) {}
        if (_jspx_page_context != null) _jspx_page_context.handlePageException(t);
        else throw new ServletException(t);
      }
    } finally {
      _jspxFactory.releasePageContext(_jspx_page_context);
    }
  }
}

```

这里可以发现html的语法部分使用out.write的输出流输出

# 配置开发环境

环境:tomcat + apache + idea 2023

![image-20231231190357972](http://111.229.225.13:81/i/2023/12/31/vhmlyn-2.png)

点击create

![image-20231231190511594](http://111.229.225.13:81/i/2023/12/31/vi9723-2.png)

​	![image-20231231192213966](http://111.229.225.13:81/i/2023/12/31/vse5sv-2.png)

少了个截图，点+号后选择java,然后选择你对应的tomcat的lib下面的jsp-api.jar和servlet-api.jar

选好后在下面可以查看安装了哪些拓展

![image-20231231192402796](http://111.229.225.13:81/i/2023/12/31/vtis6k-2.png)

然后选择右上角这个地方（这里我已经选择好了），点击edit

![image-20231231192445218](http://111.229.225.13:81/i/2023/12/31/vtrg9j-2.png)

![image-20231231192550258](http://111.229.225.13:81/i/2023/12/31/vuebpj-2.png)

jmx port 可以修改，有时候会出现端口冲突，并且你使用netstat -ano | findstr 端口号，无回显时，可以在这里修改端口号

完成后点击apply

![image-20231231192813286](http://111.229.225.13:81/i/2023/12/31/vvyf5w-2.png)

下面有一个application context的按钮设置默认允许url路径,默认的是带有你添加拓展的文件名的url,这里可以自行修改，并且还需要在添加的默认中也一并修改

然后点击右上角运行的按钮，一个三角形按钮

一般默认有一个index.jsp，如果没有，自己创建一个

![image-20231231193950582](http://111.229.225.13:81/i/2023/12/31/w2qeo0-2.png)



# 基本语法

## <% 代码片段 %>

用来包含任意量的Java语句、变量、方法、表达式

解决中文编码问题

```jsp
<%@ page language="java" contentType="text/html; charset=UTF-8"  pageEncoding="UTF-8"%>
```

## <%! declaration; [ declaration; ]+ ... %>

jsp声明一个声明语句可以声明一个或多个变量、方法，供后面的Java代码使用

## <%= 表达式 %>

一个JSP表达式中包含的脚本语言表达式，先被转化成String，然后插入到表达式出现的地方。

由于表达式的值会被转化成String，所以您可以在一个文本行中使用表达式而不用去管它是否是HTML标签。

表达式元素中可以包含任何符合Java语言规范的表达式，但是不能使用分号来结束表达式。

## jsp注释

显式注释：<!-- 注释 --> HTML注释，通过浏览器查看网页源代码时可以看见注释内容

隐式注释：<%-- 注释 --%> JSP注释，注释内容不会被发送至浏览器甚至不会被编译

## include静态包含与include动态包含

静态包含

```jsp
<%@include file="文件相对路径"%>
```

可以理解为调用变量

动态包含

```jsp
<jsp:include page="文件相对路径"></jsp:include>
```

可以理解为调用方法



