# FastAPI路由配置

### 在工程项目比较大的时候，很少把所有代码全部写在一个文件下，因此FastAPI引入APIRouter来构建一个路由管理

官网对应文档[更大的应用 - 多个文件 - FastAPI (tiangolo.com)](https://fastapi.tiangolo.com/zh/tutorial/bigger-applications/#_5)

## 创建方式

### 引入APIRouter

```python
# app/routers/items
from fastapi import APIRouter
#创建一个APIRouter对象，可以理解为一个“迷你”的FastAPI类
router = APIRouter()
#然后创建接口如下
@router.get("/")
def test():
    pass
```

### 在总路由中导入其他路由

```python
app.include_router(items.router)
```

通过APIRouter()可以将其他路由添加到主程序中

```python
# app/main.py
from fastapi import FastAPI
# 导入其他路由的模块
from .router import items
app = FastAPI()

#导入其他路由
app.include_router(items.router)
```

### APIRouter引入参数解释

```python
router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
router = APIRouter() #: 这行代码创建了一个新的API路由组实例。APIRouter类允许开发者组织他们的API路径操作（endpoints）到不同的组中，这有助于保持代码的整洁，并且方便管理不同的功能模块。
prefix="/items" #: 这个参数指定了所有在这个路由组中的API路径前缀都会自动加上/items。例如，如果你定义了一个路径/add，那么实际访问的路径将会是/items/add。
tags=["items"] #: 这个参数用于文档生成工具（如Redoc或Swagger UI），它会将这个路由组中的所有路径操作标记为“items”。这对于生成清晰的API文档是非常有用的，帮助开发者理解和使用API。
dependencies=[Depends(get_token_header)] #: 这个参数指定了一个全局依赖项。在这个例子中，任何属于这个路由组的路径操作都需要先通过get_token_header函数的验证。Depends是一个特殊的类或函数，通常用来实现诸如认证、权限检查等功能。这里的get_token_header可能是一个负责从请求头中获取认证令牌并进行验证的函数。
responses={404: {"description": "Not found"}} #: 这个参数定义了API响应的一部分结构，具体来说是指定当客户端请求的资源不存在时（即返回状态码为404的情况），应该返回什么样的描述信息。在这里，如果API返回404状态码，则会在响应体中包含“Not found”的描述。
```

## 