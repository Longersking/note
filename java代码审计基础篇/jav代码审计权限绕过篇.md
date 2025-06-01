## Java项目通常由Interceptor&Filter&Shiro&Jwt这些组件鉴权

### 1、组件介绍

Interceptor 拦截器 ，主要用于拦截请求、响应或处理过程中的某些事件，比如权限认证、日志记录、性能测试等。在 Java 中，Interceptor可以用来扩展框架，增加或修改某个方法的行为，或者对应用流程做些前置处理、后置处理、环绕处理等

Filter过滤器，可通过拦截请求实现权限校验和访问控制：首先配置 url-pattern 拦截目标路径（如 /admin/*），从 Session、Cookie 或请求头（如 JWT Token）中提取用户身份，验证其角色或权限是否匹配资源要求，合法请求放行，非法访问则重定向至登录页或返回 403/401 错误码

Apache Shiro 是一个功能全面的安全框架，提供基于角色（Role）和权限（Permission）的细粒度访问控制，通过 `Subject` 进行身份认证（如用户名密码、RememberMe）和授权，支持 Session 管理、加密及缓存，适合传统 Web 应用；

而 JWT（JSON Web Token）是一种轻量级的无状态鉴权方案，通过签名 Token（包含用户信息及权限声明）实现跨系统认证，适合前后端分离或微服务架构，需自行实现权限校验逻辑（如从 Token 解析角色）。两者可结合使用——Shiro 验证 JWT 并完成授权，兼顾无状态和灵活权限管理。

### 2、绕过思路
通常在java web项目中获取用户输入的URL的方法有这几个
```java
 String requestURI = request.getRequestURI(); // 获取整个URL  
 System.out.println("1:我是getRequestURI"+requestURI);  
 StringBuffer requestURL = request.getRequestURL();  //获取url  
 System.out.println("2:我是getRequestURl"+requestURI);  
 String servletPath = request.getServletPath();   //获取Servlet的路径  
 System.out.println("3:我是getServletPath"+requestURI);
```
