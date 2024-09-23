# FastAPI依赖注入

### 个人理解为一种类似装饰器的设计模式，但是更加方便，有助于修改或添加函数的一些功能，但是他更加侧重于解决服务器之间的一些依赖问题

官方文档[依赖项 - FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/tutorial/dependencies/)

### 作用：授权认证、数据库操作，外部服务调用，环境配置

- #### 基础使用方式

  ```python
  from fastapi import FastAPI, Depends
  
  app = FastAPI()
  
  fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
  
  def query_db():
      return fake_items_db
  
  @app.get("/items/")
  async def read_items(available_items=Depends(query_db)):
      return available_items
  ```

  `query_db` 函数作为依赖被注入到 `read_items` 路径操作函数中。每次请求 `/items/` 时，`query_db` 函数会被调用，并将结果传递给 `available_items` 参数。

- #### 多个依赖

  ```python
  from fastapi import FastAPI, Depends
  
  app = FastAPI()
  
  def query_db():
      return ["item1", "item2", "item3"]
  
  def common_parameters(q: str = "", skip: int = 0, limit: int = 100):
      return {"q": q, "skip": skip, "limit": limit}
  
  @app.get("/items/")
  async def read_items(commons=Depends(common_parameters), items=Depends(query_db)):
      return commons, items
  ```

  `common_parameters` 和 `query_db` 都作为依赖注入到 `read_items` 中。`Depends` 告诉FastAPI这是一个依赖函数，需要在执行路径操作之前调用它。

- #### 类调用

  ```python
  from fastapi import FastAPI, Depends
  
  app = FastAPI()
  
  class CommonQueryParams:
      def __init__(self, q: str = "", skip: int = 0, limit: int = 100):
          self.q = q
          self.skip = skip
          self.limit = limit
  
  @app.get("/items/")
  async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
      return commons
  ```

  `CommonQueryParams` 类被实例化并作为依赖注入到 `read_items` 函数中。