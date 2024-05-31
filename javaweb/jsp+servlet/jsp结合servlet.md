# servlet配置

环境配置2023.12.31 idea配置搭建

创建一个普通的java项目

![image-20240101145016039](http://111.229.225.13:81/i/2024/01/01/nzfgfo-2.png)

由于新版idea去除了add framework support的ui显示，可以在左边项目栏中使用快捷键shift+k或者setting中搜索add framework support在修改对应的快捷键

![image-20240101145255757](http://111.229.225.13:81/i/2024/01/01/o0t3su-2.png)

点击ok然后应该就是下面这样的结果

![image-20240101145407392](http://111.229.225.13:81/i/2024/01/01/o1pivz-2.png)

这里笔者采用maven去管理jar包，如果不打算使用maven管理可以看这个博主的[idea2023创建JavaWeb教程 解决右键没有Servlet的问题_idea2023创建找不到servlet-CSDN博客](https://blog.csdn.net/qq_61176213/article/details/130905515)

后面的操作和笔者之前用idea配置jsp的方式一样

这里再说一个创建servlet模板的方式

首先提供一份模板（很多博客都tmd不提供，我一个一个敲的！！！）

```java
#if (${PACKAGE_NAME} && ${PACKAGE_NAME} != "")package ${PACKAGE_NAME};#end
#parse("File Header.java")
@javax.servlet.annotation.WebServlet("/${Entity_Name}")
public class ${Class_Name} extends javax.servlet.http.HttpServlet {
    protected void doPost(javax.servlet.http.HttpServletRequest request, javax.servlet.http.HttpServletResponse response) throws javax.servlet.ServletException, java.io.IOException {

    }

    protected void doGet(javax.servlet.http.HttpServletRequest request, javax.servlet.http.HttpServletResponse response) throws javax.servlet.ServletException, java.io.IOException {
        this.doPost(request,response);
    }
}

```

点击左上角的file找到settings再找到Editor点开找到file and Code Templates 然后点击右边的+添加模板,把上面的模板复制粘贴上去，再命名就可以了

![image-20240101150432547](http://111.229.225.13:81/i/2024/01/01/ovmm8b-2.png)



![image-20240101150727103](http://111.229.225.13:81/i/2024/01/01/oxdonx-2.png)

