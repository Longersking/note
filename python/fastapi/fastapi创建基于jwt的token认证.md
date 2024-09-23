# 创建基于jwt的token认证

## 创建方法

官网[OAuth2 实现密码哈希与 Bearer JWT 令牌验证 - FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/tutorial/security/oauth2-jwt/)

我个人习惯下面这种方式

   0.安装并且导入相关的库和模块

        ```shell
        pip install pyjwt,python-jose[cryptography],jose
        ```



1. 配置密钥，加密方法，过期参数

   ```python
   SECRET_KEY = "your-secret"
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 3000
   ```

2. 使用jwt根据这些参数生成对应的token

   ```python
   payload = {
           "username": user.username
       }
   token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
   
   #解码
   decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
   ```

