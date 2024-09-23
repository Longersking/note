# FastAPI开发环境搭建——开发第一个web程序

## 搭建开发环境

FastAPI官方文档[学习 - FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/learn/)

### 安装fastapi框架

```python
pip install fastapi[all]
pip install uvicorn
```

### 使用对应IDE创建fastapi项目，例如pycharm,vscode和创建普通的python项目无差别

- 创建一个fastapi项目目录（就普通目录）

- 导入fastapi框架

  ```python
  from fastapi import FastAPI
  ```

- 创建FastAPI对象

  ```python
  app = FastAPI()
  ```

- 编写FastAPI接口

  ```python
  @app.get("/")
  asyn def run():
      return {"message":"hello world!"}
  ```

  ```python
  #@app.get("/")是一种装饰器用于写在函数上方方便的调用装饰器函数
  #app指的是创建的FastAPI对象,如果创建的方式为test = FastAPI(),则就应该改为@test.get("/")
  #app.get()表示创建一个get请求的接口
  #get("/")方法中的"/"表示接口的路径，是可以自行修改的，例如改成@app.get("/a"),那么在浏览器访问http://127.0.0.1:8000/a才会调用装饰器下面的函数
  #asyn def run():
  #   return {"message":"hello world!"}
  #asyn 异步关键字标识这个函数为异步函数，同时函数被调用时将会返回一个json数据{"message":"hello world"}
  ```

- 启动Fastapi程序

  ```python
  #两种方法
  #1 main方法启动
  if __name__ == "main":
      unicorn.run(app,host="0.0.0.0",port=8000)
      
  #直接在命令行中启动
  uvicorn main:app --reload #默认运行ip地址为127.0.0.1 默认端口为8000
  #自定义IP地址和端口
  uvicorn app:app --host '0.0.0.0' --port 8000 --reload
  ```

- 在浏览器输入栏中输入http://127.0.0.1:8000/

  ![image-20240923172043309](W:\note\python\fastapi\fastapi环境配置启动\image-20240923172043309.png)

### FastAPI自动生成api文档

- 启动程序后，在浏览器中输入http://127.0.0.1:8000/docs
- 一般来说如下图
- ![image-20240923173441435](W:\note\python\fastapi\fastapi环境配置启动\image-20240923173441435.png)

但是有时也会加载不出来

